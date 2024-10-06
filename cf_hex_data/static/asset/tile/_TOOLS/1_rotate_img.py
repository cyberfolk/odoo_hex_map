from PIL import Image


def ruota_immagine(input_path, output_path, angolo=60):
    with Image.open(input_path) as img:
        img_rotata = img.rotate(angolo, expand=True)  # Expand permette di mantenere tutte le dimensioni dell'immagine
        img_rotata.save(output_path)


ruota_immagine('/path1/file_input.png', '/path2/file_output.png', 30)
# ruota_immagine('bendsharp.png',  'bendsharp.png ', 30)
# ruota_immagine('bendslight.png', 'bendslight.png', 30)
# ruota_immagine('cross1.png',     'cross1.png    ', 30)
# ruota_immagine('cross2.png',     'cross2.png    ', 30)
# ruota_immagine('cross3.png',     'cross3.png    ', 30)
# ruota_immagine('end.png',        'end.png       ', 30)
# ruota_immagine('fiveway.png',    'fiveway.png   ', 30)
# ruota_immagine('sixway.png',     'sixway.png    ', 30)
# ruota_immagine('straight.png',   'straight.png  ', 30)
# ruota_immagine('triple1.png',    'triple1.png   ', 30)
# ruota_immagine('triple2.png',    'triple2.png   ', 30)
# ruota_immagine('triple3.png',    'triple3.png   ', 30)
# ruota_immagine('triple4.png',    'triple4.png   ', 30)
