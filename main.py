import os
import sys
import keyboard
from scripts import spoofka, xssfreaak, zipcrack, wifcrack, antiinet, boynextdork, sniffka, onionchik, ddos, nmup, bp, phonnum, uastl
from colorama import Fore, Style
if os.name == 'posix':
    c = os.system('which pip')
    if c == 256:
        os.system('sudo apt-get install python-pip')
    else:
        pass
else:
    print('[-] Check your pip installer')

try:
    from termcolor import colored, cprint
except:
    try:
        if os.name == 'posix':
            os.system('sudo pip install colorama termcolor requests argparse urllib3 user_agent asciistuff bs4 nmap scapy ipaddress typing ARP phonenumbers tabulate netifaces socks http.server urllib3 html5lib')
            sys.exit('[+] I have installed necessary modules for you')
        elif os.name == 'nt':
            os.system('pip install colorama requests termcolor argparse urllib3 user_agent asciistuff bs4 nmap scapy ipaddress typing ARP phonenumbers tabulate netifaces socks http.server urllib3 html5lib')
            sys.exit('[+] I have installed nessecary modules for you')
        else:
            sys.exit('[-] Download and install necessary modules: colorama requests termcolor argparse urllib3 user_agent asciistuff bs4 nmap scapy ipaddress typing ARP phonenumbers tabulate netifaces socks html5lib')
    except Exception as e:
        print('[-]', e)
valhal = '''	
		 
                                     ᛟ ᛏ ᛉ ᛃ ᛭ ᛯ ᛝ ᛪ ᛥ ᛶ ᛔ ᛤ ᛦ ᚧ ᚡ ᛨ ᚸ ᚻ ᚥ ᚱ ᛰ ᛜ ᛗ ᛒ ᛳ ᚹ ᛢ ᛖ ᚤ ᛙ ᛮ ᛴ ᛸ 
                                   ᛋ ██╗░░░██╗░█████╗░██╗░░░░░██╗░░██╗░█████╗░██╗░░░░░██╗░░░░░░█████╗░ᛋ
                                  ᛋ  ██║░░░██║██╔══██╗██║░░░░░██║░░██║██╔══██╗██║░░░░░██║░░░░░██╔══██╗  ᛋ
                                ᛋ    ╚██╗░██╔╝███████║██║░░░░░███████║███████║██║░░░░░██║░░░░░███████║    ᛋ
                                ᛲ    ░╚████╔╝░██╔══██║██║░░░░░██╔══██║██╔══██║██║░░░░░██║░░░░░██╔══██║    ᛲ
                                  ᛲ  ░░╚██╔╝░░██║░░██║███████╗██║░░██║██║░░██║███████╗███████╗██║░░██║  ᛲ
                                    ᛲ░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝╚══════╝╚═╝░░╚═╝ᛲ
                                     ᛟ ᛏ ᛉ ᛃ ᛭ ᛯ ᛝ ᛪ ᛥ ᛶ ᛔ ᛤ ᛦ ᚧ ᚡ ᛨ ᚸ ᚻ ᚥ ᚱ ᛰ ᛜ ᛗ ᛒ ᛳ ᚹ ᛢ ᛖ ᚤ ᛙ ᛮ ᛴ ᛸ 
                                     
            «Путь к Вальхалле лежит через тернистые дороги, но лишь там мужественные сердца могут обрести вечную славу.»
                                     
                                          | Мультихакинг питон скрипт  |
                            | Скрипт нужен для добровольного тестирования на проникновение и прочих легальных функций |
                                               | Русский Хакинг |
                                          | Multihacking python script |
                            | The script is needed for voluntary penetration testing and other legal functions |
                                               | Russian Hacking |     
	 Author: (っ◔◡◔)っ ♥ 卄1ᗪ乙3 ♥                                               
	 Автор не несет ответственности за действия пользователей с помощью приложения
	 The author is not responsible for user actions using the application                         
	 '''
cprint(valhal,'white',attrs=['bold'])
gfgfts = input("нажмите Enter чтобы продолжить\n")
if os.name == 'posix':
    os.system("clear")
elif os.name == 'nt':
    os.system("cls")
