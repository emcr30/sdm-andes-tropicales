import io
import zipfile

import streamlit as st

from sdm import config as C
from sdm import data as D
from sdm import ui

ui.espacio()
st.html(
    '<div class="sdm-entra">'
    '<h1 class="sdm-display" style="font-size:var(--step-title)">Método, paso a paso</h1>'
    '<p class="sdm-lead" style="margin-top:16px">El notebook sigue las seis fases de CRISP-DM. Aquí está lo que se hizo en cada una '
    "y por qué, sin código.</p>"
    "</div>"
)
ui.espacio()

PASOS = [
    ("Comprensión del problema",
     "¿Qué algoritmo de aprendizaje automático predice mejor dónde viven especies endémicas andinas usando solo datos abiertos?",
     "Éxito = el mejor AUC-ROC, AUC-PR y TSS con validación espacial, y mapas coherentes con lo que se sabe de cada especie."),
    ("Comprensión de los datos",
     "Registros de GBIF (solo Perú) e iNaturalist (grado de investigación), 19 variables bioclimáticas y la elevación de WorldClim v2.1 "
     "a 5 minutos de arco (unos 9 km), y el límite del Perú de Natural Earth.",
     "2 045 registros descargados en total; la rana de Junín apenas tiene 43."),
    ("Preparación de los datos",
     "Limpieza (coordenadas, años 1980–2024, incertidumbre ≤ 10 km, sin fósiles ni cautiverio, sin coordenadas oscurecidas), "
     "una presencia por celda y al menos 5 km entre presencias. Área accesible M de 100 km. Variables filtradas por Pearson y VIF "
     "sobre el fondo de M. Pseudoausencias 1:1 con tres estrategias.",
     "Correcciones del asesor a, b y d."),
    ("Modelado",
     "Random Forest, SVM, LightGBM y MaxEnt con la configuración de la Tabla 5, entrenados con los mismos datos y los mismos pliegues.",
     "Semilla fija (42) para que todo sea reproducible."),
    ("Evaluación",
     "Validación cruzada espacial por bloques del tamaño del rango de autocorrelación del clima (k entre 3 y 5), comparada con la "
     "validación aleatoria. Umbral de máximo TSS elegido con los datos de entrenamiento. Prueba de Friedman y análisis de sensibilidad.",
     "Corrección del asesor c."),
    ("Despliegue",
     "Mapas GeoTIFF por especie y modelo recortados al Perú, tablas de la tesis en un Excel y esta aplicación.",
     "Los mapas usan la estrategia de pseudoausencias buffer."),
]
items = "".join(f'<li><div class="t">{t}</div><div class="d">{d}</div><div class="c">{c}</div></li>' for t, d, c in PASOS)
st.html(f'<ol class="sdm-pasos">{items}</ol>')

# ---------- correcciones ----------
ui.seccion()
ui.titulo("Las cuatro correcciones del asesor", "Qué cambió respecto a la versión anterior del análisis y por qué importa para la biología del problema.")
ui.espacio()
CORR = [
    ("a · Variables redundantes",
     "Antes se usaban las 19 variables, o se filtraban con la correlación de 20 a 40 presencias, que es inestable. Ahora se filtra "
     "con miles de celdas del área M: el ambiente que la especie tiene disponible."),
    ("b · Sesgo de muestreo",
     "Los observadores se concentran en carreteras, albergues y miradores. El adelgazamiento a 5 km evita que esos lugares dominen el "
     "modelo. Con 10 km la lechucita quedaba con solo 7 presencias."),
    ("c · Validación aleatoria",
     "Con datos agrupados en el espacio, separar al azar deja vecinos casi idénticos en entrenamiento y prueba. Los bloques geográficos "
     "obligan al modelo a predecir en zonas que no vio."),
    ("d · Fondo en zonas irrelevantes",
     "Antes las pseudoausencias salían de un rectángulo con Ecuador, Brasil, Bolivia, Chile y el mar. Una rana de Junín nunca pudo "
     "llegar a la costa norte; compararla con esos climas facilita demasiado el trabajo del modelo."),
]
g = "".join(f"<div><dt>{t}</dt><dd>{d}</dd></div>" for t, d in CORR)
st.html(f'<dl class="sdm-glosario">{g}</dl>')

# ---------- adelgazamiento ----------
ui.seccion()
a1, a2 = st.columns([1, 1.3], gap="large")
with a1:
    ui.titulo("Por qué 5 km", "Cuántas presencias quedan con cada distancia mínima entre registros. Más distancia reduce el sesgo, "
              "pero deja muy pocos datos para entrenar.")
with a2:
    t5 = D.tabla("05_sensibilidad_adelgazamiento")
    if len(t5):
        t5 = t5.copy()
        t5.insert(1, "Nombre común", t5["Especie"].map({v["nombre"]: v["comun"] for v in C.ESPECIES.values()}))
        st.dataframe(t5, hide_index=True, width="stretch",
                     column_config={"Especie": st.column_config.TextColumn("Especie")})

# ---------- trazabilidad ----------
ui.seccion()
ui.titulo("Trazabilidad", "Cada objetivo de la tesis, los datos que usa y cómo quedan después de prepararlos.")
ui.espacio()
tz = D.tabla("24_trazabilidad")
if len(tz):
    cab = "".join(f"<span>{c}</span>" for c in ["Objetivo", "Datos de partida", "Datos preparados"])
    filas = [f'<div class="sdm-cab" style="grid-template-columns:repeat(3,minmax(0,1fr))">{cab}</div>']
    for _, f in tz.iterrows():
        filas.append('<div class="sdm-fila" style="grid-template-columns:repeat(3,minmax(0,1fr));align-items:start">'
                     f'<div style="font-weight:600">{f["Negocio"]}</div><div>{f["Datos"]}</div>'
                     f'<div>{f["Datos limpios"]}</div></div>')
    st.html(f'<div class="sdm-lista">{"".join(filas)}</div>')

# ---------- glosario ----------
ui.seccion()
ui.titulo("Glosario", "Los términos que aparecen en la aplicación, en lenguaje de campo.")
ui.espacio()
g = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in C.GLOSARIO.items())
st.html(f'<dl class="sdm-glosario">{g}</dl>')

# ---------- descargas ----------
ui.seccion()
d1, d2 = st.columns([1, 1.3], gap="large")
with d1:
    ui.titulo("Descargar los datos", "Las mismas tablas de la tesis y los mapas de idoneidad, para usarlos en QGIS, R o Excel.")
with d2:
    xlsx = C.DIR_TABLAS / "tablas_tesis.xlsx"
    if xlsx.exists():
        st.download_button("Tablas de la tesis (Excel)", xlsx.read_bytes(), file_name="tablas_tesis.xlsx", width="stretch",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    @st.cache_data(show_spinner=False)
    def _zip_rasters() -> bytes:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(C.DIR_RASTERS.glob("*.tif")):
                z.write(f, f.name)
        return buf.getvalue()

    @st.cache_data(show_spinner=False)
    def _zip_presencias() -> bytes:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(C.DIR_DATOS.glob("*.csv")):
                z.write(f, f.name)
        return buf.getvalue()

    with st.container(key="secundario"):
        st.download_button("Mapas de idoneidad (12 GeoTIFF)", _zip_rasters(), file_name="mapas_idoneidad.zip", width="stretch")
        st.download_button("Presencias y conjuntos de datos (CSV)", _zip_presencias(), file_name="datos_sdm.zip", width="stretch")
    ui.nota("Los GeoTIFF están en WGS84, con valores de 0 a 1 y −9999 fuera del Perú.")

ui.pie()
