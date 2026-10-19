import streamlit as st

from sdm import config as C
from sdm import data as D
from sdm import graficos as G
from sdm import ui

# ---------- portada ----------
izq, der = st.columns([1, 1.3], gap="large", vertical_alignment="center")
with izq:
    st.html(
        '<div class="sdm-entra">'
        '<h1 class="sdm-display">Dónde puede vivir cada especie</h1>'
        '<p class="sdm-lead" style="margin-top:32px">Tres especies endémicas de los Andes peruanos, cuatro algoritmos '
        "y los mismos datos de clima y relieve. Aquí se ve qué predice cada modelo y cuánto confiar en él.</p>"
        '<p class="sdm-body" style="margin-top:20px;color:var(--muted)">Los registros vienen de GBIF e iNaturalist; '
        "el clima, de WorldClim. Todo lo que aparece sale del notebook de la tesis, sin retoques.</p>"
        "</div>"
    )
    ui.espacio()
    with st.container(key="cta", horizontal=True, gap="small"):
        st.page_link("vistas/mapa.py", label="Explorar el mapa")
        st.page_link("vistas/especies.py", label="Conocer las especies")
with der:
    with st.container(key="mapa-portada"):
        ui.grafico(G.mapa_portada(alto=640), key="portada")
        ui.nota("Cada punto es una presencia depurada sobre el relieve del Perú (sombreado a partir de la elevación de WorldClim).")

# ---------- las tres especies ----------
ui.seccion()
ui.titulo("Tres especies, tres pisos de los Andes",
          "Un búho del bosque nublado, un ave de los bofedales al pie de los glaciares y una rana que solo vive en los lagos de "
          "Junín y Pasco. Las cifras son del mejor modelo de cada una, con el umbral de la tesis.")
ui.espacio()
laminas = []
for esp in C.ESPECIES:
    mod = D.mejor_modelo(esp)
    r = D.resumen_umbral(esp, mod, D.umbral_tesis(esp, mod))
    laminas.append(ui.lamina(esp, [
        (f"{len(D.presencias(esp))}", "presencias"),
        (C.NOMBRE_MODELO[mod], "mejor modelo"),
        (f"{r['pct_m']:.0f} %", "de M idóneo"),
    ]))
st.html(f'<ul class="sdm-laminas sdm-revela">{"".join(laminas)}</ul>')

# ---------- hallazgo ----------
ui.seccion()
t17 = D.tabla("17_mejor_modelo")
t15 = D.tabla("15_aleatoria_vs_espacial")
fig_rank, medias = G.ranking_global()
mejor = medias.index[0]
gana = (t17["Mejor modelo"] == mejor).sum()
inflado = t15[t15["especie"] != "Telmatobius_macrostomus"]["dif_auc_roc"].mean()

c1, c2 = st.columns([1, 1.15], gap="large")
with c1:
    ui.titulo(
        f"{C.NOMBRE_MODELO[mejor]} fue el más consistente",
        f"Quedó primero en {gana} de las 3 especies al promediar sus puestos en AUC-ROC, AUC-PR y TSS, siempre con "
        "validación espacial. Para la rana de Junín ganó Random Forest. MaxEnt, el método clásico, quedó último en las tres.",
    )
    ui.espacio()
    ui.nota(
        "La diferencia entre modelos no es estadísticamente significativa (prueba de Friedman, p > 0.05): con tres especies "
        "la prueba tiene muy poca potencia. Léelo como una tendencia, no como un veredicto."
    )
with c2:
    ui.grafico(fig_rank, key="ranking")

ui.seccion()
a, b, c = st.columns(3, gap="large")
with a:
    ui.cifra(f"−{inflado:.2f}", "AUC-ROC que pierden en promedio las dos aves al validar en bloques geográficos en vez de al azar. La validación aleatoria era optimista.")
with b:
    total = sum(len(D.presencias(e)) for e in C.ESPECIES)
    ui.cifra(f"{total}", "presencias útiles de 2 045 registros descargados: duplicados y puntos a menos de 5 km se eliminan.")
with c:
    ui.cifra("9 km", "lado de cada celda del mapa (5 minutos de arco). Es la resolución a la que el modelo “ve” el paisaje.")

# ---------- el lago ----------
ui.seccion()
lago = C.FOTOS["paisaje"]
st.html(
    '<section class="sdm-banda sdm-revela">'
    f'<div class="marco"><img src="{ui.url_foto("paisaje")}" alt="{lago["alt"]}" style="object-position:{lago["foco"]}"></div>'
    '<div class="texto">'
    '<p class="dicho">La rana gigante solo vive en los lagos de Junín y Pasco. '
    "Cada modelo se compara dentro de su mundo, no contra la costa.</p>"
    f'<p class="pie-foto">Atardecer en el lago Junín (Chinchaycocha). {ui.credito("paisaje")}</p>'
    "</div></section>"
)

# ---------- perfil altitudinal ----------
ui.seccion()
ui.titulo(
    "La altitud las separa",
    "La elevación separa a las tres mejor que cualquier otra variable. La lechucita vive en la yunga nublada; el churrete y la rana, "
    "en la puna, pero el churrete sube más, hasta el borde de los glaciares.",
)
ui.espacio()
ui.grafico(G.perfil_altitudinal(), key="perfil")
ui.nota("Elevación media de la celda de 9 km donde cae cada registro. Las bandas son las regiones naturales de Pulgar Vidal (rangos aproximados).")

ui.pie()
