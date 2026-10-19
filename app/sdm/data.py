"""Carga de los productos del notebook. Todo se cachea: los archivos no cambian durante la sesión."""
from __future__ import annotations

import json
from dataclasses import dataclass

import numpy as np
import pandas as pd
import streamlit as st

from . import config as C


# ---------- tablas ----------

@st.cache_data(show_spinner=False)
def tabla(nombre: str) -> pd.DataFrame:
    ruta = C.DIR_TABLAS / f"{nombre}.csv"
    if not ruta.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(ruta)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


@st.cache_data(show_spinner=False)
def resultados_pliegue() -> pd.DataFrame:
    return pd.read_csv(C.DIR_MODELOS / "resultados_por_pliegue.csv")


@st.cache_data(show_spinner=False)
def sensibilidad() -> pd.DataFrame:
    ruta = C.DIR_MODELOS / "sensibilidad_hiperparametros.csv"
    return pd.read_csv(ruta) if ruta.exists() else pd.DataFrame()


@st.cache_data(show_spinner=False)
def metadatos() -> dict:
    ruta = C.DIR_MODELOS / "metadatos_web.json"
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}


@st.cache_data(show_spinner=False)
def presencias(esp: str) -> pd.DataFrame:
    return pd.read_csv(C.DIR_DATOS / f"{esp}_presencias_limpias.csv")


@st.cache_data(show_spinner=False)
def dataset(esp: str) -> pd.DataFrame:
    return pd.read_csv(C.DIR_DATOS / f"{esp}_dataset_final.csv")


def variables_de(esp: str) -> list[str]:
    meta = metadatos().get(esp, {})
    if meta.get("variables"):
        return list(meta["variables"])
    d = presencias(esp)
    return [c for c in d.columns if c in C.VARIABLES]


def mejor_modelo(esp: str) -> str:
    meta = metadatos().get(esp, {})
    if meta.get("modelo"):
        return meta["modelo"]
    t = tabla("17_mejor_modelo")
    fila = t[t["Especie"] == C.ESPECIES[esp]["nombre"]]
    return fila["Mejor modelo"].iloc[0] if len(fila) else "SVM"


def umbral_tesis(esp: str, modelo: str) -> float:
    """Umbral de máximo TSS de la Tabla 22 (sección 5.6); si falta, el promedio de los pliegues espaciales."""
    t = tabla("22_area_idonea")
    if len(t):
        f = t[(t["Especie"] == C.ESPECIES[esp]["nombre"]) & (t["Modelo"] == modelo)]
        if len(f):
            return float(f["Umbral (máx. TSS)"].iloc[0])
    r = resultados_pliegue()
    sub = r[(r.especie == esp) & (r.estrategia == "buffer") & (r.validacion == "espacial") & (r.modelo == modelo)]
    return float(sub["umbral_opt"].mean()) if len(sub) else 0.5


# ---------- rásters ----------

@dataclass(frozen=True)
class Grilla:
    lon: np.ndarray  # centros de columna (ancho)
    lat: np.ndarray  # centros de fila (alto)
    res: float
    peru: np.ndarray  # máscara booleana de celdas válidas dentro del Perú
    km2: np.ndarray  # área aproximada de cada celda (km²)


def _leer_tif(ruta):
    import rasterio

    with rasterio.open(ruta) as src:
        a = src.read(1, masked=True).astype("float32").filled(np.nan)
        return a, src.transform


@st.cache_data(show_spinner=False)
def idoneidad(esp: str, modelo: str) -> np.ndarray | None:
    ruta = C.DIR_RASTERS / f"{esp}_{modelo}.tif"
    if not ruta.exists():
        return None
    a, _ = _leer_tif(ruta)
    a[a < -1] = np.nan
    return a


@st.cache_resource(show_spinner=False)
def grilla() -> Grilla:
    ruta = next(C.DIR_RASTERS.glob("*.tif"))
    a, t = _leer_tif(ruta)
    alto, ancho = a.shape
    res = float(t.a)
    lon = t.c + res * (np.arange(ancho) + 0.5)
    lat = t.f + t.e * (np.arange(alto) + 0.5)
    peru = np.isfinite(a) & (a > -1)
    km2_celda = (111.32 * res) * (110.57 * res)
    km2 = km2_celda * np.cos(np.radians(lat))[:, None] * np.ones((1, ancho))
    return Grilla(lon=lon, lat=lat, res=res, peru=peru, km2=km2)


@st.cache_data(show_spinner=False)
def capa_ambiental(var: str) -> np.ndarray | None:
    ruta = C.WORLDCLIM / f"{var}.tif"
    if not ruta.exists():
        return None
    a, _ = _leer_tif(ruta)
    return a


