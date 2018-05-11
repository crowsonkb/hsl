import pyparsing as pp
from pyparsing import pyparsing_common as ppc

from hsl import hsl_to_rgb, rgb_to_hsl


class CSSColor:
    def __init__(self, space, a, b, c, d=1):
        self.space = space
        self.value = [a, b, c, d]

    def as_hsl(self):
        if self.space == 'hsl':
            h, s, l, _ = self.value
        if self.space == 'rgb':
            h, s, l = rgb_to_hsl(self.value[:3])
        return f'hsl({h * 360:.1f}, {s * 100:.1f}%, {l * 100:.1f}%)'

    def as_hsla(self):
        if self.space == 'hsl':
            h, s, l, _ = self.value
        if self.space == 'rgb':
            h, s, l = rgb_to_hsl(self.value[:3])
        a = self.value[3]
        return f'hsla({h * 360:.1f}, {s * 100:.1f}%, {l * 100:.1f}%, {a * 100:.1f}%)'

    def as_rgb(self):
        if self.space == 'rgb':
            r, g, b, _ = self.value
        if self.space == 'hsl':
            r, g, b = hsl_to_rgb(self.value[:3])
        return f'rgb({r * 100:.1f}%, {g * 100:.1f}%, {b * 100:.1f}%)'

    def as_rgba(self):
        if self.space == 'rgb':
            r, g, b, _ = self.value
        if self.space == 'hsl':
            r, g, b = hsl_to_rgb(self.value[:3])
        a = self.value[3]
        return f'rgba({r * 100:.1f}%, {g * 100:.1f}%, {b * 100:.1f}%, {a * 100:.1f}%)'


class CSSColorParser:
    def __init__(self):
        self.parser = self._build_parser()

    @staticmethod
    def _build_parser():
        def parse_float_or_percent(t):
            v = float(t[0])
            if t.percent:
                return v / 100
            return v

        float_or_percent = (ppc.fnumber + pp.Literal('%')('percent')) | ppc.fnumber
        float_or_percent.addParseAction(parse_float_or_percent)

        def list_parser(space, n):
            def parse(toks):
                if len(toks) != n:
                    raise pp.ParseFatalException('Invalid number of values in list.')
                if space == 'hsl':
                    toks[0] /= 360
                return (space,) + tuple(toks)
            return parse

        hsl_color = pp.Suppress('hsl(') + pp.delimitedList(float_or_percent) + pp.Suppress(')')
        hsl_color.addParseAction(list_parser('hsl', 3))
        hsla_color = pp.Suppress('hsla(') + pp.delimitedList(float_or_percent) + pp.Suppress(')')
        hsla_color.addParseAction(list_parser('hsl', 4))

        rgb_color = pp.Suppress('rgb(') + pp.delimitedList(float_or_percent) + pp.Suppress(')')
        rgb_color.addParseAction(list_parser('rgb', 3))
        rgba_color = pp.Suppress('rgba(') + pp.delimitedList(float_or_percent) + pp.Suppress(')')
        rgba_color.addParseAction(list_parser('rgb', 4))

        def parse_hex_color(t):
            s = t[0]
            if len(s) not in (3, 4, 6, 8):
                return pp.ParseFatalException('Invalid number of hex characters.')
            if len(s) == 3 or len(s) == 4:
                return ('rgb',) + tuple(int(ch+ch, 16) / 255 for ch in t[0])
            if len(s) == 6 or len(s) == 8:
                r = int(s[0:2], 16) / 255
                g = int(s[2:4], 16) / 255
                b = int(s[4:6], 16) / 255
            if len(s) == 8:
                a = int(s[6:8], 16) / 255
                return 'rgb', r, g, b, a
            return 'rgb', r, g, b

        hex_color = pp.Suppress('#') + pp.Word(pp.hexnums)
        hex_color.addParseAction(parse_hex_color)

        color = hex_color ^ rgb_color ^ rgba_color ^ hsl_color ^ hsla_color
        return color

    def parse(self, s):
        result = self.parser.parseString(s, parseAll=True)[0]
        return CSSColor(*result)
