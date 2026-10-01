"use client";
import Image from "next/image";
import { useRef, useState } from "react";
import { Arrow, ArrowUpRight } from "./icons";
export function Gallery({
  images,
  title,
}: {
  images: string[];
  title: string;
}) {
  const dialog = useRef<HTMLDialogElement>(null);
  const [index, setIndex] = useState(0);
  function show(i: number) {
    setIndex(i);
    dialog.current?.showModal();
  }
  function move(delta: number) {
    setIndex((i) => (i + delta + images.length) % images.length);
  }
  return (
    <>
      <div className="gallery-grid">
        {images.map((src, i) => (
          <button
            key={src}
            onClick={() => show(i)}
            className={`gallery-image ${i === 0 ? "gallery-featured" : ""}`}
            aria-label={`Enlarge ${title} photo ${i + 1}`}
          >
            <Image
              src={src}
              alt={`${title}, project photograph ${i + 1}`}
              fill
              sizes={
                i === 0
                  ? "(max-width:700px) 100vw, 80vw"
                  : "(max-width:700px) 100vw, 40vw"
              }
            />
            <span className="image-arrow">
              <ArrowUpRight />
            </span>
          </button>
        ))}
      </div>
      <dialog
        ref={dialog}
        className="lightbox"
        aria-label={`${title} image gallery`}
        onClick={(e) => {
          if (e.target === e.currentTarget) dialog.current?.close();
        }}
        onKeyDown={(e) => {
          if (e.key === "ArrowRight") move(1);
          if (e.key === "ArrowLeft") move(-1);
        }}
      >
        <div className="lightbox-inner">
          <button
            className="lightbox-close"
            aria-label="Close image viewer"
            onClick={() => dialog.current?.close()}
          >
            ×
          </button>
          <div className="lightbox-image">
            <Image
              src={images[index]}
              alt={`${title}, photograph ${index + 1}`}
              fill
              sizes="90vw"
              style={{ objectFit: "contain" }}
            />
          </div>
          <div className="lightbox-controls">
            <button onClick={() => move(-1)} aria-label="Previous image">
              <Arrow style={{ transform: "rotate(180deg)" }} />
            </button>
            <span>
              {index + 1} / {images.length} · {title}
            </span>
            <button onClick={() => move(1)} aria-label="Next image">
              <Arrow />
            </button>
          </div>
        </div>
      </dialog>
    </>
  );
}
