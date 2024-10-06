from PIL import Image


def remove_color(image_path, output_path, color_to_remove):
    img = Image.open(image_path).convert("RGBA")  # Apri l'immagine
    data = img.getdata()

    new_data = []
    for item in data:
        # Confronta il colore (R, G, B) e se è quello che vuoi rimuovere, metti alfa a 0
        if item[:3] == color_to_remove:
            new_data.append((255, 255, 255, 0))  # Trasparente
        else:
            new_data.append(item)
    img.putdata(new_data)  # Aggiorna i dati dell'immagine
    img.save(output_path, "PNG")  # Salva l'immagine


color_to_remove = (34, 177, 76)  # Colore da rimuovere (Verde paint)


remove_color('/path1/file_input.png', '/path2/file_output.png', color_to_remove)
# remove_color('bendsharp.png',  'bendsharp.png', color_to_remove)
# remove_color('bendslight.png', 'bendslight.png', color_to_remove)
# remove_color('cross1.png',     'cross1.png', color_to_remove)
# remove_color('cross2.png',     'cross2.png', color_to_remove)
# remove_color('cross3.png',     'cross3.png', color_to_remove)
# remove_color('end.png',        'end.png', color_to_remove)
# remove_color('fiveway.png',    'fiveway.png', color_to_remove)
# remove_color('sixway.png',     'sixway.png', color_to_remove)
# remove_color('straight.png',   'straight.png', color_to_remove)
# remove_color('triple1.png',    'triple1.png', color_to_remove)
# remove_color('triple2.png',    'triple2.png', color_to_remove)
# remove_color('triple3.png',    'triple3.png', color_to_remove)
# remove_color('triple4.png',    'triple4.png', color_to_remove)
