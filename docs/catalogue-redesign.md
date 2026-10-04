# Catalogue redesign - revision 02

17 existing PDF URLs rebuilt with individual exterior designs and measured plans. All 17 now appear on the downloads page: nine offices and eight living designs. Six landscape A4 pages each; the three duplexes and roof-deck cabin have a seventh page for the additional plan. GRID AND LOGIC remains on every page and preview.

| Design | Footprint (ft) | Storeys | Bedrooms | Enclosed area (sq ft) |
| --- | --- | --- | --- | --- |
| Cedar One Bedroom Cabin | 12 x 30 | 1 | 1 | 360 |
| Sage Terrace Studio | 12 x 21 | 1 | 0 | 252 |
| Two Bedroom Family Home | 12 x 40 | 1 | 2 | 480 |
| Three Bedroom Duplex | 12 x 45 | 2 | 3 | 1080 |
| Roof Terrace Cabin | 12 x 24 | 1 | 1 | 288 |
| Compact Gabled Studio | 12 x 20 | 1 | 0 | 240 |
| Mint Site Office | 8 x 20 | 1 | - | 160 |
| Cedar Executive Office | 10 x 20 | 1 | - | 200 |
| Glazed Team Office | 12 x 20 | 1 | - | 240 |
| Olive Linear Site Hub | 8 x 40 | 1 | - | 320 |
| Two Storey Office Hub | 10 x 40 | 2 | - | 800 |
| Charcoal Loft Office | 12 x 40 | 2 | - | 960 |
| Compact Gabled Office | 8 x 20 | 1 | - | 160 |
| Twin Cabin Office | 8 x 20 | 1 | - | 160 |
| Off Grid Field Office | 8 x 20 | 1 | - | 160 |
| Two Bedroom Garden Cottage | 16 x 40 | 1 | 2 | 640 |
| Three Bedroom Courtyard Home | 24 x 40 | 1 | 3 | 720 |

## Reference review and provenance

Reviewed all 48 client reference images in `public/client-assets` through three contact sheets and selected full-size views. The references include timber cabins, pitched roofs, roof terraces, dark steel, stacked offices and courtyard homes. Each new exterior sheet uses a selected reference as architectural inspiration. Exact prompts and reference paths: `docs/catalogue-redesign-prompts.json`. New assets: `public/images/catalogues/revision-02`. Each catalogue uses a distinct four-view sheet; no sheet is shared between catalogues.

## Plans and assumptions

All dimensions are nominal feet. Room-zone geometry fills each enclosed footprint without overlaps; enclosed area includes all enclosed levels before wall deductions. Bedroom corridors provide independent access. Open studios have no separate bedrooms. The courtyard home has a 24 x 40 ft bounding footprint, with 720 sq ft enclosed and a 20 x 12 ft open courtyard (240 sq ft). Front bedrooms use courtyard access. Terrace studio: additional 12 x 5 ft terrace; total ground footprint 12 x 26 ft. Roof-deck cabin: one enclosed level plus a 288 sq ft roof terrace. Double-storey and roof-deck designs show a 4 x 16 ft external stair allowance outside the building footprint. The courtyard home requires modules assembled on site.

Furniture, openings, visualizations and stair geometry are schematic. Final clearances, wall thicknesses, structure and services are developed for the selected design and site.

## Rebuild

Run `scripts/create_catalogues.py` with Python containing ReportLab, Pillow, PyMuPDF and pypdf. It delegates to `redesign_catalogues.py` using `catalogue_redesigns.json`. Watermarks are applied before previews are rendered. Generated image assets must already exist. Final PDFs: `output/pdf`; identical website copies: `public/downloads`; previews: `public/images/pdf/revision-02`; review renders: `tmp/pdfs/revision-02`. Manifest records reference names, room geometry, unique image hashes, page counts and website mirror checks.
