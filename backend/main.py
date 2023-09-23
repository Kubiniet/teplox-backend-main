from typing import Union,List
from dataclasses import asdict

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from web.schemas import SubstanceInput,MeasuresOutput,SubstanceOutput,PreliminarCalcInput,PostCalcOutput
from domain.substance import Substance
from domain.calculator import PreliminarCalc
from usecases.get_heatexchanger_by_area import Heaters

app = FastAPI()

origins=["http://127.0.0.1:8000","http://127.0.0.1:3000","http://localhost:4000","*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
     allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )

@app.put("/substance/{subs_id}",response_model=SubstanceOutput)
def create_substance(new_substance: SubstanceInput,):
    new_sub=Substance(**new_substance.dict())
    return new_sub

@app.put("/heaters",response_model=List[PostCalcOutput])
def get_heaters(pre_calc: PreliminarCalcInput):
    in_sub=Substance(**pre_calc.in_sub.dict())
    out_sub=Substance(**pre_calc.out_sub.dict())
    k=pre_calc.const_exchange
    calc=PreliminarCalc(in_sub=in_sub,out_sub=out_sub,const_exchange=k)
    heaters=Heaters(calc)
    hes=  heaters.hes    
    return hes

@app.put("/heaters/measures")
def get_measures(pre_calc: PreliminarCalcInput):
    in_sub=Substance(**pre_calc.in_sub.dict())
    out_sub=Substance(**pre_calc.out_sub.dict())
    k=pre_calc.const_exchange
    calc=PreliminarCalc(in_sub=in_sub,out_sub=out_sub,const_exchange=k)
    heaters=Heaters(calc)
    hes=  heaters.measures
    com= heaters.num_comp
    meas=MeasuresOutput(measures=hes,compensators=com)
    return meas
