import streamlit as st

from sdm import config as C
from sdm import data as D
from sdm import graficos as G
from sdm import ui
from sdm.theme import RAMPA_IDONEIDAD, T, VERDE_IDONEO

ui.espacio()
st.html(
    '<div class="sdm-entra">'
    '<h1 class="sdm-display" style="font-size:var(--step-title)">Mapa de idoneidad</h1>'
    '<p class="sdm-lead" style="margin-top:16px">Qué tan parecido es el ambiente de cada celda del Perú al de los lugares '
    "donde se registró la especie. Mueve el umbral para ver cuánto territorio queda como idóneo.</p>"
    "</div>"
)
ui.espacio()

esp = ui.selector_especie("esp_mapa")
mejor = D.mejor_modelo(esp)

ctrl, mapa_col = st.columns([1, 2.1], gap="large")
with ctrl:
    with st.container(key="panel-controles"):
        info = C.ESPECIES[esp]
        st.html(f'<div class="sdm-mini"><img src="{ui.url_foto(esp)}" alt="{C.FOTOS[esp]["alt"]}" '
                f'style="object-position:{C.FOTOS[esp]["foco"]}"><div><div class="n">{info["comun"]}</div>'
                f'<div class="s"><span class="sdm-sci">{info["nombre"]}</span></div></div></div>')
        clave_mod = f"modelo_{esp}"
        modelo = ui.segmentado(
            "Modelo", C.MODELOS, clave_mod, default=mejor,
            format_func=lambda m: C.NOMBRE_MODELO[m] + (" ★" if m == mejor else ""),
        )
        vista = ui.segmentado("Mostrar", ["continua", "binaria"], "vista_mapa", default="continua",
                              format_func={"continua": "Idoneidad 0–1", "binaria": "Idóneo / no idóneo"}.get)
        clave_u = f"umbral_{esp}_{modelo}"
        u_tesis = round(D.umbral_tesis(esp, modelo), 3)
        if clave_u not in st.session_state:
            st.session_state[clave_u] = u_tesis
        umbral = st.slider("Umbral de idoneidad", 0.05, 0.95, step=0.001, format="%.3f", key=clave_u,
                           help="Por encima de este valor una celda se considera idónea. La tesis usa el que maximiza el TSS.")

        def _reponer():
            st.session_state[clave_u] = u_tesis

        if abs(umbral - u_tesis) > 1e-6:
            with st.container(key="secundario"):
                st.button(f"Volver al umbral de la tesis ({u_tesis:.3f})", on_click=_reponer, width="stretch")
        else:
            ui.nota(f"Es el umbral de la tesis: el que maximiza el TSS para {C.NOMBRE_MODELO[modelo]}.")
        extension = ui.segmentado("Encuadre", ["M", "Perú"], "encuadre", default="M",
                                  format_func={"M": "Área accesible", "Perú": "Todo el Perú"}.get)
        with st.container(key="capas"):
            st.html('<p class="sdm-note" style="margin-top:6px">Capas de referencia</p>')
            ver_dptos = st.checkbox("Departamentos", value=True, key="ver_dptos", disabled=D.departamentos() is None)
            ver_zonas = st.checkbox("Zonas predichas sin registros", value=True, key="ver_zonas",
                                    help="Manchas idóneas (sobre el umbral) donde todavía no hay ninguna presencia: "
                                         "lugares donde el modelo predice que la especie podría estar.")
            ver_fuera = st.checkbox("Incluir zonas fuera de M", key="ver_fuera", disabled=not ver_zonas,
                                    help="Fuera del área accesible el modelo extrapola a climas que no comparó. "
                                         "Esas zonas se muestran atenuadas y son hipótesis débiles.")
            ver_anp = st.checkbox("Áreas naturales protegidas", key="ver_anp", disabled=D.anp() is None)
            ver_rango = st.checkbox("Rango conocido (UICN / BirdLife)", key=f"ver_rango_{esp}") if D.rango(esp) else False

    r = D.resumen_umbral(esp, modelo, umbral)
    zonas = D.zonas_predichas(esp, modelo, umbral)
    candidatas = zonas[~zonas["con_registros"] & (zonas["dentro_m"] | ver_fuera)]
    nuevas = candidatas.head(C.MAX_ZONAS).reset_index(drop=True)
    conocidas = zonas[zonas["con_registros"]]
    ui.espacio()
    with st.container(key="panel-resultado"):
        ui.cifra(f"{ui.fmt_km2(r['km2_m'])} km²", f"idóneos dentro de M, el {r['pct_m']:.1f} % de su superficie")
        ui.espacio()
        ui.cifra(f"{r['pct_peru']:.1f} %", f"del Perú queda como idóneo ({ui.fmt_km2(r['km2_peru'])} km²), incluso fuera de M")
        en_anp = D.idoneo_en_anp(esp, modelo, umbral) if ver_anp else None
        if en_anp is not None:
            ui.nota(f"De lo idóneo dentro de M, el {en_anp['pct']:.0f} % ({ui.fmt_km2(en_anp['km2'])} km²) cae en un área natural protegida.")

