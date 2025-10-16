## Diagrama de Base de Datos
![ERD Mini-Blog](docs/Mini-Blog-DB.png)


# 📝 Mini Blog API  
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)
![Poetry](https://img.shields.io/badge/Poetry-managed-orange.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

API REST construida con **FastAPI** y **PostgreSQL**, diseñada para gestionar usuarios, publicaciones y comentarios.  
Este proyecto forma parte de una **prueba técnica de desarrollador Python**, demostrando un flujo completo desde el modelado de base de datos hasta la implementación del backend con buenas prácticas de desarrollo, control de versiones y documentación.

---

## 🧩 Estructura del Proyecto

mini_blog_api/
│
├── docs/ # Documentación y diagramas (ERD)
│ └── Mini-Blog-DB.png
│
├── src/
│ └── mini_blog_api/
│ ├── core/ # Configuración, base de datos, variables de entorno
│ ├── models/ # Modelos SQLAlchemy
│ ├── schemas/ # Validaciones Pydantic
│ ├── routers/ # Endpoints de API
│ └── main.py # Punto de entrada FastAPI
│
├── tests/ # Carpeta reservada para pruebas unitarias
│
├── .env.example # Ejemplo de variables de entorno
├── .gitignore
├── pyproject.toml # Gestión de dependencias con Poetry
├── poetry.lock
└── README.md


---

## 🧠 Fases del Proyecto

### **Fase 1 — Diseño y Modelado de Base de Datos**
Se diseñó el modelo relacional con tres entidades principales:

- **users** → almacena datos de los usuarios  
- **posts** → publicaciones creadas por los usuarios  
- **comments** → comentarios asociados a publicaciones

📄 **Archivo:** [`docs/Mini-Blog-DB.png`](docs/Mini-Blog-DB.png)

Relaciones principales:
- 1 usuario → *N* publicaciones  
- 1 usuario → *N* comentarios  
- 1 publicación → *N* comentarios  

Claves foráneas:
- `posts.author_id → users.id [ON DELETE RESTRICT]`
- `comments.author_id → users.id [ON DELETE RESTRICT]`
- `comments.post_id → posts.id [ON DELETE CASCADE]`

---

### **Fase 2 — Backend con FastAPI y SQLAlchemy**

#### Tecnologías principales
- **FastAPI** → framework backend asincrónico  
- **SQLAlchemy (async)** → ORM para PostgreSQL  
- **Pydantic** → validación y serialización de datos  
- **Poetry** → gestión de dependencias  
- **Uvicorn** → servidor ASGI  

#### Endpoints implementados

| Módulo | Método | Endpoint | Descripción |
|--------|---------|-----------|--------------|
| Usuarios | `POST` | `/users/` | Crear un nuevo usuario |
| Usuarios | `GET` | `/users/{user_id}` | Obtener detalles de un usuario |
| Publicaciones | `POST` | `/posts/` | Crear nueva publicación |
| Publicaciones | `GET` | `/posts/` | Listar las últimas publicaciones |
| Publicaciones | `GET` | `/posts/{post_id}` | Obtener una publicación con sus comentarios |
| Comentarios | `POST` | `/posts/{post_id}/comments` | Añadir comentario a una publicación |

---

## ⚙️ Instalación y Configuración

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/JosiasCH/mini_blog_api.git
cd mini_blog_api


2️⃣ Crear entorno con Poetry
poetry install


3️⃣ Configurar variables de entorno

Crea un archivo .env basado en .env.example:

DATABASE_URL=postgresql+asyncpg://postgres:tu_password@localhost:5432/mini_blog


4️⃣ Ejecutar migraciones (opcional, si se agrega Alembic)
poetry run alembic upgrade head


5️⃣ Levantar el servidor
poetry run uvicorn mini_blog_api.main:app --reload --app-dir src



Servidor disponible en:
👉 http://127.0.0.1:8000

Documentación interactiva Swagger:
👉 http://127.0.0.1:8000/docs



🌱 Flujo de ramas (Git Flow)
Rama	Propósito
main	Producción estable (releases)
develop	Integración de nuevas features
docs/fase1-erd	Modelado y documentación (Fase 1)
feat/fase2-api	Implementación del backend (Fase 2)


🧾 Licencia

Este proyecto se distribuye bajo la licencia MIT.
Eres libre de usarlo, modificarlo y distribuirlo, siempre que se mantengan los créditos correspondientes.


✨ Autor

Josias CH
Desarrollador Python | Data Scientist | Backend Developer
📧 20210614@aloe.ulima.edu.pe

🔗 GitHub - JosiasCH

---


