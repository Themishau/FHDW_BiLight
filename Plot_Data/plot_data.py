import pandas as pd
from SQL.SQL_API import SQL_Writer
import datetime as dt
import time
class BI_Data():

    def __init__(self, connection=None):
        self.connection = SQL_Writer()
        self.benefit_df = self.connection.get_df_select_benefits()
        self.gesch_bene_df = self.connection.get_df_select_gesch_bene()
        self.qr_code_df = self.connection.get_df_select_qr_code()
        self.bi_light_df = self.connection.get_df_select_bi_light()
        self.qr_code_pro_stunde = None
        self.qr_code_pro_month = None
        self.benefits_pro_day = None
        self.now = dt.datetime.now()
        self.date = self.now.day
        self.month = self.now.month
        self.refresh_time = self.get_current_time()
        #self.date = 22
        self.weekdaydict = {0:"Montag",
                            1:"Dienstag",
                            2:"Mittwoch",
                            3:"Donnerstag",
                            4:"Freitag",
                            5:"Samstag",
                            6:"Sonntag"}
        self.today_data = self.set_today_data()

    def get_current_time(self):
        """ Helper function to get the current time in seconds. """

        now = dt.datetime.now()
        total_time = (now.hour * 3600) + (now.minute * 60) + now.second
        return total_time


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
        if (self.get_current_time() - self.refresh_time) > 120:
            self.connection.reconnect_to_Database()
            time.sleep(1)
            self.refresh_time = self.get_current_time()
            print('- {} - '.format(dt.datetime.now()))
            print('refreshed')
            try:
                self.benefit_df = self.connection.get_df_select_benefits()
                self.gesch_bene_df = self.connection.get_df_select_gesch_bene()
                self.qr_code_df = self.connection.get_df_select_qr_code()
                self.bi_light_df = self.connection.get_df_select_bi_light()
                self.today_data = self.set_today_data()
            except:
                return


    def qr_code_pro_stunde_heute(self):
        try:
            now = dt.datetime.now()
            today = now.day
            self.qr_code_df['hour'] = self.qr_code_df['Timestamp'].dt.hour
            self.qr_code_df['day'] = self.qr_code_df['Timestamp'].dt.day
            self.qr_code_df['month'] = self.qr_code_df['Timestamp'].dt.month
            data_day = self.qr_code_df.loc[self.qr_code_df['day'] == self.date]
            self.qr_code_pro_stunde = data_day.groupby(['hour']).size().reset_index(name='counts')
        except AssertionError as e:
            print(e)
            print("-------- qr_code_pro_stunde_heute --------")
            print(self.qr_code_df['day'])
            print('------')
            print(self.date)

    def qr_code_pro_stunde_monthly(self):
        try:
            now = dt.datetime.now()
            today = now.day
            self.qr_code_df['hour'] = self.qr_code_df['Timestamp'].dt.hour
            self.qr_code_df['day'] = self.qr_code_df['Timestamp'].dt.day
            self.qr_code_df['month'] = self.qr_code_df['Timestamp'].dt.month
            self.qr_code_pro_month = self.qr_code_df.groupby(['day']).size().reset_index(name='counts')

        except AssertionError as e:
            print(e)
            print("-------- qr_code_pro_stunde_monthly --------")
            print(self.qr_code_df['day'])
            print('------')
            print(self.date)

    def benefit_heute(self):
        try:
            now = dt.datetime.now()
            today = now.day
            self.bi_light_df['hour'] = self.bi_light_df['Timestamp'].dt.hour
            self.bi_light_df['day'] = self.bi_light_df['Timestamp'].dt.day
            self.bi_light_df['month'] = self.bi_light_df['Timestamp'].dt.month
            data_day = self.bi_light_df.loc[self.bi_light_df['day'] == self.date]
            self.benefits_pro_day = data_day.groupby(['Benefit','day']).size().reset_index(name='counts').sort_values(by=['counts'], ascending=False)
        except AssertionError as e:
            print(e)
            print("--------benefit heute --------")
            print(self.bi_light_df['day'])
            print('------')
            print(self.date)

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