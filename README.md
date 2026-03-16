# 🚚 Logistics Delay Prediction

Proyecto de análisis y modelado predictivo orientado a identificar factores asociados a retrasos operacionales en un centro de almacenamiento logístico.

El objetivo del proyecto es analizar patrones de congestión en la atención de camiones en un centro de almacenamiento y desarrollar un modelo capaz de estimar el atraso esperado de una operación antes de que ocurra. Esto permite anticipar situaciones de congestión y mejorar la planificación operativa del almacén.

---

# Problema

En centros de almacenamiento logístico, los camiones deben ser atendidos en horarios programados para realizar operaciones de carga o descarga.

Cuando múltiples transportistas llegan en horarios similares o se producen retrasos en operaciones previas, pueden generarse problemas como:

- Congestión en los andenes de carga
- Acumulación de camiones en patio
- Aumento en los tiempos de espera
- Menor eficiencia operativa del centro de distribución

Comprender cuándo y por qué ocurren estos retrasos permite mejorar la planificación de las operaciones y anticipar situaciones de congestión.

---

# Dataset

El dataset "simulado" representa operaciones de camiones en un centro de almacenamiento durante el año 2025 e incluye información sobre:

- Empresa transportista
- Patente del camión
- Tipo de operación (recepción o despacho)
- Tipo de carga
- Fecha de la operación
- Hora programada de atención
- Hora real de inicio de la operación

La variable objetivo es:

"minutos_atraso"

que representa la diferencia entre el horario programado y el momento real de la llegada del camión a la instalación.

---

# Exploratory Data Analysis (EDA)

El análisis exploratorio permitió identificar patrones temporales y operacionales asociados a los retrasos.

## Distribución de atrasos

La distribución de atrasos muestra que la mayoría de las operaciones presentan retrasos moderados, aunque existe una cola hacia valores más altos que refleja eventos operacionales críticos.

![dist_minutos_atraso](image-url)

---

## Atraso promedio por empresa y hora

El heatmap permite observar cómo ciertas empresas presentan mayores niveles de atraso en determinadas franjas horarias, lo que sugiere diferencias en comportamiento operativo o planificación logística.

heatmap_atraso_promedio.png

---

## Patrones temporales de congestión

El análisis por día de la semana y hora permite identificar patrones temporales en los atrasos, evidenciando horarios donde la congestión operacional tiende a aumentar.

heatmap_congestion_hora.png

---

## Relación entre carga operacional y atrasos

Este gráfico compara el número promedio de camiones atendidos por hora con el atraso promedio observado. Se observa que en horarios con mayor carga operacional tienden a aumentar los niveles de atraso.

cargaOP_promedio.png

---

# Modelado Predictivo

Se entrenaron distintos modelos de regresión para estimar el atraso esperado de una operación logística.

Modelos evaluados:

- Linear Regression
- Random Forest
- XGBoost

La evaluación se realizó utilizando:

- MAE (Mean Absolute Error)
- R²

El modelo con mejor desempeño fue XGBoost, logrando capturar relaciones no lineales entre las variables operacionales.

---

# Interpretabilidad del modelo

Se utilizó SHAP (SHapley Additive Explanations) para analizar la importancia de las variables en las predicciones del modelo.

El análisis permitió identificar variables con mayor influencia en los retrasos, como:

- horario de operación
- empresa transportista
- tipo de operación

Esto permite entender no solo cuándo ocurren los atrasos, sino también qué factores contribuyen a ellos.

---

# Aplicación Operacional

El modelo puede utilizarse para:

- Anticipar operaciones con alto riesgo de atraso
- Detectar patrones de congestión
- Apoyar la planificación logística diaria
- Priorizar operaciones críticas

Se desarrolló además un dashboard interactivo en Streamlit para visualizar operaciones programadas y estimar atrasos en tiempo real.

---

# Tecnologías utilizadas

- Python
- Pandas
- Scikit-learn
- XGBoost
- SHAP
- Plotly
- Streamlit

---

# Estructura del repositorio

data/

notebook/

outputs/figures

---

# Autor

Paulo Baeza  
Industrial Engineer | Data Analytics | Logistics Operations
------------------------------------------------------------------------

## License

Este proyecto está licenciado bajo la *MIT License*.  
Puedes consultar el archivo [LICENSE](LICENSE) para más detalles.
