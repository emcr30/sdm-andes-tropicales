"""Rutas, metadatos de especies y textos que se reutilizan en toda la app."""
from __future__ import annotations

import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# Carpeta de resultados que escribe el notebook (en Drive: tesis_sdm/resultados)
RESULTADOS = Path(os.environ.get("SDM_RESULTADOS", RAIZ / "resultados")).expanduser()
# Capas de WorldClim recortadas al Perú (en Drive: tesis_sdm/worldclim_peru)
WORLDCLIM = Path(os.environ.get("SDM_WORLDCLIM", RAIZ / "worldclim_peru")).expanduser()

DIR_TABLAS = RESULTADOS / "tablas"
DIR_MODELOS = RESULTADOS / "models"
DIR_RASTERS = RESULTADOS / "rasters"
DIR_DATOS = RESULTADOS / "datos"
DIR_FIGURAS = RESULTADOS / "figures"

# Capas de referencia (no salen del notebook): ANP del SERNANP y, si se agregan, rangos conocidos por especie
DIR_CAPAS = RAIZ / "capas"
ARCHIVO_ANP = DIR_CAPAS / "anp_sernanp.geojson"
DIR_RANGOS = DIR_CAPAS / "rangos"  # <Especie>.geojson, p. ej. Xenoglaux_loweryi.geojson (UICN / BirdLife)

# Parámetros del estudio (celda 0.3 del notebook)
RADIO_M_KM = 100
DISTANCIA_MIN_KM = 5
UMBRAL_PEARSON = 0.7
UMBRAL_VIF = 5
RADIO_TIERRA_KM = 6371.0088

ESPECIES = {
    "Xenoglaux_loweryi": {
        "nombre": "Xenoglaux loweryi",
        "corto": "X. loweryi",
        "comun": "Lechucita bigotona",
        "grupo": "Ave",
        "habitat": "Bosque nublado de la vertiente oriental, en Amazonas y San Martín.",
        "simbolo": "circle",
    },
    "Cinclodes_palliatus": {
        "nombre": "Cinclodes palliatus",
        "corto": "C. palliatus",
        "comun": "Churrete real",
        "grupo": "Ave",
        "habitat": "Bofedales y roquedales de la puna, cerca del límite de los glaciares.",
        "simbolo": "diamond",
    },
    "Telmatobius_macrostomus": {
        "nombre": "Telmatobius macrostomus",
        "corto": "T. macrostomus",
        "comun": "Rana gigante de Junín",
        "grupo": "Anfibio",
        "habitat": "Lagos y ríos altoandinos de la meseta de Junín y Pasco.",
        "simbolo": "triangle-up",
    },
}

# Fotos servidas desde static/img (server.enableStaticServing). Cada una se acredita bajo la foto y en el pie.
FOTOS = {
    "Xenoglaux_loweryi": {
        "archivo": "xenoglaux_loweryi.jpg", "autor": "photokeen", "licencia": "CC BY-NC-ND",
        "fuente": "https://www.inaturalist.org/photos/215288643", "alt": "Lechucita bigotona posada de frente, de noche",
        "foco": "50% 40%",
    },
    "Cinclodes_palliatus": {
        "archivo": "cinclodes_palliatus.jpg", "autor": "Mickaël Villemagne", "licencia": "CC BY-NC",
        "fuente": "https://www.inaturalist.org/observations/41701153", "alt": "Churrete real con un insecto en el pico sobre una mata de musgo",
        "foco": "46% 50%",
    },
    "Telmatobius_macrostomus": {
        "archivo": "telmatobius_macrostomus.jpg", "autor": "Carlos Arias Segura", "licencia": "CC BY-SA",
        "fuente": "https://www.inaturalist.org/photos/305325648", "alt": "Rana gigante de Junín entre plantas acuáticas",
        "foco": "56% 50%",
    },
    "paisaje": {
        "archivo": "lago_junin.jpg", "autor": "Jonathan Chancasana", "licencia": "CC BY-SA 4.0",
        "fuente": "https://commons.wikimedia.org/wiki/File:Atardecer_en_el_lago_Jun%C3%ADn.jpg",
        "alt": "Atardecer sobre el lago Junín, con totorales y la cordillera al fondo", "foco": "50% 60%",
    },
}

MODELOS = ["RandomForest", "SVM", "LightGBM", "MaxEnt"]
NOMBRE_MODELO = {"RandomForest": "Random Forest", "SVM": "SVM", "LightGBM": "LightGBM", "MaxEnt": "MaxEnt"}
# Paleta categórica validada (orden fijo, nunca se recicla)
COLOR_MODELO = {"RandomForest": "#2a78d6", "SVM": "#eb6834", "LightGBM": "#1baf7a", "MaxEnt": "#eda100"}

DESCRIPCION_MODELO = {
    "RandomForest": "Muchos árboles de decisión entrenados con submuestras; la predicción es el voto promedio.",
    "SVM": "Busca la frontera que mejor separa presencias de pseudoausencias en el espacio ambiental.",
    "LightGBM": "Árboles que se suman uno tras otro, cada uno corrige los errores del anterior.",
    "MaxEnt": "El método clásico de nicho: la distribución más uniforme compatible con las presencias.",
}

