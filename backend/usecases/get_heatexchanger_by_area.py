import pandas as pd
import numpy as np

from typing import List
from typing_extensions import Self


from backend.domain.exchanger import HeatExchanger,MeasuresHeater,MeasuresCooler
from backend.domain.calculator import PostCalc, PreliminarCalc

from backend.repository.get_df import GetDF

class Heaters:
    def __init__(self,precalc:PreliminarCalc) -> None:
        self.precalc=precalc
        self.hes=self.filter_by_area()
        self.measures=self.get_exchanger_measures()
        self.num_comp=self.get_compensators()


    def filter_by_area(
        self: Self, df:pd.DataFrame = GetDF.get_df_area_xn_tn()
    ) -> List[PostCalc]:
        """_summary_

        Args:
            df (pd.DataFrame): dataframe
            pre_calc (PreliminarCalc): preliminar calculator
            with the next params    area (float)
                                    delta (float)
                                    in_let_s  (Substance)
                                    out_let_s (Substance)

        Returns:
            List[PostCalc]: return a list of postcalculators with the heatexchanger
        """
        pre_calc=self.precalc
        hes = []
        count = 0
        while len(hes) < 3:
            if len(df[df["area"] > pre_calc.area_of_exchange]) > count:
                he = df[df["area"] > pre_calc.area_of_exchange].iloc[count]
                device = HeatExchanger(
                    tipe=pre_calc.exchanger_type,
                    area_of_exchange=he["area"],
                    n_ways=he["n_ways"],
                    Dbn=he["Db"],
                    Dn_tube=he["dn_tube"],
                    l=he["L"] * 1000,
                    area_tube=he["S_inlet"],
                    in_let_s=pre_calc.in_sub,
                    out_let_s=pre_calc.out_sub,
                    area_out_tube=he["S_outlet"],
                )
                calc_2 = PostCalc(
                    he=device,
                    avg_dif_tem=pre_calc.avg_dif_temp,
                )

                if calc_2.is_good:
                    hes.append(calc_2)
            else:
                return hes
            count += 1
        return hes


    def get_exchanger_measures(self,df_tn:pd.DataFrame = GetDF.get_df_tn_measures(),df_xn:pd.DataFrame = GetDF.get_df_xn_measures())->MeasuresHeater|MeasuresCooler:
        
        measures=[]
       
        if self.hes:
            for h in self.hes:
                
                if h.he.tipe == "tn" or h.he.tipe == "tk":
                    df=df_tn
                    D=df["Dbn"]==h.he.Dbn
                    l=df["l"]==h.he.l
                    p=df["P"].str.contains(str(h.he.pressure))
                    he=df[D&p&l]
                    if he.empty:
                        measures.append(None)
                    else:
                        measure=MeasuresHeater(
                            L_1=he["L"].values[0],
                            L_2=he["L_2"].values[0],
                            l_0=he["l0"].values[0],
                            A=he["A1"].values[0],
                            Dy1=he["Dy1"].values[0],
                            Dy2=he["Dy1"].values[0],
                            Dy4=he["Dy4"].values[0],
                            Dy=he["Dy_1"].values[0],
                            Dk=he["Dk"].values[0],
                            H_2=he["H_2"].values[0],
                            h=he["h"].values[0],
                            A_0=he["A_0"].values[0],
                            l_1=he["l_1"].values[0],
                            l_1_2=he["l_1(2)"].values[0],
                            l_2_H=he["l_2_H"].values[0],
                            l_2_V=he["l_2_V"].values[0],
                            lk_H=he["lk_H"].values[0],
                            lk_V=he["lk_V"].values[0],
                            l_3=he["l_3"].values[0],
                            n_walls=he["n_walls"].values[0],
                        )
                        measures.append(measure)
                    
                else:
                    df=df_xn
                    D=df["Dbn"]==he.Dbn
                    l=df["l"]==he.l
                    p=df["P"].str.contains(str(he.pressure))
                    he=df[D&p&l]
                    if he.empty:
                        measures.append(None)
                    else:
                        measure=MeasuresCooler(
                            L_2=he["L_2"].values[0],
                            l_0=he["l0"].values[0],
                            A=he["A1"].values[0],        
                            Dy2=he["Dy2"].values[0],
                            Dy4=he["Dy4"].values[0],
                            Dy=he["Dy_1"].values[0],
                            Dk=he["Dk"].values[0],
                            H_2=he["H_2"].values[0],
                            h=he["h"].values[0],
                            A_0=he["A_0"].values[0],
                            l_1=he["l_1"].values[0],            
                            l_2_H=he["l_2_H"].values[0],
                            l_2_V=he["l_2_V"].values[0],
                            lk_H=he["lk_H"].values[0],
                            lk_V=he["lk_V"].values[0],
                            l_3=he["l_3"].values[0],
                            n_walls=he["n_walls"].values[0],
                        )
                        measures.append(measure)
                    
               
        return measures

    def get_compensators(
        self,
        df_tn:pd.DataFrame = GetDF.get_df_dif_temp_tn(),
        df_xn:pd.DataFrame = GetDF.get_df_dif_temp_xn()
    )-> int|None:
        compensators=[]
        
        for h in self.hes:
            
            if h.he.tipe == "tn" or h.he.tipe == "tk":
                df=df_tn
                D=df["Dbn"]==h.he.Dbn
                p=df["P"]==h.he.pressure
                serie=df[D&p]
                if not serie.empty:                                   
                    dif_max=serie['m1'].values[0]                    
                    if h.he.avg_dif_temp >dif_max:
                        #TODO averiguar el maximo de compensator
                        h.he.tipe="tk"
                        num_com=np.ceil((h.he.avg_dif_temp-dif_max)/6)
                        compensators.append(int(num_com))
                        
                    else:
                        h.he.tipe="tn"
                        compensators.append(0)
                
            else:
                df=df_xn
                D=df["Dbn"]==h.he.Dbn
                p_str=df["P"].str.contains(str(h.he.pressure))
                p_num=df["P"]==h.he.pressure
                serie=df[D&p_str|D&p_num]
                if not serie.empty: 
                    dif_max=serie['m1'].values[0]
                    
                    if h.he.avg_dif_temp >dif_max:
                        #TODO averiguar el maximo de compensator
                        h.he.tipe="xk"
                        num_com=np.ceil((h.he.avg_dif_temp-dif_max)/6)
                        compensators.append(int(num_com))                        
                    else:
                        h.he.tipe="xn"
                        compensators.append(0)

        return compensators

    def get_heater(self,id):
        return self.hes[id]