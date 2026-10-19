"""Tokens de diseño, hoja de estilos y plantilla de Plotly."""
from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio

FUENTE = "Schibsted Grotesk"

T = {
    "bg": "#F7F7F4",  # papel de libreta de campo
    "surface": "#ECEEE9",  # un paso de tono
    "surface2": "#E0E3DC",  # dos pasos (pistas de control, hover)
    "ink": "#0F1A14",  # verde casi negro de los bosques de Polylepis
    "muted": "#4D5851",
    "faint": "#7D867F",
    "accent": "#A0650F",  # ichu de la puna: solo en datos (pseudoausencias, umbral)
    "accent_soft": "#F1E6D2",
    "noche": "#101914",  # el campo oscuro de la franja del lago
    "grid": "#E1E4DD",
    "baseline": "#C3C7BE",
}

# Rampa secuencial de un solo tono para la idoneidad (claro = bajo, oscuro = alto)
RAMPA_IDONEIDAD = [
    [0.00, "rgba(214,230,214,0.00)"],
    [0.20, "rgba(204,226,203,0.06)"],
    [0.35, "rgba(160,203,160,0.45)"],
    [0.50, "rgba(103,170,108,0.80)"],
    [0.70, "rgba(46,128,70,0.92)"],
    [0.85, "rgba(18,94,50,0.96)"],
    [1.00, "rgba(6,61,32,1.00)"],
]
VERDE_IDONEO = "rgba(22,104,56,0.88)"