ESTRATEGIAS = {
    "buffer": "Buffer",
    "aleatoria": "Aleatoria",
    "ambiental": "Ambiental",
}
DESCRIPCION_ESTRATEGIA = {
    "aleatoria": "Celdas al azar dentro del área accesible M.",
    "buffer": "Celdas en un anillo de distancia alrededor de las presencias.",
    "ambiental": "Las celdas de M con el clima más distinto al de las presencias. Se documenta pero no entra al ranking: separa demasiado fácil y infla las métricas.",
}

VARIABLES = {
    "bio_1": ("Temperatura media anual", "°C"),
    "bio_2": ("Rango diurno medio de temperatura", "°C"),
    "bio_3": ("Isotermalidad", "%"),
    "bio_4": ("Estacionalidad de la temperatura", "°C × 100"),
    "bio_5": ("Temperatura máxima del mes más cálido", "°C"),
    "bio_6": ("Temperatura mínima del mes más frío", "°C"),
    "bio_7": ("Rango anual de temperatura", "°C"),
    "bio_8": ("Temperatura media del trimestre más lluvioso", "°C"),
    "bio_9": ("Temperatura media del trimestre más seco", "°C"),
    "bio_10": ("Temperatura media del trimestre más cálido", "°C"),
    "bio_11": ("Temperatura media del trimestre más frío", "°C"),
    "bio_12": ("Precipitación anual", "mm"),
    "bio_13": ("Precipitación del mes más lluvioso", "mm"),
    "bio_14": ("Precipitación del mes más seco", "mm"),
    "bio_15": ("Estacionalidad de la precipitación", "CV %"),
    "bio_16": ("Precipitación del trimestre más lluvioso", "mm"),
    "bio_17": ("Precipitación del trimestre más seco", "mm"),
    "bio_18": ("Precipitación del trimestre más cálido", "mm"),
    "bio_19": ("Precipitación del trimestre más frío", "mm"),
    "elevation": ("Elevación", "m s. n. m."),
}

# Lectura biológica breve de cada variable seleccionada
LECTURA_VARIABLE = {
    "bio_2": "Diferencia típica entre el día y la noche. En el bosque nublado la neblina la amortigua.",
    "bio_3": "Qué tanto pesa la oscilación diaria frente a la anual. Valores altos: días muy distintos a las noches, pero estaciones parecidas, típico de la puna tropical.",
    "bio_4": "Cuánto cambia la temperatura a lo largo del año.",
    "bio_13": "Lluvia del mes más húmedo; marca la intensidad de la temporada de lluvias.",
    "bio_15": "Qué tan concentrada está la lluvia en una época del año.",
    "bio_18": "Lluvia en los meses más cálidos, que en los Andes coinciden con la temporada húmeda.",
    "bio_19": "Lluvia en los meses más fríos, la estación seca andina.",
    "elevation": "Altitud media de la celda de 9 km. Resume temperatura y oxígeno disponibles.",
}

# Regiones naturales de Pulgar Vidal (rangos aproximados, vertiente occidental)
PISOS = [
    (0, 500, "Chala"),
    (500, 2300, "Yunga"),
    (2300, 3500, "Quechua"),
    (3500, 4000, "Suni"),
    (4000, 4800, "Puna"),
    (4800, 5600, "Janca"),
]

GLOSARIO = {
    "Presencia": "Un punto donde alguien registró a la especie (GBIF o iNaturalist), ya depurado.",
    "Pseudoausencia": "Un punto donde no hay registro y que el modelo trata como ausencia. No es una ausencia verificada en campo.",
    "Área accesible M": "La región que la especie pudo alcanzar: celdas del Perú a menos de 100 km de alguna presencia. Fuera de M el modelo extrapola.",
    "Idoneidad": "Valor de 0 a 1 que da el modelo para cada celda de 9 × 9 km. No es abundancia ni probabilidad de observarla: indica qué tan parecido es el ambiente al de las presencias.",
    "Umbral": "El corte que convierte la idoneidad en idóneo / no idóneo. La tesis usa el que maximiza el TSS en los datos de entrenamiento.",
    "AUC-ROC": "Probabilidad de que el modelo dé más idoneidad a una presencia que a una pseudoausencia elegida al azar. 0.5 es azar, 1 es perfecto.",
    "AUC-PR": "Qué tan bien ordena las presencias cuando se mira solo a las que predice como presencias. Es más exigente con pocos datos.",
    "TSS": "Sensibilidad + especificidad − 1. Va de −1 a 1; 0 es azar. Mide aciertos en presencias y en pseudoausencias a la vez.",
    "Validación espacial": "Se prueba el modelo en bloques geográficos que no vio al entrenar. Evita que puntos vecinos casi idénticos inflen las métricas.",
    "Adelgazamiento espacial": "Quitar registros demasiado cercanos (menos de 5 km) para que las zonas muy muestreadas no dominen el modelo.",
    "VIF": "Factor de inflación de la varianza. Mide cuánto se repite una variable en las demás; sobre 5 se considera redundante.",
}
