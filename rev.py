import socket
import requests
from concurrent.futures import ThreadPoolExecutor
from re import findall as reg
import os
from colorama import Fore as F

fg = F.LIGHTGREEN_EX
fr = F.LIGHTRED_EX
fw = F.LIGHTWHITE_EX
fy = F.LIGHTYELLOW_EX
fb = F.LIGHTBLUE_EX
flc = F.LIGHTCYAN_EX

def logo():
    colm = os.get_terminal_size().columns
    print("{}Reverse IP".format(fg))

def rev(host):
    if len(str(host).split('.')) == 4:
        ip = host
    else:
        ip = socket.gethostbyname(host)
    url = 'https://api.reverseip.my.id/?ip={}'.format(ip)
    req = requests.get(url).text
    req = str(req).split('":[')[1]
    sites = reg('"(.*?)"',req)
    sites = [*set(sites)]
    for site in sites:
        print('{}[{}+{}] {}'.format(fw,fg,fw,site))
        open('Reversed-sites.txt','a',errors='ignore').write(site + '\n')

def reverse():
    os.system('cls')
    logo()
    try:
        ThreadPoolExecutor(100).map(rev,list(x.strip() for x in open(input('{}[{}+{}] List: '.format(fw,fg,fw)),'r',errors='ignore').readlines()))
    except Exception as e:
        print(e)
        pass
    input('{}[{}!{}] Press {}Enter{} to Exit!{}'.format(flc,fr,flc,fr,flc,fw))


reverse()