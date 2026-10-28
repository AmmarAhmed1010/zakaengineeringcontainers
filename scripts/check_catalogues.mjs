// Verify the actual collection, its identical download copies and served routes.
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';

const root=path.resolve(import.meta.dirname,'..');
const docs=JSON.parse(await fs.readFile(path.join(root,'src/data/documents.json'),'utf8'));
const mapping=JSON.parse(await fs.readFile(path.join(root,'src/data/catalogue-filenames.json'),'utf8'));
const manifest=JSON.parse(await fs.readFile(path.join(root,'output/pdf/catalogue-manifest.json'),'utf8'));
const base=process.argv[2];
const sha=buffer=>crypto.createHash('sha256').update(buffer).digest('hex');
assert.equal(docs.length,30);assert.equal(new Set(docs.map(d=>d.file)).size,30);
for(const folder of ['output/pdf','public/downloads']){
  assert.equal((await fs.readdir(path.join(root,folder))).filter(f=>f.endsWith('.pdf')).length,30);
}
for(const d of docs){
  const name=path.basename(d.file);assert(!/zaka|client/i.test(name));
  const canonical=await fs.readFile(path.join(root,'output/pdf',name));
  const publicCopy=await fs.readFile(path.join(root,'public',d.file));
  assert.equal(canonical.subarray(0,5).toString(),'%PDF-');assert.equal(sha(canonical),sha(publicCopy));
  assert.equal(sha(canonical),manifest.find(m=>m.file===name).sha256);
  for(const asset of [d.image,d.preview])await fs.access(path.join(root,'public',asset));
}
if(base){
  const listing=await fetch(base+'/downloads');assert.equal(listing.status,200);
  const html=await listing.text();
  for(const d of docs){
    assert(html.includes(`/downloads/${d.slug}`),'Missing listing '+d.slug);
    const page=await fetch(base+'/downloads/'+d.slug);assert.equal(page.status,200);
    assert((await page.text()).includes(d.file),'Missing PDF embed '+d.slug);
    const pdf=await fetch(base+d.file,{method:'HEAD'});assert.equal(pdf.status,200);
    assert(pdf.headers.get('content-type').includes('application/pdf'));
    const preview=await fetch(base+d.preview,{method:'HEAD'});assert.equal(preview.status,200);
  }
  for(const [oldName,newName] of Object.entries(mapping)){
    const redirect=await fetch(base+'/downloads/'+oldName,{method:'HEAD',redirect:'manual'});
    assert.equal(redirect.status,308);assert(redirect.headers.get('location').endsWith('/downloads/'+newName));
  }
  console.log('HTTP checks passed: 30 listings, 30 detail pages, 30 PDFs, 30 previews, 21 old-name redirects.');
}
console.log(`Verified 30 unique catalogues, ${docs.reduce((sum,d)=>sum+d.pages,0)} pages and identical canonical/download hashes.`);
