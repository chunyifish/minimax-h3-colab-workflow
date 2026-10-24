"""Colab VM font paths (installed by cloud/vm/install_full.sh).
Override any of them with env FONT_KAI / FONT_JH / FONT_JHBD / SUB_FONT_NAME."""
import os

_C = {
    "kai": ["/usr/share/fonts/truetype/arphic/ukai.ttc", "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"],
    "jh": ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"],
    "jhbd": ["/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"],
}


def font(kind):
    """Path of the first font of this kind that exists ('kai' title, 'jh' regular, 'jhbd' bold)."""
    env = os.environ.get("FONT_" + kind.upper())
    if env:
        return env
    for p in _C[kind]:
        if os.path.exists(p):
            return p
    return _C[kind][0]


# family name for libass subtitles (ffmpeg subtitles= filter / ASS Style lines)
SUB_FONT_NAME = os.environ.get("SUB_FONT_NAME", "Noto Sans CJK TC")
