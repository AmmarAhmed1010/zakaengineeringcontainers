import projectData from "./projects.json";
import documentData from "./documents.json";
export const projects = projectData;
export const company = {
  name: "Zaka Engineering",
  legalName: "Zaka Engineering Containers & Prefab (Pvt. Ltd.)",
  phone: "+92 340 5221225",
  phoneHref: "tel:+923405221225",
  whatsapp: "https://wa.me/923405221225",
  email: "zakaurrehman3020@gmail.com",
  address:
    "Main Jinnah Avenue, near Bukhari Chowk (Attock Petrol), New Mal, Islamabad",
  maps: "https://www.google.com/maps/search/?api=1&query=Zaka+Engineering+Containers+Prefab+Islamabad",
  socials: [
    {
      name: "Instagram",
      url: "https://www.instagram.com/zakengineeringcontainersprefab/",
    },
    {
      name: "Facebook",
      url: "https://www.facebook.com/zakaengineeringcontainersprefab",
    },
    { name: "YouTube", url: "https://www.youtube.com/@ZakaEngineering-ur7kf" },
    { name: "TikTok", url: "https://www.tiktok.com/@zakaengineering" },
  ],
};
export const services = [
  {
    slug: "portable-prefab-cabins",
    title: "Portable Prefab Cabins",
    short: "Spaces that go where you do.",
    description:
      "Durable and movable prefab cabins perfect for offices, homes, and remote sites.",
    detail:
      "From site offices and guard cabins to comfortable accommodation, our prefab units give you a practical space that can move with your needs. We plan the layout, fabricate the structure, and coordinate delivery across Pakistan.",
    tags: ["Site offices", "Guard cabins", "Accommodation"],
    image: "/images/generated/office.webp",
  },
  {
    slug: "modified-shipping-units",
    title: "Modified Shipping Units",
    short: "A new purpose. A strong foundation.",
    description:
      "We design, cut, and convert shipping containers into homes, offices, and kiosks.",
    detail:
      "Give a shipping container a new life as a place to live, work, or welcome customers. Our team manages the conversion from initial design through fabrication and interior finishes, with a layout suited to the way you will use it.",
    tags: ["Container homes", "Cafes & kiosks", "Workspaces"],
    image: "/images/generated/hero.webp",
  },
  {
    slug: "customized-containers",
    title: "Customized Containers",
    short: "Your space, down to the detail.",
    description:
      "Get containers tailored to your space needs with doors, windows, and insulation.",
    detail:
      "Every project starts with your requirements. We develop door and window positions, room divisions, insulation, and interior finishes around your intended use, site, and budget.",
    tags: ["Custom layouts", "Doors & glazing", "Insulation"],
    image: "/images/generated/interior.webp",
  },
  {
    slug: "aluminum-fabrication",
    title: "Aluminum Fabrication",
    short: "Clean lines. Precise finishes.",
    description:
      "Premium quality aluminum doors, windows, partitions, and structural work done fast.",
    detail:
      "Our aluminum fabrication services support container and conventional spaces with carefully fitted doors, windows, partitions, and structural work. Discuss your dimensions and finish requirements with our team.",
    tags: ["Doors & windows", "Partitions", "Structural work"],
    image: "/images/generated/interior.webp",
  },
  {
    slug: "ms-iron-fabrication",
    title: "MS Iron Fabrication",
    short: "Strength, shaped to your needs.",
    description:
      "Strong MS iron gates, stairs, sheds, and structures made with precision and care.",
    detail:
      "We fabricate mild-steel gates, staircases, sheds, and supporting structures for practical, durable use. Each scope is planned around its dimensions, function, and installation requirements.",
    tags: ["Gates & stairs", "Sheds", "Steel structures"],
    image: "/images/generated/workshop.webp",
  },
  {
    slug: "ss-steel-fabrication",
    title: "SS Steel Fabrication",
    short: "Durability with a refined finish.",
    description:
      "Rust-free stainless steel work for railings, stairs, kitchens, and industrial use.",
    detail:
      "Stainless steel fabrication brings a clean finish to railings, stair details, kitchen fittings, and industrial applications. The grade, finish, and fabrication scope are selected to suit the project.",
    tags: ["Railings", "Kitchen fittings", "Industrial use"],
    image: "/images/generated/workshop.webp",
  },
];
export const documents = documentData;
export const process = [
  {
    title: "Tell us your vision",
    description:
      "Share your space requirements, location, and budget. We help define a clear project brief.",
  },
  {
    title: "Design with purpose",
    description:
      "We develop your layout, finishes, and specifications so every detail has a place.",
  },
  {
    title: "Build with precision",
    description:
      "Our team fabricates and assembles your container with careful attention to craftsmanship.",
  },
  {
    title: "Deliver your space",
    description:
      "We coordinate delivery and installation, helping turn your plan into a ready-to-use space.",
  },
];
