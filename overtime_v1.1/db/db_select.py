import sys
sys.path.append("C:\\myproject\\python project\\overtime\\overtime_v1.1\\db") #모듈 import가 안 될때 경로를 지정해 주기
import db.db_info as conn_info
import pymysql
from PyQt5.QtWidgets import QMessageBox

class Select:

    def __init__(self):
        db_info = conn_info.Connect()

        self.host = db_info.host
        self.user = db_info.username
        self.passwd = db_info.password
        self.db = db_info.database
        self.port = db_info.port

        self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, port=self.port, use_unicode=True, charset='utf8')        

    def select_location(self, arr_1):
        cursor = self.conn.cursor()

        try:
            # pymysql을 통해 쿼리 입력할 때, 아래와 같은 오류 문구를 만나곤 한다.
            # ValueError: unsupported format character 'Y' (0x59) at index
            # 이는 쿼리의 변수 표현에 쓰이는 %s와 data format 변경하는 (예시에서는 DATE_FORMAT) 에서의 %를 구분해주지 않았기 때문이다.
            # SELECT DATE_FORMAT(DeviceReportedTime, '%Y-%m-%d %H:%i:%s') AS date, Facility, Priority, FromHost, FromIP, Message FROM SystemEvents WHERE DeviceReportedTime BETWEEN '%s 00:00:00' AND '%s 23:59:59' ORDER BY DeviceReportedTime DESC
            # 위와 같이 작성하면 오류가 발생하는 것이다.            
            # DATE_FORMAT 안의 %를 %%로 변경해주어 아래와 같은 코드로 변경해주자. 

            query = """SELECT id, name, location, brand, package, DATE_FORMAT(c_date, '%%Y-%%m-%%d'), DATE_FORMAT(u_date, '%%Y-%%m-%%d') FROM item_location WHERE u_date BETWEEN %s AND %s;""" #날짜를 비교 하기 위해 안쪽 select문 사용, qt 테이블 입력을 위해 날짜 형식을 문자로 바꾸려고 밖의 select문 사용
            cursor.execute(query, arr_1) #excute 문에 조회용 변수를 전달 할 때는 튜블 또는 리스트로 !!!!
            result = cursor.fetchall()

            if result:
                self.conn.close()
                self.msg_box("조회완료", "정상적으로 조회 되었습니다.")
                return result
            else:
                self.conn.close()
                self.msg_box("조회결과", "조회결과가 없습니다.")
                return            

        except Exception as e:
            self.msg_box("Error", str(e))

        return result

    def select_department(self):
        cursor = self.conn.cursor()

        try:
            # pymysql을 통해 쿼리 입력할 때, 아래와 같은 오류 문구를 만나곤 한다.
            # ValueError: unsupported format character 'Y' (0x59) at index
            # 이는 쿼리의 변수 표현에 쓰이는 %s와 data format 변경하는 (예시에서는 DATE_FORMAT) 에서의 %를 구분해주지 않았기 때문이다.
            # SELECT DATE_FORMAT(DeviceReportedTime, '%Y-%m-%d %H:%i:%s') AS date, Facility, Priority, FromHost, FromIP, Message FROM SystemEvents WHERE DeviceReportedTime BETWEEN '%s 00:00:00' AND '%s 23:59:59' ORDER BY DeviceReportedTime DESC
            # 위와 같이 작성하면 오류가 발생하는 것이다.            
            # DATE_FORMAT 안의 %를 %%로 변경해주어 아래와 같은 코드로 변경해주자. 

            query = """SELECT dept_id, dept_name FROM department ORDER BY dept_id;""" #날짜를 비교 하기 위해 안쪽 select문 사용, qt 테이블 입력을 위해 날짜 형식을 문자로 바꾸려고 밖의 select문 사용
            cursor.execute(query) #excute 문에 조회용 변수를 전달 할 때는 튜블 또는 리스트로 !!!!
            result = cursor.fetchall()

            if result:
                self.conn.close()
                return result
            else:
                self.conn.close()
                return            

        except Exception as e:
            self.msg_box("Error", str(e))
    
    def select_employee(self, arg_1):
        cursor = self.conn.cursor()

        try:
            # pymysql을 통해 쿼리 입력할 때, 아래와 같은 오류 문구를 만나곤 한다.
            # ValueError: unsupported format character 'Y' (0x59) at index
            # 이는 쿼리의 변수 표현에 쓰이는 %s와 data format 변경하는 (예시에서는 DATE_FORMAT) 에서의 %를 구분해주지 않았기 때문이다.
            # SELECT DATE_FORMAT(DeviceReportedTime, '%Y-%m-%d %H:%i:%s') AS date, Facility, Priority, FromHost, FromIP, Message FROM SystemEvents WHERE DeviceReportedTime BETWEEN '%s 00:00:00' AND '%s 23:59:59' ORDER BY DeviceReportedTime DESC
            # 위와 같이 작성하면 오류가 발생하는 것이다.            
            # DATE_FORMAT 안의 %를 %%로 변경해주어 아래와 같은 코드로 변경해주자. 

            query = """SELECT dept_id, dept_name, dept_level, dept_upper FROM department WHERE dept_id = %s ORDER BY dept_id;""" #날짜를 비교 하기 위해 안쪽 select문 사용, qt 테이블 입력을 위해 날짜 형식을 문자로 바꾸려고 밖의 select문 사용
            cursor.execute(query, arg_1) #excute 문에 조회용 변수를 전달 할 때는 튜블 또는 리스트로 !!!!
            result = cursor.fetchall()

            if result:
                self.conn.close()
                return result
            else:
                self.conn.close()
            

        except Exception as e:
            self.msg_box("Error", str(e))

        return result
    
    def dept_overtime(self, arg_1):
        cursor = self.conn.cursor()

        try:
            # pymysql을 통해 쿼리 입력할 때, 아래와 같은 오류 문구를 만나곤 한다.
            # ValueError: unsupported format character 'Y' (0x59) at index
            # 이는 쿼리의 변수 표현에 쓰이는 %s와 data format 변경하는 (예시에서는 DATE_FORMAT) 에서의 %를 구분해주지 않았기 때문이다.
            # SELECT DATE_FORMAT(DeviceReportedTime, '%Y-%m-%d %H:%i:%s') AS date, Facility, Priority, FromHost, FromIP, Message FROM SystemEvents WHERE DeviceReportedTime BETWEEN '%s 00:00:00' AND '%s 23:59:59' ORDER BY DeviceReportedTime DESC
            # 위와 같이 작성하면 오류가 발생하는 것이다.            
            # DATE_FORMAT 안의 %를 %%로 변경해주어 아래와 같은 코드로 변경해주자. 

            query = """SELECT dept_name, emp_id, emp_name, overtime_date, s_time, t_time, overtime, deatail, note, c_date, u_date FROM overtime WHERE overtime_date = %s;""" #날짜를 비교 하기 위해 안쪽 select문 사용, qt 테이블 입력을 위해 날짜 형식을 문자로 바꾸려고 밖의 select문 사용
            cursor.execute(query, arr_1) #excute 문에 조회용 변수를 전달 할 때는 튜블 또는 리스트로 !!!!
            result = cursor.fetchall()

            if result:
                self.conn.close()
                self.msg_box("조회완료", "정상적으로 조회 되었습니다.")
                return result
            else:
                self.conn.close()
                self.msg_box("조회결과", "조회결과가 없습니다.")
                return            

        except Exception as e:
            self.msg_box("Error", str(e))

        return result


    def msg_box(self, msg_1, msg_2):
        msg = QMessageBox()
        msg.setWindowTitle(msg_1)               # 제목설정
        msg.setText(msg_2)                          # 내용설정
        msg.exec_()                                 # 메세지박스 실행

    # def insert_barcode(self, arr_1):
    #     cursor = self.conn.cursor()

    #     try:
    #         query = "TRUNCATE TABLE item_barcode;"
    #         cursor.execute(query)
    #         self.conn.commit()

    #         query = """INSERT INTO item_barcode (id, alias, name, barcode, sc_code, c_date) VALUES (%s, %s, %s, %s, %s, now());"""
    #         cursor.executemany(query, arr_1)
    #         self.conn.commit()
    #         self.conn.close()            
                        
    #     except Exception as e:
    #         error = ("Error", str(e))
    #         return error

    #     return ("완료", "바코드 정보가 정상적으로 업로드 되었습니다.")