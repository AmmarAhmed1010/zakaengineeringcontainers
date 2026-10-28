"""Stable, readable catalogue filenames shared by every PDF builder."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPING = json.loads((ROOT/'src/data/catalogue-filenames.json').read_text(encoding='utf-8'))

def filename(name):
    return MAPPING.get(name, name)

def original_filename(slug):
    return filename('zaka-' + slug + '.pdf')
