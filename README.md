# Sistema de Registro de Puntos de Interes Geoespacial

Este proyecto implementa una arquitectura de microservicios contenerizada para la gestion de datos geograficos. Utiliza Nginx como proxy reverso con terminacion SSL, FastAPI para la logica de negocio y PostGIS como motor de base de datos geoespacial.

## Estructura del Proyecto

La disposicion de archivos en el entorno de desarrollo es la siguiente:

- **backend/**: Contiene la logica de la API.
  - `Dockerfile`: Definicion de la imagen del servidor de aplicaciones.
  - `main.py`: Script principal de la API REST con FastAPI.
  - `requirements.txt`: Dependencias de Python.
- **db/**: Configuracion de la base de datos.
  - `init.sql`: Script de inicializacion de tablas, extension PostGIS y datos de ejemplo.
- **nginx/**: Configuracion del proxy web.
  - `nginx.conf`: Archivo de configuracion del servidor Nginx.
  - `selfsigned.crt`: Certificado SSL autofirmado generado para el dominio localhost.
  - `selfsigned.key`: Llave privada asociada al certificado SSL.
- **.env**: Archivo de variables de entorno con credenciales reales (No incluido en control de versiones).
- **.env.example**: Plantilla de configuracion para el despliegue inicial.
- **docker-compose.yml**: Orquestador encargado de la construccion y despliegue de los servicios.

## Requisitos de Contenerizacion y Red

El sistema se fundamenta en los siguientes pilares tecnicos:

1. **Contenerizacion Completa**: Cada componente (Base de datos, Servidor de aplicaciones y Proxy) se ejecuta en un contenedor independiente basado en imagenes oficiales.
2. **Red Definida por el Usuario**: Los servicios se comunican a traves de una red de tipo bridge personalizada denominada `geo_network`, permitiendo el aislamiento de los contenedores de la red externa.
3. **Proxy Reverso**: Nginx gestiona el trafico entrante, realizando una redireccion forzosa del puerto 80 (HTTP) al puerto 443 (HTTPS).

## Instrucciones de Construccion y Despliegue

### 1. Configuracion de Entorno
Cree un archivo denominado `.env` en la raiz del proyecto tomando como base el archivo `.env.example`. Asegurese de que los valores de `POSTGRES_USER`, `POSTGRES_PASSWORD` y `DATABASE_URL` sean consistentes entre si.

### 2. Generacion de Certificados SSL
Si los archivos de certificado no estan presentes, pueden generarse mediante el siguiente comando (requiere OpenSSL):
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/selfsigned.key -out nginx/selfsigned.crt -subj "/CN=localhost"
```

### 3. Ejecucion del Sistema
Para construir las imagenes e iniciar los servicios en segundo plano, ejecute: ```docker-compose up --build -d  ```