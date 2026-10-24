"""Lightweight fallback for WeTextProcessing when pynini is unavailable on the Colab VM. Pass-through: numbers/abbreviations are NOT spelled out -
write numbers as Chinese characters in the script (e.g. 二十六號, not 26號)."""


class Normalizer:
    def __init__(self, *a, **k):
        pass

    def normalize(self, text):
        return text
