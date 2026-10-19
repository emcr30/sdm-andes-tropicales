"""Piezas de interfaz reutilizables."""
from __future__ import annotations

import html
import inspect

import streamlit as st

from . import config as C
from .theme import CONFIG_PLOTLY, CSS, FUENTE, T

FUENTE_PLOT = f"{FUENTE}, Helvetica Neue, Arial, sans-serif"

PAGINAS = [
    ("vistas/resumen.py", "Resumen"),
    ("vistas/especies.py", "Especies"),
    ("vistas/mapa.py", "Mapa"),
    ("vistas/modelos.py", "Modelos"),
    ("vistas/metodo.py", "Método"),
]


def estilos():
    st.html(CSS)


# st.html descarta <svg> y las imágenes data:, así que la marca (tres cumbres, la más alta con su glaciar) es un PNG.
MARCA_SVG = '<img src="app/static/img/marca.png" width="26" height="20" alt="">'


def barra(paginas, actual=None):
    # La página activa se marca por su dirección (href). Funciona desde Streamlit 1.46 sin contenedores de ancho fijo.
    if actual is not None:
        ruta = getattr(actual, "url_path", "") or ""
        sel = f".st-key-barra a[data-testid='stPageLink-NavLink'][href='{ruta}']"
        st.html(f"<style>{sel}{{box-shadow:inset 0 -2px 0 var(--ink)!important}}{sel} p{{color:var(--ink)!important;font-weight:650}}</style>")
    with st.container(key="barra"):
        izq, der = st.columns([1.1, 2], vertical_alignment="center")
        with izq:
            st.html(f'<div class="sdm-marca">{MARCA_SVG}Nichos andinos <span>· SDM con aprendizaje automático</span></div>')
        with der:
            with st.container(horizontal=True, horizontal_alignment="right", gap="small"):
                for p in paginas:
                    st.page_link(p, label=p.title)


def seccion():
    st.html('<div class="sdm-seccion"></div>')


def espacio():
    st.html('<div class="sdm-espacio"></div>')


def titulo(texto: str, bajada: str | None = None):
    h = f'<h2 class="sdm-head">{texto}</h2>'
    if bajada:
        h += f'<p class="sdm-body" style="margin-top:12px">{bajada}</p>'
    st.html(h)


def nota(texto: str):
    st.html(f'<p class="sdm-note">{texto}</p>')


def cifra(valor: str, etiqueta: str):
    st.html(f'<div class="sdm-cifra"><span class="v">{valor}</span><span class="k">{etiqueta}</span></div>')


def leyenda(items: list[tuple[str, str, str]]):
    """items: (tipo 'punto'|'barra', color, texto)."""
    partes = []
    for tipo, color, texto in items:
        tag = "i" if tipo == "punto" else "b"
        partes.append(f'<span><{tag} style="background:{color}"></{tag}>{html.escape(texto)}</span>')
    st.html(f'<p class="sdm-leyenda">{"".join(partes)}</p>')


def grafico(fig, key=None):
    # Se fijan explícitamente: el frontend de Streamlit pinta un fondo propio si solo vienen en la plantilla.
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family=FUENTE_PLOT, color=T["ink"]))
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    st.plotly_chart(fig, config=CONFIG_PLOTLY, key=key, theme=None)


_ACEPTA_REQUIRED = "required" in inspect.signature(st.segmented_control).parameters


def segmentado(etiqueta, opciones, key, default=None, format_func=str, **kw):
    """Control segmentado que nunca queda vacío, en cualquier versión de Streamlit desde la 1.40.

    En las versiones nuevas usa required=True; en las anteriores (por ejemplo la 1.50, la última para Python 3.9)
    vuelve a marcar la opción anterior si se hace clic sobre la que ya estaba elegida.
    """
    opciones = list(opciones)
    if st.session_state.get(key) not in opciones:
        st.session_state[key] = default if default in opciones else opciones[0]
    if _ACEPTA_REQUIRED:
        return st.segmented_control(etiqueta, opciones, key=key, format_func=format_func, required=True, **kw)
    previa = f"_previa_{key}"

    def _no_vaciar():
        if st.session_state.get(key) is None:
            st.session_state[key] = st.session_state.get(previa, opciones[0])

    valor = st.segmented_control(etiqueta, opciones, key=key, format_func=format_func, on_change=_no_vaciar, **kw)
    if valor is None:
        valor = st.session_state.get(previa, opciones[0])
    st.session_state[previa] = valor
    return valor


def selector_especie(key: str = "especie", etiqueta: str = "Especie") -> str:
    opciones = list(C.ESPECIES)
    esp = segmentado(etiqueta, opciones, key, default=st.session_state.get("especie_global", opciones[0]),
                     format_func=lambda e: C.ESPECIES[e]["comun"])
    st.session_state["especie_global"] = esp
    return esp


def nombre_html(esp: str) -> str:
    return f'<span class="sdm-sci">{C.ESPECIES[esp]["nombre"]}</span>'


def fmt_km2(v: float) -> str:
    return f"{v:,.0f}".replace(",", " ")


def fmt(v: float, d: int = 2) -> str:
    return f"{v:.{d}f}"


def url_foto(clave: str) -> str:
    return f"app/static/img/{C.FOTOS[clave]['archivo']}"


def credito(clave: str) -> str:
    f = C.FOTOS[clave]
    return (f'Foto: {html.escape(f["autor"])} · <a href="{f["fuente"]}" target="_blank" rel="noopener">'
            f'{f["licencia"]}</a>')


def foto_html(clave: str, clase: str = "", pie_foto: bool = True) -> str:
    f = C.FOTOS[clave]
    cap = f"<figcaption>{credito(clave)}</figcaption>" if pie_foto else ""
    return (f'<figure class="sdm-foto {clase}"><div class="marco">'
            f'<img src="{url_foto(clave)}" alt="{html.escape(f["alt"])}" style="object-position:{f["foco"]}" '
            f'loading="eager" decoding="async"></div>{cap}</figure>')


def lamina(esp: str, datos: list[tuple[str, str]]) -> str:
    """Una especie como lámina de guía de campo: foto, nombres, hábitat y tres cifras."""
    info = C.ESPECIES[esp]
    cifras = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for v, k in datos)
    return (f'<li class="sdm-lamina">{foto_html(esp)}'
            f'<h3>{info["comun"]}</h3>'
            f'<p class="sci"><span class="sdm-sci">{info["nombre"]}</span> · {info["grupo"]}</p>'
            f'<p class="hab">{info["habitat"]}</p><dl>{cifras}</dl></li>')


def pie():
    seccion()
    creditos = "".join(
        f'<p>{C.ESPECIES[k]["comun"] if k in C.ESPECIES else "Lago Junín"}: {credito(k)}</p>' for k in C.FOTOS
    )
    st.html(
        '<div class="sdm-pie"><div>'
        '<p class="nombre">Nichos andinos</p>'
        "<p>Tesis de Evelyn Milagros Chipana Ramos · Ingeniería de Software · Universidad La Salle, Arequipa.</p>"
        "<p>Datos: GBIF, iNaturalist, WorldClim v2.1 (5′), Natural Earth; áreas naturales protegidas del SERNANP (geoservicios.sernanp.gob.pe). Resultados del notebook SDM_CRISPDM_v2.</p>"
        f"</div><div>{creditos}</div></div>"
    )
