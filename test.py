import asyncio
import json

from datamatrixRecognizer import DatamatrixRecognizer


async def main(pdf_path, params):
    recognizer = DatamatrixRecognizer()

    return await recognizer.magick(pdf_path, params)


results = asyncio.run(main("scans/51.pdf", {
    "type": "IDENTICAL",
    "segment": {"x": 1, "y": 6}
}))

print(json.dumps({"results": results}))
