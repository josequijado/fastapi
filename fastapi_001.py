# fastapi_001.py

from fastapi import FastAPI # Importamos la clase FastAPI. Previamente la habremos instalado con pip install fastapi.

app = FastAPI() # Creamos un objeto de la clase FastAPI usando su constructor.

## Diccionario que usaremos en el método mostrar_persona
personas = {1:"Juan", 2:"Yolanda", 3:"Marcos", 4:"Carmen", 5:"Susana", 6:"Martin", 7:"Eva"}

# Ruta = http://127.0.0.1:8000

## Creamos un método que devolverá una frase que saldrá por el navegador.
## El método de llamada es GET, como se ve en el decorador.
## Para poder llamar a los métodos de la API en el decorador se incluye el 
## método de llamada (get), con el argumento que es la ruta de la llamada. 
## En este caso el slash "/" representa a la ruta raíz (http://127.0.0.1:8000).
## A continuación se define el método que va a responder a esa llamada.
## OJO. Es importante que el decorador se declare en la línea inmediatamente encima del método.
## Si no se hace así, la llamada podría no funcionar.
## Así, cuando se haga la llamada a la ruta raíz, la API ejecutará el método index().
@app.get("/")
def index():
    ## El método devuelve en este ejemplo un diccionario, 
    ## que FastAPI nos envía al navegador como un objeto JSON.
    return {"mensaje":"Hola Mundo."}

## Para acceder a este método teclearemos, por ejemplo, http://127.0.0.1:8000/personas/3
## El método recibe el parámetro id, con el valor 3 (o el que hayamos tecleado). Se fuerza 
## a reconocer ese parámetro como un dato de tipo int, que es como está en el diccionario, 
## ya que, si no lo hacemos así, por defecto lo recibe como un string, y no encontraría el 
## elemento en el diccionario.
@app.get("/personas/{id}")
def mostrar_persona(id:int):
    try:
        resultado = {"mensaje": f"El id es {id}. La persona seleccionada es {personas[id]}."}
    except:
        resultado = {"mensaje": f"El id es {id}. Persona no encontrada."}
    return resultado

## COMO PONER EN MARCHA EL SERVIDOR
## En la terminal escribiremos uvicorn fastapi_001:app --reload
## Veamos la sintaxis de esta llamada:
##      uvicorn. Es la llamada al servidor para que la API funcione en el navegador.
##      fastapi_001:app. Es el nombre del script que contiene la API, sin la extensión .py
##      La sintaxis :app hace referencia al nombrre del objeto que se declara con la API
##      --reload sirve para que, una vez puesto en marcha el servidor uvicorn, si hacemos algún 
##      cambio en el código el servidor lo recargue automáticamente. 
##      De este modo solo tendremos que recargar el navegador para ver actualizados los cambios.
