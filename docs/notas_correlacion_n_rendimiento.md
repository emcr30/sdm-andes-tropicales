
## Análisis de correlación: tamaño de muestra (n) vs rendimiento (Sprint 4)

Se evaluó la relación entre el número de registros de presencia por especie
(22, 30, 40) y el AUC-ROC de cada modelo, bajo las dos estrategias de
pseudoausencia válidas (aleatoria, buffer).

### Estrategia "buffer" (prueba más exigente y comparable entre especies)
Los 4 modelos muestran una tendencia positiva consistente entre n y AUC-ROC
(Pearson r entre 0.78 y 0.82), con una meseta entre n=30 y n=40 - el mayor
incremento de rendimiento ocurre entre 22 y 30 registros. Ningún resultado
alcanza significancia estadística formal (p > 0.05 en todos los casos),
limitación esperada al tener solo 3 especies como unidades de comparación.
La consistencia de la dirección del efecto en los 4 algoritmos, aunque no
sea estadísticamente significativa, es en si misma un indicio relevante de
que el tamaño de muestra afecta el rendimiento predictivo en este contexto.

### Estrategia "aleatoria"
No muestra un patrón monótono claro (cae en n=30, sube en n=40) - se
interpreta como reflejo de que la dificultad de esta estrategia depende
más de la distribución geográfica particular de cada especie que del
tamaño de muestra en si, por lo que se prioriza la lectura de "buffer"
para las conclusiones sobre el efecto de n.

### Limitación
El análisis de correlación con solo 3 especies tiene poder estadístico
insuficiente para pruebas de hipótesis formales, los resultados deben
interpretarse como tendencia descriptiva, no como evidencia estadística
concluyente.
