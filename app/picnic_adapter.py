from __future__ import annotations

import ctypes
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"


class PicnicRequest(ctypes.Structure):
    _fields_ = [
        ("count", ctypes.c_int32),
        ("max_weight", ctypes.c_int32),
        ("heat", ctypes.c_int32),
        ("rain", ctypes.c_int32),
        ("weights", ctypes.POINTER(ctypes.c_int32)),
        ("happiness", ctypes.POINTER(ctypes.c_int32)),
        ("heat_penalty", ctypes.POINTER(ctypes.c_int32)),
        ("rain_penalty", ctypes.POINTER(ctypes.c_int32)),
        ("out_mask", ctypes.c_uint32),
        ("out_weight", ctypes.c_int32),
    ]


def _library_path() -> Path:
    suffix = "dylib" if sys.platform == "darwin" else "so"
    return BUILD / f"libpicnic.{suffix}"


def _load_kernel():
    path = _library_path()
    if not path.exists():
        raise RuntimeError(f"missing assembly build output: {path}. Run `make build`.")
    lib = ctypes.CDLL(str(path))
    fn = lib.optimize_picnic_kernel
    fn.argtypes = [ctypes.POINTER(PicnicRequest)]
    fn.restype = ctypes.c_int32
    return fn


_KERNEL = None


def _kernel():
    global _KERNEL
    if _KERNEL is None:
        _KERNEL = _load_kernel()
    return _KERNEL


def optimize_picnic_basket(items: list[dict], constraints: dict) -> dict:
    if len(items) > 20:
        raise ValueError("assembly demo supports at most 20 items")

    count = len(items)
    weights = (ctypes.c_int32 * count)(*[int(item["weight"]) for item in items])
    happiness = (ctypes.c_int32 * count)(*[int(item["happiness"]) for item in items])
    heat_penalty = (ctypes.c_int32 * count)(*[int(item["heat_penalty"]) for item in items])
    rain_penalty = (ctypes.c_int32 * count)(*[int(item["rain_penalty"]) for item in items])

    req = PicnicRequest(
        count=count,
        max_weight=int(constraints["max_weight"]),
        heat=int(constraints.get("heat", 0)),
        rain=int(constraints.get("rain", 0)),
        weights=weights,
        happiness=happiness,
        heat_penalty=heat_penalty,
        rain_penalty=rain_penalty,
        out_mask=0,
        out_weight=0,
    )
    score = int(_kernel()(ctypes.byref(req)))
    selected = [
        item for idx, item in enumerate(items)
        if req.out_mask & (1 << idx)
    ]
    warnings = []
    if req.heat >= 7 and selected:
        warnings.append("hot day: heat penalties applied")
    if req.rain >= 6 and selected:
        warnings.append("rain risk: rain penalties applied")
    return {
        "selected_ids": [str(item["id"]) for item in selected],
        "total_weight": int(req.out_weight),
        "score": score,
        "warnings": warnings,
    }
