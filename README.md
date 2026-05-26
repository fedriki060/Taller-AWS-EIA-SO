# Taller AWS - Sistemas Operativos - Universidad EIA

## 1. Gestión de archivos en Amazon S3

### a. Creación del bucket

Bucket creado desde la consola web de AWS con el nombre `user-federico-ueia-so` en la región `us-east-2`.

### b. Operaciones usando AWS CLI

```cmd
aws configure
AWS Access Key ID [None]: ****************
AWS Secret Access Key [None]: ****************
Default region name [None]: us-east-1
Default output format [None]: json

aws sts get-caller-identity
{
    "UserId": "841162702019",
    "Account": "841162702019",
    "Arn": "arn:aws:iam::841162702019:root"
}

aws configure set region us-east-2

aws s3 ls
2026-05-25 19:30:03 user-federico-ueia-so

echo Este es mi archivo de prueba > %USERPROFILE%\archivo_prueba.txt

aws s3 cp %USERPROFILE%\archivo_prueba.txt s3://user-federico-ueia-so/
upload: .\archivo_prueba.txt to s3://user-federico-ueia-so/archivo_prueba.txt

aws s3 ls s3://user-federico-ueia-so/
2026-05-25 19:30:47         31 archivo_prueba.txt

aws s3 cp s3://user-federico-ueia-so/archivo_prueba.txt -
Este es mi archivo de prueba

mkdir %USERPROFILE%\descargas_s3

aws s3 cp s3://user-federico-ueia-so/archivo_prueba.txt %USERPROFILE%\descargas_s3\
download: s3://user-federico-ueia-so/archivo_prueba.txt to descargas_s3\archivo_prueba.txt

type %USERPROFILE%\descargas_s3\archivo_prueba.txt
Este es mi archivo de prueba

mkdir %USERPROFILE%\multi

echo Archivo uno > %USERPROFILE%\multi\archivo1.txt
echo Archivo dos > %USERPROFILE%\multi\archivo2.txt
echo Archivo tres > %USERPROFILE%\multi\archivo3.txt

aws s3 cp %USERPROFILE%\multi\ s3://user-federico-ueia-so/multi/ --recursive
upload: multi\archivo2.txt to s3://user-federico-ueia-so/multi/archivo2.txt
upload: multi\archivo3.txt to s3://user-federico-ueia-so/multi/archivo3.txt
upload: multi\archivo1.txt to s3://user-federico-ueia-so/multi/archivo1.txt

aws s3 ls s3://user-federico-ueia-so/multi/
2026-05-25 19:34:56         14 archivo1.txt
2026-05-25 19:34:56         14 archivo2.txt
2026-05-25 19:34:56         15 archivo3.txt

mkdir %USERPROFILE%\descargas_s3\multi

aws s3 cp s3://user-federico-ueia-so/multi/ %USERPROFILE%\descargas_s3\multi\ --recursive
download: s3://user-federico-ueia-so/multi/archivo1.txt to descargas_s3\multi\archivo1.txt
download: s3://user-federico-ueia-so/multi/archivo2.txt to descargas_s3\multi\archivo2.txt
download: s3://user-federico-ueia-so/multi/archivo3.txt to descargas_s3\multi\archivo3.txt

dir %USERPROFILE%\descargas_s3\multi
 Volume in drive C has no label.
 Volume Serial Number is 5333-5F8A

 Directory of C:\Users\RicoB\descargas_s3\multi

05/25/2026  07:34 PM    <DIR>          .
05/25/2026  07:33 PM    <DIR>          ..
05/25/2026  07:34 PM                14 archivo1.txt
05/25/2026  07:34 PM                14 archivo2.txt
05/25/2026  07:34 PM                15 archivo3.txt
               3 File(s)             43 bytes
               2 Dir(s)  46,024,986,624 bytes free
```

### Qué cambia con múltiples archivos

Con un solo archivo se usa `cp` apuntando al archivo directamente. Con múltiples archivos se agrega el flag `--recursive` apuntando a una carpeta, lo que hace que el CLI procese todos los archivos dentro de ella de una sola vez.

### c. Operaciones usando boto3

El script `s3_operations.py` realiza las mismas operaciones que el CLI pero desde Python usando la librería boto3.

**Resultado de ejecución:**
Archivo cargado correctamente
En bucket: boto3/archivo_prueba.txt
Archivo descargado correctamente
Contenido: Este es mi archivo de prueba

texto1.txt cargado correctamente
texto2.txt cargado correctamente
texto3.txt cargado correctamente
En bucket: boto3/multiples/texto1.txt
En bucket: boto3/multiples/texto2.txt
En bucket: boto3/multiples/texto3.txt
texto1.txt descargado correctamente
texto2.txt descargado correctamente
texto3.txt descargado correctamente
Contenido de texto1.txt: Contenido de texto1.txt
Contenido de texto2.txt: Contenido de texto2.txt
Contenido de texto3.txt: Contenido de texto3.txt

### Qué cambia con múltiples archivos en boto3

Con un solo archivo se llama `upload_file` y `download_file` una vez. Con múltiples archivos se itera sobre una lista con un `for` loop, llamando estas funciones por cada archivo.