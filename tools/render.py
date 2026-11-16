import sys, glob
from PIL import Image, ImageDraw, ImageFont
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
def render(txt, png):
    f = ImageFont.truetype(FONT, 16)
    lines = open(txt, errors="replace").read().rstrip("\n").split("\n")
    lines = [l.replace("\t", "    ")[:130] for l in lines][:45]
    w = max(700, max(len(l) for l in lines) * 10 + 30)
    h = len(lines) * 22 + 60
    im = Image.new("RGB", (w, h), (24, 24, 24))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, 28], fill=(60, 60, 60))
    d.text((12, 5), "pradumn@2024UCD2124: ~/CN-Lab", font=f, fill=(220, 220, 220))
    y = 40
    for l in lines:
        col = (120, 220, 120) if l.startswith("pradumn@") else (230, 230, 230)
        d.text((14, y), l, font=f, fill=col)
        y += 22
    im.save(png)
for t in glob.glob(sys.argv[1] + "/*.txt"):
    render(t, t[:-4] + ".png")
