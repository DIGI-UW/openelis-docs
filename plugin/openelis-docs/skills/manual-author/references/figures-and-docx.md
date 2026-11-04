# Figures and the optional Word file

Capture itself is the `openelis-qa:qa-evidence` skill (manual media mode). This file covers what
the manual needs from the figures.

## Figure rules

- **Viewport shots, not full page.** `page.screenshot({ path, fullPage: false })` at 1440x900 CSS
  (2880x1800 at 2x) gives the right shape with no cropping. A `fullPage: true` capture of an editor
  with open accordions once produced a 2880x16308 strip. Scroll to the control first; collapse
  accordions open by default.
- One figure per step that opens a new screen or dialog, uses a hard-to-find control, or produces
  a state the reader must recognize.
- Populated, realistic data (no test prefixes); PII masked.
- File names `NN-short-name.png` in step order; captions say what the figure shows, with no
  "captured" or provenance wording; alt text is a real description.
- Read every figure after capture. A passing capture can still show the wrong thing.
- French screenshots only on the most used pages (`frenchFigures` in the page's translation
  property); see `translation-refresh`.

## Cropping a long form into sections

Only when one long image really must be cut. In the capture spec, after filling the form, take a
full-page screenshot and record each section heading's offset:

```js
await page.screenshot({ path: `${OUT}/_full.png`, fullPage: true, animations: 'disabled' });
const offsets = await page.evaluate(() => {
  const names = ['Lab Number', 'Sampling Site', 'Default Collection Conditions'];
  const els = [...document.querySelectorAll('h2,h3,h4,div,label,span')];
  const out = { _dpr: devicePixelRatio };
  for (const n of names) {
    const e = els.find((x) => (x.textContent || '').trim() === n && x.getBoundingClientRect().height < 60);
    if (e) out[n] = Math.round(e.getBoundingClientRect().top + scrollY);
  }
  return out;
});
require('fs').writeFileSync(`${OUT}/_offsets.json`, JSON.stringify(offsets));
```

Then crop with PIL (offsets times `_dpr`; from one section's top to the next):

```python
import json
from PIL import Image
im = Image.open('_full.png'); o = json.load(open('_offsets.json')); d = o['_dpr']
order = ['Lab Number', 'Sampling Site', 'Default Collection Conditions']
ys = [(n, int(o[n] * d)) for n in order if n in o]
for i, (n, y) in enumerate(ys):
    y2 = ys[i + 1][1] if i + 1 < len(ys) else im.height
    im.crop((0, max(0, y - 20), im.width, y2)).save(n.lower().replace(' ', '-') + '.png')
```

Check you have not cropped away the Save buttons and action rows at the bottom.

## Word file (only when Casey asks for one)

Built with the docx skill:

- US Letter (12240x15840 DXA), 1 inch margins, Arial; themed H1 and H2 per domain (clinical
  blue `15487F`, environmental green `1B5E20`).
- Header rule; footer with the menu-path breadcrumb and page number.
- Figures centered, capped near 800 px tall or 600 px wide; italic grey captions; `ImageRun`
  with `type` and `altText`.
- Validate with the docx skill's `validate.py`, render to PDF and look at the page images before
  delivering.
- Confluence import of a .docx (Insert > Import Word document) is the fallback when the publisher
  cannot run.
