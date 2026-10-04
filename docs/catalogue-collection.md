# Client catalogue collection

Historical revision 01 notes. The current 17-design collection is documented in [catalogue-redesign.md](catalogue-redesign.md).

The updated brief lists twelve distinct layouts. All twelve are provided, rather than omitting requested sizes to reach exactly ten files. Each catalogue has six landscape A4 pages: introduction, measured floor plan, front/rear renders, left/right renders, outline specifications, and project/contact notes.

## Living and portable spaces

| Layout | Enclosed area | Additional space |
| --- | --- | --- |
| Studio 12 x 30 ft | 360 sq ft | None |
| Studio 12 x 21 ft | 252 sq ft | 12 x 5 ft terrace, 60 sq ft |
| Residence 12 x 40 ft | 480 sq ft | None |
| Residence 12 x 45 ft | 540 sq ft | None |
| Studio 12 x 24 ft | 288 sq ft | None |
| Studio 12 x 20 ft | 240 sq ft | None |

The terrace is assumed additional: total footprint 12 x 26 ft, total enclosed plus terrace area 312 sq ft. This assumption is written in the PDF and can be revised if the client intended an inclusive terrace.

## Offices

| Width x length | Gross nominal area |
| --- | --- |
| 8 x 20 ft | 160 sq ft |
| 10 x 20 ft | 200 sq ft |
| 12 x 20 ft | 240 sq ft |
| 8 x 40 ft | 320 sq ft |
| 10 x 40 ft | 400 sq ft |
| 12 x 40 ft | 480 sq ft |

Office plans contain a 6 ft long service bay split into a 6 x 4 ft washroom and an entry/pantry zone spanning the remaining width. The rest is an open office with perimeter desks. Residential plans contain a 6 x 12 ft service bay split into a kitchenette and bathroom. The two longer residences have a separate 12 x 12 ft bedroom.

## Provenance and limitations

The six supplied references were used for planning and presentation context. The new floor plans are original, dimensioned schematic concepts. All measurements are in feet and areas are gross nominal zones, before wall thicknesses. Furniture and exterior images are illustrative. Heights, costs, construction approvals and performance ratings are not asserted. A wider unit may require a fabricated or joined-module structure.

The twelve exterior sheets were generated with the built-in image generation tool, with four views on each sheet. Workspace assets: `public/images/catalogues`. Exact prompts: `docs/catalogue-exterior-prompts.json`. The terrace sheet received one edit to place its extension on the correct side of the front view. That edit preserved the other three panels.

Rebuild using `scripts/create_catalogues.py`; it delegates to `create_collection.py` and shares the brand/page styles in `catalogue_style.py`. Inputs are `scripts/catalogue_layouts.json`. The generated website metadata is `src/data/documents.json`. Earlier five-file concept PDFs remain available by their direct download URLs for compatibility but are superseded in the visible collection.
