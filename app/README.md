# Nichos andinos

Aplicación Streamlit para ver los resultados del notebook **SDM_CRISPDM_v2.ipynb**
(tesis de Evelyn Milagros Chipana Ramos, Universidad La Salle, Arequipa).

No entrena modelos: lee los archivos que el notebook guarda en `tesis_sdm/resultados`
y muestra mapas de idoneidad, fichas de especies, la comparación de modelos y el método.

## Páginas

| Página   | Qué muestra |
|----------|-------------|
| Resumen  | Las tres especies sobre el relieve del Perú, el mejor modelo, el perfil altitudinal y las cifras clave. |
| Especies | Ficha por especie: limpieza de registros, presencias y pseudoausencias, ambiente, importancia de variables. |
| Mapa     | Mapa de idoneidad por especie y modelo, con umbral ajustable y superficie idónea en km². |
| Modelos  | Validación aleatoria vs. espacial, resultados por pliegue, ranking, Friedman y sensibilidad. |
| Método   | Fases de CRISP-DM, correcciones del asesor, trazabilidad, glosario y descargas. |

## Ejecutar en tu computadora

Funciona con Python 3.9 o más nuevo (con 3.9 se instala Streamlit 1.50; está probada con 1.50 y 1.66).

```bash
cd app                      # dentro del repositorio sdm-andes-tropicales
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

La carpeta debe quedar así (ya viene con los resultados de la última ejecución):

```
nichos_andinos/
├── app.py
├── sdm/              # configuración, carga de datos, gráficos y estilos
├── vistas/           # una página por archivo
├── static/           # fotos, marca y tipografía (Schibsted Grotesk), servidas por Streamlit
├── capas/            # capas de referencia: ANP del SERNANP y, opcional, rangos/<Especie>.geojson
├── resultados/       # copia de tesis_sdm/resultados (tablas, models, rasters, datos, figures)
└── worldclim_peru/   # copia de tesis_sdm/worldclim_peru (solo se usa elevation.tif para el relieve)
```

Si los resultados están en otro lugar, indícalo con variables de entorno:

```bash
SDM_RESULTADOS=/ruta/a/resultados SDM_WORLDCLIM=/ruta/a/worldclim_peru streamlit run app.py
```

Cuando vuelvas a correr el notebook, basta con reemplazar `resultados/` por la carpeta nueva.

## Ejecutar en Colab

El notebook `SDM_CRISPDM_v2_con_app.ipynb` trae una celda nueva al final (6.2). Sube esta carpeta a Drive
como `tesis_sdm/app`, cambia `VER_APP = True` y ejecútala: imprime un enlace para abrir la aplicación.

## Publicarla en internet (opcional)

Streamlit Community Cloud la publica gratis desde un repositorio de GitHub. Sube la carpeta completa
(incluidos `resultados/` y `worldclim_peru/elevation.tif`) y elige `app/app.py` como archivo principal.

## Fotos y créditos

Las fotos están en `static/img/` y sus datos en `FOTOS` (`sdm/config.py`). Cada una lleva su crédito debajo y en el pie de página.

| Foto | Autor | Licencia | Fuente |
|---|---|---|---|
| Lechucita bigotona | photokeen | CC BY-NC-ND (se muestra sin modificar) | https://www.inaturalist.org/photos/215288643 |
| Churrete real | Mickaël Villemagne | CC BY-NC | https://www.inaturalist.org/observations/41701153 |
| Rana gigante de Junín | Carlos Arias Segura | CC BY-SA (recortada la franja negra del escaneo) | https://www.inaturalist.org/photos/305325648 |
| Lago Junín | Jonathan Chancasana | CC BY-SA 4.0 | https://commons.wikimedia.org/wiki/File:Atardecer_en_el_lago_Jun%C3%ADn.jpg |

Dos son "NC" (no comercial): sirven para la tesis, pero no para un uso comercial.
Para cambiar una foto, reemplaza el archivo en `static/img/` y actualiza su autor y licencia en `FOTOS`.

## Capas de referencia del mapa

En la página Mapa hay dos casillas, apagadas por defecto:

- **Áreas naturales protegidas**: `capas/anp_sernanp.geojson`, descargado del geoservidor del SERNANP
  (`geoservicios.sernanp.gob.pe`, servicio `servicio_descarga`: ANP nacionales, zonas reservadas y áreas de conservación
  regional), simplificado a ~1 km. Al activarla, el panel indica qué parte de lo idóneo dentro de M cae en un ANP.
- **Rango conocido (UICN / BirdLife)**: solo aparece si existe `capas/rangos/<Especie>.geojson`
  (por ejemplo `capas/rangos/Xenoglaux_loweryi.geojson`). Esos polígonos se piden gratis para uso no comercial en
  https://www.iucnredlist.org/resources/spatial-data-download (la rana) y https://datazone.birdlife.org/contact-us/request-our-data
  (las dos aves). Sus términos no permiten volver a publicarlos, por eso `capas/rangos/` está en `.gitignore`.
