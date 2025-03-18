# Usamos una imagen base de Python
FROM python:3.9-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos los archivos necesarios al contenedor
COPY . /app

# Instalamos las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn  # Añadimos Uvicorn aquí

# Exponemos el puerto para acceder a la API
EXPOSE 5000

# Ejecutamos el servidor de la API
CMD ["uvicorn", "create_groups:app", "--host", "0.0.0.0", "--port", "5000"]

