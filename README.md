# Taller AWS - Sistemas Operativos - Universidad EIA

## Requisitos previos
- Python 3.11+
- AWS CLI configurado con credenciales válidas
- Docker Desktop
- Cuenta de AWS con acceso a S3, RDS, ECR y Lambda

## Clonar el repositorio
```bash
git clone https://github.com/fedriki060/Taller-AWS-EIA-SO.git
cd Taller-AWS-EIA-SO
```

---

## 1. Gestión de archivos en S3

Bucket utilizado: `user-federico-ueia-so` en `us-east-2`.

**Con AWS CLI:**
```bash
aws configure
aws s3 mb s3://user-federico-ueia-so --region us-east-2
aws s3 cp archivo.txt s3://user-federico-ueia-so/
aws s3 cp s3://user-federico-ueia-so/archivo.txt ./descargas/
aws s3 cp ./carpeta/ s3://user-federico-ueia-so/carpeta/ --recursive
```

**Con boto3:**
```bash
cd punto1
pip install boto3
python s3_operations.py
```

---

## 2. Despliegue de FastAPI en EC2

```bash
ssh -i taller-key.pem ubuntu@<IP_PUBLICA>
git clone https://github.com/fedriki060/Taller-AWS-EIA-SO.git
cd Taller-AWS-EIA-SO/test_docker_fastapi
pip install -r requirements.txt --break-system-packages
```

Configurar el daemon:
```bash
sudo nano /etc/systemd/system/fastapi.service
sudo systemctl daemon-reload
sudo systemctl enable fastapi
sudo systemctl start fastapi
```

La app queda accesible en `http://<IP_PUBLICA>:8000`. El servicio arranca automáticamente con la instancia.

Ver capturas en `capturas/punto2/`.

---

## 3. FastAPI con S3, RDS, Docker y Lambda

Crear archivo `.env` en `punto3/`:
```
DB_HOST=taller-db.cryq66muka7c.us-east-2.rds.amazonaws.com
DB_USER=admin
DB_PASSWORD=tu_password
DB_NAME=tallerdb
```

**Ejecutar localmente:**
```bash
cd punto3
pip install -r requirements.txt
uvicorn main:app --reload
```
Documentación en: http://127.0.0.1:8000/docs

**Construir y subir imagen a ECR:**
```bash
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 841162702019.dkr.ecr.us-east-2.amazonaws.com

docker buildx build --platform linux/amd64 --provenance=false \
  -t 841162702019.dkr.ecr.us-east-2.amazonaws.com/fastapi-taller:latest --push .
```

**Despliegue en Lambda:**
1. Crear función Lambda desde la imagen ECR
2. Configurar variables de entorno: `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
3. Habilitar Function URL con Auth type `NONE` y CORS habilitado

Ver capturas en `capturas/punto3/`.