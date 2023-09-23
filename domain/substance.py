from dataclasses import dataclass, field
from typing import Optional
import math

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


@dataclass
class SimpleSubstance:
    
    name: str
    t_1: float
    t_2: float
    avg_temp: float=field(init=False)
    process:Literal["heating", "cooling"]=field(init=False)

    
    def get_avg_temp(self) -> float | None:
        t_1 = self.t_1
        t_2 = self.t_2
        if t_1 > t_2 and t_2 != 0:
            return round(abs(t_1 - t_2) / math.log(t_1 / t_2), 2)
        elif t_1 != 0:
            return round(abs(t_1 - t_2) / math.log(t_2 / t_1), 2)
        else:
            return ValueError("Temperature must be greater than 0")

    
    def get_process(self) -> Literal["heating", "cooling"]:
        if self.t_1 <= self.t_2:
            return "heating"
        else:
            return "cooling"


@dataclass
class PropertiesSubstance:
    pressure_work: float
    heat_capacity: float
    density: float
    viscosity: float
    thermal_conduct: float


@dataclass
class Substance(PropertiesSubstance,SimpleSubstance):
    flow: Optional[float] = field(default=None)
    thermal_power: Optional[float] = field(default=None)
    where: Literal["inlet", "outlet"] = "inlet"

    def __post_init__(self):
        self.avg_temp=self.get_avg_temp()
        self.process=self.get_process()

        if self.flow is None:
            self.flow=self.get_flow()
        else:
            self.thermal_power=self.get_thermal_power()

    
    def get_thermal_power(self) -> float | None:
        t_1 = self.t_1
        t_2 = self.t_2
        if self.flow is not None:
            thermal_power = round(
                abs(self.heat_capacity * self.flow * (t_1 - t_2)), 2
            )
            return thermal_power
        else:
            return None
            
    def get_flow(self):
        if self.thermal_power is not None:
            delta = self.heat_capacity * abs((self.t_1 - self.t_2))
            t = self.thermal_power
            flow = round(t / delta, 2)
            return flow
        else:
            return None