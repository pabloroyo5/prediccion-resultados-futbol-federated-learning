# Predicción del Resultado de Partidos de Fútbol usando Aprendizaje Automático Federado

> Guía de uso para utilizar la aplicación web.

## Instalación

### Antes de empezar

Antes de comenzar, debemos tener instalado en nuestro sistema lo siguiente:

- [X] NPM - [instructions](https://yarnpkg.com/en/docs/install#mac-stable)
- [X] Vue Cli 3 - [instructions](https://cli.vuejs.org/guide/installation.html)
- [X] Python 3

### Comenzando

* Clona el repositorio:

    ```bash
    git clone https://github.com/pabloroyo5/prediccion-resultados-futbol-federated-learning.git
    ```

* Configura el entorno virtual, instala las dependencias y actívalo:

    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # or ".\venv\Scripts\activate" on Windows
    pip install -r requirements.txt
    ```

* Instala las dependencias de JavaScript:

    ```bash
    cd frontend/frontend
    npm install
    ```

### Development Servers

Inicia el servidor de la API creada con Flask:

```bash
cd backend
python main.py
```

Desde otra tab, colocate en el directorio `/frontend/frontend` y ejecuta el siguiente comando:

```bash
npm run serve
```

La aplicación de Vue.js se servirá desde `localhost:8080` y la API de Flask y los archivos estáticos se servirán desde `localhost:5000`.
Por tanto solom queda abrir un navegador y acceder al enlace `localhost:8080` para observar el frontend de la página.

