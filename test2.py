import asyncio
import json

from datamatrixRecognizer import DatamatrixRecognizer


async def main(pdf_path, params):
    recognizer = DatamatrixRecognizer()

    return await recognizer.magick(pdf_path, params)


imgs = [
    "scans/06.png",
    "scans/07.png",
    "scans/08.png",
    "scans/09.png",
    "scans/10.png",
    "scans/11.png",
    "scans/12.png",
    "scans/13.png",
    "scans/14.png",
    "scans/15.png",
    "scans/16.png",

    "scans/21.jpg",
    "scans/22.jpg",
    "scans/23.jpg",
    "scans/24.jpg",

    "scans/31.jpg",
    "scans/32.jpg",
    "scans/33.jpg",
    "scans/34.jpg",

    "scans/41.jpg",
]

for img in imgs:
    results = asyncio.run(main(img, {
        "type": "IDENTICAL",
        "segment": {"x": 1, "y": 6}
    }))

    print(img + ": " + json.dumps({"results": results}))

