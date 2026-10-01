# Validation record

- `npm run lint`: passed.
- `npm run typecheck`: passed.
- `npm run build`: passed; 110 generated routes.
- Source sitemap audit: every listed page captured; 46 unique pages.
- HTTP audit: 175 page/image requests succeeded; all five PDF responses succeeded with application/pdf MIME and valid signatures.
- PDFs: five files, five pages each; all page text bounds inside the page. All 25 rendered pages visually reviewed.
- Responsive browser checks: home, about, services, projects, downloads, contact, one service detail, one project detail, and one PDF preview checked at 375, 768, 1024, and 1440 pixels. No horizontal overflow; one main h1 per page.
- Mobile navigation: opens, selects destination, closes after selection.
- Project filtering: Hospitality selects two expected projects.
- Gallery: opens photograph, advances with ArrowRight, closes with Escape.
- Enquiry form: valid data creates the correct encoded WhatsApp draft. No message sent during validation.
- PDF preview: correct iframe URL and direct download link.
- Home: all 12 image elements loaded with no broken images after scrolling.

Evidence: output/playwright/http-audit.json, content/source/sitemap-audit.json, output/pdf/catalogue-manifest.json, and browser screenshots in output/playwright.
