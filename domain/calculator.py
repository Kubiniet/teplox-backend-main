from typing import Literal

from dataclasses import dataclass,field

import math

from domain.substance import Substance
from domain.exchanger import HeatExchanger


@dataclass
class PreliminarCalc:
    const_exchange: int
    in_sub: Substance
    out_sub: Substance
    exchanger_type:Literal["tn", "xn", "tk", "xk"] = "tn"
    correction_factor: float = 1.0
    coef_P: float=field(init=False)
    coef_R: float=field(init=False)
    area_of_exchange: float=field(init=False)
    avg_dif_temp:float=field(init=False)
    max_dif_temp: float=field(init=False)
    min_dif_temp: float=field(init=False)


    def __post_init__(self):
        self.coef_P=self.get_coef_P()
        self.coef_R=self.get_coef_R()        
        self.max_dif_temp=self.get_max_dif_temp()
        self.min_dif_temp=self.get_min_dif_temp()
        self.avg_dif_temp=self.get_avg_dif_temp()
        self.area_of_exchange=self.get_area_of_exchange()

    
    def get_coef_P(self) -> float:
        return round(
            abs(
                (self.out_sub.t_2 - self.out_sub.t_1)
                / (self.in_sub.t_1 - self.out_sub.t_1)
            )
            * self.correction_factor,
            2,
        )

    
    def get_coef_R(self) -> float:
        return round(
            abs(
                (self.in_sub.t_1 - self.in_sub.t_2)
                / (self.out_sub.t_2 - self.out_sub.t_1)
            )
            * self.correction_factor,
            2,
        )

   
    def get_area_of_exchange(self) -> float:
        k = self.const_exchange
        return round(self.in_sub.thermal_power / (k * self.avg_dif_temp), 2)

    
    def get_avg_dif_temp(self) -> float | None:
        min = self.min_dif_temp
        max = self.max_dif_temp
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

    
    def get_min_dif_temp(self) -> float:
        return abs(self.in_sub.t_1 - self.out_sub.t_2)

    
    def get_max_dif_temp(self) -> float:
        return abs(self.out_sub.t_1 - self.in_sub.t_2)


