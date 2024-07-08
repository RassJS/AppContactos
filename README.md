# AppContactos

# Descripcion
Aplicacion web de agenda de contactos con Flask.
Permite a los usuarios registrarse, iniciar sesion, agregar contactos, ver los contactos agregados y eliminar contactos.
La informacion de los usuarios y los contactos se almacena en una base de datos MySQL.

# Instalacion
Clonar el repositorio
git clone https://github.com/tuusuario/AppContactos.git
cd AppContactos

# Crear y activar un entorno virtual

python -m venv venv
source venv/bin/activate 

# Instalar dependencias

pip install -r requirements.txt

# Configurar la base de datos

CREATE DATABASE agenda;

# Edita la configuración de la base de datos en el archivo app.py

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://usuario:contraseña@localhost/agenda'


# Ejecuta la aplicacion

flask run
