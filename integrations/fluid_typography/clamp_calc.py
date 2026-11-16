import time
from typing import Dict, Tuple

class FluidTypographyCalculator:
    """
    Computes CSS clamp() expressions for responsive typography.
    clamp(min_rem, preferred_vw, max_rem)
    """
    def __init__(self, min_viewport: int = 320, max_viewport: int = 1440, base_font_size: int = 16):
        self.min_vp = min_viewport
        self.max_vp = max_viewport
        self.base_font_size = base_font_size

    def calculate_clamp(self, min_px: float, max_px: float) -> str:
        # slope = (max - min) / (max_vp - min_vp)
        slope = (max_px - min_px) / (self.max_vp - self.min_vp)
        # intercept in px = min_px - slope * min_vp
        y_intercept_px = min_px - (slope * self.min_vp)
        
        slope_vw = slope * 100
        intercept_rem = y_intercept_px / self.base_font_size
        min_rem = min_px / self.base_font_size
        max_rem = max_px / self.base_font_size

        return f"clamp({min_rem:.3f}rem, {intercept_rem:.3f}rem + {slope_vw:.2f}vw, {max_rem:.3f}rem)"

    def generate_typography_scale(self) -> Dict[str, str]:
        scales = {
            "font_size_display": (28, 48),
            "font_size_h1": (22, 34),
            "font_size_h2": (18, 26),
            "font_size_h3": (16, 20),
            "font_size_body": (14, 16),
            "font_size_mono_formula": (13, 17),
            "font_size_caption": (11, 13)
        }
        return {key: self.calculate_clamp(min_p, max_p) for key, (min_p, max_p) in scales.items()}

def benchmark_clamp():
    calc = FluidTypographyCalculator()
    t0 = time.perf_counter()
    scale = calc.generate_typography_scale()
    t1 = time.perf_counter()
    latency_us = (t1 - t0) * 1_000_000
    print(f"[BENCHMARK] Clamp typography scale generated in {latency_us:.2f}µs: {len(scale)} rules")
    for k, v in scale.items():
        print(f"  --cbt-fluid-{k.replace('_', '-')}: {v};")
    return latency_us

if __name__ == "__main__":
    benchmark_clamp()
