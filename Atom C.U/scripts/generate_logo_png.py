from PIL import Image, ImageDraw, ImageFont
import os

out_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'AtomC.U.png')

# size and colors
size = (512, 512)
start = (11, 102, 255)  # #0b66ff
end = (255, 122, 24)   # #ff7a18

img = Image.new('RGB', size, start)
draw = ImageDraw.Draw(img)

# vertical gradient
for y in range(size[1]):
    t = y / (size[1] - 1)
    r = int(start[0] + (end[0] - start[0]) * t)
    g = int(start[1] + (end[1] - start[1]) * t)
    b = int(start[2] + (end[2] - start[2]) * t)
    draw.line([(0, y), (size[0], y)], fill=(r, g, b))

# rounded rect mask
mask = Image.new('L', size, 0)
md = ImageDraw.Draw(mask)
radius = 48
md.rounded_rectangle([0,0,size[0],size[1]], radius=radius, fill=255)
img.putalpha(mask)

# draw text
try:
    font_big = ImageFont.truetype('arial.ttf', 200)
    font_small = ImageFont.truetype('arial.ttf', 28)
except Exception:
    font_big = ImageFont.load_default()
    font_small = ImageFont.load_default()

# center 'AC'
text = 'AC'
bbox = draw.textbbox((0,0), text, font=font_big)
w = bbox[2] - bbox[0]
h = bbox[3] - bbox[1]
draw.text(((size[0]-w)/2, (size[1]-h)/2-20), text, font=font_big, fill=(255,255,255))

# small label
label = 'Atom C.U'
bbox2 = draw.textbbox((0,0), label, font=font_small)
w2 = bbox2[2] - bbox2[0]
h2 = bbox2[3] - bbox2[1]
draw.text(((size[0]-w2)/2, (size[1]-h)/2+150), label, font=font_small, fill=(255,255,255))

# save as PNG (flatten alpha onto background for compatibility)
bg = Image.new('RGB', size, (255,255,255))
bg.paste(img, mask=img.split()[3])
bg.save(out_path)
print('Saved', out_path)
