# Nueva Vida

## Índice

1. [Iniciar tu Ambiente de Desarrollo](#iniciar-tu-ambiente-de-desarrollo)
    - [Versiones de Software](#versiones-de-software)
    - [Clonar el Repositorio y Ubicarse en la Ruta del Proyecto](#clonar-el-repositorio-y-ubicarse-en-la-ruta-del-proyecto)
    - [Copia del Archivo .env](#1-archivo-env)
    - [Instalación de virtualenv](#2-instalación-de-virtualenv)
    - [Creación de un entorno virtual](#3-creación-de-un-entorno-virtual)
        - [Activación del entorno virtual (en Windows)](#activación-del-entorno-virtual-en-windows)
        - [Activación del entorno virtual (en macOS y Linux)](#activación-del-entorno-virtual-en-macos-y-linux)
    - [Instalación de los Requisitos](#4-instalación-de-los-requisitos)
    - [Inicialización de la Base de Datos](#5-Inicialización-de-la-Base-de-Datos)
    - [Base de Datos para el Servicio Web](#6-base-de-datos-para-el-servicio-web)
    - [Ejecución del Servicio Web](#7-ejecución-del-servicio-web)

2. [Procesos para el Desarrollador](#procesos-para-el-desarrollador)
    - [Guardado de los Requisitos en un Archivo](#1-guardado-de-los-requisitos-en-un-archivo)
    - [Creación de un Proyecto Django](#2-creación-de-un-proyecto-django)

3. [Base de Datos y ropa_reutilizada/manage.py](#base-de-datos-y-ropa_reutilizadamanagepy)
    - [Cambios en los Modelos](#cambios-en-los-modelos)
    - [Super Usuario](#super-usuario)

4. [Para Administradores](#para-administradores)
    - [Configuración de un Modelo](#Configuración-de-un-Modelo)
    - [Crear Nuevas Páginas](#crear-nuevas-páginas)


## Iniciar tu Ambiente de Desarrollo

### Versiones de Software
- **Python**: 3.11.4
- **MySQL**: 8.0.32

### Clonar el Repositorio y Ubicarse en la Ruta del Proyecto

**Clona este repositorio y colócate en la ruta del proyecto `Nueva-Vida/`.**

#### 1. Archivo `.env`

Primero, copia el archivo `ecommerce/.env.bk` a `ecommerce/.env`. **Y modifícalo con tus datos**. Este archivo contiene las variables necesarias para la conexión a la base de datos MySQL.

```sh
cp ecommerce/.env.bk ecommerce/.env
```

#### 2. Instalación de `virtualenv`

Utilizaremos `virtualenv` para mantener solo las bibliotecas necesarias en nuestro entorno de desarrollo.

```sh
pip install virtualenv
```

#### 3. Creación de un entorno virtual

```sh
virtualenv venv
```

- ##### Activación del entorno virtual (en Windows):
  
  ```sh
  venv/Scripts/activate
  ```

- ##### Activación del entorno virtual (en macOS y Linux):
  
  ```sh
  source venv/bin/activate
  ```

#### 4. Instalación de los Requisitos

Asegúrate de tener el entorno virtual activado antes de ejecutar este comando.

```sh
pip install -r requirements.txt
```

#### 5. Inicialización de la Base de Datos

Ingresa a *MySQL* y crea una base de datos **vacía**.

```sh
DROP DATABASE IF EXISTS ropa;
CREATE DATABASE ropa;
```

#### 6. Base de Datos para el Servicio Web

Realiza las migraciones para la base de datos; aquí se harán los cambios para que el administrador pueda hacer el CRUD.

*IMPORTANTE:* Realizar la creación del [Super Usuario](#super-usuario)

```sh
python manage.py migrate
```

#### 7. Ejecución del Servicio Web

```sh
python manage.py runserver
```

## Procesos para el Desarrollador

### 1. Guardado de los Requisitos en un Archivo

Asegúrate de tener el entorno virtual activado antes de ejecutar este comando.

```sh
pip freeze > requirements.txt
```

### 2. Creación de un Proyecto Django

Podemos realizar varios proyectos dependientes o independientes en la aplicación.

```sh
django-admin startproject <nombre>
```

## Base de Datos y ropa_reutilizada/manage.py

### Cambios en los Modelos

```sh
# Hacer archivos para las migraciones
python manage.py makemigrations
```

### Super Usuario

Para crear un nuevo superusuario

```sh
python manage.py createsuperuser
```

## Para Administradores

### Configuración de un Modelo

1. Necesitamos crear el modelo en `models.py`.
2. Registra los modelos en el archivo `admin.py`.
3. Accede a `http://localhost:8000/admin/`.

> **NOTA:** Puedes usar ChatGPT para generar el código del modelo si es necesario, mostrándole la estructura de la tabla y él te

### Crear Nuevas Páginas


1. Agrega el archivo HTML en la carpeta `Nueva-Vida/store/templates/store`.
2. Configura la vista de Django en un archivo `views.py`:

   ```python
   from django.shortcuts import render

   def mi_pagina(request):
       return render(request, 'mi_pagina.html')
   ```

3. Configura una URL asociada a la vista que has creado en el archivo `urls.py`:

   ```python
   from django.urls import path
   from . import views

   urlpatterns = [
       path('mi_pagina/', views.mi_pagina, name='mi_pagina'),
   ]
   ```

4. Accede a la página en el navegador: `http://localhost:8000/mi_pagina/`