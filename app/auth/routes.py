# app/auth/routes.py

from . import auth_bp
from app import login_manager
from flask import render_template, redirect, url_for, flash, request, session, current_app
from flask_principal import Principal, Permission, Identity, AnonymousIdentity, RoleNeed, UserNeed, identity_loaded, identity_changed

from .models import Usuario, Role
from .forms.login import LoginForm
from .forms.register import RegisterForm

import datetime
from flask_login import LoginManager, current_user, login_user, login_required, logout_user

#le decimos a Flask-Login como obtener un usuario
@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(int(user_id))

#Se instancia el objeto LoginForm, si valida se loguea al usuario y se lo dirige al index
#o a next_page segun el requesta. Si no valida se flashea un msj de error y se rutea a Login
@auth_bp.route('/trivia/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: #flashear un msg "el usuario ya está logueado"
        flash('el usuario ya está logueado')
        return redirect(url_for('public.index'))
    form = LoginForm()
    if form.validate_on_submit():
        #get by email valida
        user = Usuario.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            # funcion provista por Flask-Login, el segundo parametro gestion el "recordar"
            login_user(user, remember=True)
            
            next_page = request.args.get('next', None)
            if not next_page:
                next_page = url_for('public.index')
            app_actual = current_app._get_current_object()
            identity_changed.send(app_actual, identity=Identity(user.id))
            return redirect(next_page)
        else:
            flash('Usuario o contraseña inválido')
            return redirect(url_for('auth.login'))
    # no loggeado, dibujamos el login con el form vacio
    return render_template('login.html', form=form)


#Se instancia el formulario Register.
#Si valida el formulario y no existe el mail se crea un usuario nuevo y se lo deja logueado
#y ruteado al Index
@auth_bp.route("/trivia/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
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
            app_actual = current_app._get_current_object()
            identity_changed.send(app_actual, identity=Identity(user.id))
            return redirect(url_for('public.index'))
    return render_template("register.html", form=form)

#se desloguea al usuario con las funciones propias de FlaskLogin y se lo rutea a Index
@auth_bp.route('/trivia/logout')
def logout():
    logout_user()
    
    # Flask-Principal: Remove session keys
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Flask-Principal: the user is now anonymous
    app_actual = current_app._get_current_object()
    identity_changed.send(app_actual, identity=AnonymousIdentity())
    return redirect(url_for('public.index'))


