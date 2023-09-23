import pandas as pd


class GetDF:
    def get_df_dif_temp_tn() -> pd.DataFrame:
        return pd.read_excel("repository/dif_temp_tn.xlsx")

    def get_df_dif_temp_xn() -> pd.DataFrame:
        return pd.read_excel("repository/dif_temp_xn.xlsx")

    def get_df_area_xn_tn() -> pd.DataFrame:
        return pd.read_csv("repository/area_xn_tn.csv")

    def get_df_tn_measures() -> pd.DataFrame:
        return pd.read_csv("repository/tn.csv")

    def get_df_xn_measures() -> pd.DataFrame:
        return pd.read_csv("repository/xn.csv")



