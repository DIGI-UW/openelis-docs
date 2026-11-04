#!/usr/bin/env node
/**
 * Build (or check) the openelis-docs plugin in plugin/openelis-docs/.
 *
 * WHY THIS EXISTS
 * The docs skills lived as account skills with no source control, each repeating parts of the
 * others, and the tooling they drive lived only on Casey's Mac. This folder is now the only source
 * of the skills, next to the tooling. The check keeps a broken plugin from being merged.
 *
 * USAGE
 *   node scripts/build-plugin.mjs           # validate, test hooks, write dist/openelis-docs.plugin
 *   node scripts/build-plugin.mjs --check   # validate only; exit 1 on any problem (CI)
 *
 * CHECKS
 *   - .claude-plugin/plugin.json parses, name is kebab-case, version is semver, license and icon set
 *   - every skills/<dir>/SKILL.md has frontmatter name == <dir> and a third-person description
 *   - every agents/*.md has name, description (a | block), model and color
 *   - hooks/hooks.json parses and every script it runs exists
 *   - no em dash anywhere in the plugin (organization writing rule)
 *   - every relative `references/<file>` and `lint/<file>` a SKILL.md names exists in that skill
 *   - the publisher in manual-publish is identical to docs-manual/publish/confluence-publish.py
 *     (when docs-manual/ is present)
 *   - the hook self-test and the linter self-check pass (skipped with a warning without python3)
 *   - evals/evals.json parses and names only skills that exist
 */

