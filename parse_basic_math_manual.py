import pymupdf
import re
import json

doc = pymupdf.open(r"d:\Kunal's Library\PYQs\Mathematics\JEE_PYQs-(JEE-Main-and-Advanced)_11th_JEE-Mains_Maths_Basic Math & Logarithm.pdf")
p1 = doc[0].get_text()
p2 = doc[1].get_text()

# Answers for JEE Main
main_answers = {
    1: {'type': 'single', 'correct': 0, 'opt': 'a'},
    2: {'type': 'single', 'correct': 1, 'opt': 'b'},
    3: {'type': 'numerical', 'correct': 3.0},
    4: {'type': 'single', 'correct': 0, 'opt': 'a'},
    5: {'type': 'numerical', 'correct': 13.0},
    6: {'type': 'numerical', 'correct': 4.0},
    7: {'type': 'single', 'correct': 1, 'opt': 'b'},
    8: {'type': 'single', 'correct': 3, 'opt': 'd'},
    9: {'type': 'single', 'correct': 0, 'opt': 'a'},
    10: {'type': 'numerical', 'correct': 11.0}, # (*) bonus / evaluated
    11: {'type': 'numerical', 'correct': 45.0},
    12: {'type': 'numerical', 'correct': 1.0},
    13: {'type': 'single', 'correct': 1, 'opt': 'b'},
    14: {'type': 'single', 'correct': 1, 'opt': 'b'},
    15: {'type': 'single', 'correct': 2, 'opt': 'c'},
    16: {'type': 'numerical', 'correct': 1.0},
    17: {'type': 'numerical', 'correct': 1.0},
    18: {'type': 'numerical', 'correct': 8.0}
}

# Answers for JEE Advanced
adv_answers = {
    1: {'type': 'single', 'correct': 0, 'opt': 'a'},
    2: {'type': 'single', 'correct': 1, 'opt': 'b'},
    3: {'type': 'single', 'correct': 0, 'opt': 'a'}, # multi-correct, primary A
    4: {'type': 'numerical', 'correct': 8.0},
    5: {'type': 'numerical', 'correct': 4.0},
    6: {'type': 'numerical', 'correct': -1.0}
}

print("Answer keys mapped.")
