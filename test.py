from hsl import hsl_to_rgb


def wrap_with_bg(s, r, g, b):
    params = (48, 2, int(r*255), int(g*255), int(b*255))
    return '\033[{}m{}\033[0m'.format(';'.join(str(p) for p in params), s)


def main():
    for i in range(19):
        h = i / 18
        s, l = 0.75, 0.5
        r, g, b = hsl_to_rgb([h, s, l])
        print(wrap_with_bg(f'{i:2}: hsl({h*100:.1f}%, {s*100:.1f}%, {l*100:.1f}%)', r, g, b))


if __name__ == '__main__':
    main()
