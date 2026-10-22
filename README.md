# Actividad 05 · Tres codificaciones del cromosoma en un algoritmo genético para secuenciar la actualización de un catálogo público de trámites

| | |
|---|---|
| **Alumno** | Víctor Manuel Santos Martínez — matrícula 253220020 |
| **Materia** | Algoritmos Evolutivos — Maestría en Inteligencia Artificial |
| **Docente** | Dr. Jaime Aguilar Ortiz |
| **Actividad** | Actividad 05 — Comparación de tres formas de realizar la codificación de los cromosomas |
| **Modalidad** | Individual |
| **Periodo** | Septiembre–diciembre de 2026 · Corte 2 |
| **Institución** | Universidad Politécnica Metropolitana de Hidalgo |

## Descripción de la actividad

> Desarrollar una aplicación industrial con suposiciones "realistas" y datos sintéticos, si es necesario, de algoritmo genético aplicando y comparando tres formas de realizar la codificación de los cromosomas del inicio.

El problema es **en qué orden regulariza una mesa de homologación las fichas vencidas** del Registro Único de Trámites y Servicios de Hidalgo (RUTS). Los datos son reales: 481 fichas publicadas que al 12 de agosto de 2026 habían excedido su periodo de actualización, tomadas de la versión pública del catálogo entregada por la Plataforma Nacional de Transparencia (folio 130213100101626). Cada ficha tiene horas de revisión, un plazo y un peso por consultas; cambiar de dependencia cuesta un alistamiento; la ficha guía de cada dependencia y la de referencia de cada grupo de homónimas van primero. Se minimiza la duración del plan más 0.7 veces la tardanza ponderada: una máquina con alistamientos y precedencias, como en el artículo modelo del curso.

Se comparan **tres codificaciones del mismo plan**, cada una con sus operadores nativos; las otras cuatro etapas, el presupuesto, la reparación y los planes iniciales son idénticos.

| Etapa | Permutación directa | Enteros de Lehmer | Claves reales |
|---|---|---|---|
| 1. Inicialización | M01 sobre permutaciones, emparejada | los mismos planes, codificados | los mismos planes, como claves |
| 2. Evaluación | M05 sobre el plan reparado | igual | igual |
| 3. Selección | M12 torneo, `k = 3` | igual | igual |
| 4. Recombinación | **OX**, cruce por orden | **M14** uniforme | **M14** uniforme |
| 5. Mutación | **intercambio** | **M18** reinicio de un dígito | **M19** gaussiana en una clave |
| 6. Reemplazo | M22 elitista, `e = 2` | igual | igual |
| 7. Paro | M26, 11 950 evaluaciones | igual | igual |

## Resultados

Cuatro instancias de evaluación (13, 17, 87 y 155 fichas del Poder Ejecutivo), treinta semillas emparejadas, 360 corridas; óptimo certificado por programación dinámica hasta 17 fichas y mejor costo conocido en las grandes; búsqueda aleatoria con el mismo presupuesto y cuatro reglas constructivas como líneas base.

| Instancia | Referencia | Permutación (brecha mediana) | Lehmer | Claves | Búsqueda aleatoria | Mejor regla |
|---|---|--:|--:|--:|--:|--:|
| I13 | óptimo certificado | 0.00 % (27/30 aciertos) | 0.00 % (25/30) | 0.00 % (28/30) | 1.3 % | 2.7 % |
| A17 | óptimo certificado | 0.00 % (30/30) | 0.36 % (5/30) | 0.00 % (28/30) | 1.5 % | 0.0 % |
| G87 | mejor conocido | 5.49 % | 6.32 % | **4.04 %** | 26.2 % | 3.8 % |
| E155 | mejor conocido | 13.63 % | 16.86 % | **9.54 %** | 40.1 % | 5.2 % |

- **Las claves reales ganan y la diferencia crece con el tamaño.** Ranking global sobre 120 bloques: claves 1.48, permutación 1.98, Lehmer 2.54 (Friedman χ² = 96.0, p < 10⁻²⁰; Wilcoxon-Holm separa a las tres). La regla fijada de antemano elige las claves reales.
- **El mecanismo es la localidad.** Una mutación de clave mueve el plan reparado entre 5 y 50 veces menos que un intercambio o un dígito de Lehmer, y M14 sobre claves hereda prioridades de fichas; un dígito de Lehmer heredado cambia de significado, y su cruce es el que peor hereda.
- **La representación no actúa sola.** Con inicio aleatorio ninguna codificación alcanza a la regla de peso sobre tiempo en G87 ni en E155. Con el inicio híbrido del artículo modelo (35 % heurístico) las tres la superan, la permutación y las claves empatan a 1.2 % en E155 y la permutación gana en G87.
- **Sesgo de reparación.** De las 40 320 permutaciones de T08, el 92 % se repara; el reparador concentra hasta 48 propuestas en un plan y una sola en otro, y en esta familia favorece a los planes que agrupan dependencias.
- **Para la mesa.** El plan genético del Poder Ejecutivo cuesta 18 % menos que atender primero lo más vencido y 3.8 % menos que la mejor regla.

