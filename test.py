from datamatrixRecognizer import DatamatrixRecognizer
from segment import Segment


def recognize(path, x, y):
    recognizer = DatamatrixRecognizer(path, Segment(x, y))
    print(recognizer.magick())


documents1 = [
    '1.png',
    '2.png',
    '3.png',
    '4.png',
    '5.png',
]

documents2 = [
    '20231129135703-1.png',
    '20231129135703-2.png',
    '20231129135703-3.png',
    '20231129135703-4.png',
    '20231129135703-5.png',
    '20231129135703-6.png',
    '20231129135703-7.png',
    'img_1.png',
    'img_2.png',
    'img_3.png',
    'img_4.png',
]

for document in documents1:
    recognize('images/' + document, 2, 6)

for document in documents2:
    recognize('images/' + document, 1, 6)
