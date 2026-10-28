# Thirty design catalogues

The website lists 30 distinct downloadable PDFs: 12 workspaces, 13 living designs,
three hospitality spaces and two portable spaces. Both `output/pdf` and
`public/downloads` contain exactly 30 PDFs, with identical copies. Descriptive
filenames omit the `zaka` and `client` prefixes. The old 21 download URLs redirect
to their renamed files through `next.config.ts`.

## Nine additions

| Design | External footprint | Programme |
| --- | --- | --- |
| Courtyard Cafe | 12 x 40 ft | 12 x 16 kitchen; 12 x 24 seating/reception; indoor serving hatch; centred front entry |
| Cedar Bistro | 24 x 40 ft | Joined-module restaurant; kitchen, 24-seat dining, reception and customer washroom |
| Charcoal Takeaway | 12 x 20 ft | Serving hatch, kitchen, dry store and staff washroom |
| Slate Team Office | 12 x 32 ft | Reception, team desks, executive room, kitchen and washroom |
| Ivory Meeting Office | 24 x 32 ft | Meeting room, reception, team office, executive/lounge and services |
| Silver One Bedroom Home | 12 x 32 ft | Bedroom, service bay, kitchen, washroom and living/dining |
| Charcoal Two Bedroom Home | 24 x 32 ft | Two bedroom suites with ensuites, living/dining and open kitchen |
| Ivory Portable Clinic | 12 x 40 ft | Consultation, reception/waiting, treatment, kitchen and washroom |
| Grey Learning Studio | 12 x 40 ft | Twelve-seat classroom, storage, kitchen and washroom |

Each addition has 13 pages: cover, measured plan, room schedule, opening schedule,
four exterior perspectives across two pages, programme/specification, five complete
material-standard pages and a project contact page. Transparent Zaka branding is
retained. Photorealistic concepts were created with the built-in image generation
tool; source assets are in `public/images/generated/collection-30` and the complete
prompts are in `collection-30-image-prompts.json`. Measured plans control openings;
exterior concepts illustrate material and atmosphere.

The four previously unlisted revised catalogues are now on the website, with their
existing floor plans and bed/window corrections preserved.

## Rebuild

Use the bundled Python runtime with reportlab, pypdf, Pillow and pypdfium2:

```powershell
python scripts/expand_catalogues.py
```

This regenerates the nine additions, refreshes previews for the four revised
designs, validates the complete 30-entry registry and synchronizes download copies.
Run this command last if rebuilding the original catalogues with
`create_catalogues.py` or `create_client_pdfs.py`. The shared `catalogue_names.py`
resolver keeps existing generators on the readable filenames. The one-time
`prepare_collection_names.py` migration is idempotent after renaming.

Final manifests contain page counts, sizes and SHA-256 hashes. Beds in the new
homes retain the shared solid-headboard and minimum 2.5 ft access checks. Rendered
review pages are kept in ignored `tmp/pdfs/collection-30`.
