import os
import socket
import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

# Initialize colorama
init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('title IP Checker - Made by Wado')

def print_ascii_art():
    ascii_art = """
,--.   ,--.  ,---.  ,------.   ,-----.      ,-----.,--.  ,--.,------. ,-----.,--. ,--.,------.,------.  
|  |   |  | /  O  \ |  .-.  \ '  .-.  '    '  .--./|  '--'  ||  .---''  .--./|  .'   /|  .---'|  .--. ' 
|  |.'.|  ||  .-.  ||  |  \  :|  | |  |    |  |    |  .--.  ||  `--, |  |    |  .   ' |  `--, |  '--'.' 
|   ,'.   ||  | |  ||  '--'  /'  '-'  '    '  '--'\|  |  |  ||  `---.'  '--'\|  |\   \|  `---.|  |\  \  
'--'   '--'`--' `--'`-------'  `-----'      `-----'`--'  `--'`------' `-----'`--' '--'`------'`--' '--' 
"""
    print(Fore.RED + ascii_art + Style.RESET_ALL)

def print_boxed_text(title, options):
    width = 42  # Adjust the width as needed
    border = '  +' + '-' * (width - 2) + '+'
    
    print(Fore.RED + border + Style.RESET_ALL)
    print(Fore.RED + '  |' + title.center(width - 2) + '|' + Style.RESET_ALL)
    print(Fore.RED + '  |' + ' ' * (width - 2) + '|' + Style.RESET_ALL)
    
    for option in options:
        print(Fore.RED + '  |' + option.ljust(width - 2) + '|' + Style.RESET_ALL)
    
    print(Fore.RED + '  |' + ' ' * (width - 2) + '|' + Style.RESET_ALL)
    print(Fore.RED + border + Style.RESET_ALL)

def generate_google_maps_url(lat, lon):
    return f"https://www.google.com/maps/?q={lat},{lon}"

def get_ip_info(ip):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    response.encoding = 'utf-8'  # Ensure proper encoding
    data = response.json()
    
    if data['status'] == 'success':
        info = {
            'IP': data['query'],
            'Country': data['country'],
            'Region': data['regionName'],
            'City': data['city'],
            'ISP': data['isp'],
            'Latitude': data['lat'],
            'Longitude': data['lon']
        }
        return info
    else:
        return {'Error': 'Could not retrieve information'}

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, port))
        return port, True
    except (socket.timeout, socket.error):
        return port, False
    finally:
        sock.close()

def scan_ports(ip, ports):
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, ip, port) for port in ports]
        for future in futures:
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
    return open_ports

def check_vpn(ip):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'success':
        # ip-api does not directly provide VPN or proxy information.
        # We need to use a different service for VPN/proxy detection.
        is_vpn = data.get('hosting', False) or data.get('proxy', False)
        return is_vpn
    else:
        return None

def main_menu():
    print_ascii_art()
    options = [
        "1. IP Information Lookup",
        "2. Port Scanning",
        "3. VPN/Proxy Detection",
        "4. Exit"
    ]
    print_boxed_text("Network Reconnaissance Tool", options)
    choice = input(Fore.RED + "Select an option: " + Style.RESET_ALL)
    return choice

def main():
    while True:
        clear_screen()
        choice = main_menu()
        if choice == '':
            continue  # If "Enter" is pressed without any input, re-prompt
        elif choice == '1':
            ip = input(Fore.RED + "Enter IP address: " + Style.RESET_ALL)
            info = get_ip_info(ip)
            if 'Error' in info:
                print(Fore.RED + info['Error'] + Style.RESET_ALL)
            else:
                print(Fore.CYAN + f"IP: {info['IP']}" + Style.RESET_ALL)
                print(Fore.CYAN + f"Country: {info['Country']}" + Style.RESET_ALL)
                print(Fore.CYAN + f"Region: {info['Region']}" + Style.RESET_ALL)
                print(Fore.CYAN + f"City: {info['City']}" + Style.RESET_ALL)
                print(Fore.CYAN + f"ISP: {info['ISP']}" + Style.RESET_ALL)
                print(Fore.CYAN + f"Latitude: {info['Latitude']}" + Style.RESET_ALL)
                print(Fore.CYAN + f"Longitude: {info['Longitude']}" + Style.RESET_ALL)
                maps_url = generate_google_maps_url(info['Latitude'], info['Longitude'])
                print(Fore.CYAN + f"Google Maps URL: {maps_url}" + Style.RESET_ALL)
        elif choice == '2':
            ip = input(Fore.RED + "Enter IP address: " + Style.RESET_ALL)
            ports = range(1, 1025)
            open_ports = scan_ports(ip, ports)
            print(Fore.CYAN + f"Open ports on {ip}: {open_ports}" + Style.RESET_ALL)
        elif choice == '3':
            ip = input(Fore.RED + "Enter IP address: " + Style.RESET_ALL)
            is_vpn = check_vpn(ip)
            if is_vpn is not None:
                print(Fore.CYAN + f"{ip} is {'a VPN/proxy' if is_vpn else 'not a VPN/proxy'}" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Could not retrieve information" + Style.RESET_ALL)
        elif choice == '4':
            print(Fore.RED + "Goodbye!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid choice, try again." + Style.RESET_ALL)
        
        input(Fore.RED + "\nPress Enter to continue..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
