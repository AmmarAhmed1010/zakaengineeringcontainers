// Export generated photographic sheets as high-quality, unresized JPEG assets.
import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';
import assert from 'node:assert/strict';

const root=path.resolve(import.meta.dirname,'..');
const styles=JSON.parse(await fs.readFile(path.join(root,'scripts/roof_style_revisions.json'),'utf8'));
const valid=new Set(styles.map(s=>s.slug));
const entries=JSON.parse(await fs.readFile(path.join(root,'tmp/roof-generation-files.json'),'utf8'));
const out=path.join(root,'public/images/catalogues/roof-revision');await fs.mkdir(out,{recursive:true});
for(const entry of entries){
  assert(valid.has(entry.slug),'Unknown catalogue '+entry.slug);
  await sharp(entry.path).jpeg({quality:92,chromaSubsampling:'4:4:4'}).toFile(path.join(out,entry.slug+'.jpg'));
}
console.log('Exported',entries.length,'revised exterior sheets.');
