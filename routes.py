# importamos la instancia de Flask (app)
from apptrivia import app, login_manager
import random
import datetime
import functools
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from forms.login import LoginForm
from forms.register import RegisterForm
from werkzeug.urls import url_parse
from werkzeug.exceptions import HTTPException
from flask_principal import AnonymousIdentity, RoleNeed, UserNeed, identity_loaded, identity_changed


# importamos los modelos a usar
from models.models import Categoria, Pregunta, Respuesta, Usuario, Role
from flask import render_template, session, redirect, url_for, flash, request, jsonify, abort

#funcion auxiliar para limpiar la partida luego de finalizar o de un logout
def limpiar_partida():
    categorias = Categoria.query.all()
    for c in categorias:
        session[str(c.id)] = False
    session["inicio"] = 0

#Ruta Home, limpio la partida, el timestamp lo tomo en el template luego del click 
# en el boton "Comenzar a Jugar"
@app.route('/trivia') 
def index():
    limpiar_partida()
    return render_template('home.html', session=session, time=datetime.datetime)
    
#Se muestran las categorias, dentro el template se consulta las categorias
#acertadas y segun los aciertos se activan o desactivan los botones
@app.route('/trivia/categorias', methods=['GET'])
@login_required
def mostrarcategorias():
    #con un IF diferencio una partida nueva de un "regreso" a categorias
    # para volver a tomar el tiempo de inicio o no
    if session["inicio"] == 0:
        session["inicio"] = datetime.datetime.now()
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=categorias, session=session)

#Se elige aleatoriamente una pregunta de la categoria seleccionada
#Se envia a jinja2 la categoria y pregunta actual y sus respuestas
#En el template se desactivan los botones de las categorias completadas
@app.route('/trivia/<int:id_categoria>/pregunta', methods=['GET'])
@login_required
def mostrarpregunta(id_categoria):
    preguntas = Pregunta.query.filter_by(categoria_id=id_categoria).all()
    # elegir pregunta aleatoria pero de la categoria adecuada
    pregunta = random.choice(preguntas)
    categ = Categoria.query.get(id_categoria)
    respuestas = Respuesta.query.filter_by(pregunta_id=pregunta.id).all()
    return render_template('preguntas.html', categoria=categ, pregunta=pregunta, respuestas=respuestas)

#Se evalua la respuesta elegida, si es correcta se guarda la categoria como completada
#en la sesion, y se evalua si ya fueron todas completadas usando una lista por comprension
#Cuando se completan las categorias se rutea a Ganaste
@app.route('/trivia/<int:id_pregunta>/resultado/<int:id_respuesta>', methods=['GET'])
@login_required
def mostrarrespuesta(id_respuesta, id_pregunta):
    pregunta = Pregunta.query.get(id_pregunta)
    respuesta = Respuesta.query.get(id_respuesta)
    categorias = Categoria.query.all()
    respuesta.text = "Respuesta incorrecta...intenta de nuevo"
    if respuesta.correcta:
        session[str(pregunta.categoria_id)] = True
        respuesta.text = "COOOORRRECTOOOO"
        completado = [x for x in categorias if session[str(x.id)] == True]
        if len(completado) == len(categorias):
            return redirect(url_for('ganaste'))
        
    return render_template('respuesta.html', pregunta=pregunta, respuesta=respuesta)

#Se toma la timestamp y se hace la resta para obtener la duracion de la sesion
@app.route('/trivia/ganaste', methods=['GET'])
@login_required
def ganaste():
    # Mido la duracion de la partida
    duracion = (datetime.datetime.now()-session["inicio"]).seconds
    # Actualizo el highscore del usuario
    u = Usuario.get_by_id(int(current_user.id))
    if int(u.highscore) == 0:
        u.update_highscore(duracion)
    elif int(u.highscore) > duracion:
        u.update_highscore(duracion)
    # Obtengo Top5 ordenada y actualizada de highscores
    # Con la partida actual y el Top 5 alimento el template
    users = [x for x in Usuario.query.all() if x.highscore != 0]
    ordenada = sorted(users, key=lambda x: x.highscore)
    ordenada = ordenada[0:5]
    duracion = str(datetime.timedelta(seconds=duracion))
    return render_template('ganaste.html', duracion=duracion, users=ordenada)

#le decimos a Flask-Login como obtener un usuario
@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(int(user_id))

#Se instancia el objeto LoginForm, si valida se loguea al usuario y se lo dirige al index
#o a next_page segun el requesta. Si no valida se flashea un msj de error y se rutea a Login
@app.route('/trivia/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: #flashear un msg "el usuario ya está logueado"
        flash('el usuario ya está logueado')
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        #get by email valida
        user = Usuario.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            # funcion provista por Flask-Login, el segundo parametro gestion el "recordar"
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page:
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Usuario o contraseña inválido')
            return redirect(url_for('login'))
    # no loggeado, dibujamos el login con el form vacio
    return render_template('login.html', form=form)


#Se instancia el formulario Register.
#Si valida el formulario y no existe el mail se crea un usuario nuevo y se lo deja logueado
#y ruteado al Index
@app.route("/trivia/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = Usuario.get_by_email(email)
        if user is not None:
            flash('El email {} ya está siendo utilizado por otro usuario'.format(email))
        else:
            # Creamos el usuario y lo guardamos
            user = Usuario(name=username, email=email, genesis=datetime.datetime.now())
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            return redirect(url_for('index'))
    return render_template("register.html", form=form)

#se desloguea al usuario con las funciones propias de FlaskLogin y se lo rutea a Index
@app.route('/trivia/logout')
def logout():
    logout_user()
    limpiar_partida()
    # Flask-Principal: Remove session keys
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Flask-Principal: the user is now anonymous
    identity_changed.send(app, identity=AnonymousIdentity())
    return redirect(url_for('index'))

""" manejo de errores """
# Se envia un template especifico por cada error
# Se incluye el error capturado aunque se deja con el texto por defecto


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error=str(e))


@app.errorhandler(401)
def unathorized(e):
    return render_template('401.html', error=str(e))


@app.errorhandler(HTTPException)
def handle_exception(e):
    return render_template('500.html', error=str(e))

""" # Ruta de prueba para los codigos de error
@app.route('/test')
def test_principal():
    abort(500)  """

# Flask-Principal: Agregamos las necesidades a una identidad, una vez que se loguee el usuario.
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Seteamos la identidad al usuario
    identity.user = current_user

    # Agregamos una UserNeed a la identidad, con el id del usuario actual.
    if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

    # Agregamos a la identidad la lista de roles que posee el usuario actual.
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.rolename))


