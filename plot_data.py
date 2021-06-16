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

    def refresh_data(self):
        self.connection = SQL_Writer()
        self.benefit_df = self.connection.get_df_select_benefits()
        self.gesch_bene_df = self.connection.get_df_select_geschaefte()
        self.qr_code_df = self.connection.get_df_select_qr_code()
        self.bi_light_df = self.connection.get_df_select_bi_light()

if __name__ == '__main__':
    data = BI_Data()
    # print(data.qr_code_df)
    #
    # max_qr_code_count = data.qr_code_df.count()
    #
    # print(max_qr_code_count)
    # data.qr_code_df['hour'] = data.qr_code_df['Timestamp'].dt.hour
    # data.qr_code_df['day'] = data.qr_code_df['Timestamp'].dt.day
    # data.qr_code_df['month'] = data.qr_code_df['Timestamp'].dt.month
    # print(data.qr_code_df)
    #
    # df_count = data.qr_code_df.groupby(['day']).size().reset_index(name='counts')
    # print(df_count)
    # print(max(6, round(df_count['counts'].iloc[-1] / 10)))

    max_bi_light_count = data.bi_light_df.count()
    df_count_benefits = data.bi_light_df.groupby(['Benefit']).size().reset_index(name='counts').sort_values(by=['counts'], ascending=False)
    print(max_bi_light_count)
    print(df_count_benefits)