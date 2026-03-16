# Logistics Delay Prediction

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

![dist_minutos_atraso Image](https://github.com/PauloBaeza/Logistics-delay-prediction/blob/main/outputs/figures/dist_minutos_atraso.png)

---

## Atraso promedio por empresa y hora

El heatmap permite observar cómo ciertas empresas presentan mayores niveles de atraso en determinadas franjas horarias, lo que sugiere diferencias en comportamiento operativo o planificación logística.

![heatmap_atraso_promedio Image](https://github.com/PauloBaeza/Logistics-delay-prediction/blob/main/outputs/figures/heatmap_atraso_promedio.png)

---

## Patrones temporales de congestión

El análisis por día de la semana y hora permite identificar patrones temporales en los atrasos, evidenciando horarios donde la congestión operacional tiende a aumentar.

![heatmap_congestion_hora Image](https://github.com/PauloBaeza/Logistics-delay-prediction/blob/main/outputs/figures/heatmap_congestion_hora.png)

---

## Relación entre carga operacional y atrasos

Este gráfico compara el número promedio de camiones atendidos por hora con el atraso promedio observado. Se observa que en horarios con mayor carga operacional tienden a aumentar los niveles de atraso.

![cargaOP_promedio Image](https://github.com/PauloBaeza/Logistics-delay-prediction/blob/main/outputs/figures/cargaOP_promedio.png)

---

# Modelado Predictivo

Se entrenaron distintos modelos de regresión para estimar el atraso esperado de una operación logística.

Modelos evaluados:

- Linear Regression
- Random Forest
- XGBoost

La evaluación se realizó utilizando las metricas MAE, R², recall y precision (para un umbral de atrasos superior a 30 min):

  Modelo	      MAE	    R2      Recall_>30	  Precision_>30
  XGBoost	      7.84	  0.75       0.79	          0.81
  Linear	      8.89	  0.67       0.78           0.77
  RandomForest	9.31	  0.65       0.73           0.78


Dado estos resultados el modelo con mejor desempeño fue XGBoost, logrando capturar relaciones no lineales entre las variables operacionales.


---

# Optimización del umbral de alerta

El modelo predice los minutos de atraso esperados para cada operación. Para su uso operativo, se definió un umbral a partir del cual una operación se considera crítica.

Se evaluaron dos escenarios:

**Umbral tradicional (30 min)**  
- Recall: ~0.79  
- Precision: ~0.81  
- Alertas generadas: 2.804

**Umbral optimizado (27 min)**  
- Recall: ~0.87  
- Precision: ~0.76  
- Alertas generadas: 3.287

Reducir el umbral a **27 minutos** permite detectar una mayor proporción de atrasos críticos, generando **483 alertas adicionales**. En un contexto operacional, esto es preferible, ya que no detectar un atraso relevante puede afectar la planificación logística.

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
