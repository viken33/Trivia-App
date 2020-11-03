import os

# configuraciones. True para que el servidor pueda ser levantado en modo debug
DEBUG = True

# configuracion BD

POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'trivia',
    'host': 'localhost',
    'port': '5432',
}


SECRET_KEY =  'A SECRET KEY'

SQLALCHEMY_TRACK_MODIFICATIONS = False

#postgresql://username:password@hostname/database
#SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/trivia"
SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES['user']}:" \
                           f"{POSTGRES['pw']}@{POSTGRES['host']}:" \
                           f"{POSTGRES['port']}/{POSTGRES['db']}"

