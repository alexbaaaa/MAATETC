# Refactor `maatetc_gui.py`

## Objetivo
- Adaptar el módulo al uso web (Flask) eliminando lógica de GUI local.
- Mantener los cálculos físicos y el comportamiento funcional del ETC.
- Conservar la salida de `run_etc` para que `handlerETC.py` siga funcionando.

## Cambios realizados
- Se eliminó código no útil para web:
  - Bloques GUI local (`PySimpleGUI`, `draw_figure`, `gui` y validaciones asociadas).
  - Dependencias e imports no usados en backend web.
  - Escritura de ficheros intermedios `SN_*.txt` y `Texpo_*.txt`.
- Se reorganizó el código en funciones auxiliares más claras:
  - Parseo de opcionales con valores por defecto.
  - Construcción de figura de aviso cuando `refwv` cae fuera de rango.
- Se sustituyó la ruta dependiente de `cwd` por una ruta robusta basada en `__file__`.
- Se redujo uso de variables globales en el flujo principal.
- Se ajustó el layout de matplotlib dentro de `run_etc` para evitar recortes en ejes/texto:
  - `fig.tight_layout(pad=1.2)`.

## Compatibilidad mantenida
- Se mantiene la firma:
  - `run_etc(values, text_elem, image_element)`
- Se mantiene el retorno:
  - `return fig, text_elem`
- `getgrating` sigue disponible para el uso externo actual.

## Cálculo científico
- No se han alterado fórmulas físicas ni constantes del modelo.
- No se han renombrado funciones públicas usadas externamente.

