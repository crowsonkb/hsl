"""Converts colors from HSL (as specified in CSS) to RGB and back."""

from functools import partial
import warnings

import numpy as np
from scipy.optimize import minimize


def tstack(a):
    """Stacks arrays in sequence along the last axis (tail)."""
    a = np.asarray(a)
    return np.concatenate([x[..., np.newaxis] for x in a], axis=-1)


def tsplit(a):
    """Splits arrays in sequence along the last axis (tail)."""
    a = np.asarray(a)
    return np.array([a[..., x] for x in range(a.shape[-1])])


def hue_to_rgb_once(m1, m2, h):
    h %= 1
    if h * 6 < 1:
        return m1 + (m2 - m1) * h * 6
    if h * 2 < 1:
        return m2
    if h * 3 < 2:
        return m1 + (m2 - m1) * (2/3 - h) * 6
    return m1


def hue_to_rgb(m1, m2, h):
    m1m2h = tstack([m1, m2, h])
    return np.apply_along_axis(lambda a: hue_to_rgb_once(*a), -1, m1m2h)


def hsl_to_rgb(hsl):
    """Converts HSL colors to RGB. See
    https://www.w3.org/TR/2018/PR-css-color-3-20180315/#hsl-color. Note that
    the ranges of H, S, and L are 0 to 1.
    """
    h, s, l = tsplit(hsl)
    m1, m2 = np.zeros_like(h), np.zeros_like(h)
    m2 += (l <= 0.5) * l * (s + 1)
    m2 += (l > 0.5) * (l + s - l * s)
    m1 = l * 2 - m2
    r = hue_to_rgb(m1, m2, h + 1/3)
    g = hue_to_rgb(m1, m2, h)
    b = hue_to_rgb(m1, m2, h - 1/3)
    return tstack([r, g, b])


def rgb_to_hsl_once(rgb, eps):
    def loss(hsl):
        rgb2 = hsl_to_rgb(hsl)
        return sum((rgb - rgb2)**2)
    x0 = np.array([0.5, 0.5, 0.5])
    res = minimize(loss, x0, method='L-BFGS-B', bounds=[(0, 1)] * 3,
                   options={'ftol': eps**2})
    hsl = res.x
    min_loss = loss(hsl)
    if min_loss > eps:
        warnings.warn(f'min_loss {min_loss:.3e} > {eps:.3e}')
    if hsl[2] < eps or hsl[2] > 1 - eps:
        hsl[1] = 0
    if hsl[1] < eps:
        hsl[0] = 0
    return hsl


def rgb_to_hsl(rgb, eps=1e-6):
    """Converts RGB colors back to HSL."""
    rgb = np.asarray(rgb)
    return np.apply_along_axis(partial(rgb_to_hsl_once, eps=eps), -1, rgb)
