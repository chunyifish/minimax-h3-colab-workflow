"""Speech-to-text with faster-whisper on the Colab VM.

Prerequisites: faster-whisper installed in the Colab VM; models cached under /content/AI/Voice/models/whisper.

Usage:
  python tools/stt.py --audio in.wav --outdir out [--model large-v3] [--language zh|auto]

Writes <outdir>/transcript.txt, transcript.srt and transcript.json.
"""
import argparse
import json
import sys
import os
from pathlib import Path

MODEL_CACHE = Path(os.environ.get("AI_ROOT", "/content/AI")) / "Voice" / "models" / "whisper"
DEFAULT_PROMPT = "繁體中文，教學、AI 影片製作、ComfyUI、MiniMax H3。"


def _add_cuda_dll_dirs():
    """ctranslate2 needs CUDA 12 runtime DLLs (cublas/cudnn). Make them discoverable."""
    import os
    import site
    roots = []
    for sp in site.getsitepackages() + [site.getusersitepackages()]:
        roots.append(Path(sp) / "nvidia")
    if os.name != "nt":  # Linux/Colab: LD_LIBRARY_PATH is only read at start-up, so preload the pip CUDA 12 libs (2026-10-10)
        import ctypes
        libs = [so for root in roots if root.is_dir()
                for pat in ("cublas/lib/libcublasLt.so.*", "cublas/lib/libcublas.so.*", "cuda_nvrtc/lib/libnvrtc.so.*", "cudnn/lib/libcudnn*.so.*")
                for so in sorted(root.glob(pat))]
        for _ in range(3):  # cudnn sub-libraries depend on each other: retry until no progress
            left = []
            for so in libs:
                try:
                    ctypes.CDLL(str(so), mode=ctypes.RTLD_GLOBAL)
                except OSError:
                    left.append(so)
            if len(left) in (0, len(libs)):
                break
            libs = left
        return
    for root in roots:
        if not root.is_dir():
            continue
        for sub in root.iterdir():
            bindir = sub / "bin"
            if bindir.is_dir():
                os.environ["PATH"] = str(bindir) + os.pathsep + os.environ.get("PATH", "")
                try:
                    os.add_dll_directory(str(bindir))
                except Exception:
                    pass



def fmt_ts(seconds: float, comma: bool = False) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    sep = "," if comma else "."
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def main() -> int:
    if os.environ.get("COLAB_RUNTIME") != "1":
        print("Speech-to-text is supported only in the Colab VM.", file=sys.stderr)
        return 2
    ap = argparse.ArgumentParser(description="Transcribe audio on the Colab VM with faster-whisper.")
    ap.add_argument("--audio", required=True)
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--language", default="zh", help="'auto' to detect")
    ap.add_argument("--prompt", default=DEFAULT_PROMPT)
    ap.add_argument("--beam-size", type=int, default=5)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--compute-type", default="float16")
    a = ap.parse_args()

    audio = Path(a.audio)
    if not audio.is_file():
        print(f"audio not found: {audio}", file=sys.stderr)
        return 2
    outdir = Path(a.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    try:
        _add_cuda_dll_dirs()
        from faster_whisper import WhisperModel
    except ImportError:
        print("faster-whisper is not installed in this Colab environment.", file=sys.stderr)
        return 3

    model = WhisperModel(a.model, device=a.device, compute_type=a.compute_type,
                         download_root=str(MODEL_CACHE), local_files_only=True)
    segments, info = model.transcribe(
        str(audio),
        language=None if a.language == "auto" else a.language,
        beam_size=a.beam_size,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
        condition_on_previous_text=False,
        initial_prompt=a.prompt,
    )

    rows = []
    for seg in segments:
        rows.append({"start": round(seg.start, 3), "end": round(seg.end, 3), "text": seg.text.strip()})
        print(f"[{fmt_ts(seg.start)} -> {fmt_ts(seg.end)}] {seg.text.strip()}", flush=True)

    (outdir / "transcript.json").write_text(json.dumps(
        {"audio": str(audio), "model": a.model, "language": info.language,
         "language_probability": info.language_probability, "duration": info.duration, "segments": rows},
        ensure_ascii=False, indent=2), encoding="utf-8")
    (outdir / "transcript.txt").write_text("\n".join(r["text"] for r in rows) + "\n", encoding="utf-8")
    srt = [f"{i}\n{fmt_ts(r['start'], True)} --> {fmt_ts(r['end'], True)}\n{r['text']}\n" for i, r in enumerate(rows, 1)]
    (outdir / "transcript.srt").write_text("\n".join(srt), encoding="utf-8")

    print(f"[done] segments={len(rows)} duration={info.duration:.1f}s language={info.language} -> {outdir}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
