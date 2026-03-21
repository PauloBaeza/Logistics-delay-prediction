# Logistics Delay Prediction

Proyecto de análisis y modelado predictivo orientado a identificar factores asociados a retrasos operacionales en un centro de almacenamiento logístico.

El objetivo del proyecto es analizar patrones de congestión en la atención de camiones en un centro de almacenamiento y desarrollar un modelo capaz de estimar el atraso esperado de una operación antes de que ocurra. Esto permite anticipar situaciones de congestión y mejorar la planificación operativa del almacén.

---

## Contexto del problema

En centros de almacenamiento logístico, los camiones llegan para realizar operaciones de carga o descarga en horarios previamente programados. Sin embargo, factores como la congestión operativa, la acumulación de camiones en determinadas franjas horarias o variaciones en los tiempos de operación pueden generar atrasos en la atención.


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

## Variables utilizadas

Variable objetivo:
- minutos_atraso: minutos de retraso respecto a la hora programada.

Variables numéricas:
- hora_programada_min: hora programada en minutos.

Variables categóricas:
- empresa: empresa de transporte.
- patente: identificador del vehículo.
- tipo_operacion: tipo de operación.
- tipo_carga: tipo de carga.
- dia_semana: día de la semana.

Preprocesamiento:
- One-Hot Encoding para variables categóricas.
- Variables numéricas sin transformación.

Modelos evaluados:

- Linear Regression
- Random Forest
- XGBoost


### Evaluación de modelos

La evaluación se realizó utilizando las métricas **MAE, R², Recall y Precision** (para un umbral de atraso superior a 30 minutos).

| Modelo        | MAE | R²  | Recall (>30 min) | Precision (>30 min) |
|---------------|-----|-----|------------------|---------------------|
| XGBoost       | 7.70 | 0.75 | 0.79 | 0.81 |
| Linear        | 8.81 | 0.67 | 0.78 | 0.76 |
| Random Forest | 9.29 | 0.65 | 0.72 | 0.78 |


Dado estos resultados el modelo con mejor desempeño fue XGBoost, logrando capturar relaciones no lineales entre las variables operacionales.

---

# Aplicación Operacional

El modelo puede utilizarse para:

- Anticipar operaciones con alto riesgo de atraso
- Detectar patrones de congestión
- Apoyar la planificación logística diaria
- Priorizar operaciones críticas

Se desarrolló además un dashboard interactivo en Streamlit para visualizar operaciones programadas y estimar atrasos en tiempo real.
Link de acceso: https://logistics-delay-prediction.streamlit.app/ 
(Para probar la app y visualizar la información se necesita ingresar un rango de fecha en el panel)

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

data/raw (set de datos sinteticos)

app (Interfaz creada en streamlit)

notebook/

outputs/figures


---

# Autor

Paulo Baeza A.
------------------------------------------------------------------------

## License

Este proyecto está licenciado bajo la *MIT License*.  
Puedes consultar el archivo [LICENSE](LICENSE) para más detalles.
