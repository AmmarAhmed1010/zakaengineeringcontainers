"use client";
import { useState } from "react";
import { projects } from "@/data/site";
import { ProjectCard } from "./ui";
export function ProjectBrowser() {
  const [filter, setFilter] = useState("All projects");
  const filtered = projects.filter(
    (p) => filter === "All projects" || p.category === filter,
  );
  return (
    <div className="container section-pad project-browser">
      <div className="filter-bar">
        <div className="filters" aria-label="Filter projects">
          {["All projects", "Workspaces", "Hospitality", "Community"].map(
            (c) => (
              <button
                key={c}
                className={filter === c ? "selected" : ""}
                aria-pressed={filter === c}
                onClick={() => setFilter(c)}
              >
                {c}
                {c === "All projects" && <span>09</span>}
              </button>
            ),
          )}
        </div>
        <span className="small muted" aria-live="polite">
          {filtered.length} projects
        </span>
      </div>
      <div className="project-grid">
        {filtered.map((p, i) => (
          <ProjectCard key={p.slug} project={p} index={i} />
        ))}
      </div>
    </div>
  );
}
