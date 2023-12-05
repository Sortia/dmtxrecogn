import asyncio
import json

from datamatrixRecognizer import DatamatrixRecognizer


async def main(pdf_path, params):
    recognizer = DatamatrixRecognizer()

    return await recognizer.magick(pdf_path, params)


results = asyncio.run(main("images/1.pdf", {
    "type": "IDENTICAL",
    "segment": {"x": 2, "y": 6}
}))

print(json.dumps({"results": results}))
