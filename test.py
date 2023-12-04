from datamatrixRecognizer import DatamatrixRecognizer
from segment import Segment
import time

def recognize(path, x, y):
    recognizer = DatamatrixRecognizer(path, Segment(x, y))
    return recognizer.magick()


documents1 = [
    '01.png',
    '02.png',
    '03.png',
    '04.png',
    '05.png',
]

documents2 = [
    '06.png',
    '07.png',
    '08.png',
    '09.png',
    '10.png',
    '11.png',
    '12.png',
    '13.png',
    '14.png',
    '15.png',
    '16.png',
]
start_time = time.time()

for document in documents1:
    start_doc_time = time.time()
    text = recognize('images/' + document, 2, 6)
    end_doc_time = time.time()
    execution_doc_time = end_doc_time - start_doc_time
    rounded_time = round(execution_doc_time * 1000) / 1000

    print(document + " " + str(rounded_time) + "s " + text)

for document in documents2:
    start_doc_time = time.time()
    text = recognize('images/' + document, 1, 6)
    end_doc_time = time.time()
    execution_doc_time = end_doc_time - start_doc_time
    rounded_time = round(execution_doc_time * 1000) / 1000

    print(document + " " + str(rounded_time) + "s " + text)

end_time = time.time()
execution_time = end_time - start_time

print(f"Время выполнения скрипта: {execution_time} секунд")
