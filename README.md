# Trabajo Práctico 0 - Programación 3 (2023)

## Descripción

Este repositorio contiene el desarrollo del Trabajo Práctico 0 para la materia Programación 3 (2023). El proyecto consiste en una aplicación web basada en Python y Flask, que utiliza SQLAlchemy para interactuar con una base de datos MySQL. El dominio de la aplicación está relacionado con la gestión de una jardinería, permitiendo manejar clientes, productos y pagos, entre otros.

## Tecnologías utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- MySQL
- PyMySQL

## Estructura del repositorio

- `app.py`: Archivo principal de la aplicación Flask.
- `insumos/`: Carpeta con scripts SQL, datos de ejemplo y notas de desarrollo.
- Otros archivos relacionados con el trabajo práctico y helpers.

## Instalación y ejecución

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/claudiomaza/p3_9023_tp0.git
   cd p3_9023_tp0
   ```

2. Instalar las dependencias de Python:
   ```bash
   pip install flask flask_sqlalchemy pymysql
   ```

3. Configurar la base de datos MySQL:
   - Crear una base de datos llamada `jardineria`.
   - Importar los datos y estructuras desde los archivos en `insumos/`.

4. Ejecutar la aplicación:
   ```bash
   python app.py
   ```

5. Acceder a la aplicación en `http://localhost:5000/`.

## Endpoints principales

- `/clientes/pais/<pais>`: Devuelve una lista de clientes por país.
- `/productos/<gama>`: Devuelve productos de una gama específica.

## Autor

- Claudio Maza