import { execFileSync, spawnSync } from 'node:child_process';
import { existsSync, readFileSync, readdirSync, statSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';
import { join, dirname, resolve, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { tmpdir } from 'node:os';

const REPO = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const PLUGIN = join(REPO, 'plugin', 'openelis-docs');
const DIST = join(REPO, 'dist');
const CHECK = process.argv.includes('--check');
const EM = String.fromCharCode(0x2014);
const problems = [];

function walk(dir) {
  const out = [];
  for (const name of readdirSync(dir)) {
    if (name === '__pycache__' || name === '.DS_Store') continue;
    const p = join(dir, name);
    if (statSync(p).isDirectory()) out.push(...walk(p));
    else out.push(p);
  }
  return out.sort();
}

function frontmatter(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---/);
  if (!m) return null;
  const fm = {};
  let key = null;
  for (const line of m[1].split('\n')) {
    const kv = line.match(/^([A-Za-z_-]+):\s*(.*)$/);
    if (kv) {
      key = kv[1];
      fm[key] = kv[2].replace(/^["']|["']$/g, '').trim();
    } else if (key && line.startsWith('  ')) {
      fm[key] = `${fm[key]} ${line.trim()}`.trim();
    } else if (key && line.trim()) {
      key = null;
    }
  }
  return { fm, raw: m[1] };
}

// 1. Manifest
let manifest = {};
try {
  manifest = JSON.parse(readFileSync(join(PLUGIN, '.claude-plugin', 'plugin.json'), 'utf8'));
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(manifest.name || '')) problems.push('plugin.json: name is not kebab-case');
  if (!/^\d+\.\d+\.\d+$/.test(manifest.version || '')) problems.push('plugin.json: version is not semver');
  if (!manifest.license) problems.push('plugin.json: license missing');
  if (!existsSync(join(PLUGIN, '.claude-plugin', 'icon.png'))) problems.push('.claude-plugin/icon.png missing');
} catch (e) {
  problems.push(`plugin.json: ${e.message}`);
}

// 2. Skills
const skills = readdirSync(join(PLUGIN, 'skills')).sort();
for (const dir of skills) {
  const skillMd = join(PLUGIN, 'skills', dir, 'SKILL.md');
  if (!existsSync(skillMd)) { problems.push(`skills/${dir}: no SKILL.md`); continue; }
  const text = readFileSync(skillMd, 'utf8');
  const parsed = frontmatter(text);
  if (!parsed) { problems.push(`skills/${dir}/SKILL.md: no frontmatter`); continue; }
  const { fm } = parsed;
  if (fm.name !== dir) problems.push(`skills/${dir}/SKILL.md: name "${fm.name}" does not match the folder`);
  if (!fm.description || fm.description.length < 80) problems.push(`skills/${dir}/SKILL.md: description missing or too short`);
  else if (!/^This skill should be used/.test(fm.description)) problems.push(`skills/${dir}/SKILL.md: description should start "This skill should be used ..."`);
  for (const m of text.matchAll(/`((?:references|lint|scripts)\/[A-Za-z0-9._/-]+\.(?:md|json|py|yml|ini))`/g)) {
    if (!existsSync(join(PLUGIN, 'skills', dir, m[1]))) {
      // A path in another skill is written "the X skill's `references/...`"; only check our own.
      const before = text.slice(Math.max(0, m.index - 60), m.index);
      if (!/skill'?s?\s*$|\bskill's\s+$|openelis-qa|qa-evidence|qa-run|openelis-design|manual-[a-z]+\s*$/.test(before)) {
        problems.push(`skills/${dir}/SKILL.md names ${m[1]}, which does not exist in the skill`);
      }
    }
  }
  // The frontmatter must parse as YAML: newer `claude plugin validate` refuses an unquoted ': '
  // inside a description, and the skill then loads with no metadata at all.
  const y = spawnSync('python3', ['-c', 'import sys,yaml; yaml.safe_load(sys.stdin.read())'], { input: parsed.raw, encoding: 'utf8' });
  if (y.status !== 0 && !/No module named/.test(y.stderr || '')) problems.push(`skills/${dir}/SKILL.md: frontmatter is not valid YAML (quote the description or drop the ': ')`);
  const words = text.split(/\s+/).length;
  if (words > 4500) problems.push(`skills/${dir}/SKILL.md: ${words} words; move detail into references/`);
}

// 3. Agents
const agentsDir = join(PLUGIN, 'agents');
if (existsSync(agentsDir)) {
  for (const f of readdirSync(agentsDir).filter((x) => x.endsWith('.md'))) {
    const parsed = frontmatter(readFileSync(join(agentsDir, f), 'utf8'));
    const fm = parsed ? parsed.fm : {};
    for (const k of ['name', 'description', 'model', 'color']) if (!fm[k]) problems.push(`agents/${f}: frontmatter lacks ${k}`);
    if (parsed && !/^description:\s*\|/m.test(parsed.raw)) problems.push(`agents/${f}: description must be a | block`);
  }
}

// 4. Hooks
const hooksJson = join(PLUGIN, 'hooks', 'hooks.json');
if (existsSync(hooksJson)) {
  try {
    const hooks = JSON.parse(readFileSync(hooksJson, 'utf8'));
    if (!hooks.hooks) problems.push('hooks.json: missing the {"hooks": {...}} wrapper');
    for (const [event, groups] of Object.entries(hooks.hooks || {})) {
      for (const g of groups) for (const h of g.hooks || []) {
        for (const m of (h.command || '').matchAll(/\$\{CLAUDE_PLUGIN_ROOT\}\/([^"\s]+)/g)) {
          if (!existsSync(join(PLUGIN, m[1]))) problems.push(`hooks.json ${event}: ${m[1]} does not exist`);
        }
      }
    }
  } catch (e) {
    problems.push(`hooks.json: ${e.message}`);
  }
}

// 5. No em dashes in the plugin
for (const f of walk(PLUGIN)) {
  if (!/\.(md|json|py|sh|txt|yml|ini|mjs)$/.test(f)) continue;
  readFileSync(f, 'utf8').split('\n').forEach((l, i) => {
    if (l.includes(EM)) problems.push(`${relative(REPO, f)}:${i + 1}: em dash (org rule: no em dashes)`);
  });
}

// 6. Publisher copy in sync with the tooling
const pubPlugin = join(PLUGIN, 'skills', 'manual-publish', 'scripts', 'confluence-publish.py');
const pubTool = join(REPO, 'docs-manual', 'publish', 'confluence-publish.py');
if (existsSync(pubTool) && readFileSync(pubTool, 'utf8') !== readFileSync(pubPlugin, 'utf8')) {
  problems.push('docs-manual/publish/confluence-publish.py differs from the manual-publish copy (keep them identical)');
}

// 7. Self-tests
const py = spawnSync('python3', ['--version']);
if (py.status === 0) {
  const t = spawnSync('python3', [join(PLUGIN, 'hooks', 'scripts', 'test_docs_hooks.py')], { encoding: 'utf8' });
  if (t.status !== 0) problems.push(`hook self-test failed:\n${t.stdout}${t.stderr}`);
  const yaml = spawnSync('python3', ['-c', 'import yaml'], { encoding: 'utf8' });
  if (yaml.status === 0) {
    const sample = join(tmpdir(), `oe-lint-selfcheck-${process.pid}.xhtml`);
    writeFileSync(sample, `<p>Open the sidebar ${EM} <a href="x">here</a>.</p>\n<p>Open the Main menu and select Order.</p>\n`);
    const r = spawnSync('python3', [join(PLUGIN, 'skills', 'manual-lint', 'lint', 'oe_lint.py'), '--json', sample], { encoding: 'utf8' });
    rmSync(sample, { force: true });
    let rules = [];
    try { rules = JSON.parse(r.stdout).map((x) => x.rule); } catch { /* reported below */ }
    for (const want of ['OpenELIS.EmDash', 'OpenELIS.Terms', 'OpenELIS.LinkText']) {
      if (!rules.includes(want)) problems.push(`linter self-check: ${want} did not fire`);
    }
  } else {
    console.warn('warning: PyYAML not installed; linter self-check skipped');
  }
} else {
  console.warn('warning: python3 not found; hook and linter self-tests skipped');
}

// 8. Evals
try {
  const ev = JSON.parse(readFileSync(join(REPO, 'evals', 'evals.json'), 'utf8'));
  if (!Array.isArray(ev.evals) || ev.evals.length === 0) problems.push('evals/evals.json: no evals');
  for (const e of ev.evals || []) {
    for (const s of e.expected_skills || []) {
      if (!skills.includes(s) && !s.includes(':')) problems.push(`evals/evals.json #${e.id}: unknown skill ${s}`);
    }
  }
} catch (e) {
  problems.push(`evals/evals.json: ${e.message}`);
}

if (problems.length) {
  console.error('\nopenelis-docs plugin check failed:\n');
  for (const p of problems) console.error(`  ${p}`);
  console.error('\nFix the files under plugin/openelis-docs/, then npm run build:plugin.\n');
  process.exit(1);
}

const files = walk(PLUGIN);
if (CHECK) {
  console.log(`openelis-docs ${manifest.version}: plugin is valid (${skills.length} skills, ${files.length} files).`);
  process.exit(0);
}

mkdirSync(DIST, { recursive: true });
const out = join(DIST, 'openelis-docs.plugin');
rmSync(out, { force: true });
execFileSync('zip', ['-q', '-r', '-X', out, '.', '-x', '*__pycache__*', '-x', '*.DS_Store'], { cwd: PLUGIN });
console.log(`built dist/openelis-docs.plugin (${manifest.version}, ${files.length} files, ${(readFileSync(out).length / 1024).toFixed(0)} KB)`);
