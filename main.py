import sys

from datamatrixRecognizer import DatamatrixRecognizer
from segment import Segment

path = sys.argv[1]
x = int(sys.argv[2])
y = int(sys.argv[3])

recognizer = DatamatrixRecognizer(path, Segment(x, y))

result = recognizer.magick()

print(result)
