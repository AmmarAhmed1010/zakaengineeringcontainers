import type { Metadata } from "next";
import { notFound } from "next/navigation";
import archive from "@/data/archive.json";
import { PageIntro } from "@/components/ui";
export const metadata: Metadata = { robots: { index: false, follow: false } };
export function generateStaticParams() {
  return archive.map((p) => ({ slug: p.slug.split("/") }));
}
export default async function ArchivePage({
  params,
}: {
  params: Promise<{ slug: string[] }>;
}) {
  const { slug } = await params;
  const p = archive.find((p) => p.slug === slug.join("/"));
  if (!p) notFound();
  return (
    <main id="main-content">
      <PageIntro
        eyebrow="Original content / Archive"
        title={p.title}
        text="Original page text, preserved as supplied. Older template content is included for completeness."
      />
      <div className="container">
        <p className="small muted" style={{ marginBottom: 30 }}>
          Source:{" "}
          <a href={p.sourceUrl} target="_blank" rel="noopener noreferrer">
            {p.sourceUrl}
          </a>
        </p>
        <div className="archive-text">{p.text}</div>
      </div>
    </main>
  );
}
