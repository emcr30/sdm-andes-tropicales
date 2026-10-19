"""Constructores de figuras. Ningún color de texto lleva el color de la serie."""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from . import config as C
from . import data as D
from .theme import RAMPA_IDONEIDAD, T, VERDE_IDONEO

ESCALA_RELIEVE = [[0, "#9EA59A"], [0.45, "#C9CDC3"], [0.75, "#E2E4DD"], [1, "#F8F9F5"]]


def _ejes_geo(fig, ext, row=None, col=None, ticks=True):
    x0, x1, y0, y1 = ext
    kw = dict(row=row, col=col) if row else {}
    fig.update_xaxes(range=[x0, x1], showgrid=False, zeroline=False, showline=False, ticks="",
                     showticklabels=ticks, ticksuffix="°", tickfont=dict(size=11, color=T["faint"]), constrain="range", **kw)
    fig.update_yaxes(range=[y0, y1], showgrid=False, zeroline=False, showline=False, ticks="",
                     showticklabels=ticks, ticksuffix="°", tickfont=dict(size=11, color=T["faint"]),
                     scaleanchor="x" if not row else None, scaleratio=1, constrain="range", **kw)


def _capa_relieve(fig, **kw):
    g = D.grilla()
    rel = D.relieve()
    if rel is None:
        z = np.where(g.peru, 1.0, np.nan)
    else:
        z = rel
    elev = D.capa_ambiental("elevation")
    fig.add_trace(go.Heatmap(z=z, x=g.lon, y=g.lat, colorscale=ESCALA_RELIEVE, zmin=0, zmax=1, showscale=False,
                             zsmooth="best", hoverinfo="skip", name="relieve"), **kw)
    return elev


def _contorno_m(fig, esp, **kw):
    g = D.grilla()
    m = D.area_m(esp).astype(float)
    fig.add_trace(go.Contour(z=m, x=g.lon, y=g.lat, contours=dict(start=0.5, end=0.5, size=1, coloring="none"),
                             line=dict(color=T["ink"], width=1.4, dash="dot"), showscale=False, hoverinfo="skip",
                             name="Área accesible M", showlegend=False), **kw)


def _presencias(fig, esp, size=8, **kw):
    p = D.presencias(esp)
    fig.add_trace(go.Scatter(
        x=p["decimalLongitude"], y=p["decimalLatitude"], mode="markers",
        marker=dict(size=size, color=T["ink"], symbol=C.ESPECIES[esp]["simbolo"], line=dict(color="#FFFFFF", width=1.6)),
        customdata=np.stack([p["anio"].fillna(0).astype(int), p["elevation"].round(0), p["fuente"]], axis=-1),
        hovertemplate="<b>Presencia</b><br>%{customdata[2]} · %{customdata[0]}<br>"
                      "Lat %{y:.3f}° · Lon %{x:.3f}°<br>Elevación de la celda %{customdata[1]:,.0f} m<extra></extra>",
        name="Presencias", showlegend=False), **kw)


def _anillos(gj):
    """Contornos de un GeoJSON como una sola polilínea separada por None, con el nombre de cada polígono."""
    xs, ys, nombres = [], [], []
    for f in gj["features"]:
        geom = f.get("geometry") or {}
        polis = geom.get("coordinates", [])
        if geom.get("type") == "Polygon":
            polis = [polis]
        p = f.get("properties") or {}
        nombre = " · ".join(v for v in (p.get("nombre"), p.get("categoria")) if v)
        for poli in polis:
            for anillo in poli:
                xs += [c[0] for c in anillo] + [None]
                ys += [c[1] for c in anillo] + [None]
                nombres += [nombre] * len(anillo) + [None]
    return xs, ys, nombres


def _capa_anp(fig):
    gj = D.anp()
    if gj is None:
        return
    xs, ys, nombres = _anillos(gj)
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", fill="toself", fillcolor="rgba(15,26,20,0.05)",
                             line=dict(color="rgba(15,26,20,0.55)", width=1), text=nombres, hoveron="fills+points",
                             hovertemplate="<b>%{text}</b><br>Área natural protegida (SERNANP)<extra></extra>",
                             name="ANP", showlegend=False))


