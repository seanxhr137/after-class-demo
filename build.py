"""Build the single story.json source into versioned browser files and a clean site."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from tools.check_story import validate_story

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--out-dir', default='.pages-dist')
args = parser.parse_args()
out = (ROOT / args.out_dir).resolve()
if out == ROOT or out.is_relative_to(ROOT / 'assets') or not out.is_relative_to(ROOT):
    raise SystemExit('输出目录必须是项目内独立子目录，不能覆盖源码或素材')
data = json.loads((ROOT / 'story.json').read_text(encoding='utf-8'))
print('剧情检查通过:', validate_story(data))
# Preserve source clarity; all browser story files are generated, not manually edited.
story = 'window.VN_STORY = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n'
outputs = {'story': story, 'app': (ROOT / 'app.js').read_text(encoding='utf-8'), 'style': (ROOT / 'style.css').read_text(encoding='utf-8')}
names = {}
if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)
for kind, contents in outputs.items():
    suffix = 'css' if kind == 'style' else 'js'
    digest = hashlib.sha256(contents.encode()).hexdigest()[:12]
    name = f'vn-{kind}-{digest}.{suffix}'
    (out / name).write_text(contents, encoding='utf-8')
    names[kind] = name
html = (ROOT / 'index.html').read_text(encoding='utf-8')
for kind in names:
    html = html.replace('{{' + kind.upper() + '_FILE}}', names[kind])
if '{{' in html:
    raise SystemExit('入口文件含有未替换的资源占位符')
(out / 'index.html').write_text(html, encoding='utf-8')
(out / '.nojekyll').touch()
shutil.copytree(ROOT / 'assets', out / 'assets')
print('发布文件已生成:', out)
