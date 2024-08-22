def luminance(r, g, b):
    # Converti valori RGB (0-255) in valori normalizzati (0-1)
    def channel_luminance(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    # Calcola la luminanza relativa
    return 0.2126 * channel_luminance(r) + 0.7152 * channel_luminance(g) + 0.0722 * channel_luminance(b)


def is_text_white(hex_color):
    if not hex_color:
        return False

    # Converti il colore esadecimale in valori RGB
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)

    # Calcola la luminanza
    lum = luminance(r, g, b)

    # Se la luminanza è inferiore a 0.5, suggerisci testo bianco
    return lum < 0.5
