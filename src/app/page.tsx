import Image from "next/image";
import Link from "next/link";
import { Arrow, ArrowUpRight, DownloadIcon } from "@/components/icons";
import { ProjectCTA } from "@/components/footer";
import { SectionTitle, ProjectCard } from "@/components/ui";
import { services, projects, process } from "@/data/site";
export default function Home() {
  return (
    <main id="main-content">
      <section className="home-hero container">
        <div className="hero-top">
          <div>
            <p className="eyebrow">
              <span />
              Container spaces. Endless possibilities.
            </p>
            <h1>
              Built for life.
              <br />
              Engineered <span className="serif-word">to move.</span>
            </h1>
          </div>
          <div className="hero-intro">
            <span className="hero-mark" aria-hidden="true">
              ↗
            </span>
            <p>
              From modern homes to vibrant cafes and efficient site offices. We
              turn steel into spaces that work beautifully.
            </p>
            <Link className="text-link" href="/projects">
              Explore our work
              <ArrowUpRight />
            </Link>
          </div>
        </div>
        <div className="hero-image">
          <Image
            src="/images/generated/hero.webp"
            alt="Architectural concept of a modern container home with warm timber and full-height glazing"
            fill
            sizes="100vw"
            loading="eager"
          />
          <span className="concept-label">
            Architectural concept / Residential
          </span>
          <div className="hero-image-bottom">
            <span>
              Strong foundations.
              <br />
              Smarter futures.
            </span>
            <Link href="/contact-us" className="hero-image-link">
              Build your vision
              <ArrowUpRight />
            </Link>
          </div>
        </div>
        <div className="hero-footnote">
          <span>Homes / Workspaces / Hospitality / Prefab structures</span>
          <span>
            Islamabad, Pakistan <span className="tiny-dot" />
          </span>
        </div>
      </section>
      <section className="stats-section">
        <div className="container stats-grid">
          <div className="stats-statement">
            Better spaces.
            <br />
            <span className="muted">Built around you.</span>
          </div>
          <div>
            <strong>
              5<span>+</span>
            </strong>
            <p>Years of hands-on experience</p>
          </div>
          <div>
            <strong>06</strong>
            <p>Specialist construction services</p>
          </div>
          <div>
            <strong>
              PK<span>↗</span>
            </strong>
            <p>Nationwide delivery & service</p>
          </div>
        </div>
      </section>
      <section className="container section-pad about-preview">
        <div className="about-image image-frame">
          <Image
            src="/images/generated/interior.webp"
            alt="Concept interior of a refined modular office with timber finishes and natural light"
            fill
            sizes="(max-width:800px) 100vw, 45vw"
          />
          <span className="concept-label">Interior concept</span>
          <div className="floating-caption">
            <span className="eyebrow">A smarter way to build</span>
            <p>
              Thoughtful by design.
              <br />
              Practical by nature.
            </p>
          </div>
        </div>
        <div className="about-copy">
          <p className="eyebrow">
            <span />
            More than a container
          </p>
          <h2>
            Good spaces
            <br />
            begin with
            <br />
            <span className="serif-word">better thinking.</span>
          </h2>
          <p>
            With 5+ years of hands-on experience, Zaka Engineering specializes
            in transforming shipping containers into fully functional homes,
            cafes, restaurants, site offices, and guard cabins.
          </p>
          <p className="muted">
            We focus on quality craftsmanship, modern design and fast project
            delivery to help you build smarter spaces with less hassle and more
            impact.
          </p>
          <div className="mini-features">
            <div>
              <span>01 /</span>
              <strong>Nationwide services</strong>
              <p>Islamabad, Rawalpindi, and all major cities in Pakistan.</p>
            </div>
            <div>
              <span>02 /</span>
              <strong>Trusted by clients</strong>
              <p>
                Builders, business owners, and individuals across industries.
              </p>
            </div>
          </div>
          <Link href="/about-us" className="text-link">
            Meet Zaka Engineering
            <ArrowUpRight />
          </Link>
        </div>
      </section>
      <section className="services-preview section-pad">
        <div className="container">
          <SectionTitle
            eyebrow="What we do"
            title="Your idea. Our expertise."
            text="From the first sketch to the final finish, we bring your space to life."
            href="/services"
            linkText="All our services"
          />
          <div className="service-showcase">
            {services.slice(0, 3).map((s, i) => (
              <Link
                href={`/services/${s.slug}`}
                className="service-showcase-card"
                key={s.slug}
              >
                <div className="service-showcase-image">
                  <Image
                    src={s.image}
                    alt={`${s.title} architectural concept`}
                    fill
                    sizes="(max-width:700px) 100vw, 33vw"
                  />
                  <span className="card-index">0{i + 1}</span>
                  <span className="image-arrow">
                    <ArrowUpRight />
                  </span>
                </div>
                <h3>{s.title}</h3>
                <p>{s.description}</p>
                <span className="small service-explore">
                  Explore solution
                  <Arrow width={16} />
                </span>
              </Link>
            ))}
          </div>
          <div className="fabrication-strip">
            <span className="eyebrow">Built down to the detail</span>
            <div>
              {services.slice(3).map((s) => (
                <Link href={`/services/${s.slug}`} key={s.slug}>
                  {s.title}
                  <ArrowUpRight width={17} />
                </Link>
              ))}
            </div>
          </div>
        </div>
      </section>
      <section className="container section-pad">
        <SectionTitle
          eyebrow="Selected work"
          title="Real spaces. Real possibilities."
          text="A closer look at what we’ve built for people and businesses across Pakistan."
          href="/projects"
          linkText="View all projects"
        />
        <div className="project-grid selected-projects">
          {[projects[0], projects[1], projects[5]].map((p, i) => (
            <ProjectCard key={p.slug} project={p} index={i} />
          ))}
        </div>
      </section>
      <section className="process-section section-pad">
        <div className="container">
          <SectionTitle
            eyebrow="From vision to reality"
            title="One team. Every step."
            text="A considered process, from design to delivery, with precision and care."
          />
          <div className="process-grid">
            {process.map((p, i) => (
              <div key={p.title}>
                <span className="process-number">0{i + 1}</span>
                <h3>{p.title}</h3>
                <p>{p.description}</p>
              </div>
            ))}
          </div>
          <div className="skill-row">
            <p>Our construction expertise</p>
            <span>
              Design & customization <strong>100%</strong>
            </span>
            <span>
              Fabrication & assembly <strong>99%</strong>
            </span>
            <span>
              Site consulting & execution <strong>75%</strong>
            </span>
          </div>
        </div>
      </section>
      <section className="container section-pad catalogue-preview">
        <div className="catalogue-copy">
          <p className="eyebrow">
            <span />
            The design collection
          </p>
          <h2>
            A little inspiration.
            <br />A lot of <span className="serif-word">possibility.</span>
          </h2>
          <p className="muted">
            Explore five thoughtfully prepared concept catalogues. Office
            cabins, comfortable homes, and site-ready spaces — with floor plans
            and details to start the conversation.
          </p>
          <Link className="button button-navy" href="/downloads">
            Explore the catalogues
            <DownloadIcon />
          </Link>
          <p className="small muted">
            5 collections / Floor plans / Specifications
          </p>
        </div>
        <Link
          href="/downloads"
          className="catalogue-art"
          aria-label="Explore the Zaka design catalogues"
        >
          <div className="catalogue-paper paper-back">
            <span>ZAKA / ENGINEERING</span>
            <strong>
              Spaces for
              <br />
              better living.
            </strong>
            <Image
              src="/images/generated/hero.webp"
              alt="Residential design collection"
              width={380}
              height={260}
            />
            <p>THE RESIDENTIAL COLLECTION / 2026</p>
          </div>
          <div className="catalogue-paper paper-front">
            <span>ZAKA / ENGINEERING</span>
            <strong>
              Designed
              <br />
              to work.
            </strong>
            <Image
              src="/images/generated/office.webp"
              alt="Office design collection"
              width={380}
              height={260}
            />
            <p>THE WORKSPACE COLLECTION / 2026</p>
            <ArrowUpRight />
          </div>
        </Link>
      </section>
      <ProjectCTA />
    </main>
  );
}
