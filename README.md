# Sistema de Gestión de Tareas con API y Base de Datos

## Descripción

API REST desarrollada con Python y Flask para gestionar usuarios y tareas, utilizando SQLite para la persistencia de datos y Argon2 para proteger las contraseñas mediante hashing.

## Tecnologías

- Python
- Flask
- SQLite
- Argon2

## Instalación y ejecución

1. Instalar las dependencias:

   ```bash
   pip install Flask argon2-cffi
   ```

2. Ejecutar el servidor:

   ```bash
   python servidor.py
   ```

3. Abrir http://127.0.0.1:5000/tareas para consultar la página de bienvenida y la documentación de los endpoints.

## Funcionalidades

- Registro de usuarios e inicio de sesión.
- Hashing de contraseñas con Argon2.
- Autenticación mediante tokens de sesión.
- Operaciones CRUD sobre tareas.
- Persistencia de datos con SQLite.
- Página HTML con la documentación de la API.

## Diagrama del sistema

![Diagrama](./diagrama.jpeg)
