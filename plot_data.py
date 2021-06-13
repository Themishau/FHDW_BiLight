import pandas as pd
import SQL_API
from SQL_API import SQL_Writer


class BI_Data():

    def __init__(self, connection=None):
        self.connection = SQL_Writer()
        self.benefit_df = self.connection.get_df_select_benefits()
        self.gesch_bene_df = self.connection.get_df_select_geschaefte()
        self.qr_code_df = self.connection.get_df_select_qr_code()
        self.bi_light_df = self.connection.get_df_select_bi_light()



if __name__ == '__main__':
    data = BI_Data()
