# Tarea 3: API & End2End Testing
Este repositorio contiene el código base necesario para el desarrollo de la Tarea 3 del curso de Testing.
La tarea se desarrolla sobre la base de la aplicación **DCCuote** que permite crear, listar y gestionar frases. Tu tarea será escribir una serie de **tests de API y E2E** que validen el comportamiento esperado de la aplicación frente a diferentes interacciones de usuario.

## Estructura del Proyecto
- [`api/`](./api/) → Contiene el backend (Flask API), los archivos docker necesarios para levantarlo, y la estructura base de API testing en pytest.
- [`web/`](./web/) → Contiene el frontend desarrollado con **React** (en TypeScript) y la estructura base de **tests E2E** de Playwright.  

En cada carpeta hay un readme que detalla cómo levantar las aplicaciones.

## Requisitos Previos
- Tener instalado **docker** y **python**
- Tener instalado **Node.js** y **npm**.

## Entrega
Para entregar tu tarea, genera un `.zip` con el siguiente comando, ejecutado desde la raíz del proyecto (la carpeta que contiene `api/` y `web/`):

```bash
git archive --format=zip --prefix=dccuote/ -o tarea3.zip HEAD
```

Este comando arma el `.zip` solo con los archivos que git tiene registrados, así que deja fuera automáticamente todo lo que está en los `.gitignore` (`node_modules/`, `venv/`, `htmlcov/`, etc.) y la carpeta `.git`.

> ⚠️ **Importante:** el comando empaqueta tu **último commit** (`HEAD`), no el estado actual de tus archivos. Cualquier cambio que no hayas commiteado **no quedará en la entrega**. Antes de generar el `.zip`, asegúrate de commitear todo:
>
> ```bash
> git add .
> git commit -m "Entrega Tarea 3"
> ```
>
> Puedes revisar con `git status` que no queden cambios pendientes.

> 💡 **Nota:** si tu carpeta todavía no es un repositorio de git (por ejemplo, si descargaste el código como `.zip`), primero ejecuta `git init` en la raíz del proyecto y luego haz el commit de arriba.