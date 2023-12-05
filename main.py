import os
import select
import sys
import json
import asyncio
from datamatrixRecognizer import DatamatrixRecognizer


async def main():
    path = sys.argv[1]

    if os.name == 'nt':
        j_doc = json.load(sys.stdin)
    else:
        if select.select([sys.stdin], [], [], 0.0)[0]:
            j_doc = json.load(sys.stdin)
        else:
            raise Exception('Pipe is empty.')

    recognizer = DatamatrixRecognizer()
    return await recognizer.magick(path, j_doc)


results = asyncio.run(main())

print(json.dumps({"results": results}))
