from domain.substance import Substance
from domain.exchanger import HeatExchanger
from domain.calculator import PreliminarCalc, PostCalc
from usecases.get_heatexchanger_by_area import Heaters


def main():
    water = Substance(
        name="water",
        t_1=45,
        t_2=90,
        flow=9.32,
        where="inlet",
        pressure_work=0.6,
        heat_capacity=4180.9,
        density=979.9,
        viscosity=4.53,
        thermal_conduct=0.277,
    )

    benzin = Substance(
        name="benzin",
        t_1=150,
        t_2=80,
        where="outlet",
        thermal_power=water._thermal_power,
        pressure_work=1.2,
        heat_capacity=2430,
        density=759,
        viscosity=6.605,
        thermal_conduct=0.10266,
    )
    calc_1 = PreliminarCalc(200, water, benzin,"xn")

    device = HeatExchanger(
        tipe="tn",
        area_of_exchange=193.6,
        n_ways=4,
        Dbn=800,
        Dn_tube=25,
        l=6000,
        area_tube=0.0329,
        in_let_s=water,
        out_let_s=benzin,
        area_out_tube=0.07,
    )
    calc_2 = water.thermal_power

    # f=Heaters.get_exchanger_measures( he=calc_2[0].he)
    # k=Heaters.get_compensators(calc_2[0].he)

    # print(f" avg temp: {calc_2[0].he.avg_dif_temp} with {k}: compensators {calc_2[0].he.tipe} ")
    # print(Heaters.get_heater(precalc= calc_1))
    print(calc_2)

if __name__ == "__main__":
    main()
