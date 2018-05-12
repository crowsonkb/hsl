#!/usr/bin/env python3

"""Converts colors from HSL (as specified in CSS) to RGB and back."""

import argparse
import sys

from hsl import CSSColorParser, ParseBaseException


try:
    from IPython.core import ultratb
    sys.excepthook = ultratb.ColorTB()
except ImportError:
    pass


def main():
    """The main function."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        '-t', choices=('hsl', 'hsla', 'rgb', 'rgba'), required=True,
        help='convert to hsl(a) or rgb(a)')
    args = ap.parse_args()

    p = CSSColorParser()
    while True:
        try:
            color = p.parse(input())
            out = getattr(color, 'as_' + args.t)()
            print(out)
        except ParseBaseException as err:
            # print(f'{err.__class__.__name__}: {err}', file=sys.stderr)
            sys.excepthook(err)
            continue
        except (EOFError, KeyboardInterrupt):
            break


if __name__ == '__main__':
    main()
