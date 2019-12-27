# -*- coding: utf-8 -*-
import paramiko
import socket
import time
import hashlib

"""
paramiko\py3compat.py 파일 수정
    def u(s, encoding='utf8'):
        if isinstance(s, bytes):
            try:   								<< 디코딩 에러시 ISO-8859 로 변환
                return s.decode(encoding)
            except UnicodeDecodeError:
                return s.decode('ISO-8859-1')  
"""

def main():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(DB_SERVER, username=DB_ACCOUNT, password=DB_PASSWD)
        stdin, stdout, stderr = ssh.exec_command(MSG1)
        stdin.flush()
        time.sleep(2)
        stdin, stdout, stderr = ssh.exec_command(MSG2)
        message = str(stdout.readline())
        message_check = hashlib.md5(message.encode())
        message_md5 = message_check.hexdigest()
        chakra_hash_file = open('/home/gabiaspol/chakra_hash', 'r')
        old_message_md5 = chakra_hash_file.read()
        list = message.split(' ; ')  # 전체를 ; 로 스플릿
        pointer_list = list[0].split('[ChakraMax Alert]')  # 첫번째 쪼개기

        if "Clinet" in pointer_list[1]:
            pointer_list[1] = "Client Table Row 경고"
        elif "OTP" in pointer_list[1]:
            pointer_list[1] = "OTP Authentication for DB Login"
        elif "change" in pointer_list[1]:
            pointer_list[1] = "Change_contact_info 테이블 Row 경고"
        elif "domain" in pointer_list[1]:
            if "partner" in pointer_list[1]:
                pass
            else:
                pointer_list[1] = "domain_contat 테이블 Row 경고"
        elif "hosting" in pointer_list[1]:
            pointer_list[1] = "hosting 테이블 Row 경고"
        elif "partner" in pointer_list[1]:
            pointer_list[1] = "partner_domain_contact 테이블 Row 경고"
        else:
            pointer_list[1] = "응답 시간 경고"  # 한글로만 된것 처리 필요
        # 나머지 문자열 치환
        # list[0] = pointer_list[0]+pointer_list[1]
        # list[0] = list[0].replace("dbsec cgw_sf:","")

        list[0] = pointer_list[1]
        list[1] = "회원데이터베이스"
        list[2] = "회원데이터베이스디비"

        if "Row" in list[3]:
            list[3] = "customer 계정 1000 Row 이상"
        if "#" in list[16]:
            try:
                list[16] = list[16].replace("#015#012#011#011#011#011", "")
                list[16] = list[16].replace("#015#012#011#011#011", "")
                list[16] = list[16].replace("#015#012", "")
                list[16] = list[16].replace("#015", "")
                list[16] = list[16].replace("#012", "")
            except:
                pass

        message = ', '.join(list)

        if message_md5 == old_message_md5:
            print("[=] 값 같음")
            chakra_hash_file.close()

        else:
            chakra_hash_file = open('/home/gabiaspol/chakra_hash', 'w')
            chakra_hash_file.write(message_check.hexdigest())
            chakra_hash_file.close()
            clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            clientSock.sendto(message.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))
            print("[+] Log message : " + message)

        ssh.close()

    except Exception as e:
        message = "[!] ChakraMAX Agent Error!!" + str(e)
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientSock.sendto(message.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))
        print("[!] ChakraMAX Agent Error!!" + str(e))


if __name__ == "__main__":
    # 접속 정보
    DB_SERVER = '111.222.333.444'
    DB_ACCOUNT = 'dbaccount'
    DB_PASSWD = 'dbpassword'
    MSG1 = 'tail -100 /var/log/messages | grep ChakraMax > /home/dbaccount/chakra_log'
    MSG2 = 'tail -1 /home/dbaccount/chakra_log'
    UDP_IP_ADDRESS = "11.22.33.44"
    UDP_PORT_NO = 5144

    main()