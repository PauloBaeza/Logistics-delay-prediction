import joblib
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path


# Configuración página

st.set_page_config(
    page_title="Logistics Analytics",
    page_icon="",
    layout="wide",
)


# CSS / estilo
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #081225 0%, #0c1a33 100%);
        color: #f8fafc;
    }

    section[data-testid="stSidebar"] {
        background: #0b1730;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1rem;
        max-width: 1500px;
    }

    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #f8fafc;
    }

    .app-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #ffffff;
    }

    .panel {
        background: rgba(18, 31, 59, 0.85);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1rem 1rem 0.8rem 1rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.25);
    }

    .kpi-card {
        background: rgba(18, 31, 59, 0.95);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 0.9rem 1rem;
        min-height: 112px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.25);
    }

    .kpi-label {
        font-size: 0.95rem;
        color: #cbd5e1;
        margin-bottom: 0.3rem;
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.1;
        color: #ffffff;
    }

    .kpi-sub {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 0.2rem;
    }

    .critical-card {
        background: rgba(18, 31, 59, 0.95);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 0.9rem 1rem;
        min-height: 112px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.25);
    }

    .pill {
        display: inline-block;
        padding: 0.28rem 0.65rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-top: 0.4rem;
    }

    .pill-critical { background: rgba(239, 68, 68, 0.18); color: #fca5a5; }
    .pill-high     { background: rgba(245, 158, 11, 0.18); color: #fcd34d; }
    .pill-medium   { background: rgba(59, 130, 246, 0.18); color: #93c5fd; }
    .pill-low      { background: rgba(34, 197, 94, 0.18); color: #86efac; }

    .table-note {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.08);
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        background: linear-gradient(180deg, #315db8 0%, #264a96 100%);
        color: white;
        font-weight: 700;
        padding: 0.7rem 1rem;
    }

    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stNumberInput > div > div,
    .stSlider > div > div {
        background: rgba(255,255,255,0.03);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Paths

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

MODEL_CANDIDATES = [
    BASE_DIR / "models" / "xgb_pipeline.pkl",
    PROJECT_ROOT / "app" / "models" / "xgb_pipeline.pkl",
    PROJECT_ROOT / "models" / "xgb_pipeline.pkl",
]

DATA_CANDIDATES = [
    PROJECT_ROOT / "data" / "raw" / "logistics_24h_hhmmss.csv",
    PROJECT_ROOT / "data" / "logistics_24h_hhmmss.csv",
    BASE_DIR / "data" / "raw" / "logistics_24h_hhmmss.csv",
]


# Carga modelo / datos

@st.cache_resource
def load_model():
    for path in MODEL_CANDIDATES:
        if path.exists():
            return joblib.load(path)

    st.error(
        "No se encontró el modelo. Revisa alguna de estas rutas:\n\n"
        + "\n".join([str(p) for p in MODEL_CANDIDATES])
    )
    st.stop()

@st.cache_data
def load_data():
    for path in DATA_CANDIDATES:
        if path.exists():
            return pd.read_csv(path)

    st.error(
        "No se encontró el CSV base. Revisa alguna de estas rutas:\n\n"
        + "\n".join([str(p) for p in DATA_CANDIDATES])
    )
    st.stop()

model = load_model()
df = load_data()


# Normalización / features

if "fecha" not in df.columns:
    st.error("El dataset debe contener la columna 'fecha'.")
    st.stop()

df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

if df["fecha"].isna().all():
    st.error("No fue posible convertir la columna 'fecha' a formato datetime.")
    st.stop()

required_base = ["empresa", "patente", "tipo_operacion", "tipo_carga", "minutos_atraso"]
for col in required_base:
    if col not in df.columns:
        st.error(f"Falta la columna requerida: '{col}'")
        st.stop()

if "hora_programada_min" not in df.columns:
    if "hora_programada" in df.columns:
        hp = pd.to_datetime(df["hora_programada"], format="%H:%M:%S", errors="coerce")
        df["hora_programada_min"] = hp.dt.hour * 60 + hp.dt.minute
    else:
        st.error("El dataset necesita 'hora_programada_min' o 'hora_programada'.")
        st.stop()

if "hora_programada" not in df.columns:
    df["hora_programada"] = (
        (df["hora_programada_min"] // 60).astype(int).astype(str).str.zfill(2)
        + ":"
        + (df["hora_programada_min"] % 60).astype(int).astype(str).str.zfill(2)
    )

# Variables temporales del modelo
mapa_dias = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo",
}

mapa_meses = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}

if "dia_semana" not in df.columns:
    df["dia_semana"] = df["fecha"].dt.dayofweek.map(mapa_dias)

if "mes" not in df.columns:
    df["mes"] = df["fecha"].dt.month.map(mapa_meses)

if "es_fin_semana" not in df.columns:
    df["es_fin_semana"] = df["dia_semana"].isin(["Sábado", "Domingo"]).astype(int)

predict_cols = [
    "empresa",
    "patente",
    "tipo_operacion",
    "tipo_carga",
    "hora_programada_min",
    "dia_semana",
    "mes",
    "es_fin_semana",
]

for col in predict_cols:
    if col not in df.columns:
        st.error(f"Falta una columna que el modelo necesita: '{col}'")
        st.stop()

# Predicción

pred_input = df[predict_cols].copy()
df["atraso_estimado"] = model.predict(pred_input)

UMBRAL_CRITICO = 27

def clasificar_riesgo(x: float) -> str:
    if x >= UMBRAL_CRITICO:
        return "Crítico"
    if x >= 19:
        return "Alto"
    if x >= 11:
        return "Medio"
    return "Bajo"

df["riesgo"] = df["atraso_estimado"].apply(clasificar_riesgo)

def riesgo_color_text(riesgo: str) -> str:
    return {
        "Crítico": "#ef4444",
        "Alto": "#f59e0b",
        "Medio": "#60a5fa",
        "Bajo": "#22c55e",
    }.get(riesgo, "#94a3b8")


# Sidebar filtros

st.markdown('<div class="app-title">Logistics Analytics</div>', unsafe_allow_html=True)

fecha_min = df["fecha"].min().date()
fecha_max = df["fecha"].max().date()

with st.sidebar:
    st.markdown("## Filtros")

    rango_fechas = st.date_input(
        "Rango de fechas",
        value=(fecha_min, fecha_max),
        min_value=fecha_min,
        max_value=fecha_max,
    )

    empresas = ["Todas"] + sorted(df["empresa"].dropna().astype(str).unique().tolist())
    tipos_operacion = ["Todas"] + sorted(df["tipo_operacion"].dropna().astype(str).unique().tolist())
    tipos_carga = ["Todas"] + sorted(df["tipo_carga"].dropna().astype(str).unique().tolist())

    empresa_sel = st.selectbox("Empresa transportista", empresas)
    tipo_op_sel = st.selectbox("Tipo de operación", tipos_operacion)
    tipo_carga_sel = st.selectbox("Tipo de carga", tipos_carga)

    min_h = int(df["hora_programada_min"].min() // 60)
    max_h = int(df["hora_programada_min"].max() // 60)
    rango_horas = st.slider("Rango horario", 0, 23, (min_h, max_h))


# Aplicar filtros

df_f = df.copy()

# fecha / rango
if isinstance(rango_fechas, tuple) and len(rango_fechas) == 2:
    fecha_ini, fecha_fin = rango_fechas
    df_f = df_f[
        (df_f["fecha"].dt.date >= fecha_ini) &
        (df_f["fecha"].dt.date <= fecha_fin)
    ]
else:
    df_f = df_f[df_f["fecha"].dt.date == rango_fechas]

if empresa_sel != "Todas":
    df_f = df_f[df_f["empresa"] == empresa_sel]

if tipo_op_sel != "Todas":
    df_f = df_f[df_f["tipo_operacion"] == tipo_op_sel]

if tipo_carga_sel != "Todas":
    df_f = df_f[df_f["tipo_carga"] == tipo_carga_sel]

hora_ini = rango_horas[0] * 60
hora_fin = rango_horas[1] * 60 + 59
df_f = df_f[
    (df_f["hora_programada_min"] >= hora_ini) &
    (df_f["hora_programada_min"] <= hora_fin)
]

df_f = df_f.sort_values("atraso_estimado", ascending=False).reset_index(drop=True)


# KPIs

total_ops = len(df_f)
avg_delay = float(df_f["atraso_estimado"].mean()) if total_ops else 0.0
critical_ops = int((df_f["atraso_estimado"] >= UMBRAL_CRITICO).sum()) if total_ops else 0

if total_ops > 0:
    top_row = df_f.iloc[0]
    top_empresa = str(top_row["empresa"])
    top_patente = str(top_row["patente"])
    top_hora = str(top_row["hora_programada"])
    top_fecha = pd.to_datetime(top_row["fecha"]).strftime("%d-%m-%Y")
    top_delay = float(top_row["atraso_estimado"])
    top_risk = str(top_row["riesgo"])
else:
    top_empresa = "-"
    top_patente = "-"
    top_hora = "-"
    top_fecha = "-"
    top_delay = 0.0
    top_risk = "-"

k1, k2, k3, k4 = st.columns([1.05, 1.05, 1.0, 1.2])

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Operaciones filtradas</div>
        <div class="kpi-value">{total_ops}</div>
        <div class="kpi-sub">según filtros seleccionados</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Atraso promedio estimado</div>
        <div class="kpi-value">{avg_delay:.1f}</div>
        <div class="kpi-sub">minutos</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Alertas críticas</div>
        <div class="kpi-value">{critical_ops}</div>
        <div class="kpi-sub">umbral crítico: {UMBRAL_CRITICO} min</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    pill_class = (
        "pill-critical" if top_risk == "Crítico"
        else "pill-high" if top_risk == "Alto"
        else "pill-medium" if top_risk == "Medio"
        else "pill-low"
    )

    st.markdown(f"""
    <div class="critical-card">
        <div class="kpi-label">Operación con mayor riesgo</div>
        <div style="font-size:1.35rem; font-weight:800; color:#ffffff;">{top_empresa}</div>
        <div class="kpi-sub">{top_patente} · {top_fecha} · {top_hora}</div>
        <div style="font-size:1.2rem; font-weight:700; color:{riesgo_color_text(top_risk)}; margin-top:0.35rem;">
            {top_delay:.1f} min
        </div>
        <div class="pill {pill_class}">{top_risk}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)


# Tabla principal + resumen lateral

left, right = st.columns([4.4, 1.2], gap="large")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Operaciones programadas")

    table_cols = [
        "fecha",
        "empresa",
        "patente",
        "tipo_operacion",
        "tipo_carga",
        "hora_programada",
        "dia_semana",
        "mes",
        "atraso_estimado",
        "riesgo",
    ]

    df_table = df_f[table_cols].copy()

    df_table["fecha"] = pd.to_datetime(df_table["fecha"]).dt.strftime("%d-%m-%Y")
    df_table["atraso_estimado"] = df_table["atraso_estimado"].round(1)

    df_table.columns = [
        "Fecha",
        "Empresa",
        "Patente",
        "Tipo Operación",
        "Tipo Carga",
        "Hora Programada",
        "Día",
        "Mes",
        "Atraso Estimado",
        "Riesgo",
    ]

    def style_risk(val):
        colors = {
            "Crítico": "background-color: rgba(239,68,68,0.18); color: #fecaca; font-weight:700;",
            "Alto": "background-color: rgba(245,158,11,0.18); color: #fde68a; font-weight:700;",
            "Medio": "background-color: rgba(59,130,246,0.18); color: #bfdbfe; font-weight:700;",
            "Bajo": "background-color: rgba(34,197,94,0.18); color: #bbf7d0; font-weight:700;",
        }
        return colors.get(val, "")

    styled = df_table.style.map(style_risk, subset=["Riesgo"])

    st.dataframe(
        styled,
        use_container_width=True,
        height=430
    )

    st.markdown(
        f"<div class='table-note'>Mostrando {len(df_table)} operaciones dentro del rango de fechas seleccionado.</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Resumen rápido")
    st.write(f"**Empresa top riesgo:** {top_empresa}")
    st.write(f"**Patente:** {top_patente}")
    st.write(f"**Fecha:** {top_fecha}")
    st.write(f"**Hora:** {top_hora}")
    st.write(f"**Atraso estimado:** {top_delay:.1f} min")
    st.write(f"**Riesgo:** {top_risk}")

    risk_counts = df_f["riesgo"].value_counts().reindex(["Bajo", "Medio", "Alto", "Crítico"], fill_value=0)

    fig_risk = px.bar(
        x=risk_counts.index,
        y=risk_counts.values,
        color=risk_counts.index,
        color_discrete_map={
            "Bajo": "#22c55e",
            "Medio": "#60a5fa",
            "Alto": "#f59e0b",
            "Crítico": "#ef4444",
        },
        template="plotly_dark"
    )
    fig_risk.update_layout(
        title="Alertas por riesgo",
        height=280,
        margin=dict(l=10, r=10, t=50, b=10),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
    )
    fig_risk.update_xaxes(title=None)
    fig_risk.update_yaxes(title=None, gridcolor="rgba(255,255,255,0.08)")
    st.plotly_chart(fig_risk, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)


# Gráficos inferiores

g1, g2 = st.columns(2, gap="large")

with g1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Distribución de atrasos estimados")

    bins = [-999, 0, 5, 10, 15, 20, 30, 45, 999]
    labels = ["<0", "0-5", "5-10", "10-15", "15-20", "20-30", "30-45", "45+"]

    tmp = df_f.copy()
    tmp["rango_atraso"] = pd.cut(tmp["atraso_estimado"], bins=bins, labels=labels)

    dist = tmp["rango_atraso"].value_counts().reindex(labels, fill_value=0).reset_index()
    dist.columns = ["Rango", "Cantidad"]

    fig_dist = px.bar(
        dist,
        x="Rango",
        y="Cantidad",
        color="Rango",
        color_discrete_sequence=["#7dd3fc", "#22c55e", "#84cc16", "#facc15", "#f59e0b", "#ef4444", "#dc2626", "#991b1b"],
        template="plotly_dark"
    )
    fig_dist.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
    )
    fig_dist.update_xaxes(title=None)
    fig_dist.update_yaxes(title=None, gridcolor="rgba(255,255,255,0.08)")
    st.plotly_chart(fig_dist, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with g2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Empresas con mayor atraso promedio")

    top_emp = (
        df_f.groupby("empresa", as_index=False)["atraso_estimado"]
        .mean()
        .sort_values("atraso_estimado", ascending=False)
        .head(8)
    )
    top_emp["atraso_estimado"] = top_emp["atraso_estimado"].round(1)

    fig_emp = px.bar(
        top_emp.sort_values("atraso_estimado", ascending=True),
        x="atraso_estimado",
        y="empresa",
        orientation="h",
        text="atraso_estimado",
        template="plotly_dark"
    )
    fig_emp.update_traces(
        marker_color="#f59e0b",
        texttemplate="%{text:.1f} min",
        textposition="outside"
    )
    fig_emp.update_layout(
        height=320,
        margin=dict(l=10, r=40, t=10, b=10),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
    )
    fig_emp.update_xaxes(title=None, gridcolor="rgba(255,255,255,0.08)")
    fig_emp.update_yaxes(title=None)
    st.plotly_chart(fig_emp, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)