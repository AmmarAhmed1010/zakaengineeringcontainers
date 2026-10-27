// Render transparent PDF logo assets from the website's original vector artwork.
import sharp from 'sharp';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const original = path.join(root, 'public/images/original');
const source = path.join(original, 'Containers-Prefab.svg');
await sharp(source, { density: 600 }).resize({ width: 1200 }).png()
  .toFile(path.join(original, 'Containers-Prefab-watermark.png'));
await sharp(source, { density: 600 }).trim().resize({
  width: 472, height: 275, fit: 'contain',
  background: { r: 0, g: 0, b: 0, alpha: 0 },
}).png().toFile(path.join(original, 'Zaka-logo-transparent.png'));
console.log('Transparent header and watermark PNGs rendered from the SVG.');
