import boto3
import os

BUCKET = 'user-federico-ueia-so'
s3 = boto3.client('s3', region_name='us-east-2')

# Cargar un archivo
s3.upload_file('archivo_prueba.txt', BUCKET, 'boto3/archivo_prueba.txt')
print('Archivo cargado correctamente')

# Listar todos los archivos e imprimirlos
response = s3.list_objects_v2(Bucket=BUCKET, Prefix='boto3/')
for obj in response['Contents']:
    print(f'En bucket: {obj["Key"]}')

# Descargar a carpeta diferente
os.makedirs('descargas_boto3', exist_ok=True)
s3.download_file(BUCKET, 'boto3/archivo_prueba.txt', 'descargas_boto3/archivo_prueba.txt')
print('Archivo descargado correctamente')

# Verificar descarga
with open('descargas_boto3/archivo_prueba.txt', 'r') as f:
    print(f'Contenido: {f.read()}')

# Cargar tres archivos
archivos = ['texto1.txt', 'texto2.txt', 'texto3.txt']

for archivo in archivos:
    with open(archivo, 'w') as f:   #abre archivo en modo write con el nombre de f 
        f.write(f'Contenido de {archivo}')
    s3.upload_file(archivo, BUCKET, f'boto3/multiples/{archivo}')
    print(f'{archivo} cargado correctamente')

# Listar los tres archivos e imprimirlos
response = s3.list_objects_v2(Bucket=BUCKET, Prefix='boto3/multiples/')
for obj in response['Contents']:
    print(f'En bucket: {obj["Key"]}')

# Descargar los tres
os.makedirs('descargas_boto3/multiples', exist_ok=True)
for archivo in archivos:
    s3.download_file(BUCKET, f'boto3/multiples/{archivo}', f'descargas_boto3/multiples/{archivo}')
    print(f'{archivo} descargado correctamente')

# Verificar descarga
for archivo in archivos:
    with open(f'descargas_boto3/multiples/{archivo}', 'r') as f:
        print(f'Contenido de {archivo}: {f.read()}')