# tfm-mucc

Repositorio del Trabajo de Fin de Máster del Máster Universitario en Ciberseguridad y Ciberinteligencia (MUCC) de la Universitat Politècnica de València (UPV).

## 📌 Descripción

Este proyecto propone un sistema para la **detección de información personal (PII)** en interacciones con modelos de lenguaje, especialmente orientado a proteger la privacidad del usuario en entornos de generación de texto automática (como asistentes conversacionales o plataformas de IA generativa).

Se plantea un enfoque que combina el procesamiento del software Presidio con modelos de lenguaje (LLMs) y el uso de templates segmentados.

## 🧠 Objetivos

- Diseñar un sistema capaz de identificar información personal (PII) en tiempo real dentro de prompts dirigidos a un modelo de lenguaje.
- Evaluar el rendimiento de distintos enfoques de detección.
- Proponer una arquitectura eficiente y usable para la integración de detección y anonimización dentro de pipelines de generación.

## 🗂 Estructura del repositorio
<code>
tfm-mucc/
├── One Template/ # Archivos para las pruebas con un template
│   ├── One_Template.ipynb # Modelo de pruebas con un único template
│   ├── normalize_single_template.ipynb # Código para normalizar las salidas del LLM
│   └── Check_Outputs.ipynb # Código para verificar el rendimiento del LLM
├── Multiple Templates/ # Sistema híbrido de detección
│   ├── Multiple_Templates.ipynb # Notebook del modelo híbrido de detección de PII
│   ├── normalize_multi_template.ipynb # Código para normalizar las salidas del LLM
│   └── Check_Outputs-Multiple.ipynb # Código para verificar el rendimiento del LLM
├── SLURM/ # Código para el despliegue del sistema en SLURM
│   ├── myscript_seg.py # Código Python del modelo híbrido para despliegue
│   └── vLLM_2.job # Script SLURM para el despliegue en HPC
└── README.md # Este archivo
</code>
## 📝 Requisitos

Para utilizar parcial o totalmente estos códigos, se requiere:

- Python 3.12
- vLLM (u otro framework de inferencia como Ollama o Hugging Face; podrían requerirse ajustes menores)
- Presidio Analyzer
- SLURM (o cualquier sistema de gestión de trabajos HPC equivalente; podrían requerirse modificaciones)
- Jupyter Notebook (u otra alternativa compatible)

## ⚠️ Notas

Los códigos proporcionados han sido utilizados para el prototipado. Se ha realizado una limpieza de información adicional y una verificación superficial, por lo que podrían no ser completamente funcionales hasta realizar una validación en profundidad.

## 🚧 TODO

- `requirements.txt`
- Sección de instalación y configuración

