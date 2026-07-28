# واضح (Wadeh) - Herramienta de Análisis Gramatical del Árabe

**Wadeh** es una aplicación web impulsada por IA que automatiza el análisis gramatical del árabe utilizando el modelo ALLaM, alojado en IBM Watsonx. La herramienta ayuda a estudiantes, educadores y entusiastas del idioma árabe proporcionando un análisis gramatical preciso y accesible en árabe.

## Descripción General del Proyecto
Wadeh fue desarrollado como parte del hackathon **Allam Challenge 2024**, seleccionado entre más de 200 ideas por su contribución única a la educación del idioma árabe. Mediante el uso de ingeniería de prompts avanzada con IBM Watsonx, Wadeh puede analizar estructuras gramaticales complejas y ayudar a los usuarios a comprender la sintaxis árabe.

### Características Principales
- **Análisis Gramatical Automatizado**: Proporciona análisis de i'rab (إعراب) para oraciones en árabe.
- **Generador de Oraciones Aleatorias**: Practica con oraciones generadas al azar.
- **Cuestionario de Gramática**: Cuestionarios interactivos para poner a prueba los conocimientos de gramática árabe de los usuarios.
- **Historial del Usuario y Secciones de Ayuda**: Acceso al historial de análisis y preguntas frecuentes para una mejor experiencia de usuario.

## Instalación
Para configurar Wadeh localmente, sigue estos pasos:

1. Clona este repositorio:
   ```bash
   git clone https://github.com/yourusername/wadeh.git
   cd wadeh
   ```

2. Crea un entorno virtual y actívalo:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Para Windows: venv\Scripts\activate
   ```

3. Instala los paquetes requeridos:
   ```bash
   pip install -r requirements.txt
   ```

### Configuración del Entorno
Crea un archivo `.env` en el directorio raíz del proyecto para almacenar las variables de entorno. Utiliza el siguiente formato para el archivo:

```plaintext
MODEL_ID=sdaia/allam-1-13b-instruct
API_URL=https://eu-de.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29
IAM_TOKEN_URL=https://iam.cloud.ibm.com/identity/token
API_KEY=your_ibm_api_key
PROJECT_ID=your_project_id
SECRET_KEY=your_flask_secret_key
```

**Nota**: Asegúrate de reemplazar `your_ibm_api_key`, `your_project_id` y `your_flask_secret_key` con tus valores reales. Mantén este archivo `.env` privado y no lo compartas.

### Uso
Inicia el servidor Flask:
```bash
flask run
```
Abre un navegador web y navega a [http://127.0.0.1:5000/](http://127.0.0.1:5000/) para usar Wadeh.

## Estructura del Proyecto
```plaintext
wadeh/
├── main.py                # Archivo principal de la aplicación
├── .env                   # Variables de entorno
├── templates/
│   └── index.html         # Plantilla HTML
├── static/
│   ├── css/
│   │   ├── styles.css     # Archivo CSS para el estilo
│   │   └── SF-Arabic.ttf  # Fuente
│   ├── js/
│   │   └── script.js      # Archivo JavaScript para la funcionalidad
│   ├── sounds/            # Efectos de sonido para respuestas correctas/incorrectas
│   │   ├── correct.mp3
│   │   └── wrong.mp3
│   └── favicon.ico        # Favicon de la aplicación
├── presentations/         # Presentaciones del proyecto
│   └── "Wadeh".pptx       # Presentación de PowerPoint del proyecto
├── requirements.txt       # Dependencias de Python
└── README.md              # Documentación del proyecto
```


## Funcionalidades
- **Análisis de Oraciones**: Ingresa una oración en árabe y Wadeh analizará su estructura gramatical, proporcionando un i'rab detallado.
- **Cuestionario de Gramática**: Pon a prueba tus conocimientos con un cuestionario de gramática interactivo que cuenta con diversas preguntas y retroalimentación instantánea.
- **Generador de Oraciones Aleatorias**: Genera una oración aleatoria en árabe para practicar el análisis o evaluar tu comprensión.
- **Historial del Usuario y Sección de Ayuda**: Accede a tu historial de análisis y consulta las preguntas frecuentes para obtener orientación.

## Tecnologías Utilizadas
- **Python**: Lógica de backend y manejo de API
- **Flask**: Framework web para manejar solicitudes y renderizar páginas
- **HTML, CSS, JavaScript**: Frontend para la interfaz de usuario
- **IBM Watsonx**: Alojamiento del modelo e ingeniería de prompts para el análisis gramatical del árabe

## Agradecimientos
Este proyecto fue desarrollado como parte del Allam Challenge 2024, centrándose en Modelos de Lenguaje Extensos (LLMs) para el idioma árabe.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT; consulta el archivo LICENSE para más detalles.

## Contacto
Para cualquier consulta o contribución, por favor contacta a **Abdullah Hani Abdellatif Al-Shobaki** en ***abdullah.hani2004@icloud.com***.
