"""Nichos andinos: visualización de los modelos de distribución de la tesis.

Ejecutar con:  streamlit run app.py
"""
import streamlit as st

st.set_page_config(page_title="Nichos andinos", layout="wide", initial_sidebar_state="collapsed")

from sdm import data as D  # noqa: E402
from sdm import ui  # noqa: E402
from sdm import config as C  # noqa: E402

ui.estilos()

if not D.hay_resultados():
    st.html('<h1 class="sdm-display" style="font-size:var(--step-title)">Faltan los resultados del notebook</h1>')
    st.html(
        '<p class="sdm-body" style="margin-top:16px">La aplicación lee la carpeta <code>resultados</code> que genera '
        "<b>SDM_CRISPDM_v2.ipynb</b> (tablas, modelos, rásters y datos). Ejecuta el notebook completo y luego indica dónde está "
        "esa carpeta con la variable <code>SDM_RESULTADOS</code>.</p>"
        f'<p class="sdm-note" style="margin-top:12px">Ruta buscada: {C.RESULTADOS}</p>'
    )
    st.stop()

paginas = [st.Page(ruta, title=titulo, default=(i == 0)) for i, (ruta, titulo) in enumerate(ui.PAGINAS)]
nav = st.navigation(paginas, position="hidden")
ui.barra(paginas, nav)
nav.run()
