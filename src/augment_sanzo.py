import json
import cmyk_icc as icc
from collections import OrderedDict
import os

dirname = os.path.dirname(os.path.abspath(__file__))

iccCMYK = os.path.join(dirname, 'data', 'icc', 'cmyk', 'U.S. Web Coated (SWOP) v2.icc')
iccRGB = os.path.join(dirname, 'data', 'icc', 'RGB', 'sRGB IEC61966-2.1.icc')
intent = icc.RELATIVE_COLORIMETRIC

def to_hex (rgb):
  rgb = [ max(0, min(255, round(n))) for n in rgb ]
  [ r, g, b ] = rgb
  return "#{0:02x}{1:02x}{2:02x}".format(r, g, b)

colors = []
palettes = {}
def add_to_palette (palette_id, index):
  if palette_id in palettes:
    palettes[palette_id].append(index)
  else:
    palettes[palette_id] = [ index ]

files = [ os.path.join(dirname, 'data', 'swatches', s) for s in [
  'swatches_a.json',
  'swatches_b.json',
  'swatches_c.json',
  'swatches_d.json',
  'swatches_e.json',
  'swatches_f.json'
] ]

for i, file in enumerate(files):
  with open(file) as json_file:
    print('Loading', file)
    swatch = json.load(json_file)
    key = [ d for d in dict.keys(swatch) ][0]
    for color in swatch[key]:
      name = color['name']
      cmyk = color['cmyk']
      combinations = color['combinations']
      rgb = icc.cmyk2rgb(cmyk, profile_rgb=iccRGB, profile_cmyk=iccCMYK, intent=intent)
      lab = icc.cmyk2lab(cmyk, profile_cmyk=iccCMYK, intent=intent)
      hex = to_hex(rgb)
      newColor = {
        'name': name,
        'combinations': combinations,
        'swatch': i,
        'cmyk': cmyk,
        'lab': lab,
        'rgb': rgb,
        'hex': hex
      }
      index = len(colors)
      colors.append(newColor)
      for palette_id in combinations:
        add_to_palette(palette_id, index)

out_data = colors
out_file = os.path.join(dirname, '../', 'colors.json')
with open(out_file, 'w') as outfile:
  json.dump(out_data, outfile, indent=2)

print('Total Colors', len(colors))
print('Total Combinations', len(palettes.values()))