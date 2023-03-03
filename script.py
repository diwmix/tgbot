import os
import json
from pathlib import Path

result = list()
stickers_dir = Path('cards')
stickers = os.listdir(stickers_dir)

for sticker in stickers:
  result.append({'sticker_path': str(stickers_dir / sticker), 'sticker_text': ''})

with open('result.json', 'w') as file:
  json.dump(result, file, indent=2)