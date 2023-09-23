from dataclasses import dataclass,field

import math

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from backend.domain.substance import Substance


@dataclass
class HeatExchanger:
    area_of_exchange: float
    Dbn: Literal[400, 600, 800, 1000, 1200]
    l: Literal[2000, 3000, 4000, 6000, 9000]
    area_tube: float
    area_out_tube: float
    n_ways: Literal[1, 2, 4]
    Dn_tube: Literal[20, 25]
    in_let_s: Substance
    out_let_s: Substance
    tipe: Literal["tn", "xn", "tk", "xk"] = "tn"
    pressure:float=field(init=False)
    avg_dif_temp:float=field(init=False)

    def __post_init__(self):
        self.pressure=self.get_pressure()
        self.avg_dif_temp=self.get_avg_dif_temp()



    def get_pressure(self) -> float:
        p_max= max(self.in_let_s.pressure_work, self.out_let_s.pressure_work)
        if p_max<=0.6: return 0.6
        elif p_max<=1: return 1.0
        elif p_max<= 1.6: return 1.6
        elif p_max<= 2.5: return 2.5
        elif p_max<=4: return 4.0
        else: return 0

    
    def get_avg_dif_temp(self) -> float | None:
        min = self.min_dif_temp()
        max = self.max_dif_temp()
        if max > min and min != 0:
            return round(
                abs(max - min) / math.log(max / min),
                2,
            )
        elif self.max_dif_temp != 0:
            return round(
                abs(min - max) / math.log(min / max),
                2,
            )
        else:
            raise ValueError("Temperature must be greater than 0")

    
    def min_dif_temp(self) -> float:
        return abs(self.in_let_s.t_1 - self.out_let_s.t_2)

    
    def max_dif_temp(self) -> float:
        return abs(self.out_let_s.t_1 - self.in_let_s.t_2)

@dataclass
class MeasuresCooler:
    """Dbn,P,l,L,L_2,l0,A,1,2,Dy_4,Dy_1,Dk,H/2,h,A_0,l_1,l_1(2),l_2_H,l_2_V,lk_H,lk_V,l_3,n_walls"""
    
    L_2:int
    l_0: int
    A:int    
    Dy2: int
    Dy4: int
    Dy: int
    Dk: int
    H_2: int
    h:int
    A_0: int
    l_1:int    
    l_2_H: int
    l_2_V: int
    lk_H: int
    lk_V: int
    l_3: int
    n_walls: int
    

@dataclass
class MeasuresHeater(MeasuresCooler):
    L_1: int
    Dy1: int
    l_1_2:int
