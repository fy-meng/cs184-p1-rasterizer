import re
import sys

DEFAULT_SIDE = 800

width_pattern = 'width="([0-9]+)(px)?"'
height_pattern = 'height="([0-9]+)(px)?"'
rgb_pattern = 'rgb\(([0-9]*), ([0-9]*), ([0-9]*)\)'
delete_pattern = 'stroke=[^/<>]*stroke-linejoin="miter"'
point_pattern = '([0-9]+),([0-9]+)'


def str2hex(match):
    return '#{:02X}{:02X}{:02X}'.format(int(match.group(1)), int(match.group(2)), int(match.group(3)))


def scaling(match, scale):
    x, y = int(match.group(1)) * scale, int(match.group(2)) * scale
    return '{:.4},{:.4}'.format(x, y)


def convert(filename):
    with open('svg/custom/' + filename + '.svg', 'r') as f:
        s = f.read()

        s = re.sub(rgb_pattern, str2hex, s)

        s = re.sub(delete_pattern, '', s)

        width = int(re.search(width_pattern, s).group(1))
        height = int(re.search(height_pattern, s).group(1))
        scale = DEFAULT_SIDE / max(width, height)
        s = re.sub(point_pattern, lambda match: scaling(match, scale), s)

        s = re.sub(width_pattern, lambda match: 'width="{}px"'.format(str(int(match.group(1)) * scale)), s)
        s = re.sub(height_pattern, lambda match: 'height="{}px"'.format(str(int(match.group(1)) * scale)), s)

    with open('svg/custom/' + filename + '_new.svg', 'w+') as f_new:
        f_new.write(s)


def __main__():
    if len(sys.argv) != 2:
        raise Exception("usage: python3 svg_convert.py FILENAME")
    convert(sys.argv[1])

__main__()
