from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).parent
DEMO_FILE = BASE_DIR / "data" / "tickets_demo.csv"
REQUIRED_COLUMNS = {
    "ticket_id",
    "created_at",
    "category",
    "priority",
    "status",
    "first_response_hours",
    "resolution_hours",
    "channel",
}

st.set_page_config(
    page_title="Mesa de Ayuda | Panel de tickets",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      :root { --ink: #182b49; --muted: #64748b; --line: #e5eaf2; }
      .stApp { background: #f5f7fb; }
      [data-testid="stHeader"] { background: rgba(245,247,251,.9); }
      .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1320px; }
      .hero { background: linear-gradient(115deg,#102543 0%,#1d4772 65%,#227d83 100%);
        padding: 1.65rem 1.9rem; border-radius: 18px; color: white; margin-bottom: 1.2rem; }
      .hero h1 { color: white; margin: 0 0 .25rem 0; font-size: 2rem; }
      .hero p { color: #d6e5f2; margin: 0; font-size: 1rem; }
      div[data-testid="stMetric"] { background: white; border: 1px solid var(--line);
        padding: 1rem 1.1rem; border-radius: 14px; box-shadow: 0 2px 8px rgba(20,40,70,.035); }
      div[data-testid="stMetricLabel"] { color: var(--muted); }
      div[data-testid="stMetricValue"] { color: var(--ink); }
      h2, h3 { color: var(--ink); }
      .caption { color: var(--muted); font-size: .9rem; }
      div[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_tickets(uploaded_file) -> pd.DataFrame:
    """Read ticket data and normalize fields used by the dashboard."""
    if uploaded_file is None:
        data = pd.read_csv(DEMO_FILE)
    else:
        data = pd.read_csv(uploaded_file)

    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError("Faltan columnas requeridas: " + ", ".join(sorted(missing)))

    data = data.copy()
    data["created_at"] = pd.to_datetime(data["created_at"], errors="coerce")
    for column in ("first_response_hours", "resolution_hours"):
        data[column] = pd.to_numeric(data[column], errors="coerce")
    data["ticket_id"] = data["ticket_id"].astype(str)
    for column in ("category", "priority", "status", "channel"):
        data[column] = data[column].fillna("Sin especificar").astype(str)
    return data.dropna(subset=["created_at"])


def format_hours(value: float) -> str:
    return "—" if pd.isna(value) else f"{value:.1f} h"


st.markdown(
    """
    <div class="hero">
      <h1>Panel de seguimiento de tickets</h1>
      <p>Una vista rápida de la atención, las prioridades y los tiempos de resolución.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Datos")
    st.caption("El panel incluye datos ficticios para la demostración.")
    uploaded = st.file_uploader("Cargar un CSV de tickets", type=["csv"])
    st.markdown("---")
    st.markdown("### Filtros")

try:
    tickets = load_tickets(uploaded)
except (ValueError, pd.errors.ParserError, UnicodeDecodeError) as exc:
    st.error(f"No pude leer el archivo: {exc}")
    st.info("Revisá que el CSV tenga las columnas indicadas en el README.")
    st.stop()

if tickets.empty:
    st.warning("No hay filas con una fecha válida para mostrar.")
    st.stop()

date_min = tickets["created_at"].min().date()
date_max = tickets["created_at"].max().date()
date_range = st.sidebar.date_input(
    "Período",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max,
    format="DD/MM/YYYY",
)
statuses = sorted(tickets["status"].unique().tolist())
categories = sorted(tickets["category"].unique().tolist())
selected_statuses = st.sidebar.multiselect("Estado", statuses, default=statuses)
selected_categories = st.sidebar.multiselect("Categoría", categories, default=categories)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range

filtered = tickets[
    tickets["created_at"].dt.date.between(start_date, end_date)
    & tickets["status"].isin(selected_statuses)
    & tickets["category"].isin(selected_categories)
].copy()

total = len(filtered)
resolved_mask = filtered["status"].str.casefold().isin({"resuelto", "cerrado"})
resolved = int(resolved_mask.sum())
open_count = total - resolved
resolution_rate = (resolved / total * 100) if total else 0
avg_response = filtered["first_response_hours"].mean()
avg_resolution = filtered.loc[resolved_mask, "resolution_hours"].mean()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Tickets en el período", f"{total}")
m2.metric("Pendientes", f"{open_count}")
m3.metric("Resueltos", f"{resolved}", f"{resolution_rate:.0f}% del total")
m4.metric("Primera respuesta promedio", format_hours(avg_response))

if filtered.empty:
    st.info("No hay tickets para los filtros seleccionados. Probá ampliar el período o elegir otras opciones.")
else:
    st.markdown("## Actividad")
    left, right = st.columns([1.2, 1])
    with left:
        st.markdown("### Tickets recibidos por día")
        daily = (
            filtered.assign(day=filtered["created_at"].dt.date)
            .groupby("day")["ticket_id"]
            .count()
            .rename("Tickets")
        )
        st.line_chart(daily, use_container_width=True, color="#217d83")
    with right:
        st.markdown("### Casos por categoría")
        by_category = filtered["category"].value_counts().rename("Tickets")
        st.bar_chart(by_category, use_container_width=True, color="#4772a3")

    st.markdown("## Detalle de atención")
    left, right = st.columns([1, 1.2])
    with left:
        st.markdown("### Estado de los tickets")
        by_status = filtered["status"].value_counts().rename("Tickets")
        st.bar_chart(by_status, use_container_width=True, color="#4f8b72")
        st.metric("Tiempo promedio de resolución", format_hours(avg_resolution))
    with right:
        st.markdown("### Tickets incluidos")
        display = filtered.sort_values("created_at", ascending=False).copy()
        display["created_at"] = display["created_at"].dt.strftime("%d/%m/%Y %H:%M")
        display = display.rename(
            columns={
                "ticket_id": "ID",
                "created_at": "Creado",
                "category": "Categoría",
                "priority": "Prioridad",
                "status": "Estado",
                "first_response_hours": "1.ª respuesta (h)",
                "resolution_hours": "Resolución (h)",
                "channel": "Canal",
            }
        )
        st.dataframe(display, use_container_width=True, hide_index=True)
        st.download_button(
            "Descargar vista filtrada (CSV)",
            data=filtered.to_csv(index=False).encode("utf-8-sig"),
            file_name="tickets_filtrados.csv",
            mime="text/csv",
        )

st.markdown("---")
st.markdown(
    '<p class="caption">Proyecto demostrativo · Los datos incluidos son ficticios. '
    "Para una integración real, reemplazá el archivo por una exportación autorizada de n8n.</p>",
    unsafe_allow_html=True,
)
