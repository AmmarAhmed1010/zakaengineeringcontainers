import Link from "next/link";
import { ArrowUpRight } from "@/components/icons";
export default function NotFound() {
  return (
    <main id="main-content" className="container empty-state">
      <p className="eyebrow" style={{ justifyContent: "center" }}>
        404 / A little off the plan
      </p>
      <h1>Let’s find your way.</h1>
      <p className="muted">
        This page isn’t here. Explore our spaces or start a conversation.
      </p>
      <Link href="/" className="button button-red">
        Back to home
        <ArrowUpRight />
      </Link>
    </main>
  );
}
