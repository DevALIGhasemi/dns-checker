#!/usr/bin/python3

import dns.resolver
import subprocess
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

print('''
       Welcome
----------------------
[1] Set     DNS
[2] Clean   DNS
[9] About Me
[0] exit
----------------------
''')

while True:
    try:
        choice = int(input('Enter Number: '))
        if choice in (0,1,2,9):
            break
        else:
            print('The number must be 0 or 1 or 2 or 9')
    except ValueError:
        print('Please enter just number')

DNS_FILE = 'list.txt'
with open(DNS_FILE, 'r') as f:
    dns_servers = [line.strip() for line in f if line.strip()]

def get_network_interfaces():
    result = subprocess.run(['ip', '-o', 'link', 'show'], capture_output=True, text=True)
    interfaces = []
    for line in result.stdout.splitlines():
        name = line.split(':')[1].strip()
        if name != 'lo':
            interfaces.append(name)
    return interfaces

interfaces = get_network_interfaces()

import dns.resolver
import time

def test_dns(dns_server, domains=['google.com', 'soft98.ir']):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    resolver.lifetime = 2 
    total_time = 0
    success_count = 0
    for domain in domains:
        start = time.time()
        try:
            resolver.resolve(domain, 'A')
            total_time += (time.time() - start) * 1000 
            success_count += 1
        except Exception:
            pass
    if success_count == 0:
        return dns_server, None
    return dns_server, total_time / success_count

def total_test():
    results = {}
    with ThreadPoolExecutor(max_workers=37) as executor:
        future_to_server = {executor.submit(test_dns, server): server for server in dns_servers}
        for future in as_completed(future_to_server):
            server, elapsed = future.result()
            if elapsed is not None:
                results[server] = elapsed

    if results:
        sorted_results = sorted(results.items(), key=lambda x: x[1])
        best_dns_list = [server for server, _ in sorted_results[:2]]  # دو DNS سریع‌تر
        print(f'\nBest DNS list: {best_dns_list}')
    else:
        print('\nNo DNS server responded')
        return

    print('<-------------------------------------->')
    for i, iface in enumerate(interfaces, 1):
        print(f'[{i}] {iface}')
    print('<-------------------------------------->')
    while True:
        try:
            index = int(input('Enter number of interface: '))
            if 1 <= index <= len(interfaces):
                break
            else:
                print('Invalid number, try again')
        except ValueError:
            print('Please enter a number')
    interface_choice = interfaces[index - 1]
    try:
        subprocess.run(['sudo', 'resolvectl', 'dns', interface_choice] + best_dns_list)
    except:
        print('Could not set DNS.')
    else:
        print(f'DNS applied on {interface_choice}: {", ".join(best_dns_list)}')

def clean():
    result = subprocess.run(['resolvectl', 'status'], capture_output=True, text=True)
    interfaces = [line.split()[1] for line in result.stdout.splitlines() if 'Link' in line]
    try:
        for iface in interfaces:
            subprocess.run(['sudo','resolvectl','revert', iface])
    except:
        print('Could not restore settings')
    else:
        print('<-------------------------------------->')
        print('DNS reverted to automatic')        
        sys.exit()
try:
    if choice == 1:
        total_test()
    elif choice == 2:
        clean()
    elif choice == 9:
        text = 'This program was created by ALIGhasemi'
        width = 56
        print('┏' + '━'*width + '┓')
        print('┃' + text.center(width) + '┃')
        print('┗' + '━'*width + '┛')
    elif choice == 0:
        sys.exit(0)
except KeyboardInterrupt:
        print('\n The user pressed CTRL+C')
        sys.exit(0)
