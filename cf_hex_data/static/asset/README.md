## Utilizzo

1. Se si modificano le immagini o la struttura della cartella `tile`, occorre rilanciare lo
   script `6_get_tiles_dict.py`, per ottenere il file `asset_tile.py` e spostarlo nella cartella `data`

## Tools per correggere gli assets

| Name                                                  | Usato per                                                          |
|-------------------------------------------------------|--------------------------------------------------------------------|
| [1_rotate_img.py](_TOOLS/1_rotate_img.py)             | Ruotare gli esagoni per portarli alla giusta angolazione.          |
| [2_crop_to_content.py](_TOOLS/2_crop_to_content.py)   | Togliere la parte dell'immagine che eccede il bordo dell'esagono.  |
| [3_add_border_green.py](_TOOLS/3_add_border_green.py) | Aggiunge un bordo verde all'esagono.                               |
| [4_cropXY_img.py](_TOOLS/4_cropXY_img.py)             | Ritagliare i bordi dell'img ti tot px pari ai parametri passati.   |
| [5_remove_color.py](_TOOLS/5_remove_color.py)         | Mandare ad Alfa il colore passato come parametro (es bordo verde). |
| [6_get_tiles_dict.py](_TOOLS/6_get_tiles_dict.py)     | Creare asset_tile.py, ovvero il file che mappa la cartella tile    |

## Credits:

Ho preso gli assets da:

- HK - Old Skool Hand Drawn
- foundation_tiles
- HK - Ordinal Simple
- SF-planetside-hexmap