with mapa_col:
    ui.grafico(G.mapa_idoneidad(esp, modelo, umbral, vista == "binaria", extension, anp=ver_anp, rango=ver_rango,
                                dptos=ver_dptos, zonas=nuevas if ver_zonas else None),
               key="mapa_principal")
    if vista == "binaria":
        ui.leyenda([("barra", VERDE_IDONEO, f"Idóneo (≥ {umbral:.3f})"), ("punto", T["ink"], "Presencia")])
    st.html(
        '<p class="sdm-leyenda" style="margin-top:6px">'
        f'<span><b style="background:transparent;border-top:2px dotted {T["ink"]};height:0;border-radius:0"></b>'
        "Límite del área accesible M: fuera de ella el modelo extrapola</span>"
        + ('<span><b style="background:transparent;border-top:1px solid rgba(15,26,20,0.42);height:0;border-radius:0"></b>'
           "Límite departamental</span>" if ver_dptos else "")
        + (f'<span><i style="background:{T["bg"]};box-shadow:inset 0 0 0 2px {T["accent"]}"></i>'
           "Zona predicha sin registros (numerada por tamaño)</span>" if ver_zonas else "")
        + ('<span><b style="background:rgba(15,26,20,0.05);box-shadow:inset 0 0 0 1px rgba(15,26,20,0.55)"></b>'
           "Áreas naturales protegidas (SERNANP)</span>" if ver_anp else "")
        + (f'<span><b style="background:transparent;border-top:2px solid {T["accent"]};height:0"></b>'
           "Rango conocido de la especie</span>" if ver_rango else "")
        + "</p>"
    )

# ---------- dónde podría estar ----------
ui.seccion()
ui.titulo(
    "Dónde podría estar la especie",
    f"La predicción de {C.NOMBRE_MODELO[modelo]} con el umbral {umbral:.3f}: las manchas idóneas que todavía no tienen "
    "ningún registro son los lugares donde convendría buscarla en campo. Los números coinciden con los del mapa.",
)
ui.espacio()
z1, z2 = st.columns([1.4, 1], gap="large")
with z1:
    st.html('<p class="sdm-head" style="font-size:1.375rem">Zonas predichas sin registros</p>')
    if nuevas.empty:
        ui.nota("Con este umbral no quedan manchas idóneas sin registros dentro de M. Baja el umbral o incluye las zonas "
                "fuera de M para ver más candidatas.")
    else:
        tabla_z = nuevas.assign(**{
            "N.º": range(1, len(nuevas) + 1),
            "Departamento": nuevas["departamentos"],
            "Superficie (km²)": nuevas["km2"].round(0).astype(int),
            "Idoneidad máx.": nuevas["idoneidad_max"].round(2),
            "Lat": nuevas["lat"].round(2), "Lon": nuevas["lon"].round(2),
            "Ubicación": nuevas["dentro_m"].map({True: "Dentro de M", False: "Fuera de M (extrapola)"}),
        })[["N.º", "Departamento", "Superficie (km²)", "Idoneidad máx.", "Lat", "Lon", "Ubicación"]]
        st.dataframe(tabla_z, hide_index=True, width="stretch", height=min(38 * len(tabla_z) + 40, 420))
        fuera = int((~zonas["con_registros"] & ~zonas["dentro_m"]).sum())
        ui.nota(f"{len(candidatas)} zonas candidatas"
                + (f" (aquí las {C.MAX_ZONAS} más grandes)" if len(candidatas) > C.MAX_ZONAS else "")
                + f" y {len(conocidas)} que ya tienen registros"
                + (f"; {fuera} más fuera de M quedan ocultas" if fuera and not ver_fuera else "") + ". Lat/Lon es la celda de mayor idoneidad "
                f"de cada zona. Solo se cuentan manchas de {C.MIN_CELDAS_ZONA} celdas o más (unos {C.MIN_CELDAS_ZONA * 85} km²).")
