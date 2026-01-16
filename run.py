#!/usr/bin/python3

import dns.resolver
import subprocess
import time
import sys
import os
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Optional

class DNSTester:
    def __init__(self, dns_file: str = 'list.txt'):
        self.dns_file = dns_file
        self.dns_servers = self.load_dns_servers()
        
    def load_dns_servers(self) -> List[str]:
        if not os.path.exists(self.dns_file):
            raise FileNotFoundError(f"DNS file {self.dns_file} not found")
            
        with open(self.dns_file, 'r') as f:
            servers = []
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if self.is_valid_ip(line):
                        servers.append(line)
            return servers
    
    def is_valid_ip(self, ip: str) -> bool:
        import socket
        try:
            socket.inet_pton(socket.AF_INET, ip)
            return True
        except socket.error:
            try:
                socket.inet_pton(socket.AF_INET6, ip)
                return True
            except socket.error:
                return False
    
    def test_dns_server(self, dns_server: str, 
                       domains: List[str] = None) -> Tuple[str, Optional[float]]:
        if domains is None:
            domains = ['google.com', 'cloudflare.com']
            
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dns_server]
        resolver.lifetime = 3  # افزایش زمان انتظار
        
        total_time = 0
        success_count = 0
        
        for domain in domains:
            try:
                start = time.perf_counter()
                answers = resolver.resolve(domain, 'A')
                elapsed = (time.perf_counter() - start) * 1000
                
                if answers and len(answers) > 0:
                    total_time += elapsed
                    success_count += 1
            except Exception:
                continue
        
        if success_count == 0:
            return dns_server, None
            
        return dns_server, total_time / success_count
    
    def find_best_dns(self, max_workers: int = None) -> List[str]:
        if not self.dns_servers:
            return []
            
        if max_workers is None:
            max_workers = min(10, len(self.dns_servers))
        
        results = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.test_dns_server, server): server 
                      for server in self.dns_servers}
            
            for future in as_completed(futures):
                server, elapsed = future.result()
                if elapsed is not None:
                    results[server] = elapsed
        
        if not results:
            return []
            
        sorted_results = sorted(results.items(), key=lambda x: x[1])
        return [server for server, _ in sorted_results[:2]]

class NetworkManager:
    @staticmethod
    def get_interfaces() -> List[str]:
        interfaces = []
        
        if platform.system() == "Linux":
            try:
                result = subprocess.run(['ip', '-o', 'link', 'show'], 
                                      capture_output=True, text=True, check=True)
                for line in result.stdout.splitlines():
                    parts = line.split(':')
                    if len(parts) >= 2:
                        name = parts[1].strip()
                        if name != 'lo' and not name.startswith('virbr'):
                            interfaces.append(name)
            except (subprocess.SubprocessError, FileNotFoundError):
                pass
                
        return interfaces
    
    @staticmethod
    def set_dns(interface: str, dns_servers: List[str]) -> bool:
        if platform.system() != "Linux":
            print("This feature is only supported on Linux")
            return False
            
        try:
            # بررسی دسترسی sudo
            test_result = subprocess.run(['sudo', '-n', 'true'], 
                                       capture_output=True, text=True)
            if test_result.returncode != 0:
                print("sudo access required. Please run with sudo or enter password when prompted")
            
            # تنظیم DNS
            cmd = ['sudo', 'resolvectl', 'dns', interface] + dns_servers
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"Failed to set DNS: {e}")
            return False
        except FileNotFoundError:
            print("resolvectl not found. Is systemd-resolved installed?")
            return False
    
    @staticmethod
    def revert_dns() -> bool:
        if platform.system() != "Linux":
            return False
            
        try:
            # دریافت اینترفیس‌ها
            result = subprocess.run(['resolvectl', 'status'], 
                                  capture_output=True, text=True)
            
            interfaces = []
            for line in result.stdout.splitlines():
                if 'Link' in line:
                    parts = line.split()
                    if len(parts) > 1:
                        interfaces.append(parts[1])
            
            success = True
            for iface in interfaces:
                try:
                    subprocess.run(['sudo', 'resolvectl', 'revert', iface], 
                                 check=True, capture_output=True)
                except subprocess.CalledProcessError:
                    success = False
            
            return success
        except Exception:
            return False

def main():
    """تابع اصلی برنامه"""
    print('''
    DNS Manager
    ----------------------
    [1] Set DNS
    [2] Clean DNS
    [3] Test DNS Speed
    [9] About
    [0] Exit
    ----------------------
    ''')
    
    try:
        while True:
            try:
                choice = input('Enter Number: ').strip()
                if not choice:
                    continue
                    
                choice = int(choice)
                if choice in (0, 1, 2, 3, 9):
                    break
                print('Please enter 0, 1, 2, 3, or 9')
            except ValueError:
                print('Please enter a number')
        
        if choice == 0:
            sys.exit(0)
        
        elif choice == 1:
            try:
                tester = DNSTester()
                best_dns = tester.find_best_dns()
                
                if not best_dns:
                    print("No working DNS servers found")
                    return
                
                print(f'\nBest DNS servers: {best_dns}')
                
                manager = NetworkManager()
                interfaces = manager.get_interfaces()
                
                if not interfaces:
                    print("No network interfaces found")
                    return
                
                print('-' * 40)
                for i, iface in enumerate(interfaces, 1):
                    print(f'[{i}] {iface}')
                print('-' * 40)
                
                while True:
                    try:
                        index = int(input('Select interface number: '))
                        if 1 <= index <= len(interfaces):
                            break
                        print(f'Please enter a number between 1 and {len(interfaces)}')
                    except ValueError:
                        print('Please enter a number')
                
                selected_iface = interfaces[index - 1]
                
                if manager.set_dns(selected_iface, best_dns):
                    print(f'DNS successfully set on {selected_iface}')
                else:
                    print('Failed to set DNS')
                    
            except FileNotFoundError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
        
        elif choice == 2:
            manager = NetworkManager()
            if manager.revert_dns():
                print('DNS settings reverted to default')
            else:
                print('Failed to revert DNS settings')
        
        elif choice == 3:
            try:
                tester = DNSTester()
                print("Testing DNS servers...")
                best_dns = tester.find_best_dns()
                
                if best_dns:
                    print("\nTop 5 fastest DNS servers:")
                    for i, dns in enumerate(best_dns[:5], 1):
                        print(f"{i}. {dns}")
                else:
                    print("No working DNS servers found")
                    
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == 9:
            print("""
            DNS Manager v2.0
            Created by DEVALIGhasemi
            ----------------------
            A tool for testing and configuring DNS servers
            """)
    
    except KeyboardInterrupt:
        print('\n\nOperation cancelled by user')
        sys.exit(0)

if __name__ == "__main__":
    main()
#DEVALIGhasemi
