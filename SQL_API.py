from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import pymysql
import cryptography
import random
import pandas as pd
from enum import Enum

class TABLENAMES(Enum):
    QR_CODE              = 'QR_Code'
    BENEFIT              = 'Benefit'
    GESCHAEFT            = 'Geschaeft'
    GESCHAEFT_BENEFIT    = 'geschaeft_benefit'
    BI_LIGHT             = 'BI_Light'

class SQL_Writer():
    def __init__(self, db_connection=None, user_name=None):
        self.db_connection = self.create_connection_pymysql()
        self.user_name = 'dummy_insert'
        self.cursor = self.db_connection.cursor()

    def testConnection(self):
        sqlEngine = create_engine("mysql+pymysql://qr_scan_reader_test:1234@localhost:3310/RheinBerg_QRCode")
        dbConnection = sqlEngine.connect()
        frame = pd.read_sql("select * from QR_Code", dbConnection)
        pd.set_option('display.expand_frame_repr', False)
        dbConnection.close()
        if frame is not None:
            print(frame)
            return True
        else:
            return False

    def create_connection(self):
        sqlEngine = create_engine("mysql+pymysql://qr_scan_reader_test:1234@localhost:3310/RheinBerg_QRCode")
        dbConnection = sqlEngine.connect()
        return dbConnection

    def select_statement_to_conncection(self, sql_statement, dbConnection):
        frame = pd.read_sql("select * from QR_Code", dbConnection)
        pd.set_option('display.expand_frame_repr', False)
        print(frame)

    def add_dummy_data_to_gesch_bene(self):

        sql = "SELECT * FROM `Geschaeft`"
        self.cursor.execute(sql)
        result_gesch = self.cursor.fetchall()

        sql = "SELECT * FROM `Benefit`"
        self.cursor.execute(sql)
        result_bene = self.cursor.fetchall()

        result_gesch = random.sample(result_gesch, len(result_gesch))
        result_bene = random.sample(result_bene, len(result_bene))
        print('Result: ')

        sql = """INSERT INTO `RheinBerg_QRCode`.`geschaeft_benefit`
                        (`Geschaeft`, 
                         `Benefit`)
                     VALUES
                        (%s, 
                         %s)
                  """

        for i in result_gesch:

            benefit_len = len(result_bene)
            benefit_len_list = list(range(benefit_len))
            random.shuffle(benefit_len_list)

            r = []
            r.append(benefit_len_list[0])
            r.append(benefit_len_list[1])
            r.append(benefit_len_list[2])

            for j in r:
                print(i[1])
                print(result_bene[j][1])
                self.cursor.execute(sql, (i[1], result_bene[j][1]))

        self.db_connection.commit()
        self.db_connection.close()

    def add_dummy_data_to_geschaeft(self):

        df = pd.read_csv('some_data/testdata1.csv', names=['RheinBergGalerieGeschaeft'], delimiter=';')
        # print(df['RheinBergGalerieGeschaeft'])
        sql = """INSERT INTO `RheinBerg_QRCode`.`Geschaeft`
                        (`Geschaeft`)
                     VALUES
                        (%s)
                  """

        for i in df.itertuples():
            try:
                self.cursor.execute(sql, i.RheinBergGalerieGeschaeft)
            except pymysql.err.IntegrityError:
                print('konnte nicht speichern:')
                print(i.RheinBergGalerieGeschaeft)
        self.db_connection.commit()
        sql = "SELECT * FROM `Geschaeft`"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print('Result: ')
        for i in result:
            print(i)

    def add_dummy_data_to_benefits(self):

        df = pd.read_csv('some_data/testdata2.csv', names=['RheinBergGalerieBenefit'], delimiter=';')
        # print(df['RheinBergGalerieGeschaeft'])
        sql = """INSERT INTO `RheinBerg_QRCode`.`Benefit`
                        (`Benefit`)
                     VALUES
                        (%s)
                  """
        cursor = self.db_connection.cursor()

        for i in df.itertuples():
            try:
                cursor.execute(sql, i.RheinBergGalerieBenefit)
            except pymysql.err.IntegrityError as e:
                print(e)
                print('konnte nicht speichern:')
                print(i.RheinBergGalerieBenefit)
        self.db_connection.commit()

    def select_benefits(self):
        sql = "SELECT * FROM `Benefit`"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print('Result: ')
        print(pd.DataFrame(list(result), columns=["Id", "Benefit", "Timestamp"]))

    def select_geschaefte(self):
        sql = "SELECT * FROM `Geschaeft`"
        self.cursor.execute(sql)
        print('Result: ')
        print(pd.DataFrame(list(self.cursor.fetchall()), columns=["Id", "Geschaeft", "Timestamp"]))

    def select_gesch_bene(self):
        sql = "SELECT * FROM `geschaeft_benefit`"
        self.cursor.execute(sql)
        print('Result: ')
        print(pd.DataFrame(list(self.cursor.fetchall()), columns=["Id", "Geschaeft", "Benefit", "Timestamp"]))

    def select_bi_light(self):
        sql = "SELECT * FROM `BI_Light`"
        self.cursor.execute(sql)
        print('Result: ')
        print(pd.DataFrame(list(self.cursor.fetchall()), columns=["Id", "Geschaeft", "Benefit", "Timestamp"]))

    def select_qr_code(self):
        sql = "SELECT * FROM `QR_Code`"
        self.cursor.execute(sql)
        print('Result: ')
        print(pd.DataFrame(list(self.cursor.fetchall()), columns=["Id", "QR_Code", "Timestamp"]))

    # returns a dataframe, full
    def get_df_select_benefits(self):
        sql = "SELECT * FROM `Benefit`"
        self.cursor.execute(sql)
        return pd.DataFrame(list(self.cursor.fetchall()), columns=["Id", "Benefit", "Timestamp"])

    def get_df_select_geschaefte(self):
        sql = "SELECT * FROM `Geschaeft`"
        self.cursor.execute(sql)
        return pd.DataFrame(list(self.cursor.fetchall()), columns=["Id", "Geschaeft", "Timestamp"])

    def get_df_select_gesch_bene(self):
        sql = "SELECT * FROM `geschaeft_benefit`"
        self.cursor.execute(sql)
        return pd.DataFrame(list(self.cursor.fetchall()), columns=["Id", "Geschaeft", "Benefit", "Timestamp"])

    def get_df_select_bi_light(self):
        sql = "SELECT * FROM `BI_Light`"
        self.cursor.execute(sql)
        return pd.DataFrame(list(self.cursor.fetchall()), columns=["Id", "Geschaeft", "Benefit", "Timestamp"])

    def get_df_select_qr_code(self):
        sql = "SELECT * FROM `QR_Code`"
        self.cursor.execute(sql)
        return pd.DataFrame(list(self.cursor.fetchall()), columns=["Id", "QR_Code", "Timestamp"])


    def get_df_count(self, df):
        return df.shape[0]


    def write_qr_code_in_database(self, qr_code):
        # format: 'https://ergebnis.lola-coronapass.de/372e7c02-9c3a-4082-971d-6e0578ddea81'
        result = self.check_if_not_duplicate(TABLENAMES.QR_CODE, qr_code)
        if result is None:
            try:
                sql = """INSERT INTO `RheinBerg_QRCode`.`QR_Code`
                                (`QR_Code`)
                             VALUES
                                (%s)
                          """
                cursor = self.db_connection.cursor()
                print('connection')
                cursor.execute(sql, qr_code)
                self.db_connection.commit()
            except pymysql.err.IntegrityError as e:
                print(e)
                print('konnte nicht speichern:')
                print(qr_code)

    def check_if_not_duplicate(self, table_name, where_clausel):
        print("checking: " + table_name)
        sql = """SELECT * FROM `%s`
                 WHERE %s
              """
        self.cursor.execute(sql, (table_name, where_clausel))
        result = self.cursor.fetchall()
        print('Result: ')
        print(pd.DataFrame(list(result), columns=["Id", "QR_Code", "Timestamp"]))
        return result

    def create_connection_pymysql(self):
        connection = pymysql.connect(host='localhost',    # change host-ip if needed
                                     port=3310,           # change port if needed
                                     user='dummy_insert',
                                     password='1234',
                                     db='RheinBerg_QRCode')
        print('success')
        return connection

    def close_connection(self):
        self.db_connection.close()