CSS = f"""
<style>
@font-face {{ font-family: "Schibsted Grotesk"; font-style: normal; font-weight: 400 900; font-display: swap;
  src: url("app/static/fonts/schibsted-normal-latin-ext.woff2") format("woff2"); unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF; }}
@font-face {{ font-family: "Schibsted Grotesk"; font-style: normal; font-weight: 400 900; font-display: swap;
  src: url("app/static/fonts/schibsted-normal-latin.woff2") format("woff2"); unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }}
@font-face {{ font-family: "Schibsted Grotesk"; font-style: italic; font-weight: 400 900; font-display: swap;
  src: url("app/static/fonts/schibsted-italic-latin-ext.woff2") format("woff2"); unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF; }}
@font-face {{ font-family: "Schibsted Grotesk"; font-style: italic; font-weight: 400 900; font-display: swap;
  src: url("app/static/fonts/schibsted-italic-latin.woff2") format("woff2"); unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }}
:root {{
  --bg: {T['bg']}; --surface: {T['surface']}; --surface-2: {T['surface2']};
  --ink: {T['ink']}; --muted: {T['muted']}; --faint: {T['faint']};
  --accent: {T['accent']}; --accent-soft: {T['accent_soft']}; --noche: {T['noche']};
  --seleccion: #CFE3D0;
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
  --step-small: 0.8125rem;
  --step-body: 1.0625rem;
  --step-lead: 1.25rem;
  --step-head: clamp(1.625rem, 1.1rem + 1.5vw, 2.375rem);
  --step-display: clamp(2.75rem, 1.2rem + 5vw, 5.5rem);
  --step-title: clamp(2.25rem, 1.2rem + 3.2vw, 4rem);
  --radius-ui: 2px;
  --radius-panel: 0px;
}}

html, body, [data-testid="stAppViewContainer"], .stApp {{
  background: var(--bg) !important;
  color: var(--ink);
  font-family: "{FUENTE}", "Helvetica Neue", Arial, sans-serif;
  font-kerning: normal;
  font-feature-settings: "ss01";
  -webkit-font-smoothing: antialiased;
}}
.stApp *:not([data-testid="stIconMaterial"]):not(.material-symbols-rounded) {{ font-family: "{FUENTE}", "Helvetica Neue", Arial, sans-serif; }}
[data-testid="stIconMaterial"] {{ font-family: "Material Symbols Rounded" !important; }}
::selection {{ background: var(--seleccion); color: var(--ink); }}
* {{ scrollbar-color: var(--surface-2) transparent; caret-color: var(--ink); }}
:focus-visible {{ outline: 2px solid var(--ink); outline-offset: 2px; }}

/* cromo de Streamlit que no aporta */
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], #MainMenu, footer, [data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}

[data-testid="stMainBlockContainer"], .block-container {{
  max-width: 1280px; padding: 0 40px 96px 40px !important;
}}
@media (max-width: 640px) {{
  [data-testid="stMainBlockContainer"], .block-container {{ padding: 0 16px 72px 16px !important; }}
}}

/* tipografía */
h1, h2, h3, h4 {{ color: var(--ink); letter-spacing: -0.025em; font-weight: 700; text-wrap: balance; }}
.stMarkdown p, .stMarkdown li {{ font-size: var(--step-body); line-height: 1.55; color: var(--ink); max-width: 68ch; text-wrap: pretty; }}
.stMarkdown em {{ font-style: italic; }}
a {{ color: var(--ink); text-decoration-color: var(--faint); text-underline-offset: 3px; text-decoration-thickness: 1px;
  transition: text-decoration-color 160ms ease; }}
a:hover {{ text-decoration-color: var(--ink); }}

.sdm-display {{ font-size: var(--step-display); line-height: 0.94; letter-spacing: -0.045em; font-weight: 800;
  margin: 0 0 0 -0.045em; max-width: 12ch; color: var(--ink); }}
.sdm-head {{ font-size: var(--step-head); line-height: 1.05; letter-spacing: -0.035em; font-weight: 750;
  margin: 0; color: var(--ink); max-width: 26ch; }}
.sdm-lead {{ font-size: var(--step-lead); line-height: 1.45; color: var(--ink); max-width: 44ch; margin: 0; }}
.sdm-body {{ font-size: var(--step-body); line-height: 1.55; color: var(--ink); max-width: 62ch; margin: 0; }}
.sdm-note {{ font-size: var(--step-small); line-height: 1.5; color: var(--muted); max-width: 70ch; margin: 0; }}
.sdm-sci {{ font-style: italic; }}
.num {{ font-variant-numeric: tabular-nums; }}

/* barra superior: marca y navegación en texto, sin píldoras */
.st-key-barra {{ padding: 20px 0 16px 0; margin-bottom: 12px; box-shadow: inset 0 -1px 0 var(--surface-2); }}
.st-key-barra [data-testid="stHorizontalBlock"] {{ align-items: center; }}
.sdm-marca {{ display: flex; align-items: center; gap: 10px; font-weight: 750; font-size: 1.0625rem; letter-spacing: -0.02em;
  color: var(--ink); line-height: 1.2; white-space: nowrap; }}
.sdm-marca svg {{ flex: none; }}
.sdm-marca span {{ color: var(--muted); font-weight: 400; letter-spacing: 0; }}
[data-testid="stPageLink"] a, [data-testid="stPageLink-NavLink"] {{
  border-radius: 0 !important; padding: 6px 2px !important; margin: 0 8px; background: transparent !important;
  box-shadow: inset 0 -2px 0 transparent; transition: box-shadow 200ms var(--ease-out);
}}
[data-testid="stPageLink-NavLink"] p, [data-testid="stPageLink-NavLink"] span {{ font-size: 0.9375rem !important; color: var(--muted) !important;
  font-weight: 500; transition: color 160ms ease; }}
.st-key-barra [data-testid="stPageLink-NavLink"][aria-current="page"] {{ box-shadow: inset 0 -2px 0 var(--ink); }}
.st-key-barra [data-testid="stPageLink-NavLink"][aria-current="page"] p {{ color: var(--ink) !important; font-weight: 650; }}
@media (hover: hover) and (pointer: fine) {{
  .st-key-barra [data-testid="stPageLink-NavLink"]:hover p {{ color: var(--ink) !important; }}
  .st-key-barra [data-testid="stPageLink-NavLink"]:hover {{ box-shadow: inset 0 -2px 0 var(--surface-2); }}
}}

@media (max-width: 640px) {{
  .sdm-marca span {{ display: none; }}
  .st-key-barra [data-testid="stPageLink-NavLink"] {{ margin: 0 2px; }}
  .st-key-barra [data-testid="stPageLink-NavLink"] p {{ font-size: 0.8125rem !important; }}
  .st-key-barra [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"], .st-key-barra [data-testid="stLayoutWrapper"] {{ gap: 0 !important; }}
}}

/* enlaces como botones: el primero es la acción principal */
.st-key-cta [data-testid="stPageLink-NavLink"] {{ margin: 0; padding: 12px 22px !important; background: var(--surface) !important;
  border-radius: var(--radius-ui) !important; transition: background-color 160ms ease, transform 160ms var(--ease-out); }}
.st-key-cta [data-testid="stPageLink-NavLink"] p {{ color: var(--ink) !important; font-weight: 600; font-size: 1rem !important; }}
.st-key-cta [data-testid="stElementContainer"]:first-child [data-testid="stPageLink-NavLink"] {{ background: var(--ink) !important; }}
.st-key-cta [data-testid="stElementContainer"]:first-child [data-testid="stPageLink-NavLink"] p {{ color: var(--bg) !important; }}
.st-key-cta [data-testid="stPageLink-NavLink"]:active {{ transform: scale(0.97); }}
@media (hover: hover) and (pointer: fine) {{
  .st-key-cta [data-testid="stElementContainer"]:not(:first-child) [data-testid="stPageLink-NavLink"]:hover {{ background: var(--surface-2) !important; }}
  .st-key-cta [data-testid="stElementContainer"]:first-child [data-testid="stPageLink-NavLink"]:hover {{ background: #24322A !important; }}
}}

/* controles segmentados: esquinas rectas, el activo en tinta */
[data-testid="stButtonGroup"] {{ gap: 4px !important; flex-wrap: wrap; }}
[data-testid="stButtonGroup"] button {{
  border: 0 !important; border-radius: var(--radius-ui) !important; background: var(--surface) !important;
  color: var(--ink) !important; padding: 7px 16px !important; min-height: 38px; box-shadow: none !important;
  transition: background-color 160ms ease, color 160ms ease, transform 160ms var(--ease-out);
}}
[data-testid="stButtonGroup"] button p {{ font-size: 0.9375rem; font-weight: 500; }}
[data-testid="stButtonGroup"] button[kind$="Active"], [data-testid="stButtonGroup"] button[aria-checked="true"], [data-testid="stButtonGroup"] button[aria-pressed="true"] {{
  background: var(--ink) !important; color: var(--bg) !important;
}}
[data-testid="stButtonGroup"] button[kind$="Active"] p, [data-testid="stButtonGroup"] button[aria-checked="true"] p {{ color: var(--bg) !important; }}
[data-testid="stButtonGroup"] button:active {{ transform: scale(0.97); }}
@media (hover: hover) and (pointer: fine) {{
  [data-testid="stButtonGroup"] button:not([aria-checked="true"]):not([kind$="Active"]):hover {{ background: var(--surface-2) !important; }}
}}
[data-testid="stButtonGroup"] button:focus-visible {{ outline: 2px solid var(--ink); outline-offset: 2px; }}

.stButton button, .stDownloadButton button {{
  border-radius: var(--radius-ui) !important; border: 0 !important; background: var(--ink) !important; color: var(--bg) !important;
  padding: 10px 18px !important; box-shadow: none !important; transition: transform 160ms var(--ease-out), background-color 160ms ease;
}}
.stButton button p, .stDownloadButton button p {{ color: var(--bg) !important; font-weight: 600; }}
.stButton button:active, .stDownloadButton button:active {{ transform: scale(0.97); }}
.st-key-secundario .stButton button, .st-key-secundario .stDownloadButton button {{ background: var(--surface) !important; color: var(--ink) !important; }}
.st-key-secundario .stButton button p, .st-key-secundario .stDownloadButton button p {{ color: var(--ink) !important; }}
@media (hover: hover) and (pointer: fine) {{
  .st-key-secundario .stButton button:hover, .st-key-secundario .stDownloadButton button:hover {{ background: var(--surface-2) !important; }}
}}

[class*="st-key-panel-"] .st-key-secundario .stButton button {{ background: var(--surface-2) !important; }}

/* casillas de capas: discretas, en el tono del texto */
.st-key-capas [data-testid="stCheckbox"] label p {{ font-size: 0.875rem; color: var(--ink); }}
.st-key-capas [data-testid="stCheckbox"] label span:first-child {{ border-radius: 2px !important; }}
.st-key-capas [data-testid="stVerticalBlock"] {{ gap: 2px !important; }}

/* etiquetas de widgets */
[data-testid="stWidgetLabel"] p {{ font-size: var(--step-small) !important; color: var(--muted) !important; font-weight: 500; }}

/* deslizador */
[data-testid="stSlider"] [role="slider"] {{ background: var(--ink) !important; box-shadow: 0 0 0 4px var(--surface) !important; border-radius: 2px !important; }}
[data-testid="stSliderThumbValue"], [data-testid="stThumbValue"] {{ color: var(--ink) !important; font-variant-numeric: tabular-nums; font-weight: 650; }}
[data-testid="stSliderTickBarMin"], [data-testid="stSliderTickBarMax"] {{ color: var(--muted) !important; }}

/* paneles por paso de tono, sin líneas ni sombras */
.st-key-panel, [class*="st-key-panel-"] {{ background: var(--surface); border-radius: var(--radius-panel); padding: 24px 26px; }}
.st-key-panel [data-testid="stVerticalBlock"], [class*="st-key-panel-"] [data-testid="stVerticalBlock"] {{ gap: 10px; }}

[data-testid="stExpander"] details {{ border: 0 !important; background: var(--surface); border-radius: var(--radius-panel); }}
[data-testid="stExpander"] summary p {{ font-weight: 600; }}

[data-testid="stPlotlyChart"] {{ background: transparent; }}
.stPlotlyChart .modebar {{ display: none !important; }}

/* separación entre secciones: espacio, no reglas */
.sdm-seccion {{ height: 128px; }}
.sdm-espacio {{ height: 28px; }}
@media (max-width: 640px) {{ .sdm-seccion {{ height: 72px; }} }}

/* fotos: esquinas rectas, crédito pequeño debajo */
.sdm-foto {{ margin: 0; }}
.sdm-foto .marco {{ overflow: hidden; background: var(--surface-2); }}
.sdm-foto img {{ display: block; width: 100%; height: 100%; object-fit: cover; }}
.sdm-foto figcaption {{ font-size: 0.75rem; line-height: 1.4; color: var(--muted); margin-top: 8px; }}
.sdm-foto figcaption a {{ color: var(--muted); }}

/* láminas de especie: la guía de campo */
.sdm-laminas {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 28px; margin: 0; padding: 0; list-style: none; }}
.sdm-lamina {{ display: flex; flex-direction: column; }}
.sdm-lamina .marco {{ aspect-ratio: 649 / 800; }}
.sdm-lamina img {{ transition: transform 900ms var(--ease-out); }}
@media (hover: hover) and (pointer: fine) {{ .sdm-lamina:hover img {{ transform: scale(1.035); }} }}
.sdm-lamina h3 {{ font-size: 1.625rem; line-height: 1.05; letter-spacing: -0.03em; font-weight: 750; margin: 18px 0 0 0; padding: 0; }}
.sdm-lamina .sci {{ font-size: 0.9375rem; color: var(--muted); margin: 6px 0 0 0; }}
.sdm-lamina .hab {{ font-size: 0.9375rem; line-height: 1.5; color: var(--ink); margin: 12px 0 0 0; max-width: 40ch; }}
.sdm-lamina dl {{ display: grid; grid-template-columns: repeat(3, auto); justify-content: start; gap: 4px 28px; margin: 18px 0 0 0; }}
.sdm-lamina dt {{ font-size: 0.75rem; color: var(--muted); order: 2; }}
.sdm-lamina dd {{ margin: 0; font-size: 1.25rem; font-weight: 700; letter-spacing: -0.02em; order: 1; }}
.sdm-lamina dl > div {{ display: flex; flex-direction: column; }}
@media (max-width: 860px) {{ .sdm-laminas {{ grid-template-columns: 1fr; gap: 48px; }} .sdm-lamina .marco {{ aspect-ratio: 4 / 3; }} }}

/* franja del lago: un campo oscuro con la foto, una sola vez */
.sdm-banda {{ background: var(--noche); color: #E8ECE6; display: grid; grid-template-columns: minmax(0, 1.6fr) minmax(0, 1fr); }}
.sdm-banda .marco {{ min-height: 440px; overflow: hidden; }}
.sdm-banda img {{ display: block; width: 100%; height: 100%; object-fit: cover; }}
.sdm-banda .texto {{ padding: 44px 40px; display: flex; flex-direction: column; justify-content: space-between; gap: 32px; }}
.sdm-banda p.dicho {{ font-size: clamp(1.375rem, 1rem + 1vw, 1.875rem); line-height: 1.2; letter-spacing: -0.025em; font-weight: 650;
  margin: 0; color: #F3F5F1; max-width: 22ch; text-wrap: balance; }}
.sdm-banda p.pie-foto {{ font-size: 0.75rem; color: #A9B3AC; margin: 0; line-height: 1.45; }}
.sdm-banda p.pie-foto a {{ color: #A9B3AC; text-decoration-color: #5E6A62; }}
@media (max-width: 860px) {{ .sdm-banda {{ grid-template-columns: 1fr; }} .sdm-banda .marco {{ min-height: 260px; aspect-ratio: 3 / 2; }}
  .sdm-banda .texto {{ padding: 28px 22px; }} }}

/* ficha de especie: foto grande y datos al lado */
.sdm-ficha .marco {{ aspect-ratio: 649 / 800; }}
.sdm-datos {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 28px 32px; margin: 0; }}
.sdm-datos > div {{ display: flex; flex-direction: column; gap: 4px; }}
.sdm-datos dd {{ margin: 0; order: 1; font-size: clamp(2rem, 1.4rem + 1.6vw, 2.75rem); line-height: 1; font-weight: 750;
  letter-spacing: -0.035em; }}
.sdm-datos dt {{ order: 2; font-size: 0.875rem; line-height: 1.4; color: var(--muted); max-width: 26ch; }}

/* miniatura de la especie en el mapa */
.sdm-mini {{ display: flex; gap: 14px; align-items: center; }}
.sdm-mini img {{ width: 52px; height: 64px; object-fit: cover; display: block; flex: none; }}
.sdm-mini .n {{ font-weight: 700; font-size: 1.0625rem; letter-spacing: -0.015em; line-height: 1.2; }}
.sdm-mini .s {{ font-size: var(--step-small); color: var(--muted); }}

/* lista de especies / filas de tabla */
.sdm-lista {{ display: grid; gap: 0; margin: 0; padding: 0; list-style: none; }}
.sdm-fila {{ display: grid; grid-template-columns: minmax(0, 2.2fr) repeat(4, minmax(0, 1fr)); gap: 16px; align-items: baseline;
  padding: 18px 4px; box-shadow: inset 0 -1px 0 var(--surface-2); }}
.sdm-fila .t {{ font-size: 1.25rem; font-weight: 700; letter-spacing: -0.02em; line-height: 1.2; }}
.sdm-fila .s {{ font-size: var(--step-small); color: var(--muted); margin-top: 2px; }}
.sdm-fila .v {{ font-size: 1.25rem; font-weight: 700; font-variant-numeric: tabular-nums; line-height: 1.2; }}
.sdm-fila .k {{ font-size: var(--step-small); color: var(--muted); }}
.sdm-cab {{ display: grid; grid-template-columns: minmax(0, 2.2fr) repeat(4, minmax(0, 1fr)); gap: 16px; padding: 0 4px 10px 4px;
  box-shadow: inset 0 -1px 0 var(--ink); }}
.sdm-cab span {{ font-size: var(--step-small); color: var(--muted); font-weight: 500; }}
@media (max-width: 760px) {{
  .sdm-fila {{ grid-template-columns: 1fr 1fr; }}
  .sdm-fila > div:first-child {{ grid-column: 1 / -1; }}
  .sdm-cab {{ display: none; }}
}}

/* cifras: tipo, no tarjetas */
.sdm-cifra {{ display: flex; flex-direction: column; gap: 6px; }}
.sdm-cifra .v {{ font-size: 2.25rem; line-height: 1; font-weight: 750; letter-spacing: -0.035em; }}
.sdm-cifra .k {{ font-size: 0.875rem; color: var(--muted); line-height: 1.45; max-width: 34ch; }}

/* leyenda manual */
.sdm-leyenda {{ display: flex; flex-wrap: wrap; gap: 6px 18px; font-size: var(--step-small); color: var(--muted); margin: 0; }}
.sdm-leyenda i {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; vertical-align: -1px; }}
.sdm-punto {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 8px; vertical-align: 0; }}
.sdm-leyenda b {{ display: inline-block; width: 28px; height: 10px; margin-right: 6px; vertical-align: -1px; }}

/* pasos del método: el orden de CRISP-DM sí es información */
.sdm-pasos {{ counter-reset: paso; list-style: none; margin: 0 !important; padding: 0 !important; display: grid; gap: 0; }}
.sdm-pasos li {{ margin: 0 !important; padding: 22px 4px 22px 72px; position: relative; max-width: none; box-shadow: inset 0 -1px 0 var(--surface-2); }}
.sdm-pasos li::before {{ counter-increment: paso; content: counter(paso); position: absolute; left: 4px; top: 16px;
  font-size: 2rem; font-weight: 800; letter-spacing: -0.04em; color: var(--ink); font-variant-numeric: tabular-nums; line-height: 1; }}
.sdm-pasos .t {{ font-weight: 700; font-size: 1.1875rem; letter-spacing: -0.015em; margin-bottom: 6px; }}
.sdm-pasos .d {{ color: var(--ink); line-height: 1.55; max-width: 72ch; }}
.sdm-pasos .c {{ color: var(--muted); font-size: var(--step-small); margin-top: 8px; }}

/* glosario */
.sdm-glosario {{ margin: 0 !important; padding: 0 !important; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 40px; }}
.sdm-glosario div {{ padding: 18px 0; box-shadow: inset 0 -1px 0 var(--surface-2); }}
.sdm-glosario dt {{ font-weight: 700; margin-bottom: 4px; }}
.sdm-glosario dd {{ margin: 0; line-height: 1.5; color: var(--ink); }}
@media (max-width: 760px) {{ .sdm-glosario {{ grid-template-columns: 1fr; }} }}

/* movimiento: una entrada escalonada y las fotos que se descubren de abajo arriba, una sola vez */
@keyframes sdm-sube {{ from {{ opacity: 0; transform: translateY(18px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes sdm-descubre {{ from {{ clip-path: inset(100% 0 0 0); transform: scale(1.06); }} to {{ clip-path: inset(0 0 0 0); transform: none; }} }}
@keyframes sdm-aparece {{ from {{ opacity: 0; transform: scale(0.985); filter: blur(4px); }} to {{ opacity: 1; transform: none; filter: none; }} }}
.sdm-entra > * {{ animation: sdm-sube 620ms var(--ease-out) both; }}
.sdm-entra > *:nth-child(2) {{ animation-delay: 80ms; }}
.sdm-entra > *:nth-child(3) {{ animation-delay: 160ms; }}
.sdm-entra > *:nth-child(4) {{ animation-delay: 240ms; }}
.sdm-revela .marco {{ animation: sdm-descubre 1100ms var(--ease-out) both; }}
.sdm-laminas > li:nth-child(2) .marco {{ animation-delay: 110ms; }}
.sdm-laminas > li:nth-child(3) .marco {{ animation-delay: 220ms; }}
.sdm-revela .marco img {{ animation: sdm-aparece 1400ms var(--ease-out) both; }}
.st-key-mapa-portada {{ animation: sdm-aparece 800ms var(--ease-out) 140ms both; }}

@media (prefers-reduced-motion: reduce) {{
  .sdm-entra > *, .st-key-mapa-portada, .sdm-revela .marco, .sdm-revela .marco img {{ animation: sdm-fundido 200ms ease both !important; }}
  @keyframes sdm-fundido {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
  * {{ transition-duration: 0ms !important; }}
}}

/* pie: el nombre vuelve, los créditos quedan pequeños */
.sdm-pie {{ padding-top: 36px; box-shadow: inset 0 1px 0 var(--ink); display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr); gap: 32px; }}
.sdm-pie p.nombre {{ color: var(--ink); font-size: clamp(1.75rem, 1.2rem + 2vw, 3rem); font-weight: 800; letter-spacing: -0.045em; line-height: 0.95; margin: 0 0 16px 0; }}
.sdm-pie p {{ font-size: var(--step-small); color: var(--muted); margin: 0 0 6px 0; max-width: 60ch; line-height: 1.5; }}
.sdm-pie a {{ color: var(--muted); }}
@media (max-width: 760px) {{ .sdm-pie {{ grid-template-columns: 1fr; }} }}

[data-testid="stAlert"] {{ background: var(--surface) !important; border: 0 !important; border-radius: var(--radius-panel); color: var(--ink); }}
</style>
"""


