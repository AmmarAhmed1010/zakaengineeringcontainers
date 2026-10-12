# Client corrections - revision 03 / 12 October 2026

The two supplied material documents are byte-identical. Their full content is preserved in `content/specifications/client-standard-materials.txt`. Every catalogue now includes all 20 numbered sections plus Quality & Customization across five additional pages. The website also shows the complete schedule in expandable sections. Final product thicknesses, grades, brands and inclusion remain subject to the approved quotation, as stated by the client.

## Markup interpretation

The user confirmed the client's instructions are unclear and authorised implementation judgement. For the 12 x 45 ft duplex, the user selected following the marked bedrooms on both floors. The resulting concept has two bedrooms at opposite ends on each floor, four total, with a central kitchen and washroom on each floor. Wet areas are vertically aligned. Original enclosed area remains 1,080 sq ft.

The two 12 x 24 ft hand sketches are interpreted together as a compact duplex: one bedroom downstairs, with a wardrobe alcove, a recessed 4 x 6 ft washroom and an open living/kitchen zone; two bedrooms upstairs with a central 4 x 6 ft washroom and 4 x 6 ft kitchen/entry. The former roof-terrace catalogue now contains two enclosed floors (576 sq ft), with newly generated exterior views. This interpretation satisfies the request for kitchen and washroom on both levels and one bedroom on the lower level. It remains a concept for client review.

| Marked catalogue | Implemented correction |
| --- | --- |
| 12 x 30 ft cedar cabin | Removed crossed-out 3 ft corridor; bedroom is now full-width 12 x 12 ft, entered from the living room. |
| 12 x 21 ft terrace studio | Main entrance moved to the right short end through the additional 12 x 5 ft terrace. Old front entrance removed from plan and exterior. |
| 12 x 40 ft family home | Full-width 10 x 12 ft bedrooms at opposite ends; central open living area with washroom and kitchen; removed corridor. |
| 12 x 45 ft duplex | Two full-width bedrooms per floor, central living/kitchen/washroom on both floors, right-end external stairs. |
| 12 x 24 ft compact duplex | Applied both hand sketches, one bedroom below and two above, services on each floor and right-end stairs. |
| 16 x 40 ft garden cottage | Bedrooms placed at opposite ends with central living/kitchen/washroom; corridor removed. |
| Courtyard home | Retained the existing unmarked courtyard arrangement. |

Right-end stairs use a nominal 4 x 16 ft allowance outside the building footprint. A 3 ft deep upper front access balcony connects the stair landing to the shared entrance, also outside the enclosed area. Final stair geometry, structural design, wall thicknesses and clearances are developed for the approved project. Dimensions shown are nominal feet; L-shaped areas explicitly state deducted service recesses. New exterior renders remain illustrative rather than fabrication elevations.

## Reproduction and assets

Run `scripts/create_catalogues.py`. Explicit revised geometry and openings: `scripts/client_plan_revisions.json`. Renderer: `scripts/client_floor_plans.py`. Material pagination and full-text source parser: `scripts/client_materials.py`. Unmarked configurations remain in `scripts/catalogue_redesigns.json`.

Three new four-view image sheets are in `public/images/catalogues/revision-03`, with exact prompts in `docs/catalogue-revision-03-prompts.json`. Other individual exterior sheets remain from revision 02. All cover previews are regenerated into `public/images/pdf/revision-03` after watermarking. PDF URLs retain their filenames and website links use a revision query to refresh cached downloads. PDFs contain 11 or 12 pages (191 total). All 17 PDFs retain GRID AND LOGIC on every page and are mirrored byte-for-byte to `public/downloads`.
