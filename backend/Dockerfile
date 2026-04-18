# 1. Usar una imagen base de Python oficial
FROM python:3.11-slim

# 2. Crear una carpeta de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar la lista de ingredientes e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar el resto del código (main.py)
COPY . .

# 5. Comando para encender el servidor cuando el contenedor inicie
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]