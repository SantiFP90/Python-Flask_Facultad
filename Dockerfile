FROM python:3.9.7

WORKDIR /src
# CONFIGURAMOS src COMO RAIZ

# Copiar el resto de los archivos
COPY src/requirements.txt .
# copiar requirements.txt primero permite instalar las dependencias antes de copiar el resto de los archivos del proyecto

# Instala las dependencias desde el archivo requirements.txt en la imagen
RUN pip install --no-cache-dir -r requirements.txt

#Copiamos todo lo que tenemos en /src a la imagen
COPY ./src /src

# Comando para ejecutar la aplicación, ejecutamos el ./app.py
ENTRYPOINT ["python", "./app.py"]



