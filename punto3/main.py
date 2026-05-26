import boto3
import pymysql
import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from datetime import datetime

app = FastAPI()

# Configuración S3
S3_BUCKET = 'user-federico-ueia-so'
s3 = boto3.client('s3', region_name='us-east-2')

# Configuración RDS
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def get_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS imagenes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario VARCHAR(255) NOT NULL,
                ruta_s3 VARCHAR(500) NOT NULL,
                fecha_creacion DATETIME NOT NULL
            )
        ''')
    conn.commit()
    conn.close()

@app.on_event("startup")
def startup():
    init_db()

@app.post("/imagenes/")
async def subir_imagen(
    usuario: str = Form(...),
    imagen: UploadFile = File(...)
):
    # Validar formato
    extension = imagen.filename.split('.')[-1].lower()
    if extension not in ['png', 'jpg', 'jpeg']:
        raise HTTPException(status_code=415, detail="Formato no permitido. Use PNG o JPG/JPEG.")

    # Subir a S3
    ruta_s3 = f"{usuario}/{imagen.filename}"
    contenido = await imagen.read()
    s3.put_object(Bucket=S3_BUCKET, Key=ruta_s3, Body=contenido)

    # Registrar en RDS
    fecha = datetime.now()
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute(
            'INSERT INTO imagenes (usuario, ruta_s3, fecha_creacion) VALUES (%s, %s, %s)',
            (usuario, ruta_s3, fecha)
        )
    conn.commit()
    conn.close()

    return {"mensaje": "Imagen subida correctamente", "ruta_s3": ruta_s3, "fecha": fecha}

@app.get("/imagenes/")
def obtener_imagen(usuario: str, nombre_imagen: str):
    # Buscar en RDS
    ruta_s3 = f"{usuario}/{nombre_imagen}"
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute(
            'SELECT * FROM imagenes WHERE usuario=%s AND ruta_s3=%s',
            (usuario, ruta_s3)
        )
        resultado = cursor.fetchone()
    conn.close()

    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario o imagen no encontrados.")

    # Generar URL prefirmada
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': S3_BUCKET, 'Key': ruta_s3},
        ExpiresIn=3600
    )

    return {
        "url": url,
        "fecha_creacion": resultado['fecha_creacion']
    }

from mangum import Mangum
handler = Mangum(app)