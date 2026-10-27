# Client catalogue revision 04

Four new catalogue PDFs were prepared from the client sketches, with grey,
charcoal and white finish combinations and individual border treatments.
The client confirmed two ground-floor bedrooms and two upstairs for the family home.
Photorealistic exterior concepts were generated with the built-in image generator.
The dimensioned plans and opening schedules govern the layouts.

| Catalogue | Pages | Output and website download filename |
| --- | --- | --- |
| Family home, two floors and terrace | 13 | zaka-client-01-family-home-two-floors.pdf |
| Two-bedroom residence, 12 x 40 and 12 x 44 ft | 13 | zaka-client-02-two-bedroom-12x40-and-12x44.pdf |
| Office, 12 x 40 and 12 x 44 ft | 13 | zaka-client-03-office-12x40-and-12x44.pdf |
| Studio, 12 x 26 ft including terrace | 12 | zaka-client-04-studio-12x26-with-terrace.pdf |

## File locations

- Final PDFs: `output/pdf/`.
- Copies for static website downloads: `public/downloads/`.
- Four exterior image plates: `public/images/generated/client-revision-04/`.
- Image prompts: `docs/catalogue-revision-04-prompts.md`.
- Editable builder: `scripts/create_client_pdfs.py`.
- Regenerated page previews: `tmp/pdfs/client-revision-04/` (Git ignored; created when the builder runs).

Redundant archives, partial clones, extracted copies and temporary previews were removed after verifying the repository files.

The builder uses the original two-bedroom catalogue in `output/pdf/` as its
material-standard and contact-page reference. Its Python dependencies are
ReportLab, pypdf, pypdfium2 and Pillow. Run it from the repository root with
`python scripts/create_client_pdfs.py` to regenerate the four catalogues.

The website's original catalogue listing is preserved; the four new static
download copies are available by their `/downloads/<filename>` URLs.

## Local client corrections - 27 October 2026

- Family ground floor: L-shaped rear kitchen, adjusted beds and an L-shaped living sofa near the side service wall.
- Family upper floor: both ensuites rotated to 4 ft along the building length by 6 ft along the 12 ft end; cupboards remain 2 ft deep.
- Residence 12 x 40 ft: 12 ft bedroom + 4 ft middle service band with two 4 x 6 ft ensuites + 12 ft bedroom + 12 ft living/open kitchen. The first bedroom uses its separate outside entry shown in the source sketch.
- Residence 12 x 44 ft: ensuites moved to the two outside rear bedroom corners, away from the central living entrances. The central living/open kitchen remains 12 x 16 ft.
- Offices: enclosed kitchen and washroom open onto a 2.5 ft passage entered from reception. The bedroom opens onto that passage as sketched; neither service room has a direct bedroom door. The 12 ft width resolves as 4.5 ft kitchen + 2.5 ft passage + 5 ft washroom, within the existing 6 ft service-bay length.
- Studio: wardrobe moved beside the washroom, 2 ft deep x 6 ft long. Washroom access faces the main studio to avoid the wardrobe.
- Cedar Executive Office 10 x 20 ft: entry/pantry renamed Kitchen; sink and hob shown. Kitchen windows are 3 x 3 ft; workspace windows are 4 x 4 ft on the front, opposite 10 ft end and rear.
- All 21 PDF catalogues use a faint watermark rendered from the website header's `Containers-Prefab.svg`. The old text watermark is removed. `scripts/watermark_catalogues.py` updates the canonical and download copies idempotently.

Source builders and PDFs are versioned together so subsequent client revisions can be reproduced.

The website SVG's white background rectangle was subsequently removed. Transparent header and watermark PNGs are rendered from that vector source with `node scripts/prepare_brand_logo.mjs`; the PDF builders preserve their alpha masks.

## Bed directions and executive glazing

All 28 illustrated beds across the collection are now 5 x 6.5 ft, with their headboards against solid wall segments. Sleeping furniture is centered away from corners, window openings, service fixtures and door swings. The builders check at least 2.5 ft at both long sides and the foot; the per-bed results are saved in `output/pdf/bed-layout-audit.json`.

The family home's ground-floor beds turn onto the inner partitions; upstairs headboards use the solid rear walls. Residence beds use side partitions, with the 40 ft option's wardrobes and rear windows repositioned to keep access clear. The office bedroom uses the solid front wall and an upper-hinged passage door that clears the bed. The terrace studio's rear window moves alongside the bed rather than behind its headboard.

Both 40/44 ft executive-office options now have front and right-end glazing, with the opposite rear window removed. The Cedar Executive Office 10 x 20 ft keeps its front/end glazing and loses its rear workspace window.

Run `python scripts/refresh_bed_layouts.py` with the existing catalogue-builder dependencies to regenerate the affected plans, all four client PDFs, download copies, cache revisions, manifests and visual-review sheets. The shared bed renderer and geometry checks are in `scripts/bed_furniture.py`.
