MAP_CR_EXP = {
    "0.0": 0,
    "0": 0,
    "0.125": 25,
    "0.25": 50,
    "0.5": 100,
    "1.0": 200,
    "2.0": 450,
    "3.0": 700,
    "4.0": 1100,
    "5.0": 1800,
    "6.0": 2300,
    "7.0": 2900,
    "8.0": 3900,
    "9.0": 5000,
    "10.0": 5900,
    "11.0": 7500,
    "12.0": 8400,
    "13.0": 10000,
    "14.0": 11500,
    "15.0": 13000,
    "16.0": 15000,
    "17.0": 18000,
    "18.0": 20000,
    "19.0": 22000,
    "20.0": 25000,
    "21.0": 33000,
    "22.0": 41000,
    "23.0": 50000,
    "24.0": 62000,
    "25.0": 75000,
    "26.0": 90000,
    "27.0": 105000,
    "28.0": 120000,
    "29.0": 135000,
    "30.0": 155000,
}

MAP_QTY_MOD = {
    "0": 0,
    "1": 1,
    "2": 1.5,
    "3": 2,
    "4": 2,
    "5": 2,
    "6": 2,
    "7": 2.5,
    "8": 2.5,
    "9": 2.5,
    "10": 2.5,
    "11": 3,
    "12": 3,
    "13": 3,
    "14": 3,
    "15": 4,
    "16": 4,
    "17": 4,
    "18": 4,
    "19": 4,
    "20": 4,
}

# Dizionario che collega "1 PG di liv " all'exp che avrebbe con 1 Scontro
# "Easy", "Medium", "Hard", "Deadly" e il "Daily Budget" ovvero l'exp massima che potrebbe accumulare in una giornata
# "livello_PG": ("Easy", "Medium", "Hard", "Deadly", "Daily Budget")
MAP_LEVEL_EXP = {
    "0": (0, 0, 0, 0, 0),
    "1": (25, 50, 75, 100, 300),
    "2": (50, 100, 150, 200, 600),
    "3": (75, 150, 225, 400, 1200),
    "4": (125, 250, 375, 500, 1700),
    "5": (250, 500, 750, 1100, 3500),
    "6": (300, 600, 900, 1400, 4000),
    "7": (350, 750, 1100, 1700, 5000),
    "8": (450, 900, 1400, 2100, 6000),
    "9": (550, 1100, 1600, 2400, 7500),
    "10": (600, 1200, 1900, 2800, 9000),
    "11": (800, 1600, 2400, 3600, 10500),
    "12": (1000, 2000, 3000, 4500, 11500),
    "13": (1100, 2200, 3400, 5100, 13500),
    "14": (1250, 2500, 3800, 5700, 15000),
    "15": (1400, 2800, 4300, 6400, 18000),
    "16": (1600, 3200, 4800, 7200, 20000),
    "17": (2000, 3900, 5900, 8800, 25000),
    "18": (2100, 4200, 6300, 9500, 27000),
    "19": (2400, 4900, 7300, 10900, 30000),
    "20": (2800, 5700, 8500, 12700, 40000),
}

# Dizionario per creare degli scontri a SML X con solo creature di CR Y
# Nella tupla sono riportate la quantity di creature di quel CR per ottenere quel SML
# "SML": ("q_cr0125", "q_cr025", "q_cr05", "q_cr1", "q_cr2", "q_cr3", "q_cr4, "q_cr5", "q_cr6", "q_cr7", "q_cr8")
LIST_CR = [0.125, 0.25, 0.5, 1, 2, 3, 4, 5, 6, 7, 8]
MAP_SML_QTY = {
    "3": (16, 11, 7, 4, None, None, None, 1, None, None, None),
    "4": (20, 14, 9, 5, 3, 2, None, None, 1, None, None),
    "5": (45, 22, 14, 9, 5, 3, None, None, None, None, None),
    "6": (56, 28, 15, 10, 6, 4, None, 2, None, None, None),
    "7": (68, 33, 17, 11, None, 5, 3, None, 2, None, None),
    "8": (84, 42, 21, 14, 8, 6, 4, None, None, None, None),
    "9": (96, 48, 24, 15, 9, None, None, 3, None, None, None),
    "10": (120, 56, 28, 15, 10, 7, 5, None, None, None, 2),
}
