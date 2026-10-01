import type { MetadataRoute } from "next";
import { projects, services, documents } from "@/data/site";
export default function sitemap(): MetadataRoute.Sitemap {
  const base = "https://zakaengineeringcontainers.com";
  return [
    "",
    "/about-us",
    "/services",
    "/projects",
    "/contact-us",
    "/downloads",
    ...projects.map((p) => `/projects/${p.slug}`),
    ...services.map((s) => `/services/${s.slug}`),
    ...documents.map((d) => `/downloads/${d.slug}`),
  ].map((path) => ({
    url: base + path,
    changeFrequency: "monthly",
    priority: path === "" ? 1 : 0.7,
  }));
}
