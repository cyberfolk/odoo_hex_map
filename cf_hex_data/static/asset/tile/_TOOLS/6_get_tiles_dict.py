"""Script che scansiona ricorsivamente il contenuto della cartella 'tile' per generare il file 'asset_tile.py'.
Questo file contiene un dizionario che mappa ricorsivamente tutte le immagini presenti nella cartella corrente,
includendo i percorsi relativi. Una volta creato, il file deve essere spostato manualmente nella cartella 'data',
dove verrà utilizzato nel 'post_init_hook' per caricare i dati relativi agli asset grafici ('asset_tile').
NB! Per funzionare spostarlo al primo livello dentro la cartella static/asset/tile"""

import os

root_dir = os.getcwd()  # Cartella di partenza: la directory corrente (tile)
image_extensions = {'.png', '.jpg', '.jpeg', '.gif'}  # Estensioni di file immagine da includere
asset_tile_dicts = []  # Lista che conterrà il dizionario delle immagini


# Funzione per cercare immagini in maniera ricorsiva
def process_directory(current_dir):
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            extension = os.path.splitext(file)[1].lower()  # Estrai l'estensione del file
            if extension in image_extensions:
                image_name = os.path.splitext(file)[0]  # Estrai il nome del file senza estensione
                relative_path = os.path.relpath(os.path.join(root, file), root_dir)  # Crea il percorso relativo
                asset_tile_dicts.append({  # Aggiungi il dizionario per ogni immagine
                    'name': image_name,
                    'image_path': 'static/asset/tile/' + relative_path.replace("\\", "/")
                })


process_directory(root_dir)  # Processa la directory di partenza
output_file = os.path.join(root_dir, 'asset_tile.py')  # Nome del file di output Python

# Scrivi il contenuto nel file Python
with open(output_file, 'w') as f:
    f.write("asset_tile_dicts = [\n")
    for item in asset_tile_dicts:
        f.write(f"    {{'name': '{item['name']}', 'image_path': '{item['image_path']}'}},\n")
    f.write("]\n")

print(f"File Python generato: {output_file}")
