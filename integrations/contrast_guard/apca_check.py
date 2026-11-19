import math
import time
from typing import Tuple, Dict, Any

class APCAContrastValidator:
    """
    Simplified implementation of APCA (Accessible Perceptual Contrast Algorithm)
    designed for high-stakes CBT display readability checks.
    """
    # Exponents for sRGB to Y (luminance)
    MAIN_TRC = 2.4
    R_COEFF = 0.2126729
    G_COEFF = 0.7151522
    B_COEFF = 0.0721750

    @classmethod
    def hex_to_rgb(cls, hex_color: str) -> Tuple[int, int, int]:
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 3:
            hex_color = "".join([c * 2 for c in hex_color])
        return (int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))

    @classmethod
    def srgb_to_y(cls, r: int, g: int, b: int) -> float:
        # Simple sRGB gamma to linear luminance
        r_lin = (r / 255.0) ** cls.MAIN_TRC
        g_lin = (g / 255.0) ** cls.MAIN_TRC
        b_lin = (b / 255.0) ** cls.MAIN_TRC
        return cls.R_COEFF * r_lin + cls.G_COEFF * g_lin + cls.B_COEFF * b_lin

    @classmethod
    def calculate_lc(cls, txt_hex: str, bg_hex: str) -> float:
        """
        Calculates Lightness Contrast (Lc) value between text and background.
        Returns float between -108 and +108. Positive: dark text on light bg; Negative: light text on dark bg.
        """
        r_txt, g_txt, b_txt = cls.hex_to_rgb(txt_hex)
        r_bg, g_bg, b_bg = cls.hex_to_rgb(bg_hex)

        y_txt = cls.srgb_to_y(r_txt, g_txt, b_txt)
        y_bg = cls.srgb_to_y(r_bg, g_bg, b_bg)

        # Soft clamping for black clamp
        if y_txt < 0.022:
            y_txt += (0.022 - y_txt) ** 1.414
        if y_bg < 0.022:
            y_bg += (0.022 - y_bg) ** 1.414

        # Dark mode: text is lighter than bg
        if y_txt > y_bg:
            c = ((y_txt ** 0.56) - (y_bg ** 0.65)) * 1.14159265358979323846
            lc = (c - 0.027) * 100.0 if c > 0.027 else 0.0
        else:
            # Light mode: bg is lighter than text
            c = ((y_txt ** 0.62) - (y_bg ** 0.56)) * 1.14159265358979323846
            lc = (c + 0.027) * 100.0 if c < -0.027 else 0.0

        return abs(round(lc, 1))

    @classmethod
    def evaluate(cls, txt_hex: str, bg_hex: str, min_lc: float = 75.0) -> Dict[str, Any]:
        lc = cls.calculate_lc(txt_hex, bg_hex)
        passed = lc >= min_lc
        return {
            "text": txt_hex,
            "background": bg_hex,
            "contrast_lc": lc,
            "min_required_lc": min_lc,
            "passed": passed,
            "rating": "OPTIMAL_READABILITY" if lc >= 75 else ("READABLE" if lc >= 60 else "FAIL_FATIGUE_RISK")
        }

def benchmark_apca():
    validator = APCAContrastValidator()
    # Test primary ClockEE colors
    pairs = [
        ("#f8fafc", "#07090e"), # Primary white on obsidian
        ("#f59e0b", "#07090e"), # Amber accent on obsidian
        ("#94a3b8", "#0d111a"), # Secondary slate on card
        ("#64748b", "#0d111a"), # Muted gray on card
    ]
    t0 = time.perf_counter()
    results = [validator.evaluate(t, b) for t, b in pairs]
    t1 = time.perf_counter()
    latency_us = ((t1 - t0) / len(pairs)) * 1_000_000

    print(f"[BENCHMARK] APCA calculation: {latency_us:.2f}µs per color pair")
    for r in results:
        print(f"  {r['text']} on {r['background']}: Lc {r['contrast_lc']} -> {r['rating']} (Passed: {r['passed']})")
    return latency_us

if __name__ == "__main__":
    benchmark_apca()
