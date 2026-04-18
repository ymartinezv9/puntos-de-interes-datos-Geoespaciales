# Sistema de Registro de Puntos de Interes Geoespacial

Este proyecto implementa una arquitectura de microservicios contenerizada para la gestion de datos geograficos. Utiliza Nginx como proxy reverso con terminacion SSL, FastAPI para la logica de negocio y PostGIS como motor de base de datos geoespacial.

## Estructura del Proyecto

```text
.
├── backend/  
│   ├── app/
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── db/
│   └── init.sql
├── nginx/
│   ├── nginx.conf
│   ├── selfsigned.crt
│   └── selfsigned.key
├── .env.example
├── .gitignore
└── docker-compose.yml
```
### Descripcion de componentes:
- **backend/**: Contiene la logica de la API.
  - `Dockerfile`: Definicion de la imagen del servidor de aplicaciones.
  - `main.py`: Script principal de la API REST con FastAPI.
  - `requirements.txt`: Dependencias de Python.
- **db/**: Configuracion de la base de datos.
  - `init.sql`: Script de inicializacion de tablas, extension PostGIS y datos de ejemplo.
- **nginx/**: Configuracion del proxy web.
  - `nginx.conf`: Archivo de configuracion del servidor Nginx.
  - `selfsigned.crt`: Certificado SSL autofirmado generado para localhost.
  - `selfsigned.key`: Llave privada asociada al certificado SSL.
- **.env.example**: Plantilla de configuracion para el despliegue inicial.
- **docker-compose.yml**: Orquestador encargado de la construccion y despliegue de los servicios.
- **.gitignore**: Archivo para excluir datos sensibles del control de versiones.

## Requisitos de Contenerizacion y Red

El sistema se fundamenta en los siguientes pilares tecnicos:

1. **Contenerizacion Completa**: Cada componente (Base de datos, Servidor de aplicaciones y Proxy) se ejecuta en un contenedor independiente basado en imagenes oficiales.
2. **Red Definida por el Usuario**: Los servicios se comunican a traves de una red de tipo bridge personalizada denominada `geo_network`, permitiendo el aislamiento de los contenedores de la red externa.
3. **Proxy Reverso**: Nginx gestiona el trafico entrante, realizando una redireccion forzosa del puerto 80 (HTTP) al puerto 443 (HTTPS) para garantizar conexiones cifradas.

## Instrucciones de Construccion y Despliegue

### 1. Configuracion de Entorno
Cree un archivo denominado `.env` en la raiz del proyecto tomando como base el archivo `.env.example`. Los valores de `POSTGRES_USER`, `POSTGRES_PASSWORD` y `DATABASE_URL` deben ser consistentes para permitir la conexion.

### 2. Ejecucion del Sistema
Para construir las imagenes e iniciar los servicios en segundo plano, ejecute el siguiente comando en la terminal:
```bash
docker-compose up --build -d 
```
### Uso de la API y Endpoints

El sistema estara accesible a traves de la direccion: ```https://localhost/```

Debido al uso de certificados autofirmados, el navegador presentara una advertencia de seguridad. Es necesario seleccionar la opcion de proceder al sitio de forma manual.

#### Endpoints Disponibles:

- **GET /:** Verificacion de estado del sistema.
- **GET /mostrar:** Recupera el listado de todos los puntos de interes almacenados en formato JSON.
- **POST /agregar:** Registra un nuevo punto geoespacial proporcionando Nombre, Descripcion, Categoria, Latitud y Longitud.
- **Documentacion Interactiva:** ```https://localhost/docs```  (Interfaz Swagger UI para pruebas de endpoints).


#### Persistencia de Datos
La persistencia se gestiona mediante volumenes de Docker, lo que garantiza que la informacion geoespacial almacenada en PostGIS no se pierda al detener los contenedores. Para realizar una limpieza completa, incluyendo la eliminacion de los volumenes de datos, utilice el comando:
```bash
docker-compose down -v
```

**Mecanismo de Almacenamiento:** Se ha definido un volumen nombrado para el servicio de base de datos:
**Nombre del volumen:** postgres_data
**Punto de montaje:** ```/var/lib/postgresql/data dentro del contenedor poi_db. ```

Este mecanismo asegura que:
- Los registros geoespaciales persistan tras reiniciar los contenedores con docker-compose down y docker-compose up.
- El rendimiento de lectura/escritura sea optimo al delegar la gestion del sistema de archivos al motor de Docker.
- Se mantenga una separacion clara entre el ciclo de vida del software (contenedores) y los datos (volumenes).