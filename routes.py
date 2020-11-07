# importamos la instancia de Flask (app)
from apptrivia import app, login_manager
import random
import datetime
import functools
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from forms.login import LoginForm
from forms.register import RegisterForm


# importamos los modelos a usar
from models.models import Categoria, Pregunta, Respuesta, Usuario

from flask import render_template, session, redirect, url_for, flash, request

@app.route('/trivia')
def index():
    if current_user.is_authenticated:
        session.clear()
        session["inicio"] = datetime.datetime.now()
        return render_template('home.html')
    else:
        return redirect(url_for('login'))
    

@app.route('/trivia/categorias', methods=['GET'])
@login_required
def mostrarcategorias():
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=categorias, session=session)


@app.route('/trivia/<int:id_categoria>/pregunta', methods=['GET'])
@login_required
def mostrarpregunta(id_categoria):
    preguntas = Pregunta.query.filter_by(categoria_id=id_categoria).all()
    # elegir pregunta aleatoria pero de la categoria adecuada
    pregunta = random.choice(preguntas)
    categ = Categoria.query.get(id_categoria)
    respuestas = Respuesta.query.filter_by(pregunta_id=pregunta.id).all()
    return render_template('preguntas.html', categoria=categ, pregunta=pregunta, respuestas=respuestas)


@app.route('/trivia/<int:id_pregunta>/resultado/<int:id_respuesta>', methods=['GET'])
@login_required
def mostrarrespuesta(id_respuesta, id_pregunta):
    pregunta = Pregunta.query.get(id_pregunta)
    respuesta = Respuesta.query.get(id_respuesta)
    categorias = Categoria.query.all()
    respuesta.text = "mmmmnnnnaaaaaaaaaa"
    if respuesta.correcta:
        session[str(pregunta.categoria_id)] = True
        respuesta.text = "COOOORRRECTOOOO"
        completado = [x for x in categorias if str(x.id) in session]
        if len(completado) == len(categorias):
            return redirect(url_for('ganaste'))
        
    return render_template('respuesta.html', pregunta=pregunta, respuesta=respuesta)


@app.route('/trivia/ganaste', methods=['GET'])
@login_required
def ganaste():
    duracion = datetime.datetime.now()-session["inicio"]
    return render_template('ganaste.html', duracion=duracion)

#le decimos a Flask-Login como obtener un usuario
@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(int(user_id))

@app.route('/trivia/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        #get by email valida
        user = Usuario.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            # funcion provista por Flask-Login, el segundo parametro gestion el "recordar"
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next', None)
            if not next_page:
                next_page = url_for('index')
            return redirect(next_page)
            
        else:
            flash('Usuario o contraseña inválido')
            return redirect(url_for('login'))
    # no loggeado, dibujamos el login con el form vacio
    return render_template('login.html', form=form)

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
            user = Usuario(name=username, email=email)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            return redirect(url_for('index'))
    return render_template("register.html", form=form)


@app.route('/trivia/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))