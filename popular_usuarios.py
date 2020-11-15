from apptrivia import db
from models.models import  Usuario, Role

# agregamos 2 usuarios
u1 = Usuario(name='admin', email='admin@antel.com.uy')
u2 = Usuario(name='user2', email='bla2@antel.com.uy')
u1.set_password("admin123")
u2.set_password("bla2")
db.session.add_all([u1, u2])
db.session.commit()

db.session.add_all(
         [Role(rolename='admin', usuario=u1),
          Role(rolename='user', usuario=u1),  # multiples roles
          Role(rolename='user', usuario=u2)])
db.session.commit()