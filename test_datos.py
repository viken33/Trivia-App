#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apptrivia import db
from models.models import Categoria, Pregunta,Usuario, Respuesta

db.drop_all()
db.create_all()

# categorias
c_geogra = Categoria(descripcion="Geografía")
c_deporte = Categoria(descripcion="Deportes")
c_historia = Categoria(descripcion="Historia")

# preguntas
q_Laos = Pregunta(text="¿Cuál es la capital de Laos?",categoria=c_geogra)
q_Armenia = Pregunta(text="¿Cuál es la población aproximada de Armenia?",categoria=c_geogra)
q_mundial = Pregunta(text="¿En qué país se jugó la Copa del Mundo de 1962?",categoria=c_deporte)
q_Artigas = Pregunta(text="¿En qué año nació Artigas?")

# respuestas
r_1 = Respuesta(text="3 millones",pregunta=q_Armenia, correcta=True)
r_2 = Respuesta(text="5 millones",pregunta=q_Armenia, correcta=False)
r_3 = Respuesta(text="10 millones",pregunta=q_Armenia, correcta=False)
r_4 = Respuesta(text="5000 millones",pregunta=q_Armenia, correcta=False)


db.session.add(c_geogra)
db.session.add(c_deporte)
db.session.add(c_historia)

db.session.add(q_Laos)
db.session.add(q_Armenia)
db.session.add(q_mundial)

db.session.commit()

# creamos otros usuarios (…) y los recorremos
categorias = Categoria.query.all()
for c in categorias:
    print(c.id, c.descripcion)
    # para cada categoria, obtenemos sus preguntas y las recorremos
    for p in c.preguntas:
        print(p.id, p.text)


cat = Categoria.query.get(1)
print(cat)

#Creo un usuario administrador
admin = Usuario(name="Administrador",email="admin@app.com",admin=True,password="passwd")
db.session.add(admin)
db.session.commit()