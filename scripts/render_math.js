const fs = require('fs');
const path = require('path');
const os = require('os');

// Load mathjax-full from local cache outside iCloud, or fallback to local node_modules
const cacheModules = path.join(os.homedir(), '.cache', 'hoo-wiki-mathjax', 'node_modules');
const mathjaxPath = fs.existsSync(path.join(cacheModules, 'mathjax-full'))
  ? path.join(cacheModules, 'mathjax-full')
  : 'mathjax-full';

const { mathjax } = require(path.join(mathjaxPath, 'js', 'mathjax.js'));
const { TeX } = require(path.join(mathjaxPath, 'js', 'input', 'tex.js'));
const { SVG } = require(path.join(mathjaxPath, 'js', 'output', 'svg.js'));
const { liteAdaptor } = require(path.join(mathjaxPath, 'js', 'adaptors', 'liteAdaptor.js'));
const { RegisterHTMLHandler } = require(path.join(mathjaxPath, 'js', 'handlers', 'html.js'));
const { AllPackages } = require(path.join(mathjaxPath, 'js', 'input', 'tex', 'AllPackages.js'));

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);

const tex = new TeX({ packages: AllPackages });
const svg = new SVG({ fontCache: 'none' });
const html = mathjax.document('', { InputJax: tex, OutputJax: svg });

const input = fs.readFileSync(0, 'utf8');
const items = JSON.parse(input);

const results = items.map(({ tex: formula, display }) => {
  const node = html.convert(formula, { display: Boolean(display) });
  const inner = adaptor.innerHTML(node);
  // Extract the <svg ...>...</svg> element cleanly for WeChat compatibility
  const match = inner.match(/<svg[\s\S]*<\/svg>/);
  const svgStr = match ? match[0] : inner;
  if (display) {
    return `<section style="text-align: center; margin: 16px 0; overflow-x: auto; max-width: 100%;">${svgStr}</section>`;
  }
  return svgStr;
});

process.stdout.write(JSON.stringify(results));