def _capa_rango(fig, esp):
    gj = D.rango(esp)
    if gj is None:
        return
    xs, ys, _ = _anillos(gj)
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=T["accent"], width=1.6), hoverinfo="skip",
                             name="Rango conocido", showlegend=False))


def mapa_idoneidad(esp: str, modelo: str, umbral: float, binario: bool, vista: str, alto: int = 640,
                   anp: bool = False, rango: bool = False):
    g = D.grilla()
    mapa = D.idoneidad(esp, modelo)
    fig = go.Figure()
    elev = _capa_relieve(fig)
    elev_c = np.where(np.isfinite(elev), elev, np.nan) if elev is not None else np.full_like(mapa, np.nan)
    if binario:
        z = np.where(np.isfinite(mapa), (mapa >= umbral).astype(float), np.nan)
        z = np.where(z > 0, 1.0, np.nan)
        fig.add_trace(go.Heatmap(z=z, x=g.lon, y=g.lat, colorscale=[[0, VERDE_IDONEO], [1, VERDE_IDONEO]], showscale=False,
                                 customdata=np.dstack([mapa, elev_c]),
                                 hovertemplate="Idóneo · idoneidad %{customdata[0]:.2f}<br>Elevación %{customdata[1]:,.0f} m"
                                               "<br>Lat %{y:.2f}° · Lon %{x:.2f}°<extra></extra>", name="idóneo"))
    else:
        fig.add_trace(go.Heatmap(z=mapa, x=g.lon, y=g.lat, colorscale=RAMPA_IDONEIDAD, zmin=0, zmax=1,
                                 customdata=elev_c,
                                 colorbar=dict(title=dict(text="Idoneidad", side="top", font=dict(size=12, color=T["muted"])),
                                               orientation="h", x=0, xanchor="left", y=-0.02, yanchor="top", len=0.45,
                                               thickness=10, outlinewidth=0, tickvals=[0, 0.25, 0.5, 0.75, 1],
                                               tickfont=dict(size=11, color=T["muted"])),
                                 hovertemplate="Idoneidad %{z:.2f}<br>Elevación %{customdata:,.0f} m"
                                               "<br>Lat %{y:.2f}° · Lon %{x:.2f}°<extra></extra>", name="idoneidad"))
    if anp:
        _capa_anp(fig)
    if rango:
        _capa_rango(fig, esp)
    _contorno_m(fig, esp)
    _presencias(fig, esp, size=9)
    ext = D.extension(D.area_m(esp), 0.9) if vista == "M" else D.extension(g.peru, 0.3)
    _ejes_geo(fig, ext)
    fig.update_layout(height=alto, margin=dict(l=0, r=0, t=0, b=36 if not binario else 0), showlegend=False)
    return fig


def mini_mapa(esp: str, modelo: str, umbral: float, binario: bool):
    g = D.grilla()
    mapa = D.idoneidad(esp, modelo)
    fig = go.Figure()
    _capa_relieve(fig)
    if binario:
        z = np.where(np.isfinite(mapa) & (mapa >= umbral), 1.0, np.nan)
        fig.add_trace(go.Heatmap(z=z, x=g.lon, y=g.lat, colorscale=[[0, VERDE_IDONEO], [1, VERDE_IDONEO]], showscale=False, hoverinfo="skip"))
    else:
        fig.add_trace(go.Heatmap(z=mapa, x=g.lon, y=g.lat, colorscale=RAMPA_IDONEIDAD, zmin=0, zmax=1, showscale=False,
                                 hovertemplate="%{z:.2f}<extra></extra>"))
    _contorno_m(fig, esp)
    _presencias(fig, esp, size=5)
    _ejes_geo(fig, D.extension(D.area_m(esp), 0.9), ticks=False)
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
    return fig


