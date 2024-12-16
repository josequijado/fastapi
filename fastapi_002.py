# fastapi_002.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict # Importamos la clase Dict para gestionar el diccionario.
## La clase Dict para gestionar diccionarios presenta diferencias frente al tipo nativo dict de Python:
## 1. ¿Por qué Dict requiere importación?
## El módulo typing de Python introduce tipos genéricos que permiten anotar estructuras de datos 
## de manera más específica en términos de sus tipos internos. Aunque Python tiene el tipo nativo dict, 
## este no proporciona información sobre qué tipos de datos se esperan como claves y valores. 
## Por eso, Dict de typing es útil cuando queremos añadir ese nivel de detalle.

## Por ejemplo:
## from typing import Dict

# Esto especifica que las claves son enteros y los valores son objetos de tipo Persona.
## personas: Dict[int, Persona] = {}
## Esto no cambia cómo funciona el diccionario en tiempo de ejecución, 
## pero ayuda al editor y a herramientas de análisis estático (como MyPy)
## a detectar errores y dar sugerencias más precisas.

## 2. Diferencia visual en VS Code
## En Visual Studio Code, los colores de las clases y los módulos dependen de su propósito 
## y de cómo el lenguaje los categoriza:
## Dict de typing:
## Es un alias de tipo usado para anotar el código, pero no tiene un impacto directo en la ejecución.
## Esto puede aparecer con un color diferente porque VS Code lo considera parte de la tipificación estática.
## Clases estándar de Python (como FastAPI, HTTPException, etc.):
## Son clases "reales" utilizadas en tiempo de ejecución y su color en VS Code refleja que tienen 
## un uso operativo en el código.

## 3. ¿Es obligatorio usar Dict en lugar de dict?
## No, no es obligatorio. Puedes usar el tipo nativo dict sin ningún problema si no necesitas 
## anotaciones detalladas de tipo.
## Por ejemplo:
## personas: dict = {}
## Sin embargo, dict no especifica qué tipos de datos contendrán las claves y los valores. 
## Si usas Dict[int, Persona], estás indicando explícitamente que:
##  Las claves serán de tipo int.
##  Los valores serán de tipo Persona.
## Esto mejora la claridad del código y ayuda a herramientas como linters,
##  MyPy o editores avanzados a detectar errores antes de ejecutar el programa.

## 4. Diferencias clave entre Dict y dict
##  Aspecto             dict (nativo)                       Dict (de typing)
##  Importación         No requiere importación.            Requiere importación desde typing.
##  Tipado              No especifica claves y valores.     Permite definir claves y valores con tipos concretos.
##  Uso principal       Para uso cotidiano en ejecución.    Para anotaciones estáticas en el código.
##  Ejemplo             personas: dict                      personas: Dict[int, Persona]

## 5. ¿Por qué Dict aparece diferente en tiempo de ejecución?
## En tiempo de ejecución, Dict y dict son equivalentes. 
## El propósito principal de Dict es proporcionar información adicional 
## de tipo durante el desarrollo, pero en la ejecución real, solo el tipo dict nativo es relevante.
## Por eso, en algunos editores, Dict se distingue visualmente para reflejar que 
## pertenece al ámbito de tipificación estática.

## Conclusión
## El uso de Dict en el módulo typing no es obligatorio, pero es una buena práctica 
## si quieres que tu código sea más claro y esté preparado para herramientas de análisis estático. 
## Su propósito es ayudarte durante el desarrollo, y en tiempo de ejecución, 
## simplemente se comporta como un dict normal.
## Si estás trabajando en proyectos más grandes o colaborativos, 
## usar Dict para especificar tipos puede ser muy beneficioso. 

## MODELO DE DATOS PARA LOS OBJETOS "PERSONA"
## Las clases que representan a los objetos que gestionará nuestra API heredan de BaseModel.
## Esto es lo que permite declarar el tipo de cada dato para que la API.
## Además, si queremos que un dato sea opcional le asociaremos la clase Optional del módulo typing, 
## con la sintaxis que se ve en el ejemplo.
class Persona(BaseModel):
    """
    Clase que representa el esquema de datos de una Persona.
    Validación automática con Pydantic.
    """
    id: int  # ID único de la persona (será asignado automáticamente)
    nombre: str  # Nombre de la persona
    edad: int  # Edad de la persona
    nacionalidad: Optional[str] = None  # Nacionalidad, opcional

