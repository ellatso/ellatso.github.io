from typing import Union

def clamp_duration(x: Union[int,float], lo: float, hi: float) -> float:
    return float(max(lo, min(hi, x)))
