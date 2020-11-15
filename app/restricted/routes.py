# app/restricted/routes.py

from . import restricted_bp

from app import db, admin
from flask_login import current_user, login_required
from flask_principal import Principal, Permission, Identity, AnonymousIdentity, RoleNeed, UserNeed, identity_loaded, identity_changed
from flask import render_template, current_app, g
from flask_admin.contrib.sqla import ModelView

from app.auth.models import Usuario, Role
from app.public.models import Categoria, Pregunta, Respuesta
from flask_admin import AdminIndexView


# Agregamos las necesidades a una identidad, una vez que se loguee el usuario.
admin_permission = Permission(RoleNeed('admin'))

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    # Seteamos la identidad al usuario
    identity.user = current_user
    # Agregamos una UserNeed a la identidad, con el usuario actual.
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
    # Agregamos a la identidad la lista de roles que posee el usuario actual.
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.rolename))


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


admin._set_admin_index_view(MyAdminIndexView())
# agregadmos al admin de todos los modelos
admin.add_view(MyModelView(Categoria, db.session))
admin.add_view(MyModelView(Pregunta, db.session))
admin.add_view(MyModelView(Respuesta, db.session))
admin.add_view(MyModelView(Usuario, db.session))
admin.add_view(MyModelView(Role, db.session))

