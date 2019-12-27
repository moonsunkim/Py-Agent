# -*- coding: utf-8 -*-
import ibm_db as db2
import socket

# DB 접속
def make_conn(server, port, database, username, password, timeout):
    return db2.connect('DATABASE={0};'.format(database) + 'HOSTNAME={0};'.format(server) + 'PORT={0};'.format(str(port)) + 'PROTOCOL=TCPIP;' + 'UID={0};'.format(username) + 'PWD={0};'.format(password) + 'ConnectTimeout={0};'.format(str(timeout)), '', '')

# SQL RAW UDP 전송
def apc_conn(sql):
    db2_connect = make_conn(APC_SERVER, APC_PORT, APC_DB, APC_ACCOUNT, APC_PASSWD, '30')
    smtm = db2.exec_immediate(db2_connect, sql)
    result = db2.fetch_both(smtm)

    while(result):
        message=str(result[6])+', '+result[1]+', '+result[2]+', '+result[3]+', '+result[4]+', '+result[5]+', '+result[0]
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientSock.sendto(message.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))
        print("[+] Log message : " + message)
        result = db2.fetch_both(smtm)

def main():
    # sql_1. 바이러스 감염정보 마지막 1분
    sql_2 = "SELECT NodeSerial, clientipaddr, name, path, db2inst1.afn_getmsgbodybyid(status) apc_Status, db2inst1.afn_getmsgbodybyid(scantype), SERVERTIME FROM AVWV3SZALERTLOG WHERE timestamp(SERVERTIME) > (current timestamp - " + DB_SEARCH_TIME + ") WITH ur"
    # sql_2. 악성코드 감염정보 마지막 1분
    sql_1 = "SELECT NodeSerial, clientipaddr, name, path, db2inst1.afn_getmsgbodybyid(status), db2inst1.afn_getmsgbodybyid(scantype), SERVERTIME FROM AVWV3VIRUSALERTLOG WHERE timestamp(SERVERTIME) > (current timestamp - " + DB_SEARCH_TIME + ") WITH ur"
    try:
        apc_conn(sql_1)
        apc_conn(sql_2)
    except Exception as e:
        message = str(e)
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientSock.sendto(message.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))
        print("[!] Apc Agent Error!!" + str(e))

if __name__ == "__main__":
    # APC 접속 정보
    APC_SERVER = '111.222.333.444'
    APC_PORT = '00000'
    APC_DB = 'DBDB'
    APC_ACCOUNT = 'APC'
    APC_PASSWD = 'PASSWORD'
    # DB 검색 시간 : days, hours, minutes,
    DB_SEARCH_TIME = '1 minutes'
    # Graylog 접속 정보 ###
    UDP_IP_ADDRESS = "11.22.33.44"
    UDP_PORT_NO = 514

    main()

