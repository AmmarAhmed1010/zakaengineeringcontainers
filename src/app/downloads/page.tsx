import type { Metadata } from "next";
import Link from "next/link";
import Image from "next/image";
import { documents } from "@/data/site";
import materialSpecifications from "@/data/material-specifications.json";
import { PageIntro } from "@/components/ui";
import { DownloadIcon, ArrowUpRight } from "@/components/icons";
import { ProjectCTA } from "@/components/footer";
export const metadata: Metadata = {
  title: "Design Catalogues",
  description:
    "Explore 30 office, home, cafe, restaurant and portable-space designs with measured floor plans, opening schedules, four exterior views and material specifications.",
};
const collections = [
  {
    id: "offices",
    title: "Offices",
    label: "Office catalogues",
    category: "Workspace",
    description:
      "Site cabins, executive suites, meeting spaces and two-storey office hubs. Compare measured layouts, sizes and finishes.",
  },
  {
    id: "studios",
    title: "Studios & portable living",
    label: "Studio & living catalogues",
    category: "Living",
    description:
      "Open studios, one- and two-bedroom homes, family duplexes, terrace living and a courtyard home. Detailed plans include furniture, kitchens and washrooms.",
  },
  {
    id: "hospitality",
    title: "Cafes & restaurants",
    label: "Cafe & restaurant catalogues",
    category: "Hospitality",
    description:
      "A 12 x 40 ft cafe with a dedicated kitchen and indoor serving hatch, a joined-module restaurant and a compact takeaway kitchen.",
  },
  {
    id: "portable",
    title: "Portable spaces",
    label: "Portable-space catalogues",
    category: "Portable",
    description:
      "A portable clinic and learning studio, with service rooms, furniture, door swings and window sizes shown in each catalogue.",
  },
];

function layoutSummary(d: (typeof documents)[number]) {
  if (d.storeys !== 2) return "Single storey";
  if (d.slug === "portable-12x24")
    return "Double storey · Ground-floor kitchen · First-floor entrance lobby";
  if (d.slug === "family-home-two-floors-40x24")
    return "Double storey · Ground-floor kitchen · Upper terrace";
  return "Double storey · Kitchen + washroom on both floors";
}

export default function Downloads() {
  return (
    <main id="main-content">
      <PageIntro
        eyebrow="The design collection"
        title="Ideas worth building on."
        text="Explore 30 designs by use, size and layout. Every catalogue includes floor plans measured in feet, four exterior concept views and material specifications."
      />
      <div className="container">
        <nav
          className="catalogue-collections"
          aria-label="Choose a catalogue collection"
        >
          {collections.map((collection) => (
            <a href={`#${collection.id}`} key={collection.id}>
              <div>
                <span className="eyebrow">Browse by space</span>
                <strong>{collection.label}</strong>
                <span className="catalogue-collection-count">
                  {
                    documents.filter((d) => d.category === collection.category)
                      .length
                  }{" "}
                  PDFs / Floor plans in feet
                </span>
              </div>
              <ArrowUpRight width={24} />
            </a>
          ))}
        </nav>
        <div className="document-note">
          <strong>Designed to start a conversation.</strong>
          <p>
            These catalogues contain illustrative layouts and concept visuals.
            Final dimensions, specifications, and pricing are agreed for your
            project before fabrication.
          </p>
        </div>
        {collections.map((collection, collectionIndex) => {
          const items = documents.filter(
            (d) => d.category === collection.category,
          );
          return (
            <section
              id={collection.id}
              className="catalogue-section"
              aria-labelledby={`${collection.id}-heading`}
              key={collection.id}
            >
              <div className="catalogue-section-heading">
                <div>
                  <p className="eyebrow">
                    {items.length} downloadable catalogues
                  </p>
                  <h2 id={`${collection.id}-heading`}>{collection.title}</h2>
                  <p className="muted">{collection.description}</p>
                </div>
                <a href="#main-content" className="text-link">
                  Back to collections <ArrowUpRight width={16} />
                </a>
              </div>
              <nav
                className="catalogue-sizes"
                aria-label={`${collection.title} sizes`}
              >
                <span>Choose your size</span>
                {items.map((d) => (
                  <a href={`#catalogue-${d.slug}`} key={d.slug}>
                    {d.subtitle.split(" / ")[0]} · {d.storeys === 2 ? "2 storeys" : d.category === "Living" ? d.bedrooms ? `${d.bedrooms} bed` : "Studio" : d.title.replace("Office", "").trim()}
                    {d.slug.includes("terrace") ? " + terrace" : ""}
                  </a>
                ))}
              </nav>
              <div className="downloads-grid">
                {items.map((d, index) => (
                  <article
                    className="download-card"
                    id={`catalogue-${d.slug}`}
                    key={d.slug}
                  >
                    <div className="catalogue-card-label">
                      <span
                        className={`catalogue-type ${collection.category === "Living" ? "catalogue-type-living" : ""}`}
                      >
                        {collection.category === "Hospitality"
                          ? "Cafe / restaurant"
                          : collection.category === "Portable"
                            ? "Portable space"
                            : collection.category === "Workspace"
                          ? "Office"
                          : d.bedrooms > 0
                            ? `${d.bedrooms} bedroom${d.bedrooms > 1 ? "s" : ""}`
                            : d.slug.includes("terrace")
                              ? "Studio + terrace"
                              : "Studio"}
                      </span>
                      <span>
                        {d.code} / {d.pages}-page PDF
                      </span>
                    </div>
                    <Link
                      href={`/downloads/${d.slug}`}
                      className="download-cover"
                      aria-label={`Preview ${d.title}`}
                    >
                      <Image
                        src={d.preview}
                        alt={`${d.title} catalogue cover`}
                        width={1094}
                        height={773}
                        sizes="(max-width: 640px) 90vw, (max-width: 900px) 45vw, 30vw"
                        loading={
                          collectionIndex === 0 && index < 3 ? "eager" : "lazy"
                        }
                      />
                    </Link>
                    <h3>{d.title}</h3>
                    <p className="document-size">{d.subtitle}</p>
                    <p className="catalogue-layout-meta">{layoutSummary(d)}{d.slug === "compact-container-home" ? " · Open courtyard" : ""}</p>
                    <p>{d.description}</p>
                    <div className="download-actions">
                      <Link href={`/downloads/${d.slug}`}>
                        Preview catalogue
                        <ArrowUpRight width={17} />
                      </Link>
                      <a
                        href={`${d.file}?revision=${d.revision}`}
                        download
                        aria-label={`Download ${d.title} PDF`}
                      >
                        Download PDF
                        <DownloadIcon width={17} />
                      </a>
                    </div>
                  </article>
                ))}
              </div>
            </section>
          );
        })}
        <section className="catalogue-section" aria-labelledby="materials-heading">
          <div className="catalogue-section-heading">
            <div>
              <p className="eyebrow">Included in every catalogue</p>
              <h2 id="materials-heading">Standard materials & specifications</h2>
              <p className="muted">Zaka’s complete material schedule. Final thickness, gauge, brand, finish and accessories follow the approved quotation and design.</p>
            </div>
          </div>
          <div className="catalogue-materials">
            {materialSpecifications.map((section) => (
              <details key={section.title}>
                <summary>{section.title}</summary>
                <div>{section.lines.map((line, index) => <p key={index}>{line}</p>)}</div>
              </details>
            ))}
          </div>
        </section>
      </div>
      <ProjectCTA />
    </main>
  );
}
