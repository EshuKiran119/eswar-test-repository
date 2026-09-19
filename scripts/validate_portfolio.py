"""Fail the Pages build on broken local links, missing assets or stale domain references."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, zipfile
ROOT=Path(__file__).resolve().parents[1]/'docs'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.links=[];self.h1=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:
   assert a['id'] not in self.ids, f'Duplicate ID: {a["id"]}'
   self.ids.add(a['id'])
  if tag=='h1': self.h1+=1
  for key in ['href','src']:
   if a.get(key):self.links.append(a[key])
p=Page();p.feed((ROOT/'index.html').read_text());assert p.h1==1
checked=0
for raw in p.links:
 u=urlsplit(raw)
 if u.scheme or u.netloc:continue
 if not u.path:
  assert u.fragment in p.ids, f'Missing anchor: {raw}'
 else:
  path=unquote(u.path).removeprefix('/eswar-test-repository/')
  assert (ROOT/path).is_file(), f'Missing local file: {raw}'
 checked+=1
for path in ROOT.rglob('*'):
 if path.is_file() and path.suffix in ['.html','.css','.js','.xml','.txt','.md','.webmanifest']:
  assert 'eswar-singamsetty-qa-portfolio.com' not in path.read_text(),f'Stale domain: {path}'
assert not (ROOT/'CNAME').exists(), 'Unexpected custom-domain configuration'
for suffix in ['pdf','docx']:
 f=ROOT/'assets'/f'Eswar_Sai_Kiran_Singamsetty_ATS_Resume.{suffix}'
 assert f.stat().st_size>10000
 if suffix=='pdf':assert f.read_bytes().startswith(b'%PDF-')
 else:
  with zipfile.ZipFile(f) as z:
   assert z.testzip() is None
   assert b'eswar-singamsetty-qa-portfolio.com' not in z.read('word/_rels/document.xml.rels')
json.loads((ROOT/'manifest.webmanifest').read_text())
print(f'PASS: {checked} internal links/assets, {len(p.ids)} unique IDs, valid resume files, no custom domain')
