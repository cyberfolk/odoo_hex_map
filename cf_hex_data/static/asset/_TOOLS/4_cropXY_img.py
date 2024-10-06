from PIL import Image


def cropXY(input_path, output_path, cropX_px=15, cropY_px=13):
    image = Image.open(input_path)  # Carica l'immagine
    width, hight = image.size  # Ottieni le dimensioni originali
    # Definisci i bordi per il ritaglio
    left = cropX_px
    top = cropY_px
    right = width - cropX_px
    bottom = hight - cropY_px
    ritagliata = image.crop((left, top, right, bottom))  # Ritaglia l'immagine
    ritagliata.save(output_path)  # Salva l'immagine ritagliata


cropXY('/path1/file_input.png', '/path2/file_output.png', cropX_px=15, cropY_px=13)
# cropXY('bendsharp.png',  'bendsharp.png',  cropX_px=15, cropY_px=13)
# cropXY('bendslight.png', 'bendslight.png', cropX_px=15, cropY_px=13)
# cropXY('cross1.png',     'cross1.png',     cropX_px=15, cropY_px=13)
# cropXY('cross2.png',     'cross2.png',     cropX_px=15, cropY_px=13)
# cropXY('cross3.png',     'cross3.png',     cropX_px=15, cropY_px=13)
# cropXY('end.png',        'end.png',        cropX_px=15, cropY_px=13)
# cropXY('fiveway.png',    'fiveway.png',    cropX_px=15, cropY_px=13)
# cropXY('sixway.png',     'sixway.png',     cropX_px=15, cropY_px=13)
# cropXY('straight.png',   'straight.png',   cropX_px=15, cropY_px=13)
# cropXY('triple1.png',    'triple1.png',    cropX_px=15, cropY_px=13)
# cropXY('triple2.png',    'triple2.png',    cropX_px=15, cropY_px=13)
# cropXY('triple3.png',    'triple3.png',    cropX_px=15, cropY_px=13)
# cropXY('triple4.png',    'triple4.png',    cropX_px=15, cropY_px=13)
