# Zaka Engineering redesign

## Design decisions

UI/UX Pro Max was used for the initial design-system search, typography selection, accessibility guidance, and a second UX review. The chosen direction is an architectural editorial website: generous spacing, large type, restrained material colours, photographic spaces, and precise dividers. UI Styling guided responsive implementation.

- Navy `#091d35` and brick red `#851c1d` are sampled from the original company logo.
- Warm white `#faf9f6`, stone `#efede7`, and muted slate support the original palette.
- Manrope headings and DM Sans body text are loaded through `next/font`.
- Georgia italic provides a restrained editorial accent.
- Keyboard focus, reduced motion, labelled form fields, native image dialogs, and mobile navigation are included.
- Every completed project uses the original website photographs. Generated scenes are labelled as concepts.

## Content coverage

The migration archive contains 47 page captures representing 46 unique pages. Nine completed projects and six live services are represented in the primary navigation and detail pages. All original extracted text is also accessible through `/source-content`, including template material. Original HTML, text, media provenance, and broken-link records live in `content/source`. Older URLs are served by the legacy route and marked `noindex`.

Some original project copy conflicts with its project metadata (the portable-office body uses a different client name, and several office descriptions reuse call-center or hotel copy). Those texts are preserved for client review rather than silently inventing corrections. Unverified demo staff, testimonials, and pricing remain in the archive.

The downloads section provides five original five-page concept catalogues, inspired by the six supplied PDFs. Each includes a cover visualization, a newly drawn schematic plan, exterior elevations, and an outline material schedule. The compact home includes a second residential layout. Plans are nominal and not to scale; supplied certification stamps and pricing are not carried into the new designs.

## Reproduction

- `scripts/crawl_source.py` captures source pages and media.
- `scripts/repair_asset_collisions.py` preserves files whose names collide across upload directories.
- `scripts/prepare_content.py` generates typed-use JSON records and the migration report.
- `scripts/read_references.py` extracts reference text and renders all pages.
- `scripts/create_catalogues.py` generates PDFs, website copies, previews, and QA images using ReportLab and PyMuPDF.
- PDF builder dependencies: `reportlab`, `pillow`, `pymupdf`.
- Crawl dependencies: `requests`, `beautifulsoup4`.

The browser screenshots and validation notes are in `output/playwright`. The PDF source outputs and manifest are in `output/pdf`; downloadable website copies are in `public/downloads`.
