# Trivia 
Entrega trabajo final curso Taller de Python de Antel
***

Para ejecutar la trivia localmente, debe seguir los siguientes pasos:

- Clonar el repositorio
- Instalar las dependencias en su entorno Python utilizando `pip install -r requirements.txt`

> Opcionalmente puede hacerlo en un entorno virtual:
> - `virtualenv env`
> - `cd env/Scripts`
> - `activate`
> - `cd /trivia`
> - `pip install -r requirements.txt`

Una vez completada la instalación, se ejecuta la aplicación:
- `python entrypoint.py`

El archivo `popular_db.py` carga una muestra de preguntas y respuestas, un usuario administrador y 4 usuarios de prueba.
Para adaptar la trivia a su base de datos, debe modificar la funcion `create_app()` en el archivo `trivia/app/__init__.py`
