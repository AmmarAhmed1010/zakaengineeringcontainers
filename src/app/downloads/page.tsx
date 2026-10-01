import type { Metadata } from "next";
import Link from "next/link";
import Image from "next/image";
import { documents } from "@/data/site";
import { PageIntro } from "@/components/ui";
import { DownloadIcon, ArrowUpRight } from "@/components/icons";
import { ProjectCTA } from "@/components/footer";
export const metadata: Metadata = {
  title: "Design Catalogues",
  description:
    "Download 12 container concept catalogues with floor plans measured in feet, four finished exterior views, and specification schedules.",
};
export default function Downloads() {
  return (
    <main id="main-content">
      <PageIntro
        eyebrow="The design collection"
        title="Ideas worth building on."
        text="Twelve spaces. Countless possibilities. Explore studios, portable residences, and offices with measured floor plans and four exterior views."
      />
      <div className="container">
        <div className="document-note">
          <strong>Designed to start a conversation.</strong>
          <p>
            These catalogues contain illustrative layouts and concept visuals.
            Final dimensions, specifications, and pricing are agreed for your
            project before fabrication.
          </p>
        </div>
        <section className="downloads-grid">
          {documents.map((d, index) => (
            <article className="download-card" key={d.slug}>
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
                  loading={index < 3 ? "eager" : "lazy"}
                />
              </Link>
              <p className="eyebrow">
                {d.code} / {d.category} collection
              </p>
              <h3>{d.title}</h3>
              <p className="document-size">{d.subtitle}</p>
              <p>{d.description}</p>
              <div className="download-actions">
                <Link href={`/downloads/${d.slug}`}>
                  Preview catalogue
                  <ArrowUpRight width={17} />
                </Link>
                <a href={d.file} download>
                  PDF / {d.pages} pages
                  <DownloadIcon width={17} />
                </a>
              </div>
            </article>
          ))}
        </section>
      </div>
      <ProjectCTA />
    </main>
  );
}