def plantilla() -> go.layout.Template:
    t = go.layout.Template()
    t.layout = go.Layout(
        font=dict(family=f"{FUENTE}, Helvetica Neue, Arial, sans-serif", size=13, color=T["ink"]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=["#2a78d6", "#eb6834", "#1baf7a", "#eda100"],
        margin=dict(l=8, r=8, t=8, b=8),
        hoverlabel=dict(bgcolor=T["ink"], bordercolor=T["ink"], font=dict(color=T["bg"], size=13, family=FUENTE)),
        xaxis=dict(gridcolor=T["grid"], zeroline=False, linecolor=T["baseline"], tickcolor=T["baseline"],
                   tickfont=dict(color=T["muted"], size=12), title=dict(font=dict(color=T["muted"], size=12)), ticks=""),
        yaxis=dict(gridcolor=T["grid"], zeroline=False, linecolor=T["baseline"], tickcolor=T["baseline"],
                   tickfont=dict(color=T["muted"], size=12), title=dict(font=dict(color=T["muted"], size=12)), ticks=""),
        legend=dict(font=dict(color=T["muted"], size=12), bgcolor="rgba(0,0,0,0)", orientation="h", x=0, y=1.08, xanchor="left"),
        separators=". ",
        dragmode=False,
    )
    return t


pio.templates["sdm"] = plantilla()
pio.templates.default = "sdm"

CONFIG_PLOTLY = {"displayModeBar": False, "scrollZoom": False, "responsive": True, "locale": "es"}