# Clase para gestionar el CRUD de personas
class PersonaManager:
    """
    Clase que gestiona las operaciones CRUD y el almacenamiento de personas.
    Usa un diccionario interno para almacenar las personas, donde:
    - La clave es el ID único.
    - El valor es un subdiccionario con los datos de la persona.
    """
    def __init__(self):
        # Inicializamos el diccionario con datos predefinidos
        self.personas: Dict[int, Persona] = {
            1: Persona(id=1, nombre="Juan", edad=30, nacionalidad="Española"),
            2: Persona(id=2, nombre="María", edad=25, nacionalidad="Argentina"),
            3: Persona(id=3, nombre="Luis", edad=40, nacionalidad="Mexicana"),
            4: Persona(id=4, nombre="Ana", edad=35, nacionalidad="Colombiana"),
        }
        # Ajustamos el contador al siguiente ID disponible
        self.counter = max(self.personas.keys()) + 1

    def agregar_persona(self, nombre: str, edad: int, nacionalidad: Optional[str]):
        """
        Crea una nueva persona con un ID autoincremental y la almacena en el diccionario.
        """
        nueva_persona = Persona(id=self.counter, nombre=nombre, edad=edad, nacionalidad=nacionalidad)
        self.personas[self.counter] = nueva_persona
        self.counter += 1
        return nueva_persona

    def obtener_persona(self, id: int):
        """
        Obtiene una persona por su ID. Lanza una excepción si no existe.
        """
        if id not in self.personas:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        return self.personas[id]

    def actualizar_persona(self, id: int, nombre: Optional[str], edad: Optional[int], nacionalidad: Optional[str]):
        """
        Actualiza los datos de una persona existente.
        """
        if id not in self.personas:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        persona = self.personas[id]
        # Actualizamos los campos si son proporcionados
        if nombre is not None:
            persona.nombre = nombre
        if edad is not None:
            persona.edad = edad
        if nacionalidad is not None:
            persona.nacionalidad = nacionalidad
        return persona

    def eliminar_persona(self, id: int):
        """
        Elimina una persona del diccionario por su ID.
        """
        if id not in self.personas:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        del self.personas[id]
        return {"mensaje": f"Persona con ID {id} eliminada exitosamente"}

    def listar_personas(self):
        """
        Devuelve una lista de todas las personas almacenadas.
        """
        return list(self.personas.values())

# Instancia de FastAPI
app = FastAPI()

# Instancia del gestor de personas
persona_manager = PersonaManager()

# Endpoints del API
## El primer endpoint se declara añadiéndole include_in_schema=False. 
## Esto hace que sólo sea accsible desde el navegador, mediante su propia ruta 
##  (en este caso la ruta raíz), pero no sea accesible desde la documentación generada con Swagger.
@app.get("/", include_in_schema=False)
def index():
    return {"mensaje": "Utiliza Swagger (http://127.0.0.1:8000/docs)"}

## Al declaraar los métodos de la API, si estos manejan directamente un objeto de una clase 
## delarada en la aplicación la referiremos con response_model.
## Para agrupar los métodos en la página de documentación de Swagger usaremos el atributo tags.
@app.post("/personas/", response_model=Persona, tags=["CRUD"])
def crear_persona(nombre: str, edad: int, nacionalidad: Optional[str] = None):
    """
    Crea una nueva persona. El ID se asigna automáticamente.
    """
    return persona_manager.agregar_persona(nombre, edad, nacionalidad)

@app.get("/personas/{id}", response_model=Persona, tags=["CRUD"])
def leer_persona(id: int):
    """
    Obtiene una persona por su ID.
    """
    return persona_manager.obtener_persona(id)

@app.put("/personas/{id}", response_model=Persona, tags=["CRUD"])
def actualizar_persona(id: int, nombre: Optional[str] = None, edad: Optional[int] = None, nacionalidad: Optional[str] = None):
    """
    Actualiza los datos de una persona por su ID.
    """
    return persona_manager.actualizar_persona(id, nombre, edad, nacionalidad)

@app.delete("/personas/{id}", tags=["CRUD"])
def eliminar_persona(id: int):
    """
    Elimina una persona por su ID.
    """
    return persona_manager.eliminar_persona(id)

@app.get("/personas/", tags=["Listar"])
def listar_personas():
    """
    Lista todas las personas almacenadas.
    """
    return persona_manager.listar_personas()