@dataclass
class PostCalc:
    
    he: HeatExchanger
    avg_dif_tem: float
    pollution: float = 0.0002
    wall_tr: float = 40
    n_tube_calc:float=field(init=False)
    vel_flow_in:float=field(init=False)
    vel_flow_out:float=field(init=False)
    num_reynolds_in:float=field(init=False)
    num_reynolds_out: float=field(init=False)
    mode_flow_in: str=field(init=False)
    mode_flow_out:str=field(init=False)
    relation_reynold_in:float=field(init=False)
    relation_reynold_out:float=field(init=False)
    num_prandtla_in:float=field(init=False)
    num_prandtla_out:float=field(init=False)
    num_nusel_in:float=field(init=False)
    num_nusel_out:float=field(init=False)
    heat_transfer_coef_in:float=field(init=False)
    heat_transfer_coef_out:float=field(init=False)
    factor_heat_transfer_calc:float=field(init=False)
    required_area_exchange:float=field(init=False)
    area_margin_percent:float=field(init=False)
    is_good:bool=field(init=False)


    def __post_init__(self):

        self.n_tube_calc=round(self.get_n_tube_calc(),2)
        self.vel_flow_in=round(self.get_vel_flow_in(),2)
        self.vel_flow_out=round(self.get_vel_flow_out(),2)
        self.num_reynolds_in=round(self.get_num_reynolds_in(),2)
        self.num_reynolds_out=round(self.get_num_reynolds_out(),2)
        self.mode_flow_in=self.get_mode_flow_in()
        self.mode_flow_out=self.get_mode_flow_out()
        self.relation_reynold_in=round(self.get_relation_reynold_in(),2)
        self.relation_reynold_out=round(self.get_relation_reynold_out(),2)
        self.num_prandtla_in=round(self.get_num_prandtla_in(),2)
        self.num_prandtla_out=round(self.get_num_prandtla_out(),2)
        self.num_nusel_in=round(self.get_num_nusel_in(),2)
        self.num_nusel_out=round(self.get_num_nusel_out(),2)
        self.heat_transfer_coef_in=round(self.get_heat_transfer_coef_in(),2)
        self.heat_transfer_coef_out=round(self.get_heat_transfer_coef_out(),2)
        self.factor_heat_transfer_calc=round(self.get_factor_heat_transfer_calc(),2)
        self.required_area_exchange=round(self.get_required_area_exchange(),2)
        self.area_margin_percent=round(self.get_area_margin_percent(),2)
        self.is_good=self.get_is_good()

    
    def get_n_tube_calc(self) -> float:
        a = self.he.area_of_exchange
        return a / (3.1416 * self.he.Dn_tube * self.he.l * 0.000001) + 1

    
    def get_vel_flow_in(self) -> float:
        flow = self.he.in_let_s.flow
        return flow / (self.he.in_let_s.density * self.he.area_tube)
       

    
    def get_vel_flow_out(self) -> float:
        flow = self.he.out_let_s.flow
        return flow / (self.he.out_let_s.density * self.he.area_out_tube)      
    
    def get_num_reynolds_in(self) -> float:
        v = self.he.in_let_s.viscosity * 10**-7
        return self.vel_flow_in * (self.he.Dn_tube - 4) / (1000 * v)
    
    def get_num_reynolds_out(self) -> float:
        v = self.he.out_let_s.viscosity * 10**-7
        return self.vel_flow_out * (self.he.Dn_tube) / (1000 * v)
    
    def get_mode_flow_in(self) -> str:
        if self.num_reynolds_in > 1000:
            return "turb"
        else:
            return "laminar"
    
    def get_mode_flow_out(self) -> str:
        if self.num_reynolds_out > 1000:
            return "turb"
        else:
            return "laminar"
    
    def get_relation_reynold_in(self) -> float:
        if self.he.in_let_s.process == "heating":
            return 1.0
        else:
            return 0.93
    
    def get_relation_reynold_out(self) -> float:
        if self.he.out_let_s.process == "heating":
            return 1.0
        else:
            return 0.93
    
    def get_num_prandtla_in(self) -> float:
        v = self.he.in_let_s.viscosity * 10**-7
        return (
            self.he.in_let_s.heat_capacity
            * self.he.in_let_s.density
            * v
            / self.he.in_let_s.thermal_conduct
        )
    
    def get_num_prandtla_out(self) -> float:
        v = self.he.out_let_s.viscosity * 10**-7
        return (
            self.he.out_let_s.heat_capacity
            * self.he.out_let_s.density
            * v
            / self.he.out_let_s.thermal_conduct
        )
    
    def get_num_nusel_in(self) -> float:
        num = self.num_prandtla_in**0.43 * self.relation_reynold_in
        if self.num_reynolds_in <= 10000:
            return 0.008 * self.num_reynolds_in**0.9 * num
        else:
            return 0.021 * self.num_reynolds_in**0.8 * num

    #   TODO REVISAR numero de nuselt y criterio de flujo
    
    def get_num_nusel_out(self) -> float:
        num = self.num_prandtla_out**0.36 * self.relation_reynold_out * 0.6
        if self.num_reynolds_out <= 1000:
            return 0.56 * self.num_reynolds_out**0.5 * num
        else:
            if self.relation_reynold_in == 1.0:
                return 0.22 * self.num_reynolds_out**0.65 * num
            else:
                
                return 0.4 * self.num_reynolds_out**0.6 * num

    
    def get_heat_transfer_coef_in(self) -> float:
        return round((
            self.num_nusel_in
            * 1000
            * self.he.in_let_s.thermal_conduct
            / (self.he.Dn_tube - 4)
        ),2)

    
    def get_heat_transfer_coef_out(self) -> float:
        return round( (
            self.num_nusel_out
            * 1000
            * self.he.out_let_s.thermal_conduct
            / (self.he.Dn_tube)
        ),2)

    
    def get_factor_heat_transfer_calc(self) -> float:
        a_1 = self.heat_transfer_coef_in
        a_2 = self.heat_transfer_coef_out
        w = self.wall_tr
        la = self.pollution
        return 1 / (1 / a_1 + 1 / a_2 + la + 0.002 / w)

    
    def get_required_area_exchange(self) -> float:
        f = self.factor_heat_transfer_calc
        t = self.avg_dif_tem
        if self.he.in_let_s.thermal_power:
            return self.he.in_let_s.thermal_power / (f * t)
        else:
            return self.he.in_let_s._thermal_power / (f * t)

    
    def get_area_margin_percent(self) -> float:
        f = self.he.area_of_exchange
        return (f - self.required_area_exchange) / f * 100

    
    def get_is_good(self) -> bool:
        if self.area_margin_percent >= 10:
            return True
        else:
            return False