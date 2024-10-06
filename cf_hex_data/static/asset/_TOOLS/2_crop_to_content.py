"""NB! Per funzionare deve stare all'interno della cartella roads."""
from PIL import Image


def crop_to_content(large_image_path, output_image_path, background_color=(0, 0, 0, 0)):
    """ Rimuove il bordo in eccesso dall'immagine più grande, mantenendo solo il contenuto. """
    large_image = Image.open(large_image_path)
    large_image = large_image.convert("RGBA")  # Converti l'immagine in formato RGBA per gestire la trasparenza
    bbox = large_image.getbbox()  # Trova il box dei pixel non trasparenti o diversi dal colore di sfondo
    if bbox:  # Se viene trovato un bounding box, ritaglia l'immagine
        cropped_image = large_image.crop(bbox)
    else:
        cropped_image = large_image  # Nessun bordo rilevato, non ritagliare
    cropped_image.save(output_image_path)  # Salva l'immagine di output


crop_to_content('/path1/file_input.png', '/path2/file_output.png')
# crop_to_content('bendsharp.png',  'bendsharp.png')
# crop_to_content('bendslight.png', 'bendslight.png')
# crop_to_content('cross1.png',     'cross1.png')
# crop_to_content('cross2.png',     'cross2.png')
# crop_to_content('cross3.png',     'cross3.png')
# crop_to_content('end.png',        'end.png')
# crop_to_content('fiveway.png',    'fiveway.png')
# crop_to_content('sixway.png',     'sixway.png')
# crop_to_content('straight.png',   'straight.png')
# crop_to_content('triple1.png',    'triple1.png')
# crop_to_content('triple2.png',    'triple2.png')
# crop_to_content('triple3.png',    'triple3.png')
# crop_to_content('triple4.png',    'triple4.png')
