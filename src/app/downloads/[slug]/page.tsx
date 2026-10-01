import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { documents } from "@/data/site";
import { PageIntro } from "@/components/ui";
import { DownloadIcon, ArrowUpRight } from "@/components/icons";
export function generateStaticParams() {
  return documents.map((d) => ({ slug: d.slug }));
}
export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const d = documents.find((d) => d.slug === slug);
  return { title: d?.title, description: d?.description };
}
export default async function Document({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const d = documents.find((d) => d.slug === slug);
  if (!d) notFound();
  return (
    <main id="main-content">
      <PageIntro
        eyebrow={`${d.code} / ${d.category} collection`}
        title={d.title}
        text={d.description}
      />
      <div className="container">
        <div className="document-toolbar">
          <span className="download-meta">
            <span>{d.subtitle}</span>
            <span className="muted">PDF / {d.pages} pages</span>
          </span>
          <a href={d.file} download className="button button-red">
            Download catalogue
            <DownloadIcon />
          </a>
        </div>
        <iframe
          src={`${d.file}#view=FitH`}
          className="pdf-viewer"
          title={`${d.title} PDF catalogue`}
        />
        <p className="small muted">
          If the preview is unavailable on your device,{" "}
          <a
            className="text-link"
            href={d.file}
            target="_blank"
            rel="noopener noreferrer"
          >
            open the PDF directly
            <ArrowUpRight width={14} />
          </a>{" "}
          or use the download button above.
        </p>
        <div className="document-description">
          <p>
            Illustrative concept, prepared for client discussion. Plans are not
            to scale and are not fabrication or permit drawings. Please contact
            our team for a project-specific design and quotation.
          </p>
          <div className="project-next">
            <Link href="/downloads" className="text-link">
              All catalogues
              <ArrowUpRight />
            </Link>
            <Link href="/contact-us" className="text-link">
              Make this space yours
              <ArrowUpRight />
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}
