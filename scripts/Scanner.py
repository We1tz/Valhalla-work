import argparse
import nmap
from socket import *

def nmup():


    def nmapScan(tgtHost, tgtPort):
        nmscan = nmap.PortScanner()
        nmscan.scan(tgtHost, tgtPort)
        try:
            state = nmscan[tgtHost]['tcp'][int(tgtPort)]['state']
            print(' [*] ' + tgtHost + ' tcp/' + tgtPort + ' ' + state)
        except KeyError as e:
            print(e)
            print('The specified IP address is unreachable')
            exit()

    def main():
        tgtHost = str(input("Введите хост: | Input host:\n"))

        if (tgtHost == None):
            pass
        for tgtPort in range(0,1025):
            tgtPort = str(tgtPort)
            nmapScan(tgtHost, tgtPort)
    main()
    pass
