#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apptrivia import db
from models.models import Categoria, Pregunta,Usuario, Respuesta, Role

db.drop_all()
db.create_all()

# categorias
c_geogra = Categoria(descripcion="Geografía")
c_deporte = Categoria(descripcion="Deportes")
c_historia = Categoria(descripcion="Historia")
c_arte = Categoria(descripcion="Arte")

# preguntas
q_Laos = Pregunta(text="¿Cuál es la capital de Laos?",categoria=c_geogra)
q_Armenia = Pregunta(text="¿Cuál es la población aproximada de Armenia?",categoria=c_geogra)
q_mundial = Pregunta(text="¿En qué país se jugó la Copa del Mundo de 1962?",categoria=c_deporte)
q_Artigas = Pregunta(text="¿En qué año nació Artigas?", categoria=c_historia)
q_Blanes = Pregunta(text="¿Qué pintor uruguayo se destaca por la temática gauchesca", categoria=c_arte)

# respuestas
r_1 = Respuesta(text="3 millones",pregunta=q_Armenia, correcta=True)
r_2 = Respuesta(text="5 millones",pregunta=q_Armenia, correcta=False)
r_3 = Respuesta(text="10 millones",pregunta=q_Armenia, correcta=False)

r_4 = Respuesta(text="Vientian",pregunta=q_Laos, correcta=True)
r_5 = Respuesta(text="Vientnam",pregunta=q_Laos, correcta=False)
r_6 = Respuesta(text="Montevideo",pregunta=q_Laos, correcta=False)

r_7 = Respuesta(text="Chile", pregunta=q_mundial, correcta=True)
r_8 = Respuesta(text="Mexico", pregunta=q_mundial, correcta=False)
r_9 = Respuesta(text="Brasil", pregunta=q_mundial, correcta=False)

r_10 = Respuesta(text="1764", pregunta=q_Artigas, correcta=True)
r_11 = Respuesta(text="1762", pregunta=q_Artigas, correcta=False)
r_12 = Respuesta(text="1761", pregunta=q_Artigas, correcta=False)

r_13 = Respuesta(text="Blanes", pregunta=q_Blanes, correcta=True)
r_14 = Respuesta(text="Figari", pregunta=q_Blanes, correcta=False)
r_15 = Respuesta(text="Torres García", pregunta=q_Blanes, correcta=False)

db.session.add_all([c_geogra, c_deporte, c_historia, c_arte])

db.session.add_all([q_Laos, q_Armenia, q_mundial, q_Artigas, q_Blanes])

db.session.add_all([r_1, r_2, r_3, r_4, r_5, r_6, r_7, r_8, r_9, r_10, r_11, r_12, r_13, r_14, r_15])

db.session.commit()

# agregamos 1 admin y 4 users
u_admin = Usuario(name='admin', email='admin@antel.com.uy')
u_admin.set_password("admin123")

u1 = Usuario(name='user1', email='user1@antel.com.uy')
u1.set_password("pass1")

u2 = Usuario(name='user2', email='user2@antel.com.uy')
u2.set_password("pass2")

u3 = Usuario(name='user3', email='user3@antel.com.uy')
u3.set_password("pass3")

u4 = Usuario(name='user4', email='user4@antel.com.uy')
u4.set_password("pass4")

db.session.add_all([u_admin, u1, u2, u3, u4])

# Agregamos y asignamos los roles respectivos

db.session.add_all(
         [
          Role(rolename='admin', usuario=u_admin),
          Role(rolename='user', usuario=u_admin),  # multiples roles
          Role(rolename='user', usuario=u1),
          Role(rolename='user', usuario=u2),
          Role(rolename='user', usuario=u3),
          Role(rolename='user', usuario=u4)
          ]
          )
          
db.session.commit()