## Contenido del repositorio

| Ruta | Contenido |
|---|---|
| `Actividad_05_Secuenciacion_RUTS.ipynb` | Cuadernillo autocontenido y ejecutado: datos e instancias, modelo, tres codificaciones, reparación, referencia exacta, líneas base, siete etapas, dieciséis pruebas, sesgo, localidad, calibración, experimentos, estadística, figuras y lectura de resultados |
| `datos/preparar_datos.py` | Genera `fichas_vencidas.csv` a partir de la versión pública del RUTS (no incluida): filtra las fichas publicadas y vencidas y deriva horas, plazos y pesos |
| `datos/fichas_vencidas.csv` | Las 481 fichas vencidas con columnas estructurales del catálogo; ningún dato de personas |
| `resultados/instancias.csv`, `lineas_base.csv` | Instancias, óptimos certificados, planes factibles y reglas constructivas |
| `resultados/sesgo_t08.csv` | Preimágenes de los 3 360 planes factibles de T08 |
| `resultados/localidad_neutralidad.csv` | Neutralidad, localidad y herencia de los operadores por instancia |
| `resultados/calibracion.csv`, `calibracion_elegidos.csv` | 150 corridas de calibración en B23 y parámetros elegidos |
| `resultados/corridas.csv`, `historiales.csv` | 360 corridas de evaluación y su trayectoria por generación |
| `resultados/corridas_hibrido.csv`, `historiales_hibrido.csv` | 180 corridas con inicio híbrido en G87 y E155 |
| `resultados/busqueda_aleatoria.csv`, `historial_busqueda_aleatoria.csv` | 120 búsquedas aleatorias con presupuesto idéntico |
| `resultados/resumen.csv`, `pruebas_estadisticas.csv`, `ranking_global.csv`, `resumen_hibrido.csv` | Agregados, Friedman, Wilcoxon-Holm y ranking |
| `resultados/mecanismo_medianas.csv` | Reparación, fenotipos distintos y diversidad por generación |
| `resultados/caso_principal_*.csv`, `caso_i13_detalle.csv` | Planes del caso principal (E155) y de I13 |
| `resultados/manifiesto.json` | Versiones, configuración, semillas, referencias y huellas SHA-256 |
| `figuras/` | Nueve figuras PNG generadas desde los datos de la ejecución |

## Reproducir

Desde esta carpeta, con el entorno conda `science`:

```bash
conda run -n science jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=3600 Actividad_05_Secuenciacion_RUTS.ipynb
```

El cuadernillo no importa módulos `.py` propios y no descarga nada; sólo lee `datos/fichas_vencidas.csv`. La primera celda falla si el kernel no pertenece al entorno `science`. Las dieciséis pruebas se ejecutan antes de cualquier experimento, y el cuadernillo se detiene si una falla.

Entorno comprobado: Python 3.11.16, NumPy 2.4.6, pandas 3.0.6, SciPy 1.17.1 y Matplotlib 3.11.2, en macOS arm64. La ejecución completa tarda unos dos minutos y medio. Dos ejecuciones dan archivos idénticos salvo en las columnas de tiempo.

Para regenerar el CSV de datos hace falta la carpeta de salida de la respuesta PNT (`01_catalogo_tramites.csv` y `04b_consultas_mensuales.csv`):

```bash
python -I datos/preparar_datos.py <carpeta_salida_pnt>
```

## Alcance y límites

- **Los datos son reales; las suposiciones, declaradas.** Horas por ficha, tolerancia de 60 días, una hora diaria de mesa, pesos por cuartil de consultas, alistamiento de una hora y las dos reglas de precedencia son supuestos de trabajo, no mediciones.
- **Sin datos de personas.** El CSV conserva sólo columnas estructurales del catálogo (identificadores, nombres de trámites, dependencias, fechas, conteos de consultas).
- **Los óptimos certificados valen hasta 17 fichas.** En G87 y E155 las brechas se miden contra el mejor costo conocido y son cotas superiores.
- **El algoritmo con inicio aleatorio no alcanza a una regla de prioridad en el tamaño real** con el presupuesto fijado; con inicio híbrido sí la supera.

## Referencias principales

Bean (1994) para las claves aleatorias; Davis (1985) para OX; Vepsalainen y Morton (1987) para la regla ATC; Held y Karp (1962) para la programación dinámica sobre subconjuntos; Rothlauf (2006) para localidad y redundancia de representaciones; Demšar (2006) y Holm (1979) para las comparaciones estadísticas. La lista completa está en el informe.