with z2:
    st.html('<p class="sdm-head" style="font-size:1.375rem">Superficie idónea por departamento</p>')
    por_d = D.idoneo_por_departamento(esp, modelo, umbral)
    if por_d.empty:
        ui.nota("Falta la capa de departamentos (capas/departamentos_peru.geojson).")
    else:
        st.dataframe(por_d.assign(**{
            "Idóneo (km²)": por_d["km2"].round(0).astype(int),
            "% del departamento": por_d["pct_dpto"].round(1),
            "Registros": por_d["registros"],
        })[["Departamento", "Idóneo (km²)", "% del departamento", "Registros"]],
            hide_index=True, width="stretch", height=min(38 * len(por_d) + 40, 420))
        ui.nota("Un departamento con superficie idónea y sin registros es una predicción a verificar, no una presencia confirmada.")

# ---------- cómo leerlo ----------
ui.seccion()
l1, l2, l3 = st.columns(3, gap="large")
with l1:
    st.html('<p class="sdm-head" style="font-size:1.375rem">Qué es la idoneidad</p>')
    st.html(f'<p class="sdm-body" style="margin-top:10px">{C.GLOSARIO["Idoneidad"]}</p>')
with l2:
    st.html('<p class="sdm-head" style="font-size:1.375rem">Por qué importa M</p>')
    st.html('<p class="sdm-body" style="margin-top:10px">El modelo solo vio pseudoausencias dentro de M. Fuera de esa línea '
            "predice sobre climas que nunca comparó, por eso una mancha verde lejos de las presencias es una hipótesis, no un hallazgo.</p>")
with l3:
    st.html('<p class="sdm-head" style="font-size:1.375rem">Qué no dice el mapa</p>')
    st.html('<p class="sdm-body" style="margin-top:10px">No incluye cobertura de bosque, ríos ni barreras. Un lugar puede tener el clima '
            "adecuado y estar deforestado o fuera del alcance de la especie.</p>")

# ---------- comparación ----------
ui.seccion()
ui.titulo(
    "Los cuatro modelos, lado a lado",
    "Mismos datos, mismas variables, mismos pliegues. Cada modelo con su propio umbral de la tesis. "
    "Si los cuatro coinciden en una zona, esa predicción es más robusta.",
)
ui.espacio()
umbrales = {m: D.umbral_tesis(esp, m) for m in C.MODELOS}
fila1 = st.columns(2, gap="medium")
fila2 = st.columns(2, gap="medium")
for col, m in zip(fila1 + fila2, C.MODELOS):
    with col:
        with st.container(key=f"panel-mini-{m}"):
            st.html(f'<p class="sdm-body" style="font-weight:600">{C.NOMBRE_MODELO[m]}'
                    f'<span style="color:var(--muted);font-weight:400"> · umbral {umbrales[m]:.2f}'
                    f'{" · mejor modelo" if m == mejor else ""}</span></p>')
            ui.grafico(G.mini_mapa(esp, m, umbrales[m], vista == "binaria"), key=f"mini_{m}")
ui.espacio()
a1, a2 = st.columns([1, 1.4], gap="large")
with a1:
    st.html('<p class="sdm-head" style="font-size:1.375rem">Cuánto de M marca cada modelo</p>')
    res = {m: D.resumen_umbral(esp, m, umbrales[m]) for m in C.MODELOS}
    amplio = max(res, key=lambda m: res[m]["pct_m"])
    estrecho = min(res, key=lambda m: res[m]["pct_m"])
    st.html('<p class="sdm-body" style="margin-top:10px">Un modelo que marca casi todo como idóneo no discrimina. '
            f"Para esta especie el más generoso es {C.NOMBRE_MODELO[amplio]} ({res[amplio]['pct_m']:.0f} % de M) y el más "
            f"estricto {C.NOMBRE_MODELO[estrecho]} ({res[estrecho]['pct_m']:.0f} %).</p>")
with a2:
    ui.grafico(G.areas_modelos(esp, umbrales), key="areas")

ui.pie()
