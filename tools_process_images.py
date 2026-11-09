"""Convert source visuals into optimized WebP for the site.
Usage: python3 tools_process_images.py <visuals_dir> <out_img_dir>"""
import sys, os, glob
from PIL import Image, ImageOps
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)

def save(im, name, widths=(1920, 960), q=78):
    im = im.convert('RGB')
    for w in widths:
        c = im.copy()
        if c.width > w:
            c = c.resize((w, round(c.height * w / c.width)), Image.LANCZOS)
        c.save(os.path.join(out, f"{name}-{w}.webp"), 'WEBP', quality=q, method=6)

for f in glob.glob(os.path.join(src, '*.jpeg')):
    base = os.path.basename(f).rsplit('.', 1)[0].lower()
    if base.startswith('icons_sheet') or base.startswith('company_team-backdrop'):
        continue
    name = base.split('_', 1)[0] + '_' + base.split('_', 1)[1].rsplit('_', 1)[0] if base.count('_') >= 2 else base
    im = Image.open(f)
    if base.startswith('og_'):
        im = ImageOps.fit(im, (1200, 630), Image.LANCZOS)
        im.convert('RGB').save(os.path.join(out, 'og.jpg'), 'JPEG', quality=85)
        continue
    save(im, name)

# icon sheet -> 16 transparent PNG icons
names = ['note','invoice','hourglass','clock','tower','supplier','vault','civic',
         'ledger','shield','search','loop','chart','exchange','scales','chat']
sheet = Image.open(os.path.join(src, 'icons_sheet_1x1.jpeg')).convert('RGB')
cw, ch = sheet.width // 4, sheet.height // 4
icon_dir = os.path.join(out, 'icons'); os.makedirs(icon_dir, exist_ok=True)
for i, n in enumerate(names):
    r, c = divmod(i, 4)
    cell = sheet.crop((c*cw, r*ch, (c+1)*cw, (r+1)*ch))
    px = cell.load(); rgba = Image.new('RGBA', cell.size); po = rgba.load()
    for y in range(cell.height):
        for x in range(cell.width):
            R, G, B = px[x, y]; m = min(R, G, B)
            a = max(0, min(255, int((250 - m) * 9)))
            po[x, y] = (R, G, B, a)
    bbox = rgba.getbbox()
    if bbox:
        pad = 16
        bbox = (max(0,bbox[0]-pad), max(0,bbox[1]-pad), min(cw,bbox[2]+pad), min(ch,bbox[3]+pad))
        rgba = rgba.crop(bbox)
    side = max(rgba.size); canvas = Image.new('RGBA', (side, side), (0,0,0,0))
    canvas.paste(rgba, ((side-rgba.width)//2, (side-rgba.height)//2))
    canvas = canvas.resize((256, 256), Image.LANCZOS)
    canvas.save(os.path.join(icon_dir, f"{n}.webp"), 'WEBP', quality=90)

# team headshots -> square, original black & white
team_dir = os.path.join(out, 'team'); os.makedirs(team_dir, exist_ok=True)
for f in glob.glob(os.path.join(src, 'managment', '*.jpeg')):
    n = os.path.basename(f).rsplit('.', 1)[0].lower()
    im = ImageOps.fit(Image.open(f).convert('L'), (800, 800), Image.LANCZOS, centering=(0.5, 0.35))
    im.convert('RGB').save(os.path.join(team_dir, f"{n}.webp"), 'WEBP', quality=82)
print('done')
