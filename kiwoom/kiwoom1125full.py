#import  os
#import sys
#from openpyxl import Workbook
#from openpyxl import load_workbook
#import xlrd
import pandas as pd
import xlwings as xw
import win32com.client
from datetime import datetime
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from PyQt5.QtTest import *
#from PyQt5.QTest import *
from lims.config.errorCode import errors


class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        print("kiwoom클레스입니다.")

        ### event loop를 실행하기 위한 변수 모임
        self.login_event_loop =QEventLoop()
        self.detail_account_info_event_loop = QEventLoop()  #예수금 요청용 이벤트 루프
        self.calculator_event_loop =QEventLoop()
        ###################################

        ### 계좌 관련된 변수
        self.account_num =None          #계좌번호
        self.deposit = 0                #예수금
        self.use_money = 0              #실제 투자에 사용할 금액
        self.use_money_percent = 0.5    #예수금에서 실제 사용한 비율
        self.output_deposit = 0         #출력가능 금액
        self.total_profit_loss_money = 0    #총평가손익금액
        self.total_profit_loss_rate = 0.0   #총수익율(%)
        self.account_stock_dict = {}
        self.not_account_stock_dict = {}
        self.iw = None             #관심종목 파일 입력용
        self.run_code = ""          #종목코드 공유용
        #self.code_info = None              #종목코드
        self.interest_stock_list = []               #관심정보 정보
        ###############################

        ### 요청 스크린 번호
        self.screen_my_info = "2000"    #계좌관련 스크린 번호
        self.screen_calculation_stock = "4000"
        ##############################

        ##### 종목분석용 데이타
        self.calcul_data = []
        #############################

        ### 초기 셋팅 함수들 바로 실행
        self.get_ocx_instance()         #OCX방식을 파이썬에 사용 할 수 있게 변환해 주는 함수
        self.event_slots()              #키움과 연결하기 위한 시그널 / 슬롯 모음
        self.signal_login_commConnect() #로그린 요청 함수 포함
        self.get_account_info()         #계좌번호 가져오기
        self.get_interest_stock()       #계좌관심종목 가져오기
        self.ref_kiwoom_db()            #투자자현황 가져오기
        #self.basic_info()              #종목별 기본 정보 가져오기(현재가포함)
        #self.detail_account_info()      #예수금 요청 시그널 포함
        #self.detail_account_mystock()   #계좌평가잔고내역 가져오기


        #self.calculator_fnc()           #종목분석용, 임시용으로 실행
        ###############################

    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPIctrl.1")

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)
        self.OnReceiveTrData.connect(self.trdata_slot)  #트랜잭션 요청 관련 이벤트

    def signal_login_commConnect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop.exec_()           #이벤트루프 실행

    def login_slot(self,err_Code):
        print(errors(err_Code)[1])

        self.login_event_loop.exit()            #이벤트루프 종료

    def get_account_info(self):
        account_list = self.dynamicCall("GetLoginInfo(QString)","ACCNO")
        #account_id = self.dynamicCall("GetLoginInfo(QString)","USER_ID")
        account_num = account_list.split(';')[0]
        self.account_num = account_num
        #self.account_id = account_id
        print("계좌번호 : %s" % account_num)
        #print("계좌ID : %s" % account_id)

    def get_interest_stock(self):
        #self.in_file = open("C:/pythonfiles/lims/files/interest.txt", "r")
        #wb = load_workbook('./files/Test.xlsm', keep_vba=True)
        #count = 0
        #self.inter
        self.iw = pd.read_excel("C:/pythonfiles/lims/files/interest.xlsx",index_col=None,dtype={'code':str,'종목명':str})

        for row in self.iw.index:
            code = self.iw.iloc[row,0]
            self.dynamicCall("SetInputValue(QString,QString)","종목코드",code)
            self.dynamicCall("CommRqData(QString,QString,int,QString)","기본정보요청","opt10001",0,self.screen_my_info)
            self.detail_account_info_event_loop.exec_()
            QTest.qWait(500)
        QTest.qWait(3000)
        df = pd.DataFrame(self.interest_stock_list)
        df['52최고일'] = pd.to_datetime(df['52최고일'], format="%Y%m%d")
        df['52최저일'] = pd.to_datetime(df['52최저일'], format="%Y%m%d")
        df['52최고일'] = df['52최고일'].dt.date                                   #일자형식으로 시간 버림
        df['52최저일'] = df['52최저일'].dt.date                                   #일자형식으로 시간 버림
        df.head()
        # with pd.ExcelWriter("C:/pythonfiles/lims/files/report.xlsx") as writer:                   #행 인텍스로 시트이름
        #     count = 0
        #     for code in df.code:
        #        s_name = df.종목명
        #        df[df.code == f'{code}'].to_excel(writer, sheet_name=f'{s_name[count]}')
        #        count += 1
        # writer.close()

        #df = df.transpose()                                                     #데이타프레임 종행 변경
        #df = df.rename(columns=df.iloc[1])                                      #코드명 컬럼이름으로
        #df = df.drop(df.index[1]);                                              #코드행 한줄 삭제
        ## print(df.info()); print(df.shape); print(df.head()); df.to_excel("c:/temp/test.xlsx",'temp')
        # with pd.ExcelWriter("C:/pythonfiles/lims/files/data.xlsx", mode='a', engine='openpyxl') as writer:      # 기본데이터 시트
        #     df.to_excel(writer, sheet_name='data', index=False)
        #df.to_excel("C:/pythonfiles/lims/files/data.xlsx")   #데이타프레임 html
        #df.to_excel("C:/pythonfiles/lims/files/test.xlsm",sheet_name='sheet11')   #데이타프레임 html
        excel = win32com.client.Dispatch("Excel.Application")
        wb_test = xw.Book("C:/pythonfiles/lims/files/report.xlsm")
        ws1 = wb_test.sheets['data']

        ws1.range("A1").value = df
        # ws1.cells.clear_contents()
        # for i in range(1, 10):
        #     for j in range(1, 20):
        #         ws1.cells(i, j).value = "^.^"

        wb_test.save()
        #wb_test.close()
        #excel.Quit()

        # ## 엑셀 파일에 직접 입력...xlsm파일 Writting이 안되어서
        # excel = win32com.client.Dispatch("Excel.Application")
        # workbook = excel.Workbooks.Open("C:/pythonfiles/leanpy/basic/test.xlsm")
        # #excel.Application.Run("test.xlsm!Module1.Macro1")
        # sheet = workbook.Sheets("data")
        # for i in range(len(df.index)):
        #     for j in range(df.shape[1]):
        #         print(i,j)
        #         sheet.Cells(i, j).Value = df.iloc[i, j]
        # workbook.Save()
        # excel.quit()
        # QTest.qWait(5000)
        print('엑셀출력끝')

    def ref_kiwoom_db(self):
        print("투자자현황")
        for row in  self.iw.index:
            self.run_code  = code = self.iw.iloc[row,0]
            print(code)
            date = datetime.today().strftime('%Y%m%d')
            self.dynamicCall("SetInputValue(QString,QString)", "일자", date)
            self.dynamicCall("SetInputValue(QString,QString)","종목코드",code)
            self.dynamicCall("SetInputValue(QString,QString)","금액수량구분","2")
            self.dynamicCall("SetInputValue(QString,QString)","매매구분","0")
            self.dynamicCall("SetInputValue(QString,QString)","단위구분","1")
            self.dynamicCall("CommRqData(QString,QString,int,QString)","종목별투자자기관별요청","opt10059",0,self.screen_my_info)  #self.screen_my_info
            self.calculator_event_loop.exec_()
            QTest.qWait(500)

        #print(self.calcul_data)
        column = ["code","일자","현재가","대비기호","전일대비","등락율","누적거래량","누적거래대금","개인투자자","외국인투자자","기관계", \
                  "금융투자","보험","투신","기타금융","은행","연기금등","사모펀드","국가","기타법인","내외국인"]
        df =  pd.DataFrame(self.calcul_data,columns=column)
        wb_test = xw.Book("C:/pythonfiles/lims/files/report.xlsm")
        ws1 = wb_test.sheets['투자자']
        ws1.range("A1").value = df
        wb_test.save()
        wb_test.close()
        print(df.info())
        print(df.head())

    def detail_account_info(self,sPrevNext="0"):
        self.dynamicCall("SetInputValue(QString,QString)","계좌번호",self.account_num)
        self.dynamicCall("SetInputValue(QString,QString)","비밀번호","0000")
        self.dynamicCall("SetInputValue(QString,QString)","비밀번호입력매체구분","00")
        self.dynamicCall("SetInputValue(QString,QString)","조회구분","1")
        self.dynamicCall("CommRqData(QString,QString,int,QString)","예수금상세현황요청","opw00001",sPrevNext,self.screen_my_info)

        self.detail_account_info_event_loop = QEventLoop()
        self.detail_account_info_event_loop.exec_()

    def stop_screen_cancel(self,sScrNo=None):
        self.dynamicCall("DisconnectRealData(QString)",sScrNo)      #스크린번호 끊기

    def detail_account_mystock(self,sPrevNext="0"):
        #print("계좌평가잔고내역요청")
        self.dynamicCall("SetInputValue(QString,QString)","계좌번호",self.account_num)
        self.dynamicCall("SetInputValue(QString,QString)","비밀번호","0000")
        self.dynamicCall("SetInputValue(QString,QString)","비밀번호입력매체구분","00")
        self.dynamicCall("SetInputValue(QString,QString)","조회구분","2")
        self.dynamicCall("CommRqData(QString,QString,int,QString)","계좌평가잔고내역요청","opw00018",sPrevNext,self.screen_my_info)

        self.detail_account_info_event_loop.exec_()

    def not_concluded_account(self,sPrevNext="0"):
        print("미체결 종목 요청")
        self.dynamicCall("SetInputValue(QString,QString)","계좌번호",self.account_num)
        self.dynamicCall("SetInputValue(QString,QString)","체결구분","1")
        self.dynamicCall("SetInputValue(QString,QString)","매매구분","0")
        self.dynamicCall("CommRqData(QString,QString,int,QString)","실시간미체결요청","opt10075",sPrevNext,self.screen_my_info)

        self.detail_account_info_event_loop.exec_()

    def day_kiwoom_db(self,code=None,date=None,sPrevNext="0"):
        ##print("주식일봉차트조회")
        self.dynamicCall("SetInputValue(QString,QString)","종목코드",code)
        self.dynamicCall("SetInputValue(QString,QString)","수정주가구분","1")
        if date != None:
            self.dynamicCall("SetInputValue(QString,QString)","기준일자",date)
        self.dynamicCall("CommRqData(QString,QString,int,QString)","주식일봉차트조회","opt10081",sPrevNext,self.screen_calculation_stock)
        QTest.qWait(3600)
        self.calculator_event_loop.exec_()

    def get_code_list_by_market(self, market_code):
        '''
        종목코드 리스트 받기
        #0:장내, 10:코스닥

        :param market_code: 시장코드 입력
        :return:
        '''
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market_code)
        code_list = code_list.split(';')[:-1]
        return code_list

    def calculator_fnc(self):
        code_list = self.get_code_list_by_market("10")
        print("코스닥 갯수 %s" % len(code_list))

        for idx, code in enumerate(code_list):
            self.dynamicCall("DisconnectRealData(QSting)",self.screen_calculation_stock)

            print("%s / %s :코스닥 종목 코드 : %s is updating...." % (idx+1, len(code_list), code))

            self.day_kiwoom_db(code=code)

    def input_sep(self,temp):
        if '.' in temp:
            temp = float(temp)
        else:
            try:
                temp = int(temp)
            except:
                if len(temp.split())>=1:
                    temp = temp.split()
                else:
                    temp = 0
        return temp

    def trdata_slot(self,sScrNo,sRQName,sTrCode,sRecordName,sPrevNext):
        '''
        tr요청하는 구역이다! 슬롯이다
        :param sScrNo: 스크린번호
        :param sRQName: 내가 요청할때 지은 이름
        :param sTrCode: 요청id,tr코드
        :param sRecordName: 사용안함
        :param sPrevNext: 다음페이지가 있는지
        :return:
        '''
        if sRQName == "예수금상세현황요청":
            deposit = self.dynamicCall("GetCommData(QString,QString,int,QString)",sTrCode,sRQName,0,"예수금")
            self.deposit = int(deposit)
            print("예수금 %s" % self.deposit)
            deposit = self.dynamicCall("GetCommData(QString,QString,int,QString)",sTrCode,sRQName,0,"출금가능금액")
            self.deposit = int(deposit)
            print("출금가능금액 %s" % self.deposit)
            use_money = float(self.deposit) * self.use_money_percent
            self.use_money = int(use_money)
            self.use_money = self.use_money/4
            self.stop_screen_cancel(self.screen_my_info)

            self.detail_account_info_event_loop.exit()

        elif sRQName == "기본정보요청":
            #rows = self.dynamicCall("GetRepeatCnt(QString,QString)",sTrCode,sRQName)
            #for i in range(rows):
            code = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "종목코드")
            code = code.strip()
            code_nm = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "종목명")
            account_mon = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "결산월")
            par_value = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "액면가")
            capital = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "자본금")
            tot_stocks = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "상장주식")
            credit_per = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "신용비율")
            year_max = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "연중최고")
            year_min = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "연중최저")
            tot_market = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "시가총액")
            foreign_per = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0,
                                           "외인소진률")
            per = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "PER")
            EPS = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "EPS")
            ROE = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "ROE")
            PBR = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "PBR")
            EV = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "EV")
            BPS = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "BPS")
            sales = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "매출액")
            buss_profits = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0,
                                            "영업이익")
            net_profits = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0,
                                           "당기순이익")
            max_52 = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "250최고")
            min_52 = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "250최저")
            start_price = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "시가")
            high_price = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "고가")
            low_price = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "저가")
            up_limit = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "상한가")
            down_limit = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "하한가")
            std_price = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "기준가")
            exp_price = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "예상체결가")
            exp_quantity = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0,
                                            "예상체결수량")
            date_max = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "250최고가일")
            per_max = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0,
                                       "250최고가대비율")
            date_min = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "250최저가일")
            per_min = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0,
                                       "250최저가대비율")
            now_price = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "현재가")
            now_sign = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "대비기호")
            now_yesterday = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0,
                                             "전일대비")
            now_yesper = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "등락율")
            now_quantity = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "거래량")
            now_quaper = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "거래대비")
            now_unit = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0, "액면가단위")
            retail_stocks = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0,
                                             "유통주식")
            retail_stoper = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, 0,
                                             "유통비율")

            temp_dict = {}

            temp_dict.update({'code': code.strip()})
            temp_dict.update({'종목명': code_nm.strip()})
            temp_dict.update({'현재가':abs(int(now_price.strip()))})
            temp_dict.update({'기호':now_sign.strip()})
            temp_dict.update({'전일비':int(now_yesterday.strip())})
            temp_dict.update({'전일%':float(now_yesper.strip())})
            temp_dict.update({'거래량':int(now_quantity.strip())})  ##111
            temp_dict.update({'거래%':float(now_quaper.strip())})
            temp_dict.update({'기준가':int(std_price.strip())})
            temp_dict.update({'시작가':int(start_price.strip())})
            temp_dict.update({'최고가':int(high_price.strip())})
            temp_dict.update({'최저가':int(low_price.strip())*-1})
            temp_dict.update({'상한가':int(up_limit.strip())})
            temp_dict.update({'하한가':int(down_limit.strip())*-1})
            temp_dict.update({'52최고':int(max_52.strip())})
            temp_dict.update({'52최저':int(min_52.strip())*-1})
            temp_dict.update({'52최고일':date_max.strip()})
            temp_dict.update({'52최고비':float(per_max.strip())})
            temp_dict.update({'52최저일':date_min.strip()})
            temp_dict.update({'52최저비':float(per_min.strip())})
            temp_dict.update({'유통주':self.input_sep(retail_stocks)})
            temp_dict.update({'유통비':self.input_sep(retail_stoper)})
            temp_dict.update({'예상가':int(exp_price.strip())})
            temp_dict.update({'예상수량':int(exp_quantity.strip())})
            temp_dict.update({'결산월':int(account_mon.strip())})
            temp_dict.update({'액면가':int(par_value.strip())})
            temp_dict.update({'자본금':int(capital.strip())})
            temp_dict.update({'상장주':int(tot_stocks.strip())})
            temp_dict.update({'신용율':self.input_sep(credit_per)})
            temp_dict.update({'년최고':int(year_max.strip())})
            temp_dict.update({'년최저':int(year_min.strip())})
            temp_dict.update({'시가총액':int(tot_market.strip())})
            temp_dict.update({'외국%':self.input_sep(foreign_per)})
            temp_dict.update({'매출액':self.input_sep(sales)})
            temp_dict.update({'영업이익':self.input_sep(buss_profits)})
            temp_dict.update({'세전이익':self.input_sep(net_profits)})
            temp_dict.update({'per':self.input_sep(per)})
            temp_dict.update({'EPS':self.input_sep(EPS)})
            temp_dict.update({'ROE':self.input_sep(ROE)})
            temp_dict.update({'PBR':self.input_sep(PBR)})
            temp_dict.update({'EV':self.input_sep(EV)})
            temp_dict.update({'BPS':self.input_sep(BPS)})

            print(temp_dict)
            self.interest_stock_list.append(temp_dict)

            self.detail_account_info_event_loop.exit()

        elif sRQName == "계좌평가잔고내역요청":
            total_buy_money = self.dynamicCall("GetCommData(QString,QString,int,QString)",sTrCode,sRQName,0,"총매입금액")               #출력 : 000000000746100
            self.total_buy_money = int(total_buy_money)
            total_profit_loss_money = self.dynamicCall("GetCommData(QString,QString,int,QString)",sTrCode,sRQName,0,"총평가손익금액")    #출력 : 000000000746100
            self.total_profit_loss_money = int(total_profit_loss_money)
            total_profit_loss_rate = self.dynamicCall("GetCommData(QString,QString,int,QString)",sTrCode,sRQName,0,"총수익률(%)")          #출력 : 0000000001.31
            self.total_profit_loss_rate = float(total_profit_loss_rate)

            print("계좌평가잔고내역요청 싱글데이터 : %s - %s - %s" % (self.total_buy_money,self.total_profit_loss_money,self.total_profit_loss_rate))

            rows = self.dynamicCall("GetRepeatCnt(QString,QString)",sTrCode,sRQName)
            print("가지고 있는 종목**** 수 ***** : %s" % rows)
            cnt = 0
            for i in range(rows):
                code = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"종목번호")
                code = code.strip()[1:]
                code_nm = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"종목명")
                stock_quantity = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"보유수량")
                buy_price = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"매입가")
                learn_rate = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"수익률(%)")
                current_price = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"현재가")
                total_chegual_price = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, i, "매입금액")
                possible_quantity = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, i, "매매가능수량")
                print("종목코드 : %s -종목명 : %s -보유수량 : %s -매입가 : %s -수익률 : %s -현재가 : %s " %(code,code_nm,stock_quantity,buy_price,learn_rate,current_price))
                if code in self.account_stock_dict:
                    pass
                else:
                    self.account_stock_dict[code] = {}

                code_nm =code_nm.strip()
                stock_quantity = int(stock_quantity.strip())
                buy_price = int(buy_price.strip())
                learn_rate = float(learn_rate.strip())
                current_price = int(current_price.strip())
                total_chegual_price = int(total_chegual_price.strip())
                possible_quantity = int(possible_quantity.strip())

                self.account_stock_dict[code].update({"종목명":code_nm})
                self.account_stock_dict[code].update({"보유수량":stock_quantity})
                self.account_stock_dict[code].update({"매입가":buy_price})
                self.account_stock_dict[code].update({"수익률(%)":learn_rate})
                self.account_stock_dict[code].update({"현재가":current_price})
                self.account_stock_dict[code].update({"매입금액":total_chegual_price})
                self.account_stock_dict[code].update({"매매가능수량":possible_quantity})

                f = open("files/buy_stock.txt", "a", encoding="utf8")
                f.write("%s\t%s\t%s\n" % (code, code_nm, str(buy_price)))
                f.close()

                cnt +=1  #몇개 종목을 가지고 있는가
            print("가지고 있는 종목 No. : %s" % self.account_stock_dict)
            print("계좌에 보유종목 카운트 No. : %s" % cnt)


            if sPrevNext == "2":
                self.detail_account_mystock(sPrevNext="2")
            else:
                self.detail_account_info_event_loop.exit()


        elif sRQName == "실시간미체결요청":
            rows = self.dynamicCall("GetRepeatCnt(QString,QString)",sTrCode,sRQName)
            for i in range(rows):
                code = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"종목코드")
                #code = code.strip()[1:]
                code_nm = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"종목명")
                order_no = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"주문번호")
                order_status = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"주문상태")  #접수,확인,체결
                order_quantity = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"주문수량")
                order_price = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"주문가격")
                order_gubun = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"주문구분")  #
                not_quantity = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"미체결수량")
                ok_quantity = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"체결량")

                code = code.strip()
                code_nm = code_nm.strip()
                order_no = int(order_no.strip())
                order_status = order_status.strip()
                order_quantity = int(order_quantity.strip())
                order_price = int(order_price.strip())
                order_gubun = order_gubun.strip().lstrip('+').lstrip('-')
                not_quantity = int(not_quantity.strip())
                ok_quantity = int(ok_quantity.strip())

                if order_no in self.not_account_stock_dict:
                    pass
                else:
                    self.not_account_stock_dict[order_no]= {}

                nasd = self.not_account_stock_dict[order_no]

                nasd.update({"종목코드" : code})
                nasd.update({"종목명" : code_nm})
                nasd.update({"주문번호" : order_no})
                nasd.update({"주문상태" : order_status})
                nasd.update({"주문수량" : order_quantity})
                nasd.update({"주문가격" : order_price})
                nasd.update({"주문구분" : order_gubun})
                nasd.update({"미체결수량" : not_quantity})
                nasd.update({"체결량" : ok_quantity})

                print("미체결 종목 : %s" % self.not_account_stock_dict[order_gubun])

            self.detail_account_info_event_loop.exit()

        elif sRQName == "종목별투자자기관별요청":

            cnt = self.dynamicCall("GetRepeatCnt(QString,QString)",sTrCode,sRQName)
            #print("남은 일자 수 %s" % cnt)

            for i in range(cnt):
                data = []
                date = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"일자")
                value = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"현재가")
                sign = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"대비기호")  #접수,확인,체결
                nowyesterday = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"전일대비")
                per = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"등락율")
                tot_quan = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"누적거래량")
                tot_price = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"누적거래대금")  #
                person = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"개인투자자")
                foreign = self.dynamicCall("GetCommData(QString,QString,int,QString),", sTrCode, sRQName, i,"외국인투자자")
                fund = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"기관계")
                finance_inv = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"금융투자")
                insurance = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"보험")  #접수,확인,체결
                investment = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"투신")
                finance_bank = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"기타금융")
                bank = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"은행")  #
                yengi = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"연기금등")
                samo = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"사모펀드")
                gorve = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"국가")  #접수,확인,체결
                etc_com = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"기타법인")
                inforeign = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"내외국인")

                #data.append("")
                data.append(self.run_code )
                date = pd.to_datetime(date.strip(), format="%Y%m%d")
                data.append(date)
                data.append(abs(int(value.strip())))
                data.append(int(sign.strip()))
                data.append(int(nowyesterday.strip()))
                data.append(float(nowyesterday.strip()))
                data.append(int(tot_quan.strip()))
                data.append(int(tot_price.strip()))
                data.append(int(person.strip()))
                data.append(int(foreign.strip()))
                data.append(int(fund.strip()))
                data.append(int(finance_inv.strip()))
                data.append(int(insurance.strip()))
                data.append(int(investment.strip()))
                data.append(int(finance_bank.strip()))
                data.append(int(bank.strip()))
                data.append(int(yengi.strip()))
                data.append(int(samo.strip()))
                data.append(int(gorve.strip()))
                data.append(int(etc_com.strip()))
                data.append(int(inforeign.strip()))
                #data.append("")
                #print(data)
                self.calcul_data.append(data.copy())
            self.calculator_event_loop.exit()
            #f1 = open("files/list_stock.txt", "a", encoding="utf8")
            #f1.write("%s\t%s\t%s\n" % (code, code_nm, str(self.calcul_data[0][1])))
            #f1.close()

        elif sRQName == "주식일봉차트조회":
            code = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,0,"종목코드")
            code = code.strip()[1:]
            print("주식일봉자료요청 %s" % code)

            cnt = self.dynamicCall("GetRepeatCnt(QString,QString)",sTrCode,sRQName)
            print("남은 일자 수 %s" % cnt)

            # cnt = self.dynamicCall("GetRepeatCnt(QString,QString),",sTrCode,sRQName)
            # self.logging.logger.debug("남은일자수 %s" % cnt)

            for i in range(cnt):
                data = []
                current_price = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"현재가")
                value = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"거래량")
                trading_value = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"거래대금")  #접수,확인,체결
                date = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"일자")
                start_price = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"시가")
                high_price = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"고가")  #
                low_price = self.dynamicCall("GetCommData(QString,QString,int,QString),",sTrCode,sRQName,i,"저가")

                data.append("")
                data.append(current_price.strip())
                data.append(value.strip())
                data.append(trading_value.strip())
                data.append(date.strip())
                data.append(start_price.strip())
                data.append(high_price.strip())
                data.append(low_price.strip())
                data.append("")

                self.calcul_data.append(data.copy())
                code_nm = self.dynamicCall("GetMasterCodeName(QString)", code)

            #f1 = open("files/list_stock.txt", "a", encoding="utf8")
            #f1.write("%s\t%s\t%s\n" % (code, code_nm, str(self.calcul_data[0][1])))
            #f1.close()

            print(len(self.calcul_data))

            if sPrevNext == "2":
                self.day_kiwoom_db(code = code,sPrevNext=sPrevNext)
            else:
                print("총일수 %s" % len(self.calcul_data))
                pass_success =False

                # 120일 이평선을 그릴만큼의 데이터가 있는지 체크
                if self.calcul_data == None or len(self.calcul_data) < 120:
                    pass_success = False

                else:

                    # 120일 이평선의 최근 가격 구함
                    total_price = 0
                    for value in self.calcul_data[:120]:
                        total_price += int(value[1])
                    moving_average_price = total_price / 120

                    # 오늘자 주가가 120일 이평선에 걸쳐있는지 확인
                    bottom_stock_price = False
                    check_price = None
                    if int(self.calcul_data[0][7]) <= moving_average_price and moving_average_price <= int(self.calcul_data[0][6]):
                        print("오늘 주가 120이평선 아래에 걸쳐있는 것 확인")
                        bottom_stock_price = True
                        check_price = int(self.calcul_data[0][6])


                    # 과거 일봉 데이터를 조회하면서 120일 이평선보다 주가가 계속 밑에 존재하는지 확인
                    prev_price = None
                    if bottom_stock_price == True:

                        moving_average_price_prev = 0
                        price_top_moving = False
                        idx = 1
                        while True:

                            if len(self.calcul_data[idx:]) < 120:  # 120일치가 있는지 계속 확인
                                print("120일치가 없음")
                                break

                            total_price = 0
                            for value in self.calcul_data[idx:120+idx]:
                                total_price += int(value[1])
                            moving_average_price_prev = total_price / 120

                            if moving_average_price_prev <= int(self.calcul_data[idx][6]) and idx <= 20:
                                print("20일 동안 주가가 120일 이평선과 같거나 위에 있으면 조건 통과 못함")
                                price_top_moving = False
                                break

                            elif int(self.calcul_data[idx][7]) > moving_average_price_prev and idx > 20:  # 120일 이평선 위에 있는 구간 존재
                                print("120일치 이평선 위에 있는 구간 확인됨")
                                price_top_moving = True
                                prev_price = int(self.calcul_data[idx][7])
                                break

                            idx += 1

                        # 해당부분 이평선이 가장 최근의 이평선 가격보다 낮은지 확인
                        if price_top_moving == True:
                            if moving_average_price > moving_average_price_prev and check_price > prev_price:
                                print("포착된 이평선의 가격이 오늘자 이평선 가격보다 낮은 것 확인")
                                print("포착된 부분의 저가가 오늘자 주가의 고가보다 낮은지 확인")
                                pass_success = True

                if pass_success == True:
                    print("조건부 통과됨")

                    code_nm = self.dynamicCall("GetMasterCodeName(QString)", code)

                    f = open("files/condition_stock.txt", "a", encoding="utf8")
                    f.write("%s\t%s\t%s\n" % (code, code_nm, str(self.calcul_data[0][1])))
                    f.close()


                elif pass_success == False:
                    print("조건부 통과 못함")

                self.calcul_data.clear()
                self.calculator_event_loop.exit()

