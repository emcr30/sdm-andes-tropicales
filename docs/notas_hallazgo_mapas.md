
## Hallazgo Sprint 4: discrepancia entre metrica de CV y coherencia espacial del mapa

Para Telmatobius macrostomus, aunque RandomForest obtuvo el mejor AUC-ROC en
validacion cruzada (0.903 vs 0.884 de SVM bajo estrategia buffer), su mapa de
prediccion mostro un patron espacialmente disperso e inconsistente: multiples
manchas de alta idoneidad distribuidas en zonas altoandinas distantes de la
laguna de Junin (unico habitat conocido de la especie), en vez de una mancha
unica y concentrada.

Se probo restringir max_depth=3 en RandomForest, sin mejora sustancial
(0.10% vs 0.14% de pixeles con prob>0.8), lo que indica que el problema no
es sobreajuste de arboles individuales sino una limitacion estructural del
metodo: RandomForest evalua umbrales de variables de forma independiente,
por lo que marca como aptas todas las zonas altoandinas que comparten rangos
climaticos similares a Junin, sin capturar la combinacion conjunta especifica
de variables ni la restriccion geografica real de la especie.

SVM, al operar en el espacio de variables completo (distancias), produjo un
mapa mucho mas concentrado y coherente geograficamente, a pesar de un AUC
ligeramente menor en validacion cruzada.

Decision metodologica: se utiliza SVM (no el modelo de mayor AUC) para el
mapa final de distribucion potencial de Telmatobius macrostomus, priorizando
coherencia espacial sobre metrica de CV marginal. Este hallazgo es coherente
con el marco teorico del diagrama BAM (Soberon y Peterson) - los SDM basados
unicamente en variables climaticas (componente A, abiotico) no incorporan el
componente de accesibilidad/dispersion (M), por lo que pueden sobreestimar
habitat climaticamente similar pero geograficamente inalcanzable para
especies con capacidad de dispersion muy limitada.
