# importamos la instancia de la BD
from apptrivia import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Categoria(db.Model):
    __tablename__ = 'categoria'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(64), index=True, unique=True)

    preguntas = db.relationship('Pregunta', backref='categoria', lazy='dynamic')

    def __repr__(self):
        return f'<Categoria: {self.descripcion}>'


class Pregunta(db.Model):
    __tablename__ = 'pregunta'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False, unique=True)

    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    respuestas = db.relationship('Respuesta', backref='pregunta', lazy='dynamic')

    def __repr__(self):
        return f'<Pregunta {self.text}>'

class Respuesta(db.Model):
    __tablename__ = 'respuesta'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False, unique=True)
    correcta = db.Column(db.Boolean)

    pregunta_id = db.Column(db.Integer, db.ForeignKey('pregunta.id'))

    def __repr__(self):
        return f'<Respuesta {self.text}>'

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    genesis = db.Column(db.DateTime, nullable=True)
    highscore = db.Column(db.Integer, default=0)
    password = db.Column(db.String(128), nullable=False)
    roles = db.relationship('Role', backref='usuario', lazy='dynamic')

    def set_password(self,password):
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

    def __repr__(self):
        return f'<Usuario {self.name} Email: {self.email}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def update_highscore(self, hs):
        self.highscore = int(hs)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Usuario.query.get(id)

    @staticmethod
    def get_by_email(email):
        return Usuario.query.filter_by(email=email).first()

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    
    def __repr__(self):
        return f'<Role {self.rolename}>'