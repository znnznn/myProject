import mysql.connector
import datetime

SECRET_KEY = '&uig(c6l^ph+$eb%e@cweq1zvwy)#lzoj#a-83ty8v^5q0pkmy'


class DataBase:
    """ work with the database """
    def __init__(self, user: dict):
        self.connection = None
        self.cursor = None
        self.user = user
        self.data_base()

    def data_base(self):
        """ connection to the database """
        try:
            self.connection = mysql.connector.connect(host='localhost', database='postgres', port=3306,
                                                      user='postgres', password='postgres')
            self.cursor = self.connection.cursor(dictionary=True)
        except:
            self.cursor.close()
            return False

    def take_user(self):
        """ takes data from database by email """
        try:
            self.cursor.execute("SELECT * FROM users WHERE EMAIL = %s", (f"{self.user['EMAIL']}",))
            user = self.cursor.fetchone()
            if user:
                self.cursor.close()
                self.connection.commit()
                return user
            self.cursor.close()
            self.connection.commit()
            return False
        except Exception as e:
            self.cursor.close()
            self.connection.commit()
            print(e, 'take_user')
            return False

    def take_user_id(self):
        """ takes data from database by id(integer)  (used for Userlogin.UserMixin)"""
        try:
            self.cursor.execute(f"SELECT * FROM users WHERE id = {self.user};")
            user = self.cursor.fetchone()
            if user:
                self.cursor.close()
                self.connection.commit()
                return user
            self.cursor.close()
            self.connection.commit()
            return False
        except Exception as e:
            self.cursor.close()
            self.connection.commit()
            print(e, 'take_user_id')
            return False

    def edit_user(self):
        """ changes the data in the database by id """
        try:
            self.data_base()
            self.cursor.execute("""UPDATE users
                                        SET FIRST_NAME=%s, LAST_NAME=%s,
                                            USERNAME=%s, PASSWORD=%s,
                                            EMAIL=%s, ADDRESS=%s  WHERE id=%s;""", (f"{self.user['firstName']}",
                                                                                    f"{self.user['lastName']}",
                                                                                    f"{self.user['username']}",
                                                                                    f"{self.user['password']}",
                                                                                    f"{self.user['email']}",
                                                                                    f"{self.user['address']}",
                                                                                    f"{self.user['id']}"))

            self.cursor.close()
            self.connection.commit()
            return True
        except Exception as e:
            print(e, 'edit_user')
            self.user['Error'] = e
            self.cursor.close()
            self.connection.commit()

    def del_user(self):
        """ deletes user data in the database (delete profile) """
        try:
            sql = f""" DROP TABLE {self.user['refactor_email']};"""
            self.cursor.execute("""DELETE FROM users WHERE id = %s;""", (f"{self.user['id']}",))
            self.cursor.execute(sql)
            self.cursor.close()
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            self.user['Error'] = e
            return False

    def add_user(self):
        """ adds the user to the database after registration """
        if self.take_user():
            return False
        self.data_base()
        try:
            table = self.create_tab()
            if table:
                self.data_base()
                self.cursor.execute(f"""INSERT INTO users(FIRST_NAME, LAST_NAME, USERNAME,
                                    PASSWORD, EMAIL, ADDRESS, OPER_DATE)
                                    VALUES(%s, %s, %s, %s, %s, %s, %s);""", (f"{self.user['firstName']}",
                                                                             f"{self.user['lastName']}",
                                                                             f"{self.user['USERNAME']}",
                                                                             f"{self.user['PASSWORD']}",
                                                                             f"{self.user['EMAIL']}",
                                                                             f"{self.user['ADDRESS']}",
                                                                             f"{self.user['date']}"))

                self.cursor.close()
                self.connection.commit()
                return True
            return False
        except Exception as e:
            print('add_user', e)
            self.connection.rollback()
            self.user['Error'] = e
            return False

    def del_user_views(self):
        """ deletes the data on which the user conducts analytics """
        try:
            sql_del = f"DELETE FROM {self.user['refactor_email']} WHERE id = {self.user['stock']['id']};"
            self.cursor.execute(sql_del)
            self.user['stock']['exch'] = 'profit'
            self.user['stock']['prevclose'] = self.user['stock']['profit']
            self.user['stock']['trade_date'] = f'''від {self.user["stock"]["trade_date"]}
                                                   до {str(datetime.datetime.today())[:16]}'''
            self.cursor.close()
            self.connection.commit()
            self.data_base()
            user = self.add_user_views()
            return True
        except Exception as e:
            print('del_user_views', e)
            self.connection.rollback()
            self.user['Error'] = e
            return False

    def add_user_views(self):
        """ adds the data on which the user conducts analytics """
        user = self.take_user()
        try:
            if user:
                sql = f"""INSERT INTO {self.user['refactor_email']}
                                                   (symbol, description, exch, type, open, high, low, bid, ASK,
                                                   change_percentage, prevclose, week_52_high, week_52_low, trade_date)
                                                VALUES('{self.user['stock']['symbol']}',
                                                       '{self.user['stock']['description']}',
                                                       '{self.user['stock']['exch']}',
                                                       '{self.user['stock']['type']}',
                                                       {self.user['stock']['open']},
                                                       {self.user['stock']['high']},
                                                       {self.user['stock']['low']},
                                                       {self.user['stock']['bid']},
                                                       {self.user['stock']['ask']},
                                                       {self.user['stock']['change_percentage']},
                                                       {self.user['stock']['prevclose']},
                                                       {self.user['stock']['week_52_high']},
                                                       {self.user['stock']['week_52_low']},
                                                       '{self.user['stock']['trade_date']}');"""
                self.data_base()
                self.cursor.execute(sql)
                self.cursor.close()
                self.connection.commit()
                return user
            return False
        except Exception as e:
            print('add_user_views', e)
            self.cursor.close()
            self.connection.commit()
            self.user['Error'] = e
            return False

    def take_user_views(self):
        """ takes data on which the user conducts analytics """
        try:
            take_sql = f"""SELECT * FROM {self.user['refactor_email']} WHERE exch !='profit';"""
            self.cursor.execute(take_sql)
            user = self.cursor.fetchall()
            stock = [s for s in user]
            self.cursor.close()
            self.connection.commit()
            if user:
                return stock
            return False
        except Exception as e:
            self.cursor.close()
            self.connection.commit()
            self.user['Error'] = e
            print('take_user_views', e)
            return False

    def take_user_views_symbol(self):
        """ checks for stock in the database """

        try:
            sql = f"""SELECT * FROM {self.user['refactor_email']}
                            WHERE symbol='{self.user['stock']['symbol']}' and exch != 'profit';"""
            self.cursor.execute(sql)
            user = self.cursor.fetchall()
            stock = [dict(s) for s in user]
            if user:
                self.cursor.close()
                self.connection.commit()
                return stock
            self.cursor.close()
            self.connection.commit()
            return False
        except Exception as e:
            self.cursor.close()
            self.connection.commit()
            self.user['Error'] = e
            print('take_user_views_symbol', e)
            return False

    def take_user_profit(self):
        """ takes data about all profit """
        try:
            sql = f"""SELECT * FROM {self.user['refactor_email']} WHERE exch='profit';"""
            self.cursor.execute(sql)
            user = self.cursor.fetchall()
            list_profit = [dict(s) for s in user]
            if user:
                self.cursor.close()
                self.connection.commit()
                return list_profit
            self.cursor.close()
            self.connection.commit()
            return False
        except Exception as e:
            self.cursor.close()
            self.connection.commit()
            self.user['Error'] = e
            print('take_user_profit', e)
            return False

    def create_tab(self):
        """ creating a table of users and a table of wishes of users """
        try:
            name = self.user['refactor_email']
            sql = f"""CREATE TABLE IF NOT EXISTS {name}
                                                             (id INT AUTO_INCREMENT,
                                                              symbol VARCHAR(500),
                                                              description text,
                                                              exch VARCHAR(70),
                                                              type VARCHAR(70),
                                                              open double,
                                                              high double,
                                                              low double,
                                                              bid double,
                                                              ask double,
                                                              change_percentage double,
                                                              prevclose double,
                                                              week_52_high double,
                                                              week_52_low double,
                                                              trade_date VARCHAR(500),
                                                              PRIMARY KEY (id)
                                                              );"""

            self.cursor.execute(sql)
            sql_user = """CREATE TABLE IF NOT EXISTS users (
                                                  id INT AUTO_INCREMENT,
                                                  FIRST_NAME VARCHAR(500),
                                                  LAST_NAME VARCHAR(500),
                                                  USERNAME VARCHAR(500),
                                                  PASSWORD VARCHAR(500),
                                                  EMAIL VARCHAR(500),
                                                  ADDRESS VARCHAR(500),
                                                  oper_date VARCHAR(500),
                                                  PRIMARY KEY(id)
                                                  );"""
            self.cursor.execute(sql_user)
            self.cursor.close()
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            self.user['Error'] = e
            print('create_tab', e)
            return False

    def add_message(self):
        """ adds sent user messages to the database """
        try:
            print(1)
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS message (
                                                              id INT AUTO_INCREMENT,
                                                              username VARCHAR(500),
                                                              email VARCHAR(500),
                                                              message text,
                                                              oper_date VARCHAR(500)б
                                                              PRIMARY KEY(id)
                                                              );""")
            print(2)
            self.cursor.execute("""INSERT INTO message(username, email, message, oper_date)
                                VALUES(%s, %s, %s, %s);""", (f"{self.user['username']}",
                                                             f"{self.user['email']}",
                                                             f"{self.user['message']}",
                                                             f"{self.user['date']}",))
            print(3)
            self.cursor.close()
            print(4)
            self.connection.commit()
            return True
        except Exception as e:
            print('add_message', e)
            self.connection.rollback()
            self.user['Error'] = e
            return False

