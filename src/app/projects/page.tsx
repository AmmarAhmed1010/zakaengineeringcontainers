import type { Metadata } from "next";
import { PageIntro } from "@/components/ui";
import { ProjectBrowser } from "@/components/project-browser";
import { ProjectCTA } from "@/components/footer";
export const metadata: Metadata = {
  title: "Our Projects",
  description:
    "Explore nine completed Zaka Engineering container projects, including offices, a hotel and restaurant, a kitchen, and a community mosque.",
};
export default function Projects() {
  return (
    <main id="main-content">
      <PageIntro
        eyebrow="Our portfolio"
        title="Possibility, built."
        text="Homes for new ideas. Places for people. Explore our completed container projects across Pakistan."
      />
      <ProjectBrowser />
      <ProjectCTA />
    </main>
  );
}
