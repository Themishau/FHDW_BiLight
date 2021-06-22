import pandas as pd
import SQL_API
from SQL_API import SQL_Writer
import datetime as dt

class BI_Data():

    def __init__(self, connection=None):
        self.connection = SQL_Writer()
        self.benefit_df = self.connection.get_df_select_benefits()
        self.gesch_bene_df = self.connection.get_df_select_geschaefte()
        self.qr_code_df = self.connection.get_df_select_qr_code()
        self.bi_light_df = self.connection.get_df_select_bi_light()
        self.qr_code_pro_stunde = None
        self.qr_code_pro_month = None
        self.benefits_pro_day = None
        self.weekdaydict = {0:"Montag",
                            1:"Dienstag",
                            2:"Mittwoch",
                            3:"Donnerstag",
                            4:"Freitag",
                            5:"Samstag",
                            6:"Sonntag"}
        self.today_data = self.set_today_data()

    def set_today_data(self):
        now = dt.datetime.now()
        hour = now.hour
        today = now.day
        weekday = int(str(now.weekday()))
        weekday = self.weekdaydict[weekday]
        month = now.month
        df = pd.DataFrame(data= {"now": [now],
                                 "hour": [hour],
                                 "today": [today],
                                 "weekday": [weekday],
                                 "month": [month]
                                 })
        return df

    def refresh_data(self):
        self.connection = SQL_Writer()
        self.benefit_df = self.connection.get_df_select_benefits()
        self.gesch_bene_df = self.connection.get_df_select_geschaefte()
        self.qr_code_df = self.connection.get_df_select_qr_code()
        self.bi_light_df = self.connection.get_df_select_bi_light()
        self.today_data = self.set_today_data()

    def qr_code_pro_stunde_heute(self):
        # korrekte umsetzung
        now = dt.datetime.now()
        today = now.day
        #print("Heute ist:" + str(today))
        self.qr_code_df['hour'] = self.qr_code_df['Timestamp'].dt.hour
        self.qr_code_df['day'] = self.qr_code_df['Timestamp'].dt.day
        self.qr_code_df['month'] = self.qr_code_df['Timestamp'].dt.month
        data_day = self.qr_code_df.loc[self.qr_code_df['day'] == today]
        self.qr_code_pro_stunde = data_day.groupby(['hour']).size().reset_index(name='counts')
        #print(self.qr_code_pro_stunde)

    def qr_code_pro_stunde_monthly(self):
        # korrekte umsetzung
        now = dt.datetime.now()
        today = now.day
        #print("Heute ist:" + str(today))
        self.qr_code_df['hour'] = self.qr_code_df['Timestamp'].dt.hour
        self.qr_code_df['day'] = self.qr_code_df['Timestamp'].dt.day
        self.qr_code_df['month'] = self.qr_code_df['Timestamp'].dt.month
        data_day = self.qr_code_df.loc[self.qr_code_df['day'] == today]
        self.qr_code_pro_month = data_day.groupby(['month']).size().reset_index(name='counts')
        #print(self.qr_code_pro_stunde)

    def benefit_heute(self):
        # korrekte umsetzung
        # data.bi_light_df.groupby(['Benefit']).size().reset_index(name='counts').sort_values(by=['counts'], ascending=False)
        now = dt.datetime.now()
        today = now.day
        #print("Heute ist:" + str(today))
        self.bi_light_df['hour'] = self.bi_light_df['Timestamp'].dt.hour
        self.bi_light_df['day'] = self.bi_light_df['Timestamp'].dt.day
        self.bi_light_df['month'] = self.bi_light_df['Timestamp'].dt.month
        data_day = self.bi_light_df.loc[self.bi_light_df['day'] == today]
        self.benefits_pro_day = data_day.groupby(['Benefit','day']).size().reset_index(name='counts').sort_values(by=['counts'], ascending=False)
        #print(self.benefits_pro_day)
        #print(self.benefit_pro_day)

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