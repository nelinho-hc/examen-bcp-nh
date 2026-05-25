# 🚀 API de Optimización de Pricing - Modelo CLV (Customer Lifetime Value)

## 📌 Descripción Ejecutiva
Este proyecto implementa una solución de alto rendimiento para el cálculo del **Customer Lifetime Value (CLV)** y la optimización de la **Tasa Efectiva Anual (TEA)** basada en un ROA objetivo. Diseñada con una arquitectura limpia e implementada mediante **FastAPI**, esta API expone el motor de *pricing* para ser integrado en procesos reactivos y proactivos de asignación de tasas.

El refactor del modelo original elimina cuellos de botella críticos, garantizando respuestas en milisegundos y estandarizando los flujos de salida para asegurar consistencia en procesos de consolidación y reportería aguas abajo.

---

## 🏗️ Arquitectura y Decisiones Técnicas

El código *legacy* fue reescrito desde cero aplicando principios SOLID, modularidad y separación de responsabilidades:

* **Optimización de Accesos a Datos $O(1)$:** El motor original leía archivos CSV iterativamente y utilizaba funciones ineficientes de Pandas (`.iterrows`). Esto fue reemplazado por un patrón de carga única en memoria al inicio de la aplicación (Singleton *DataLoader*), transformando los DataFrames en diccionarios de Python para consultas instantáneas.
* **Algoritmo de Bisección Pura:** Se eliminó el barrido lineal ineficiente en la búsqueda de la TEA. Se implementó un algoritmo de búsqueda binaria (bisección) que converge hacia la tasa óptima para el ROA target en complejidad logarítmica, logrando una precisión ≤ 0.01.
* **Cálculos Financieros Vectorizados:** Las operaciones de interpolación de tasas de fondeo (`np.interp`) y la generación de curvas de supervivencia y amortización utilizan el poder de **NumPy** a nivel de C.
* **Salidas Estandarizadas:** Los esquemas de respuesta fueron rediseñados mediante **Pydantic** para priorizar y asegurar el orden de las columnas (ej. identificadores de operación, producto y métricas), facilitando auditorías y flujos ETL posteriores.

---

## 📂 Estructura del Proyecto

El repositorio sigue una arquitectura de capas diseñada para escalar:

> ```text
> ├── app/
> │   ├── main.py                 # Entry point y definición de endpoints FastAPI
> │   ├── core/
> │   │   ├── config.py           # Centralización de configuraciones y rutas
> │   │   └── data_loader.py      # Gestor de memoria optimizado para DataFrames
> │   ├── data/                   # Archivos de insumo (Costos, Curvas PD, Fondeo)
> │   ├── models/
> │   │   └── schemas.py          # Validación de inputs y estandarización de outputs
> │   └── services/
> │       ├── clv_engine.py       # Orquestador del flujo de caja (Ingresos, Egresos, PE)
> │       ├── financial_core.py   # Lógica matemática, interpolación y amortización
> │       └── tea_optimizer.py    # Algoritmo de bisección para búsqueda de TEA
> ├── tests/
> │   └── test_clv.py             # Suite de pruebas automatizadas (cobertura total)
> ├── requirements.txt            # Dependencias del proyecto
> └── README.md                   # Documentación principal
> ```

---

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3.12+
* **Framework REST:** FastAPI & Uvicorn
* **Cálculo Numérico:** NumPy, Pandas
* **Testing:** Pytest, Httpx
* **Validación:** Pydantic

---

## ⚙️ Instrucciones de Instalación y Despliegue

La API está configurada para levantarse de manera ágil. Sigue estos pasos para ejecutar el proyecto en un entorno local:

**1. Clonar el repositorio y acceder a la carpeta:**
```bash
git clone https://github.com/nelinho-hc/examen-bcp-nh.git
```

**2. Configurar entorno virtual e instalar dependencias:**
```bash
python -m venv venv
pip install -r requirements.txt
```

**3. Iniciar el servicio (Un solo comando):**
```bash
uvicorn app.main:app --reload
```

## 📖 Uso de la API (Endpoints)

Una vez iniciado el servicio, puedes acceder a la interfaz interactiva de Swagger UI visitando:
👉 http://127.0.0.1:8000/docs

Endpoints Disponibles:
* GET /health: Validación de estado (Healthcheck).
* POST /calcular: Calcula el CLV y la TEA para una operación individual.
* POST /calcular/lote: Procesa un array de operaciones y devuelve la consolidación optimizada en un solo request.

## 🧪 Pruebas y Aseguramiento de Calidad

El proyecto incluye una suite exhaustiva para garantizar que las refactorizaciones mantienen la integridad de los modelos financieros (tolerancia máxima de ≤ 0.01). Para ejecutar los tests unitarios y de integración, utiliza el siguiente comando en la raíz del proyecto:
```bash
python -m pytest -v
```
