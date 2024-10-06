from PIL import Image

border_green_path = "border-green.png"  # Accidentalmente eliminato, è e da rifare


def add_border_green(input_path, output_path):
    border_green = Image.open(border_green_path)
    bend_sharp = Image.open(input_path)
    border_green = border_green.resize(bend_sharp.size)  # Resize border_green per avere la stessa dim di bend_sharp
    combined_image = bend_sharp.copy()  # Sovrapponi border_green su bend_sharp con trasparenza
    combined_image.paste(border_green, (0, 0), border_green)
    combined_image.save(output_path)


add_border_green('/path1/file_input.png', '/path2/file_output.png')
# add_border_green('bendsharp.png',  'bendsharp.png')
# add_border_green('bendslight.png', 'bendslight.png')
# add_border_green('cross1.png',     'cross1.png')
# add_border_green('cross2.png',     'cross2.png')
# add_border_green('cross3.png',     'cross3.png')
# add_border_green('end.png',        'end.png')
# add_border_green('fiveway.png',    'fiveway.png')
# add_border_green('sixway.png',     'sixway.png')
# add_border_green('straight.png',   'straight.png')
# add_border_green('triple1.png',    'triple1.png')
# add_border_green('triple2.png',    'triple2.png')
# add_border_green('triple3.png',    'triple3.png')
# add_border_green('triple4.png',    'triple4.png')