menu = '''
     Выберите скрипт для уничтожения ᛒᛜᚹᛜᛚᛜᛒ (введите цифру скрипта):
     1 - 𐌀𐌐𐌓 𐌔𐌓𐌏𐌏𐌅
     2 - 403 𐌁𐌙𐌓𐌀𐌔𐌔
     3 - 𐌃𐌏𐌐𐌊𐌄𐌐
     4 - Ꮤ𐌉𐌅𐌉 𐌊𐌉𐌋𐌋𐌄𐌐 (работает лишь часть)
     5 - onion 𐌔𐌂𐌀n ( в доработке)
     6 - 𐌓𐌀𐌂𐌊𐌄𐌕 sniffer
     7 - 𐌂𐌀𐌋𐌋𐌕𐌐𐌀𐌂𐌊
     8 - 𐌃𐌏𐌔 𐌀𐌕𐌕𐌀𐌂𐌊
     9 - n𐌄𐌕𐌔𐌂𐌀n
     10 - Ꮤ𐌉𐌅𐌉 𐌂𐌐𐌀𐌂𐌊𐌄𐌐 (Только для макинтош или Линукс | only for mac or linux)
     11 - X𐌔𐌔 𐌅𐌐𐌄𐌀𐌊
     12 - Ɀ𐌉𐌓𐌂𐌐𐌀𐌂𐌊
     13 - Us𐌄𐌐𐌀Ᏽ𐌄𐌍𐌕 𐌔𐌕𐌄𐌀𐌋𐌄𐌐
'''
while True:
    try:
        n = int(input(menu))
        if os.name == 'posix':
            os.system("clear")
        elif os.name == 'nt':
            os.system("cls")
        if n == 1:
            arpt = input('Введите цель: | Input target:\n')
            arpg = input('Введите выходной шлюз: | Input gateway:\n')
            spoofka(arpt,arpg)
        elif n == 2:
            dm = input('Введите домен, включая http:// или https:// : | Input domain, include http:// or https:// :\n')
            pth = input('Введите путь после домена: | Input path after domain:\n')
            bp(dm, pth)
        elif n == 3:
            dorka = input('Введите домен: | Input domain:\n')
            boynextdork(dorka)
        elif n == 4:
            antiinet()
        elif n == 5:
            inpurl = input('Введите .onion url, если вы импортируете из файла, то оставьте это поле пустым и нажмите "Enter": | Input .onion url, if you are importing from a file then leave this field blank and press "Enter":\n')
            inpfile = input('Input путь до файла с ссылками, если вы импортируете из него, если нет, то оставьте это поле пустым и нажмите "Enter": | Input the path to the file with links if you are importing from it, if not, then leave this field empty and press "Enter":\n')
            inpoutp = input('Введите куда сохранить файл с отчетом, вы можете оставить это поле пустым и нажать "Enter", тогда отчет сохранится в reports/onioff+(время отчета): | Input where to save the report file, you can leave this field empty and press "Enter", then the report will be saved in reports/onioff+ (report time):\n')
            inpact = input('Если вы хотите просмотреть все логи работы скрипта, то напишите что угодно в это поле, иначе оставьте это поле пустым и нажмите "Enter": | If you want to view all the logs of the script, then input anything in this field, otherwise leave this field empty and press "Enter":\n')
            onionchik(inpurl, inpfile, inpoutp, inpact)
        elif n == 6:
            flt = input('Введите протокол для снифферинга: | Input filter for sniffering\n')
            sniffka(flt)
        elif n == 7:
            phonnum()
        elif n == 8:
            dom = input('Введите домен или айпи адрес цели: | Input your target such an ip or domain name:\n')
            tout = input('Введите тайм-аут для сокета(по умолчанию 5.0): | Set timeout for socket(default = 5.0):\n')
            pak = input('Введите по какому количеству пакетов нужно слать(по умолчанию 1000): | Set threads number for connection (default = 1000):\n')
            prt = input('Введите порт для атаки(по умолчанию 80): | Specify port target (default = 80):\n')
            slp = input('Введите время отдыха для переподключения(по умолчанию 100): | Set sleep time for reconnection(default = 100):\n')
            spip = input('Введите ложный айпи адрес атакующего, если вы не используете технологию fake-ip(если не нужно, то оставьте поле пустым: | Input a false IP address of the attacker, if you do not use fake-ip technology (if not necessary, leave the field empty:\n')
            fip = input('Введите что угодно чтобы использовать технологию fakeip или оставьте поле пустым, если вам это не нужно: | Input anything to use fake ip technology or leave the field blank if you don`t need it:\n')
            tip = input('Введите название типа атаки из списка(Request, Synflood, Pyslow): | Input the name of the attack type from the list (Request, Synflood, Pyslow):\n')
            ddos(dom, tout, pak, prt, slp, spip, fip, tip)

        elif n == 9:
            nmup()
        elif n == 10:
            wifcrack()
        elif n == 11:
            xssfreaak()
        elif n == 12:
            zipka = input('Введите путь файла: | Input file`s path:\n')
            wordl = input('Введите словарь: | Input wordlist:\n')
            zipcrack(zipka,wordl)
        elif n == 13:
            uastl()
    except KeyboardInterrupt:
        print(Style.BRIGHT + Fore.WHITE + " ")
        print("\nНазад в меню | Back to the menu\n")
        continue

