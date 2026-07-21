
## Sprint 1 - Comprensión del dominio y datos

### Fuentes usadas
- GBIF: ocurrencias con coordenadas, país=PE, año 1980-2024 
- iNaturalist: taxon_id confirmado por especie (place_id correcto = 7513, Perú)
- WorldClim v2.1, resolución 5 arc-min (bio1-bio19), recortado a bbox Andes tropicales peruanos

### Decisiones y hallazgos importantes
- Telmatobius macrostomus: el filtro 1980-2024 deja solo 4 registros GBIF (mayoría de la
  colección es histórica, 1916-1950).
- Recorte de WorldClim para preservar el valor NoData (se perdía al escribir
  el raster recortado con rasterio, causando errores de visualización).
