# importamos la instancia de Flask (app)
from apptrivia import app
import random
import datetime
import functools


# importamos los modelos a usar
from models.models import Categoria, Pregunta, Respuesta

from flask import render_template, session, redirect, url_for

@app.route('/trivia')
def index():
    session.clear()
    session["inicio"] = datetime.datetime.now()
    return render_template('home.html')
    

@app.route('/trivia/categorias', methods=['GET'])
def mostrarcategorias():
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=categorias, session=session)


@app.route('/trivia/<int:id_categoria>/pregunta', methods=['GET'])
def mostrarpregunta(id_categoria):
    preguntas = Pregunta.query.filter_by(categoria_id=id_categoria).all()
    # elegir pregunta aleatoria pero de la categoria adecuada
    pregunta = random.choice(preguntas)
    categ = Categoria.query.get(id_categoria)
    respuestas = Respuesta.query.filter_by(pregunta_id=pregunta.id).all()
    return render_template('preguntas.html', categoria=categ, pregunta=pregunta, respuestas=respuestas)


@app.route('/trivia/<int:id_pregunta>/resultado/<int:id_respuesta>', methods=['GET'])
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
def ganaste():
    duracion = datetime.datetime.now()-session["inicio"]
    return render_template('ganaste.html', duracion=duracion)