@st.cache_data(show_spinner=False)
def relieve() -> np.ndarray | None:
    """Sombreado del relieve a partir de la elevación de WorldClim, solo dentro del Perú."""
    elev = capa_ambiental("elevation")
    if elev is None:
        return None
    g = grilla()
    z = np.where(np.isfinite(elev), elev, np.nanmin(elev)).astype("float64")
    dy = 110.57e3 * g.res
    dx = 111.32e3 * g.res * np.cos(np.radians(g.lat))[:, None]
    gy, gx = np.gradient(z)
    gx = gx / dx
    gy = -gy / dy  # las filas van de norte a sur
    z_factor = 6.0
    pend = np.arctan(z_factor * np.hypot(gx, gy))
    aspecto = np.arctan2(gy, -gx)
    azim, alt = np.radians(315.0), np.radians(42.0)
    som = np.sin(alt) * np.cos(pend) + np.cos(alt) * np.sin(pend) * np.cos(azim - aspecto)
    som = np.clip(som, 0, 1)
    return np.where(g.peru, som, np.nan).astype("float32")


def _haversine_min(lat_c, lon_c, lat_p, lon_p):
    la1, lo1 = np.radians(lat_c)[:, None], np.radians(lon_c)[:, None]
    la2, lo2 = np.radians(lat_p)[None, :], np.radians(lon_p)[None, :]
    h = np.sin((la2 - la1) / 2) ** 2 + np.cos(la1) * np.cos(la2) * np.sin((lo2 - lo1) / 2) ** 2
    return (2 * C.RADIO_TIERRA_KM * np.arcsin(np.sqrt(h))).min(axis=1)


@st.cache_data(show_spinner=False)
def area_m(esp: str) -> np.ndarray:
    """Celdas del Perú a menos de RADIO_M_KM de alguna presencia (sección 3.3 del notebook)."""
    g = grilla()
    p = presencias(esp)
    filas, cols = np.nonzero(g.peru)
    d = _haversine_min(g.lat[filas], g.lon[cols], p["decimalLatitude"].to_numpy(), p["decimalLongitude"].to_numpy())
    m = np.zeros_like(g.peru)
    m[filas, cols] = d <= C.RADIO_M_KM
    return m


def extension(mascara: np.ndarray, margen: float = 0.6):
    g = grilla()
    filas, cols = np.nonzero(mascara)
    return (
        float(g.lon[cols.min()] - margen),
        float(g.lon[cols.max()] + margen),
        float(g.lat[filas.max()] - margen),
        float(g.lat[filas.min()] + margen),
    )


def resumen_umbral(esp: str, modelo: str, umbral: float) -> dict:
    g = grilla()
    mapa = idoneidad(esp, modelo)
    m = area_m(esp)
    idoneo = np.isfinite(mapa) & (mapa >= umbral)
    km2_peru = float(g.km2[idoneo & g.peru].sum())
    km2_m = float(g.km2[idoneo & m].sum())
    return {
        "km2_peru": km2_peru,
        "km2_m": km2_m,
        "pct_m": 100 * float(np.nanmean(mapa[m] >= umbral)) if m.any() else 0.0,
        "pct_peru": 100 * float(np.nanmean(mapa[g.peru] >= umbral)),
        "km2_total_m": float(g.km2[m].sum()),
    }


# ---------- capas de referencia ----------

@st.cache_data(show_spinner=False)
def anp() -> dict | None:
    return json.loads(C.ARCHIVO_ANP.read_text(encoding="utf-8")) if C.ARCHIVO_ANP.exists() else None


@st.cache_data(show_spinner=False)
def rango(esp: str) -> dict | None:
    ruta = C.DIR_RANGOS / f"{esp}.geojson"
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else None


@st.cache_resource(show_spinner=False)
def mascara_anp() -> np.ndarray | None:
    """Celdas de la grilla cuyo centro cae dentro de alguna ANP."""
    gj = anp()
    if gj is None:
        return None
    from rasterio.features import rasterize
    from rasterio.transform import from_origin

    g = grilla()
    t = from_origin(g.lon[0] - g.res / 2, g.lat[0] + g.res / 2, g.res, g.res)
    formas = [(f["geometry"], 1) for f in gj["features"] if f.get("geometry")]
    return rasterize(formas, out_shape=g.peru.shape, transform=t, fill=0, dtype="uint8").astype(bool) & g.peru


def idoneo_en_anp(esp: str, modelo: str, umbral: float) -> dict | None:
    m_anp = mascara_anp()
    if m_anp is None:
        return None
    g = grilla()
    idoneo = (np.nan_to_num(idoneidad(esp, modelo), nan=-1) >= umbral) & area_m(esp)
    total = float(g.km2[idoneo].sum())
    dentro = float(g.km2[idoneo & m_anp].sum())
    return {"km2": dentro, "pct": 100 * dentro / total if total else 0.0}


def hay_resultados() -> bool:
    return C.DIR_RASTERS.exists() and any(C.DIR_RASTERS.glob("*.tif")) and (C.DIR_MODELOS / "resultados_por_pliegue.csv").exists()
