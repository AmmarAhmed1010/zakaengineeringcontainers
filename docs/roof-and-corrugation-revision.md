# Roof and corrugation revision: all 30 catalogues

Every catalogue uses deep vertical shipping-container-style corrugated steel,
corner posts and perimeter rails, following the three supplied appearance references.
Realistic four-view sheets were edited with the built-in image generation tool.
The final photographic assets are high-quality, unresized JPEGs in
`public/images/catalogues/roof-revision`; full prompts are in
`roof-revision-prompts.json`. Original generated PNGs remain in the local generated
image store. Website cover previews are in `public/images/pdf/roof-revision`.

## Roof rules

- All 12 ft units have flat container-style roofs with level top rails.
- The existing 8 ft and 10 ft cabins also use flat container roofs.
- The 16 ft garden cottage has a single-slope metal roof.
- The 24 ft bistro and two-bedroom home have A-shaped gable roofs.
- The 24 ft meeting office and family home use single-slope roofs. For the family
  home a canopy spans the upper container and open-sided terrace; enclosed upper
  floor area stays unchanged.
- The 24 ft courtyard home uses single-slope roofs over its occupied U-shaped
  wings. The courtyard stays open to the sky.

The two formerly named Gabled Studio and Gabled Office are now Compact Container
Studio and Compact Container Office. Their PDF filenames follow the new titles;
both old readable filenames and old branded filenames redirect to the new files.

## Preserving the approved plans

`scripts/refresh_roof_catalogues.py` replaces exactly four pages per catalogue:
the cover, two exterior pages and the individual specification page. All other
decoded page-content streams are checked against their pre-revision SHA-256 hashes.
This preserves the latest entrances, kitchens, bathroom access, bed positions,
opening schedules, room schedules, material standards and contact pages. It also
preserves the 30 catalogue count and 359 total page count.

The transparent Zaka header and watermark remain in every PDF. Website copies
match canonical PDFs, previews and metadata use new revision paths, and roof types
are shown on catalogue cards. Final file hashes and preserved-page evidence are
in `output/pdf/roof-revision-audit.json`.

## Rebuild

`scripts/roof_style_revisions.json` is the canonical appearance specification.
The original, client and new-catalogue builders share `roof_styles.py` so future
builds retain the material and roof rules. Run this last for the complete registry:

```powershell
python scripts/refresh_roof_catalogues.py
node scripts/check_catalogues.mjs
```

Use the bundled Python runtime and add `tmp/python-deps` to PYTHONPATH for the
original catalogue imports. `prepare_roof_styles.py` initializes the specification
from the catalogue inventory; editing the JSON directly preserves explicit choices.
`import_roof_assets.mjs` exports the selected generated images using the temporary
file list in ignored `tmp/roof-generation-files.json`.
