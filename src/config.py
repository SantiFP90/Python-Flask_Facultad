from dotenv import load_dotenv
import os

load_dotenv()

# Obtener las variables de entorno
user = os.environ.get("MYSQL_USER", "root")         # Por defecto, usuario es 'root'
password = os.environ.get("MYSQL_PASSWORD", "")     # Por defecto, sin contraseña
host = os.environ.get("MYSQL_HOST", "localhost")    # Por defecto, host es 'localhost'
database = os.environ.get("MYSQL_DATABASE", "flaskmysql")  # Nombre de la base de datos

# Construir la URI de conexión
DATABASE_CONNECTION_URI = f'mysql+pymysql://{user}:{password}@{host}/{database}'


#print(DATABASE_CONNECTION_URI)