# Map My World Backend API
Este es el backend para Map My World, una aplicación que permite explorar y revisar diferentes ubicaciones y categorías del mundo, como restaurantes, parques y museos.

## Requisitos
* Python 3.7 o superior
* PostgreSQL

## Instalación
### Clonar el repositorio


### Instalar dependencias:

#### Se recomienda usar un entorno virtual para gestionar las dependencias del proyecto.


# Crear y activar el entorno virtual (opcional, pero recomendado)
* python -m venv venv 
* source venv/bin/activate  # En Windows sería `venv\Scripts\activate`

# Instalar las dependencias
* pip install -r requirements.txt

# Configurar la base de datos:

* Asegúrate de tener PostgreSQL instalado y configurado.
* Crea una base de datos para el proyecto (ej. mapmyworld).

# Configuración de variables de entorno:

## Crea un archivo .env en la raíz del proyecto con la configuración necesaria, como la URL de la base de datos PostgreSQL:
#### Nota* recuerda cambiar el usuario y contraseña, por lo general el usuario es "postgres" y la contraseña es la que utilizaste para crear al servidor
* POSTGRES_USER=user
* POSTGRES_PASSWORD=password
* POSTGRES_DB=database
* DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
  
# Ejecución
## Para ejecutar el servidor FastAPI:

* uvicorn app.main:app --reload
* Esto iniciará el servidor en http://localhost:8000.

# Documentación de la API
## Puedes acceder a la documentación interactiva de la API en http://localhost:8000/docs o http://localhost:8000/redoc. Aquí podrás explorar todos los endpoints disponibles y probarlos directamente desde tu navegador.

# Ejecutar pruebas
## Para ejecutar las pruebas unitarias:


* python -m unittest discover -s tests
* Asegúrate de que tu servidor de base de datos esté en funcionamiento ya que el proceso utiliza la base de datos para el proceso de pruebas.

# Docker:
## Ejecuta el siguiente comando para construir y levantar los contenedores de la aplicación y la base de datos:
* docker-compose up --build
#### Esto construirá las imágenes de Docker y levantará los contenedores necesarios para ejecutar la aplicación y la base de datos PostgreSQL.
#### Una vez que los contenedores estén en funcionamiento, la aplicación estará disponible en http://localhost:8000.