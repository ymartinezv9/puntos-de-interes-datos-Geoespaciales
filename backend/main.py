from fastapi import FastAPI, Query
import psycopg2
import os
from pydantic import BaseModel

app = FastAPI(title="Sistema de Puntos de Interés")

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.get("/")
def home():
    return {"mensaje": "Bienvenido al Sistema Geoespacial"}

@app.get("/mostrar")
def listar_puntos(
    lat: float = Query(None, description="Latitud para búsqueda por proximidad"),
    lon: float = Query(None, description="Longitud para búsqueda por proximidad"),
    radio: int = Query(None, description="Radio en metros (ej. 10000 para 10km)")
):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Si el usuario manda coordenadas y radio, filtramos por cercanía
    if lat is not None and lon is not None and radio is not None:
        query = """
            SELECT id, nombre, descripcion, categoria, ST_AsText(ubicacion)
            FROM puntos
            WHERE ST_DWithin(
                ubicacion, 
                ST_GeogFromText('POINT(' || %s || ' ' || %s || ')'), 
                %s
            );
        """
        cur.execute(query, (lon, lat, radio))
    else:
        # Si no, listamos todo como antes
        cur.execute("SELECT id, nombre, descripcion, categoria, ST_AsText(ubicacion) FROM puntos;")
    
    rows = cur.fetchall()
    resultado = [
        {"id": r[0], "nombre": r[1], "descripcion": r[2], "categoria": r[3], "coords": r[4]} 
        for r in rows
    ]
    
    cur.close()
    conn.close()
    return resultado


class PuntoInteres(BaseModel):
    nombre: str
    descripcion: str
    categoria: str
    latitud: float
    longitud: float

# Nueva ruta para REGISTRAR/AGREGAR
@app.post("/agregar")
def registrar_punto(poi: PuntoInteres):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Insertamos los datos usando la función ST_GeogFromText para el punto geográfico
    query = """
        INSERT INTO puntos (nombre, descripcion, categoria, ubicacion)
        VALUES (%s, %s, %s, ST_GeogFromText('POINT(' || %s || ' ' || %s || ')'))
        RETURNING id;
    """
    cur.execute(query, (poi.nombre, poi.descripcion, poi.categoria, poi.longitud, poi.latitud))
    nuevo_id = cur.fetchone()[0]
    
    conn.commit() # ¡Importante! Guarda los cambios
    cur.close()
    conn.close()
    
    return {"mensaje": "Punto registrado con éxito", "id": nuevo_id}