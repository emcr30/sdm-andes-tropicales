
import pandas as pd
from sklearn.neighbors import BallTree
import numpy as np

def combinar_fuentes(gbif_path, inat_path):
    """Combina GBIF + iNaturalist y elimina duplicados por coordenadas casi-exactas."""
    df_gbif = pd.read_csv(gbif_path)
    df_inat = pd.read_csv(inat_path)

    df_gbif["fuente"] = "gbif"
    df_inat["fuente"] = "inat"

    combinado = pd.concat([
        df_gbif[["decimalLatitude", "decimalLongitude", "fuente"]],
        df_inat[["decimalLatitude", "decimalLongitude", "fuente"]]
    ], ignore_index=True).dropna()

    combinado["lat_r"] = combinado["decimalLatitude"].round(4)
    combinado["lon_r"] = combinado["decimalLongitude"].round(4)
    combinado = combinado.drop_duplicates(subset=["lat_r", "lon_r"]).drop(columns=["lat_r", "lon_r"])

    return combinado.reset_index(drop=True)


def rarefaccion_espacial(df, umbral_km, lat_col="decimalLatitude", lon_col="decimalLongitude"):
    """Conserva un solo punto por vecindad definida por umbral_km."""
    coords_rad = np.radians(df[[lat_col, lon_col]].values)
    tree = BallTree(coords_rad, metric="haversine")

    radio_tierra_km = 6371.0
    umbral_rad = umbral_km / radio_tierra_km

    conservados = []
    descartados = set()

    for i in range(len(df)):
        if i in descartados:
            continue
        conservados.append(i)
        vecinos = tree.query_radius([coords_rad[i]], r=umbral_rad)[0]
        for v in vecinos:
            if v != i:
                descartados.add(v)

    return df.iloc[conservados].reset_index(drop=True)
