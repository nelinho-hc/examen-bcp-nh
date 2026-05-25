# Modelo CLV - Pricing API

Esta API REST expone un modelo optimizado para el cálculo del Customer Lifetime Value (CLV) y la búsqueda de la Tasa Efectiva Anual (TEA) óptima basada en un ROA target. 

El proyecto ha sido refactorizado para eliminar ineficiencias (O(N) a O(1) en búsquedas), implementando cálculos vectorizados con NumPy y un algoritmo de bisección matemática (O(log N)) que reduce el tiempo de ejecución a milisegundos.

## 🚀 Requisitos Previos
- Python 3.12+

## ⚙️ Instalación

1. Clonar el repositorio y acceder a la carpeta del proyecto.
2. Crear un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # En Windows