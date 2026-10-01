import Image from "next/image";
import Link from "next/link";
import { ArrowUpRight, Pin } from "./icons";
import { projects } from "@/data/site";
export function SectionTitle({
  eyebrow,
  title,
  text,
  href,
  linkText,
}: {
  eyebrow: string;
  title: string;
  text?: string;
  href?: string;
  linkText?: string;
}) {
  return (
    <div className="section-heading">
      <div>
        <p className="eyebrow">
          <span />
          {eyebrow}
        </p>
        <h2>{title}</h2>
      </div>
      <div className="section-heading-side">
        {text && <p className="muted">{text}</p>}
        {href && (
          <Link href={href} className="text-link">
            {linkText || "Explore more"}
            <ArrowUpRight />
          </Link>
        )}
      </div>
    </div>
  );
}
export function PageIntro({
  eyebrow,
  title,
  text,
}: {
  eyebrow: string;
  title: string;
  text: string;
}) {
  return (
    <section className="page-intro container">
      <p className="eyebrow">
        <span />
        {eyebrow}
      </p>
      <div className="page-intro-row">
        <h1>{title}</h1>
        <p>{text}</p>
      </div>
    </section>
  );
}
export function ProjectCard({
  project,
  index = 0,
}: {
  project: (typeof projects)[number];
  index?: number;
}) {
  return (
    <Link className="project-card" href={`/projects/${project.slug}`}>
      <div className="project-image">
        <Image
          src={project.images[0]}
          alt={`${project.title}, completed project in ${project.location}`}
          fill
          sizes="(max-width:640px) 100vw, (max-width:1000px) 50vw, 33vw"
        />
        <span className="project-tag">{project.category}</span>
        <span className="image-arrow">
          <ArrowUpRight />
        </span>
      </div>
      <div className="project-card-caption">
        <div>
          <p className="small muted project-location">
            <Pin />
            {project.location}
          </p>
          <h3>{project.title}</h3>
        </div>
        <span className="card-number">
          {String(index + 1).padStart(2, "0")}
        </span>
      </div>
    </Link>
  );
}
