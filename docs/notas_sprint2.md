
## Sprint 2 - Preparación de datos

### Deduplicación y rarefacción espacial
- Se combinaron registros GBIF + iNaturalist, eliminando duplicados por coordenadas
  casi-exactas (redondeo a 4 decimales, ~11m).
- Hallazgo: en Xenoglaux loweryi, de 919 registros GBIF solo 157 corresponden a
  coordenadas geográficas distintas -- alta repetición de esfuerzo de muestreo en
  pocos sitios conocidos (comportamiento típico de especies raras muy buscadas).
- Umbral de rarefacción adaptado por especie según su rango de distribución conocido
  y la cantidad de datos disponible, no un valor único para las tres:
  - Telmatobius macrostomus: 1 km (especie confinada a una sola laguna, rango
    naturalmente pequeño) -> 40 registros
  - Xenoglaux loweryi: 5 km (umbral de 9km, equivalente a resolución del raster,
    dejaba solo 13 registros, por debajo del mínimo de 20 definido) -> 22 registros
  - Cinclodes palliatus: 15 km -> 30 registros
