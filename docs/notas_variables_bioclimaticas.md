
## Selección de variables bioclimáticas (Sprint 2)

Se utilizó reducción por correlación de pares (umbral |r| > 0.8) en vez de VIF puro,
debido a que el enfoque VIF (basado en regresión OLS) producía valores infinitos o
matrices singulares dado el bajo número de observaciones (22-40 registros) frente a
19 variables candidatas -- un problema común y documentado en SDM con datos escasos.

Variables finales por especie:
- Xenoglaux_loweryi: ['bio_2', 'bio_3', 'bio_4', 'bio_13', 'bio_15']
- Cinclodes_palliatus: ['bio_2', 'bio_3', 'bio_4', 'bio_5', 'bio_15', 'bio_18']
- Telmatobius_macrostomus: ['bio_4', 'bio_5', 'bio_7', 'bio_9', 'bio_18']
