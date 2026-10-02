"""Apply an editable GRID AND LOGIC preview watermark to all published PDFs.

The 17 source files in output/pdf are edited in place, and the corresponding
website download copies are synchronised to match them. Re-running is safe:
documents that already contain the watermark are not stamped twice.
"""
from __future__ import annotations

from io import BytesIO
import json
import os
from pathlib import Path
import shutil

import pymupdf
from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/pdf"
DOWNLOADS = ROOT / "public/downloads"
QA = ROOT / "tmp/pdfs/watermark-review"
QA.mkdir(parents=True, exist_ok=True)
LABEL = "GRID AND LOGIC"


def make_overlay(width: float, height: float) -> PdfReader:
    buffer = BytesIO()
    layer = canvas.Canvas(buffer, pagesize=(width, height), pageCompression=1)
    layer.saveState()
    layer.setFillColor(HexColor("#851c1d"))
    layer.setFillAlpha(0.24)
    layer.setFont("Helvetica-Bold", 46)
    layer.translate(width / 2, height / 2)
    layer.rotate(34)
    layer.drawCentredString(0, 0, LABEL)
    layer.restoreState()
    layer.save()
    buffer.seek(0)
    return PdfReader(buffer)


def add_watermark(source: Path, destination: Path) -> dict:
    reader = PdfReader(source, strict=False)
    if not reader.pages:
        raise ValueError(f"PDF has no pages: {source.name}")
    already_stamped = all(LABEL in (page.extract_text() or "") for page in reader.pages)
    if not already_stamped:
        writer = PdfWriter(clone_from=reader)
        for page in writer.pages:
            box = page.mediabox
            overlay = make_overlay(float(box.width), float(box.height))
            page.merge_page(overlay.pages[0], over=True)
        temporary = QA / (source.name + ".tmp")
        with temporary.open("wb") as stream:
            writer.write(stream)
        os.replace(temporary, destination)
    else:
        destination = source

    public_copy = DOWNLOADS / source.name
    if destination.resolve() != public_copy.resolve():
        shutil.copy2(destination, public_copy)

    checked = PdfReader(destination, strict=False)
    missing = [i + 1 for i, page in enumerate(checked.pages) if LABEL not in (page.extract_text() or "")]
    if missing:
        raise RuntimeError(f"Watermark missing from {source.name}, pages {missing}")
    return {
        "file": source.name,
        "pages": len(checked.pages),
        "watermark": LABEL,
        "bytes": destination.stat().st_size,
        "websiteCopyMatches": destination.read_bytes() == public_copy.read_bytes(),
    }


def main() -> None:
    sources = sorted(OUTPUT.glob("zaka-*.pdf"))
    if len(sources) != 17:
        raise RuntimeError(f"Expected 17 catalogues; found {len(sources)}")
    results = [add_watermark(path, path) for path in sources]

    # Render a current six-page catalogue and one legacy reference design to
    # review watermark size, opacity, and readability across both formats.
    review_names = ["zaka-office-8x20.pdf", "zaka-single-cabin-office.pdf"]
    for name in review_names:
        doc = pymupdf.open(OUTPUT / name)
        pix = doc[1].get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5), alpha=False)
        pix.save(QA / (Path(name).stem + "-page-2.png"))
        pix = doc[0].get_pixmap(matrix=pymupdf.Matrix(1.2, 1.2), alpha=False)
        pix.save(QA / (Path(name).stem + "-page-1.png"))

    (OUTPUT / "watermark-manifest.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    print(f"Watermarked {len(results)} PDFs / {sum(x['pages'] for x in results)} pages.")
    print(f"All website copies match: {all(x['websiteCopyMatches'] for x in results)}")


if __name__ == "__main__":
    main()
