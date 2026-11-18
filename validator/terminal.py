"""Small terminal color helper; redirected output remains plain by default."""

import os
import sys

COLORS = {"PASS": "32", "FAIL": "31", "WARN": "33", "NOT CHECKED": "33"}


def _enable_windows_vt() -> bool:
    if os.name != "nt":
        return True
    try:
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.windll.kernel32
        kernel.GetStdHandle.argtypes = [wintypes.DWORD]
        kernel.GetStdHandle.restype = wintypes.HANDLE
        kernel.GetConsoleMode.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
        kernel.SetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        handle = kernel.GetStdHandle(wintypes.DWORD(-11).value)
        mode = wintypes.DWORD()
        return bool(kernel.GetConsoleMode(handle, ctypes.byref(mode)) and kernel.SetConsoleMode(handle, mode.value | 0x0004))
    except (AttributeError, OSError):
        return False


def use_color(mode: str = "auto") -> bool:
    if mode == "always":
        return True
    if mode == "never" or "NO_COLOR" in os.environ or os.environ.get("TERM") == "dumb":
        return False
    return bool(sys.stdout.isatty() and _enable_windows_vt())


def label(status: str, color: bool) -> str:
    text = f"[{status}]"
    return f"\033[{COLORS[status]}m{text}\033[0m" if color else text
