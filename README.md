# Zaka Engineering Containers

The redesigned Zaka Engineering website, built with Next.js 16, React 19, TypeScript, Tailwind CSS 4, and ESLint.

## Requirements

- Node.js 20.9 or newer
- npm

## Getting started

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). Edit `src/app/page.tsx` to update the home page. Routes, layouts, and styles live under `src/app`.

## Available commands

- `npm run dev` — start the development server.
- `npm run lint` — check the project with ESLint.
- `npm run typecheck` — generate route types and check TypeScript.
- `npm run build` — create an optimized production build.
- `npm run start` — serve the production build locally.

## Learn more

- [Next.js documentation](https://nextjs.org/docs)
- [Learn Next.js](https://nextjs.org/learn)
- [Deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying)

## Website structure

- Home, About Us, Services, Projects, Contact Us, and Downloads.
- Six individual service pages and nine original project galleries.
- Seventeen individual 11- or 12-page PDF catalogues: nine offices and eight living designs, including single and double storeys, studios, one to four bedrooms, a terrace studio and a courtyard home. Each includes measured floor plans, four exterior renders, individual specifications, the full client material schedule and project notes.
- All 46 unique original pages retained in the source-content archive.
- Older source URLs are preserved through the legacy route and excluded from indexing.
- Contact enquiries produce a WhatsApp draft for the visitor to review and send.

Edit `src/data/site.ts` for company details, services, and document metadata. Project records are in `src/data/projects.json`. Main visual styles live in `src/app/globals.css`.

The original website HTML, text, and media index are in `content/source`. See `content/migration-report.json` for original broken links, unreachable assets, and source-copy inconsistencies. The sitemap audit confirms no published sitemap pages were missed.

Generated concept assets are in `public/images/generated`. See `docs/generated-image-prompts.md` for the exact prompts and `docs/design-direction.md` for design decisions and regeneration steps. Original reference PDFs are treated as visual references and are not redistributed by the site.

PDF outputs are in `output/pdf`, website downloads are in `public/downloads`, and the editable PDF builder is `scripts/create_catalogues.py`. The PDF generation script requires Python with ReportLab, Pillow, PyMuPDF and pypdf. Current corrections, client interpretations and measurement assumptions are documented in `docs/catalogue-revision-03.md`.


## Client catalogue revision 04

Four additional client catalogues, their photorealistic exterior assets, and the editable builder are organized in this repository. See [the revision 04 file guide](docs/catalogue-revision-04.md).
