from pydantic import BaseModel

from typing import Literal,Union,List


class SubstanceInput(BaseModel):
   
    name: str
    t_1: float
    t_2: float
    pressure_work: float
    heat_capacity: float
    density: float
    viscosity: float
    thermal_conduct: float
    flow:float|None=None
    thermal_power: float|None=None
    where: Literal["inlet", "outlet"]

class SubstanceOutput(BaseModel):
    
    name: str
    t_1: float
    t_2: float
    pressure_work: float
    heat_capacity: float
    density: float
    viscosity: float
    thermal_conduct: float
    flow:float|None
    thermal_power: float|None
    where: Literal["inlet", "outlet"] 
    avg_temp: float|None
    process:Literal["heating", "cooling"]


class PreliminarCalcInput(BaseModel):
    const_exchange: int
    in_sub: SubstanceInput
    out_sub: SubstanceInput

class HeatExchanger(BaseModel):
    area_of_exchange: float
    Dbn: Literal[400, 600, 800, 1000, 1200]
    l: Literal[2000, 3000, 4000, 6000, 9000]
    area_tube: float
    area_out_tube: float
    n_ways: Literal[1, 2, 4]
    Dn_tube: Literal[20, 25]
    in_let_s: SubstanceOutput
    out_let_s: SubstanceOutput
    tipe: Literal["tn", "xn", "tk", "xk"]
    pressure:float
    avg_dif_temp:float

class PostCalcOutput(BaseModel):
    
    he: HeatExchanger
    avg_dif_tem: float
    pollution: float 
    wall_tr: float 
    n_tube_calc:float
    vel_flow_in:float
    vel_flow_out:float
    num_reynolds_in:float
    num_reynolds_out: float
    mode_flow_in: str
    mode_flow_out:str
    relation_reynold_in:float
    relation_reynold_out:float
    num_prandtla_in:float
    num_prandtla_out:float
    num_nusel_in:float
    num_nusel_out:float
    heat_transfer_coef_in:float
    heat_transfer_coef_out:float
    factor_heat_transfer_calc:float
    required_area_exchange:float
    area_margin_percent:float
    is_good:bool


class MeasuresCooler(BaseModel):
   
    
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
    


class MeasuresHeater(MeasuresCooler):
    L_1: int
    Dy1: int
    l_1_2:int

class MeasuresOutput(BaseModel):
    measures: List[ Union[MeasuresCooler,MeasuresHeater]]
    compensators: List[int]