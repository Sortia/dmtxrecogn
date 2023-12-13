import asyncio
import json

from datamatrixRecognizer import DatamatrixRecognizer


async def main(pdf_path, params):
    recognizer = DatamatrixRecognizer()

    return await recognizer.magick(pdf_path, params)


results = asyncio.run(main("images/03.png", {
    "type": "IDENTICAL",
    "segment": {"x": 2, "y": 6}
}))

print(json.dumps({"results": results}))
