
## Cierre Sprint 3 - Modelado y comparación de algoritmos

### Modelos evaluados
Random Forest, SVM, LightGBM, MaxEnt (vía elapid), con validación cruzada
estratificada k=5 (apropiado para el tamaño de muestra chico, 22-40 registros
por especie).

### Estrategias de pseudoausencia probadas
- Aleatoria: background sobre toda el área de estudio
- Buffer: anillo alrededor de las presencias (radio adaptado por especie)
- Ambiental: puntos más distintos climáticamente a las presencias

### Hallazgo clave: la estrategia "ambiental" no es válida para comparar modelos
Genera una tarea de clasificación trivialmente separable (AUC cercano a 1.0 en
casi todos los modelos), ya que selecciona por construcción los casos más
extremos posibles. Se documenta como hallazgo metodológico pero se excluye
del ranking comparativo de modelos.

### Corrección aplicada: LightGBM con datasets pequeños
Los hiperparámetros por defecto (min_child_samples=20) impedían cualquier split
del árbol con ~35 muestras de entrenamiento por fold, resultando en AUC=0.5
(predicción constante). Se ajustaron min_child_samples/min_data_in_leaf=3 y
num_leaves=7 para permitir árboles simples pero funcionales.

### Resultado principal (estrategias válidas: aleatoria + buffer)
Random Forest fue el modelo más consistente, quedando primero o empatado en
primer lugar en las 3 especies bajo ambas estrategias. SVM fue el segundo más
consistente. LightGBM y MaxEnt tuvieron desempeño más variable, con menor
rendimiento relativo en general en esta escala de datos.

La estrategia "buffer" produjo sistemáticamente AUC más bajos que "aleatoria"
en las 3 especies -- consistente con ser una prueba más exigente y realista
(pseudoausencias más cercanas geográficamente a las presencias reales).

### Limitación estadística
Con solo 3 especies como unidades de comparación, el test de Friedman no
alcanza significancia estadística formal (p > 0.05) -- limitación esperada
del tamaño de muestra a nivel de especies, no de los registros por especie.
