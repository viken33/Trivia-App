# app/public/routes.py

from app import login_required, login_manager
from flask import render_template, session, redirect, url_for
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from . import public_bp
from .models import Categoria, Pregunta, Respuesta
from app.auth.models import Usuario
import random
import datetime

#funcion auxiliar para limpiar la partida luego de finalizar o de un logout
def limpiar_partida():
    categorias = Categoria.query.all()
    for c in categorias:
        session[str(c.id)] = False
    session["inicio"] = 0

#Ruta Home, limpio la partida, el timestamp lo tomo en el template luego del click 
# en el boton "Comenzar a Jugar"
@public_bp.route('/trivia') 
def index():
    limpiar_partida()
    return render_template('home.html', session=session, time=datetime.datetime)
    
#Se muestran las categorias, dentro el template se consulta las categorias
#acertadas y segun los aciertos se activan o desactivan los botones
@public_bp.route('/trivia/categorias', methods=['GET'])
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
@public_bp.route('/trivia/<int:id_categoria>/pregunta', methods=['GET'])
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
@public_bp.route('/trivia/<int:id_pregunta>/resultado/<int:id_respuesta>', methods=['GET'])
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
            return redirect(url_for('public.ganaste'))
        
    return render_template('respuesta.html', pregunta=pregunta, respuesta=respuesta)

#Se toma la timestamp y se hace la resta para obtener la duracion de la sesion
@public_bp.route('/trivia/ganaste', methods=['GET'])
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




