# coding: utf-8
import socket
import argparse

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    print(ip)

def init():
    try:
        welcome = 'welcome'
        parser = argparse.ArgumentParser(description=welcome)
        parser.add_argument("--ip","-ip",help="get",action="store_true")
        arg = parser.parse_args()
        if arg.ip:
            print('ip')
    except Exception as e:
        print(e)