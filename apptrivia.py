from flask import Flask, g, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_principal import Principal, Permission, RoleNeed

# from routes import *
# from models.models import Categoria,Pregunta,Usuario,Respuesta
from flask_login import LoginManager, current_user
import os

# Flask-Principal: Creamos un permiso con una sola necesidad que debe ser satisfecho para entrar al admin.
admin_permission = Permission(RoleNeed('admin'))

class MyModelView(ModelView):
    def is_accessible(self):
        has_auth = current_user.is_authenticated
        has_perm = admin_permission.allows(g.identity)
        return has_auth and has_perm

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        has_auth = current_user.is_authenticated
        has_perm = admin_permission.allows(g.identity)
        return has_auth and has_perm

migrate = Migrate()

# instancia Flask
app = Flask(__name__)
login_manager = LoginManager(app)
admin = Admin(app, index_view=MyAdminIndexView())

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or \
    'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

# inicializa la base de datos con la config leida
db = SQLAlchemy(app)

# lee la config desde el archivo config.py
app.config.from_pyfile('config.py')


# rutas disponibles
from routes import *
from models.models import Categoria,Pregunta,Usuario,Respuesta,Role

# Flask-Principal: ---  Setup ------------------------------------
principal = Principal()
principal.init_app(app)





# Los modelos que queremos mostrar en el admin
admin.add_view(MyModelView(Categoria, db.session))
admin.add_view(MyModelView(Pregunta, db.session))
admin.add_view(MyModelView(Respuesta, db.session))
#Agrego el modelo Usuario al Flask Admin
admin.add_view(MyModelView(Usuario, db.session))
admin.add_view(MyModelView(Role, db.session))

migrate.init_app(app, db)

# subimos el server (solo cuando se llama directamente a este archivo)
if __name__ == '__main__':
    app.run(debug=True)