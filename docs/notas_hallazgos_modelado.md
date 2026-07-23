
## Hallazgo Sprint 3: limitaciones de la estrategia "ambiental" para comparación de modelos

La estrategia de pseudoausencia "ambiental" selecciona los puntos con mayor distancia
en el espacio de variables respecto a las presencias. Esto genera una tarea de
clasificación trivialmente separable (AUC cercano a 1.0 en casi todos los modelos),
ya que por construcción los pseudoausencias son los casos más extremos posibles.
Por lo tanto, esta estrategia NO se utiliza para el ranking comparativo de modelos
(Sprint 4), solo se documenta como hallazgo metodológico. La comparación formal se
basa en las estrategias "aleatoria" y "buffer", que representan un desafío de
clasificación más realista.

## Corrección: LightGBM con datos pequeños
Se ajustaron los hiperparámetros min_child_samples/min_data_in_leaf de LightGBM
(default=20) a valores menores (3), ya que con datasets de 22-40 registros el
valor por defecto impedía cualquier split del árbol, resultando en AUC=0.5
(predicción constante) para Xenoglaux loweryi en todas las estrategias.