def mapa_portada(alto: int = 620):
    """Las tres especies sobre el relieve del Perú, cada una con su forma y rotulada en el mapa."""
    g = D.grilla()
    fig = go.Figure()
    _capa_relieve(fig)
    anot = []
    for esp, info in C.ESPECIES.items():
        p = D.presencias(esp)
        fig.add_trace(go.Scatter(
            x=p["decimalLongitude"], y=p["decimalLatitude"], mode="markers",
            marker=dict(size=9, color=T["ink"], symbol=info["simbolo"], line=dict(color="#FFFFFF", width=1.5)),
            name=info["comun"],
            customdata=np.stack([p["elevation"].round(0)], axis=-1),
            hovertemplate=f"<b>{info['comun']}</b><br><i>{info['nombre']}</i><br>"
                          "Elevación de la celda %{customdata[0]:,.0f} m<extra></extra>"))
        cx, cy = float(p["decimalLongitude"].median()), float(p["decimalLatitude"].median())
        anot.append((esp, cx, cy))
    pos = {
        # colas del rótulo en coordenadas geográficas: siguen dentro del mapa a cualquier ancho
        "Xenoglaux_loweryi": dict(ax=-75.4, ay=-3.6, yanchor="bottom"),
        "Cinclodes_palliatus": dict(ax=-77.6, ay=-15.4, yanchor="top"),
        "Telmatobius_macrostomus": dict(ax=-72.4, ay=-9.6, yanchor="bottom"),
    }
    for esp, cx, cy in anot:
        info = C.ESPECIES[esp]
        fig.add_annotation(x=cx, y=cy, text=f"<b>{info['comun']}</b><br><i>{info['nombre']}</i>", showarrow=True,
                           arrowhead=0, arrowwidth=1.2, arrowcolor=T["ink"], font=dict(size=13, color=T["ink"]),
                           align="center", xanchor="center", axref="x", ayref="y", bgcolor="rgba(242,243,239,0.92)",
                           borderpad=6, **pos[esp])
    _ejes_geo(fig, D.extension(g.peru, 0.25), ticks=False)
    fig.update_layout(height=alto, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
    return fig


def perfil_altitudinal(alto: int = 360):
    """Elevación (de la celda WorldClim) de cada presencia, sobre las regiones naturales de Pulgar Vidal."""
    fig = go.Figure()
    filas = list(C.ESPECIES)
    ys = {e: i for i, e in enumerate(reversed(filas))}
    tonos = [T["bg"], T["surface"]]
    for i, (a, b, nombre) in enumerate(C.PISOS):
        fig.add_vrect(x0=a, x1=b, fillcolor=tonos[i % 2], line_width=0, layer="below")
        fig.add_annotation(x=(a + b) / 2, y=len(filas) - 0.35, text=nombre, showarrow=False, yanchor="bottom",
                           font=dict(size=11, color=T["muted"]), textangle=0)
    rng = np.random.default_rng(7)
    for esp in filas:
        info = C.ESPECIES[esp]
        p = D.presencias(esp)
        y = ys[esp] + rng.uniform(-0.16, 0.16, len(p))
        lo, hi = p["elevation"].min(), p["elevation"].max()
        fig.add_trace(go.Scatter(x=[lo, hi], y=[ys[esp]] * 2, mode="lines", line=dict(color=T["baseline"], width=10),
                                 hoverinfo="skip", showlegend=False))
        fig.add_trace(go.Scatter(
            x=p["elevation"], y=y, mode="markers",
            marker=dict(size=8, color=T["ink"], symbol=info["simbolo"], line=dict(color=T["bg"], width=1.4)),
            hovertemplate=f"<b>{info['comun']}</b><br>%{{x:,.0f}} m<extra></extra>", showlegend=False))
        fig.add_annotation(x=float(p["elevation"].median()), y=ys[esp] - 0.42,
                           text=f"mediana {p['elevation'].median():,.0f} m".replace(",", " "), showarrow=False,
                           font=dict(size=11, color=T["muted"]))
    fig.update_yaxes(tickvals=[ys[e] for e in filas],
                     ticktext=[f"<b>{C.ESPECIES[e]['comun']}</b>  " for e in filas],
                     range=[-0.7, len(filas) - 0.05], showgrid=False, tickfont=dict(size=13, color=T["ink"]))
    fig.update_xaxes(range=[0, 5600], dtick=1000, showgrid=False, tickformat=",", tickangle=0,
                     title="Elevación (m s. n. m.)")
    fig.update_layout(height=alto, margin=dict(l=8, r=8, t=8, b=8), separators=". ")
    return fig


def embudo(esp: str):
    b = D.tabla("04_bitacora_limpieza")
    sub = b[b["Especie"] == C.ESPECIES[esp]["nombre"]].copy()
    sub["Paso"] = sub["Paso"].str.replace(r"^\d+\.\s*", "", regex=True).str.replace(r"\s*\(corrección b\)", "", regex=True)
    n = len(sub)
    colores = [T["faint"]] * (n - 1) + [T["ink"]]
    fig = go.Figure(go.Bar(
        x=sub["Registros"], y=sub["Paso"], orientation="h", marker=dict(color=colores, cornerradius=4),
        text=[f"{v:,}".replace(",", " ") for v in sub["Registros"]], textposition="outside", cliponaxis=False,
        textfont=dict(color=T["ink"], size=12), width=0.62,
        customdata=np.stack([sub["GBIF"], sub["iNaturalist"]], axis=-1),
        hovertemplate="%{y}<br>%{x:,} registros<br>GBIF %{customdata[0]:,} · iNaturalist %{customdata[1]:,}<extra></extra>"))
    fig.update_yaxes(autorange="reversed", showgrid=False, tickfont=dict(size=12, color=T["ink"]))
    fig.update_xaxes(showticklabels=False, showgrid=False, range=[0, sub["Registros"].max() * 1.18])
    fig.update_layout(height=34 * n + 30, margin=dict(l=8, r=8, t=4, b=4), bargap=0.3)
    return fig


def mapa_puntos(esp: str, estrategia: str | None):
    """Presencias y, opcionalmente, las pseudoausencias de una estrategia."""
    fig = go.Figure()
    _capa_relieve(fig)
    _contorno_m(fig, esp)
    if estrategia:
        d = D.dataset(esp)
        ps = d[d["estrategia_pseudo"] == estrategia]
        fig.add_trace(go.Scatter(x=ps["decimalLongitude"], y=ps["decimalLatitude"], mode="markers",
                                 marker=dict(size=7, color="rgba(0,0,0,0)", line=dict(color=T["accent"], width=1.8), symbol="circle"),
                                 hovertemplate=f"Pseudoausencia ({C.ESTRATEGIAS[estrategia].lower()})<br>Lat %{{y:.2f}}° · Lon %{{x:.2f}}°<extra></extra>",
                                 showlegend=False))
    _presencias(fig, esp, size=9)
    _ejes_geo(fig, D.extension(D.area_m(esp), 0.6))
    fig.update_layout(height=520, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
    return fig


def distribuciones(esp: str, estrategia: str = "buffer"):
    d = D.dataset(esp)
    d = d[d["estrategia_pseudo"].isin(["presencia_real", estrategia])]
    vars_ = D.variables_de(esp)
    fig = make_subplots(rows=len(vars_), cols=1, vertical_spacing=0.2 / max(len(vars_), 1) + 0.04,
                        subplot_titles=[f"{C.VARIABLES[v][0]} ({C.VARIABLES[v][1]})" for v in vars_])
    rng = np.random.default_rng(3)
    for i, v in enumerate(vars_, start=1):
        for clase, y0, color, nombre in [(1, 1.0, T["ink"], "Presencias"), (0, 0.0, T["accent"], "Pseudoausencias")]:
            s = d[d["presencia"] == clase][v]
            fig.add_trace(go.Box(x=s, y=[y0] * len(s), orientation="h", boxpoints=False, fillcolor="rgba(0,0,0,0)",
                                 line=dict(color=T["baseline"], width=1.5), width=0.55, showlegend=False, hoverinfo="skip"), row=i, col=1)
            fig.add_trace(go.Scatter(x=s, y=y0 + rng.uniform(-0.17, 0.17, len(s)), mode="markers",
                                     marker=dict(size=7, color=color if clase else "rgba(0,0,0,0)",
                                                 line=dict(color=T["bg"] if clase else color, width=1.4 if clase else 1.6)),
                                     name=nombre, showlegend=False,
                                     hovertemplate=f"{nombre}: %{{x:,.1f}} {C.VARIABLES[v][1]}<extra></extra>"), row=i, col=1)
        fig.update_yaxes(row=i, col=1, tickvals=[0, 1], ticktext=["Pseudoaus.", "Presencias"], range=[-0.55, 1.55],
                         showgrid=False, tickfont=dict(size=11, color=T["muted"]))
        fig.update_xaxes(row=i, col=1, showgrid=True, gridcolor=T["grid"], tickformat=",")
    for a in fig.layout.annotations:
        a.update(font=dict(size=13, color=T["ink"]), x=0, xanchor="left")
    fig.update_layout(height=150 * len(vars_) + 30, margin=dict(l=8, r=8, t=28, b=8), separators=". ")
    return fig


def importancia(esp: str):
    t = D.tabla("23_importancia_variables")
    sub = t[t["Especie"] == C.ESPECIES[esp]["nombre"]].sort_values("Caída media de AUC-ROC")
    modelo = sub["Modelo"].iloc[0]
    etiquetas = [C.VARIABLES[v][0] for v in sub["Variable"]]
    fig = go.Figure(go.Bar(
        x=sub["Caída media de AUC-ROC"], y=etiquetas, orientation="h",
        marker=dict(color=C.COLOR_MODELO[modelo], cornerradius=4), width=0.5,
        error_x=dict(type="data", array=sub["Desv. est."], color=T["muted"], thickness=1.2, width=4),
        hovertemplate="%{y}<br>Caída media de AUC-ROC %{x:.3f}<extra></extra>"))
    fig.update_xaxes(title="Cuánto baja el AUC-ROC al desordenar la variable", showgrid=True, gridcolor=T["grid"], zeroline=True,
                     zerolinecolor=T["baseline"])
    fig.update_yaxes(showgrid=False, tickfont=dict(size=12, color=T["ink"]))
    fig.update_layout(height=60 * len(sub) + 70, margin=dict(l=8, r=8, t=8, b=8))
    return fig, modelo


METRICAS = {"auc_roc": "AUC-ROC", "auc_pr": "AUC-PR", "tss_opt": "TSS"}


def pliegues(metrica: str, estrategia: str):
    r = D.resultados_pliegue()
    r = r[(r.validacion == "espacial") & (r.estrategia == estrategia)]
    esps = list(C.ESPECIES)
    fig = make_subplots(rows=1, cols=3, shared_yaxes=True, horizontal_spacing=0.04,
                        subplot_titles=[C.ESPECIES[e]["comun"] for e in esps])
    rng = np.random.default_rng(11)
    for j, e in enumerate(esps, start=1):
        for k, m in enumerate(C.MODELOS):
            s = r[(r.especie == e) & (r.modelo == m)][metrica]
            fig.add_trace(go.Scatter(x=k + rng.uniform(-0.12, 0.12, len(s)), y=s, mode="markers",
                                     marker=dict(size=8, color=C.COLOR_MODELO[m], opacity=0.55, line=dict(color=T["bg"], width=1.2)),
                                     name=C.NOMBRE_MODELO[m], legendgroup=m, showlegend=False,
                                     hovertemplate=f"{C.NOMBRE_MODELO[m]} · pliegue<br>{METRICAS[metrica]} %{{y:.2f}}<extra></extra>"),
                          row=1, col=j)
            fig.add_trace(go.Scatter(x=[k - 0.26, k + 0.26], y=[s.mean()] * 2, mode="lines", line=dict(color=C.COLOR_MODELO[m], width=3),
                                     showlegend=(j == 1), name=C.NOMBRE_MODELO[m], legendgroup=m,
                                     hovertemplate=f"{C.NOMBRE_MODELO[m]} · media<br>{METRICAS[metrica]} {s.mean():.3f}<extra></extra>"),
                          row=1, col=j)
        fig.update_xaxes(row=1, col=j, tickvals=list(range(4)), ticktext=[C.NOMBRE_MODELO[m].replace(" ", "<br>") for m in C.MODELOS],
                         range=[-0.6, 3.6], showgrid=False, tickangle=0, tickfont=dict(size=11, color=T["muted"]))
    lo = -0.4 if metrica == "tss_opt" else 0.0
    fig.update_yaxes(range=[lo, 1.05], gridcolor=T["grid"])
    azar = 0 if metrica == "tss_opt" else 0.5
    for j in range(1, 4):
        fig.add_hline(y=azar, line=dict(color=T["muted"], width=1, dash="dot"), row=1, col=j)
    fig.add_annotation(xref="x domain", yref="y", x=1, y=azar, text="azar", showarrow=False, xanchor="right", yanchor="bottom",
                       font=dict(size=11, color=T["muted"]))
    for a in fig.layout.annotations:
        if a.text in [C.ESPECIES[e]["comun"] for e in esps]:
            a.update(font=dict(size=13, color=T["ink"]))
    fig.update_layout(height=420, margin=dict(l=8, r=8, t=56, b=8), legend=dict(y=1.2))
    return fig


def inflacion(metrica: str = "auc_roc"):
    t = D.tabla("15_aleatoria_vs_espacial")
    col_a, col_e = f"{metrica}_aleatorio", f"{metrica}_espacial"
    esps = list(C.ESPECIES)
    fig = make_subplots(rows=1, cols=3, shared_yaxes=True, horizontal_spacing=0.05,
                        subplot_titles=[C.ESPECIES[e]["comun"] for e in esps])
    for j, e in enumerate(esps, start=1):
        sub = t[t.especie == e].set_index("modelo").reindex(C.MODELOS)
        for k, m in enumerate(C.MODELOS):
            a, s = sub.loc[m, col_a], sub.loc[m, col_e]
            fig.add_trace(go.Scatter(x=[a, s], y=[k, k], mode="lines", line=dict(color=T["baseline"], width=3),
                                     hoverinfo="skip", showlegend=False), row=1, col=j)
            fig.add_trace(go.Scatter(x=[a], y=[k], mode="markers", marker=dict(size=11, color=T["bg"], line=dict(color=T["ink"], width=2)),
                                     name="Validación aleatoria", legendgroup="a", showlegend=(j == 1 and k == 0),
                                     hovertemplate=f"{C.NOMBRE_MODELO[m]}<br>Aleatoria {a:.3f}<extra></extra>"), row=1, col=j)
            fig.add_trace(go.Scatter(x=[s], y=[k], mode="markers", marker=dict(size=11, color=C.COLOR_MODELO[m], line=dict(color=T["bg"], width=2)),
                                     name="Validación espacial", legendgroup="e", showlegend=(j == 1 and k == 0),
                                     hovertemplate=f"{C.NOMBRE_MODELO[m]}<br>Espacial {s:.3f}<br>Diferencia {a - s:+.3f}<extra></extra>"),
                          row=1, col=j)
        fig.update_xaxes(row=1, col=j, range=[0.55 if metrica == "auc_roc" else 0.1, 1.0], gridcolor=T["grid"])
    fig.update_yaxes(tickvals=list(range(4)), ticktext=[C.NOMBRE_MODELO[m] for m in C.MODELOS], showgrid=False,
                     tickfont=dict(size=12, color=T["ink"]), range=[-0.6, 3.6])
    for a in fig.layout.annotations:
        a.update(font=dict(size=13, color=T["ink"]))
    fig.update_layout(height=300, margin=dict(l=8, r=8, t=56, b=8), legend=dict(y=1.28))
    return fig


def ranking_global():
    t = D.tabla("17_mejor_modelo")
    cols = {m: f"Puesto promedio {m}" for m in C.MODELOS}
    medias = pd.Series({m: t[c].mean() for m, c in cols.items()}).sort_values()
    fig = go.Figure(go.Bar(
        x=medias.values, y=[C.NOMBRE_MODELO[m] for m in medias.index], orientation="h",
        marker=dict(color=[C.COLOR_MODELO[m] for m in medias.index], cornerradius=4), width=0.52,
        text=[f"{v:.2f}" for v in medias.values], textposition="outside", cliponaxis=False,
        textfont=dict(color=T["ink"], size=13),
        hovertemplate="%{y}<br>Puesto promedio %{x:.2f}<extra></extra>"))
    fig.update_yaxes(autorange="reversed", showgrid=False, tickfont=dict(size=13, color=T["ink"]))
    fig.update_xaxes(range=[0, 4.6], dtick=1, gridcolor=T["grid"], title="Puesto promedio (1 = mejor)")
    fig.update_layout(height=250, margin=dict(l=8, r=8, t=8, b=8))
    return fig, medias


def sensibilidad(estrategia: str):
    s = D.sensibilidad()
    if s.empty:
        return None
    t = D.tabla("19_sensibilidad_resumen")
    esps = list(C.ESPECIES)
    fig = make_subplots(rows=1, cols=3, shared_yaxes=True, horizontal_spacing=0.04,
                        subplot_titles=[C.ESPECIES[e]["comun"] for e in esps])
    for j, e in enumerate(esps, start=1):
        for k, m in enumerate(C.MODELOS):
            v = s[(s.especie == e) & (s.estrategia == estrategia) & (s.modelo == m)]["auc_roc"]
            fig.add_trace(go.Box(y=v, x=[k] * len(v), name=C.NOMBRE_MODELO[m], marker=dict(color=C.COLOR_MODELO[m], size=3),
                                 line=dict(color=C.COLOR_MODELO[m], width=1.6), fillcolor="rgba(0,0,0,0)", boxpoints="outliers",
                                 width=0.5, showlegend=False, hovertemplate=f"{C.NOMBRE_MODELO[m]}<br>AUC-ROC %{{y:.3f}}<extra></extra>"),
                          row=1, col=j)
            ini = t[(t.especie == e) & (t.estrategia == estrategia) & (t.modelo == m)]["config_inicial"]
            if len(ini):
                fig.add_trace(go.Scatter(x=[k], y=[float(ini.iloc[0])], mode="markers",
                                         marker=dict(symbol="diamond", size=11, color=T["ink"], line=dict(color=T["bg"], width=1.5)),
                                         name="Configuración inicial (Tabla 5)", legendgroup="ini", showlegend=(j == 1 and k == 0),
                                         hovertemplate=f"{C.NOMBRE_MODELO[m]} · configuración inicial<br>AUC-ROC {float(ini.iloc[0]):.3f}<extra></extra>"),
                              row=1, col=j)
        fig.update_xaxes(row=1, col=j, tickvals=list(range(4)), ticktext=[C.NOMBRE_MODELO[m].replace(" ", "<br>") for m in C.MODELOS],
                         range=[-0.6, 3.6], showgrid=False, tickangle=0, tickfont=dict(size=11, color=T["muted"]))
    fig.update_yaxes(gridcolor=T["grid"], range=[0, 1.04], title_text="AUC-ROC espacial", row=1, col=1)
    for a in fig.layout.annotations:
        a.update(font=dict(size=13, color=T["ink"]))
    fig.update_layout(height=400, margin=dict(l=8, r=8, t=56, b=8), legend=dict(y=1.22))
    return fig


def areas_modelos(esp: str, umbrales: dict[str, float]):
    filas = []
    for m in C.MODELOS:
        r = D.resumen_umbral(esp, m, umbrales[m])
        filas.append((m, r["pct_m"], r["pct_peru"]))
    df = pd.DataFrame(filas, columns=["modelo", "pct_m", "pct_peru"])
    fig = go.Figure(go.Bar(
        x=df["pct_m"], y=[C.NOMBRE_MODELO[m] for m in df["modelo"]], orientation="h",
        marker=dict(color=[C.COLOR_MODELO[m] for m in df["modelo"]], cornerradius=4), width=0.5,
        text=[f"{v:.1f} %" for v in df["pct_m"]], textposition="outside", cliponaxis=False, textfont=dict(color=T["ink"], size=12),
        hovertemplate="%{y}<br>%{x:.1f} % del área M es idónea<extra></extra>"))
    fig.update_yaxes(autorange="reversed", showgrid=False, tickfont=dict(size=12, color=T["ink"]))
    fig.update_xaxes(range=[0, max(5, df["pct_m"].max() * 1.3)], ticksuffix=" %", gridcolor=T["grid"])
    fig.update_layout(height=210, margin=dict(l=8, r=8, t=8, b=8))
    return fig
