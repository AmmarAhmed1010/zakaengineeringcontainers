import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { projects } from "@/data/site";
import { PageIntro } from "@/components/ui";
import { Gallery } from "@/components/gallery";
import { ProjectCTA } from "@/components/footer";
import { ArrowUpRight } from "@/components/icons";
export function generateStaticParams() {
  return projects.map((p) => ({ slug: p.slug }));
}
export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const p = projects.find((p) => p.slug === slug);
  return {
    title: p?.title,
    description: p?.paragraphs[0]?.slice(0, 155),
    openGraph: { images: p?.images[0] },
  };
}
export default async function Project({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const p = projects.find((p) => p.slug === slug);
  if (!p) notFound();
  const next = projects[(projects.indexOf(p) + 1) % projects.length];
  return (
    <main id="main-content">
      <PageIntro
        eyebrow={`${p.category} / ${p.location}`}
        title={p.title}
        text="A completed Zaka Engineering project. Explore the original photographs, project details, and the spaces within."
      />
      <div className="container">
        <dl className="project-meta">
          {[
            { label: "Client", value: p.client },
            { label: "Location", value: p.location },
            { label: "Started", value: p.startDate },
            { label: "Completed", value: p.endDate },
          ].map((m) => (
            <div key={m.label}>
              <dt>{m.label}</dt>
              <dd>{m.value}</dd>
            </div>
          ))}
        </dl>
        <Gallery images={p.images} title={p.title} />
        <section className="section-pad project-description">
          <p className="eyebrow">
            <span />
            The project story
          </p>
          <h2>Designed to make space for more.</h2>
          {p.paragraphs.map((text, i) => (
            <p key={i}>{text}</p>
          ))}
          <div className="project-next">
            <Link href="/projects" className="text-link">
              All projects
              <ArrowUpRight />
            </Link>
            <Link href={`/projects/${next.slug}`} className="text-link">
              Next / {next.title}
              <ArrowUpRight />
            </Link>
          </div>
        </section>
      </div>
      <ProjectCTA />
    </main>
  );
}
