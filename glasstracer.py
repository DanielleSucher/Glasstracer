import argparse
from glassworld import World

parser = argparse.ArgumentParser(description='See what any image will look ' +
    'like through a slab of glass of the given thickness.')
parser.add_argument('--img', '-i',
                   help='the image you want to distort, ie "-i image.jpg"')
parser.add_argument('--th', '-t',
                   help='the thickness of the glass in centimeters, ' +
                   'ie "-t 100"')
args = parser.parse_args()


w = World(args.img)

w.render_image(args.img[:-4] + "-refracted" + args.img[-4:])
