#!/usr/bin/env python3
# -.- coding: utf-8 -.-
# onioff.py



import socket, socks, requests, sys, os, datetime, re
from urllib.request import urlopen
from termcolor import colored
from bs4 import BeautifulSoup
from time import process_time, sleep
from threading import Thread
import queue as queue

def onionchik( inpfile, inpoutp, inpact,inpurl):
    hr = 0
    BLUE, RED, WHITE, YELLOW, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[32m', '\033[0m'
    sys.stdout.write(RED + """
     ██████╗ ███╗   ██╗██╗ ██████╗ ███████╗
    ██╔═══██╗████╗  ██║██║██╔═══██╗██╔════╝
    ██║   ██║██╔██╗ ██║██║██║   ██║█████╗ 
    ██║   ██║██║╚██╗██║██║██║   ██║██╔══╝  
    ╚██████╔╝██║ ╚████║██║╚██████╔╝██║     
     ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝      v2.2
    """  + END + BLUE +
    '\n' + '{}Onion URL Inspector ({}ONIOF{}){}'.format(YELLOW, RED, YELLOW, BLUE).center(67) +
    '\n' + 'Made with <3{}'.format(YELLOW, RED, YELLOW, BLUE).center(67) +
    '\n' + 'Version: {}2.2{}'.format(YELLOW, END).center(57) + '\n')


    def nowPrint(msg, error=False, ext=False, heavy=False):
        if ext:
            msg, msg_e = msg.split(' --> ')
            msg += ' --> '

        if error:
            sys.stdout.write(colored(msg, 'red'))
            if ext:
                sys.stdout.write(colored(msg_e, 'red', attrs = ['bold']))
        elif heavy:
            sys.stdout.write(colored(msg, 'yellow'))
            if ext:
                sys.stdout.write(colored(msg_e, 'yellow', attrs = ['bold']))
        else:
            sys.stdout.write(colored(msg, 'green'))
            if ext:
                sys.stdout.write(colored(msg_e, 'green', attrs = ['bold']))

        sleep(0.1)



    # Create TOR connection
    def connectTor():
        global pure_ip

        ipcheck_url = 'https://locate.now.sh/ip'
        pure_ip = requests.get(ipcheck_url).text.replace('\n','')

        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
        socket.socket = socks.socksocket
        def create_connection(address, timeout=None, source_address=None):
            sock = socks.socksocket()
            sock.connect(address)
            return sock
        socket.create_connection = create_connection

        tor_ip = requests.get(ipcheck_url).text.replace('\n','')
        if pure_ip == tor_ip:
            nowPrint("[-] Unsuccessful Tor connection", True)
            nowPrint("\n[-] Exiting...\n", True)
            os._exit(1)
        else:
            nowPrint("\n[+] Tor running normally\n")



    # Perform onion status & title inspection
    def checkOnion(onion):
        global gathered, response, outFile

        ipcheck_url = 'https://locate.now.sh/ip'
        check_ip = requests.get(ipcheck_url).text.replace('\n','')
        if check_ip != pure_ip:
            try:
                response = urlopen(onion).getcode()
            except Exception as e:
                response = e

            if response == 200:
                try:
                    soup = BeautifulSoup(urlopen(onion), 'lxml')
                    response2 = soup.title.string
                except:
                    response2 = 'UNAVAILABLE'

                show = ("[O] {} ({}ACTIVE{}) ==> '{}'").format(onion, GREEN, END, response2)
                gathered[onion] = 'ACTIVE', response2
            else:
                response = str(response).strip().replace(':','')
                response2 = 'UNAVAILABLE (Onion Inactive)'
                if len(response) > 2:
                    show = ("[O] {} ({}INACTIVE{}) - {}").format(onion, RED, END, str(response).strip())
                else:
                    show = ("[O] {} ({}INACTIVE{})").format(onion, RED, END)
                if not inpact:
                    gathered[onion] = 'INACTIVE', response2

            return show

        else:
            nowPrint("[-] Lost Tor connection", True)
            nowPrint("\n[-] Exiting...\n", True)
            os._exit(1)



    # Extract onion URLs from file
    def readFile(file):
        try:
            with open(file, 'r') as myFile:
                if os.path.getsize(file) > 0:
                    onions = myFile.readlines()
                    for onion in re.findall(r'(?:https?://)?(?:www)?\S*?\.onion', '\n'.join(onions)):
                        onion = onion.replace('\n', '')
                        if not len(onion) > len('.onion'):
                            pass
                        else:
                            if not onion.startswith('http') and not onion.startswith('https'):
                                onion = 'http://'+str(onion)
                            q.put(onion)

                else:
                    nowPrint("[-] Onion file is empty --> Please enter a valid file", True)
                    nowPrint("\n[-] Exiting...\n", True)
                    os._exit(1)

            q.join()
            myFile.close()

        except IOError:
            nowPrint("[-] Invalid onion file --> Please enter a valid file path", True)
            nowPrint("\n[-] Exiting...\n", True)
            os._exit(1)



    # Unique output filename generation
    def uniqueOutFile(checkFile):
        f = checkFile.split('.')
        if len(f) < 2:
            checkFile += '.txt'
        if os.path.exists(checkFile):
            fName, fType = checkFile.split('.')
            fList = list(fName)
            exists = True
            fName += '-{}'
            i = 1
            while exists:
                tempFile = (str(fName)+'.'+str(fType))
                tempFile = tempFile.format(i)
                if os.path.exists(tempFile):
                    i += 1
                else:
                    outFile = tempFile
                    exists = False
        else:
            outFile = checkFile

        return outFile



    def main():

        if hr == 0:


            nowPrint("\n[+] Commencing onion inspection")
            try:
                connectTor()
            except KeyboardInterrupt:
                print('\nHave a great day! :)')
                os._exit(1)
            except:
                nowPrint("\n[-] Tor offline --> Please make sure Tor is running", True)
                nowPrint("\n[-] Exiting...\n", True)
                os._exit(1)


            def inspect():
                while True:
                    onion = q.get()
                    response = checkOnion(onion)
                    sys.stdout.write(response+'\n')
                    sleep(0.1)
                    q.task_done()

            for i in range(concurrent):
                t = Thread(target=inspect)
                t.daemon = True
                t.start()

            try:
                if len(inpurl) > 0:
                    if not inpurl.startswith('http') and not inpurl.startswith('https'):
                       nowPrint("[-] No onion URL found --> Please enter a valid URL", True)
                       nowPrint("\n[-] Exiting...\n", True)
                       os._exit(1)
                    else:
                       q.put(inpurl)
                       q.join()
            except KeyboardInterrupt:
                print('\nHave a great day! :)')
                os._exit(1)


            if len(inpfile) > 0:
                file = inpfile
                readFile(file)


            try:
                outFile = uniqueOutFile(inpoutp)
                with open(outFile, 'a') as OutFile:
                    for k, v in gathered.items():
                        # output format: {some_link.onion} - {page_title}
                        if 'ACTIVE' in v[0]:
                            OutFile.write('{} - {}'.format(k, v[1]) + '\n')
                        else:
                            OutFile.write('{} - {}'.format(k, v[0]) + '\n')
            except IOError:
                nowPrint("[-] Invalid path to out file given --> Please enter a valid path", True)
                nowPrint("\n[-] Exiting...\n", True)
                os._exit(1)
            except KeyboardInterrupt:
                print('\nHave a great day! :)')
                os._exit(1)


            nowPrint("[!] Onion inspection successfully complete", False, False, True)
            saved_msg = "\n[!] Inspection report saved as --> " + str(outFile)
            nowPrint(saved_msg, False, True, True)
            print("\nComp/tional time elapsed:", (process_time() - start))

        else:
            nowPrint("\n[!] Use '-h' or '--help' for usage options\n", False, False, True)


    start = process_time()

    if len(inpoutp) == 0 :
        inpoutp = 'reports/onioff_{}'.format(str(datetime.datetime.now())[:-7].replace(' ', '_'))
    if len(inpact) > 0:
        inpact = True

    gathered = {}

    concurrent = 200
    q = queue.Queue(concurrent * 2)

    main()
    pass