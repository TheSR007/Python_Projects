import requests
import time
from concurrent.futures import ThreadPoolExecutor
import json
from datetime import datetime
import argparse

# Color constants
COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_BLUE = '\033[94m'
COLOR_RESET = '\033[0m'

class ProxyChecker:
    def __init__(self, max_workers=20, fast_mode=False):
        self.max_workers = max_workers
        self.timeout = 10  # seconds
        self.test_url = "http://httpbin.org/ip"
        self.headers_test_url = "http://httpbin.org/headers"
        self.ipinfo_url = "http://ipinfo.io/{}/json"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.protocols_to_check = ['http', 'https', 'socks4', 'socks5']
        self.fast_mode = fast_mode
        
    def check_proxy(self, proxy_input):
        """Check a single proxy with all protocols or specified protocol"""
        if "://" in proxy_input:
            protocol, proxy = proxy_input.split("://")
            result = self._check_single_protocol(proxy, protocol.lower())
            print(" " * 50, end="\r")  # Clear the line
            return result
        else:
            results = []
            for protocol in self.protocols_to_check:
                result = self._check_single_protocol(proxy_input, protocol)
                if result and result["Status"] == "Alive":
                    results.append(result)
                    if self.fast_mode:
                        print(" " * 50, end="\r")  # Clear the line
                        return results[0]
            print(" " * 50, end="\r")  # Clear the line
            return results[0] if results else None
    
    def _check_single_protocol(self, proxy, protocol):
        """Check proxy with a specific protocol"""
        print(f"{COLOR_BLUE}Checking {protocol.upper()}://{proxy}{COLOR_RESET}", end="\r")
        
        proxy_info = {
            "IP": "",
            "Port": "",
            "Protocol": protocol,
            "Status": "Dead",
            "Response Time": 0
        }
        
        if not self.fast_mode:
            proxy_info.update({
                "Location": "N/A",
                "Country": "N/A",
                "ISP": "N/A",
                "Anonymity": "Unknown",
                "Last Checked": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        try:
            ip_port = proxy.split(":")
            if len(ip_port) != 2:
                return None
            
            proxy_info["IP"] = ip_port[0]
            proxy_info["Port"] = ip_port[1]
            
            proxies = {}
            if protocol in ['http', 'https']:
                proxies = {
                    "http": f"{protocol}://{proxy}",
                    "https": f"{protocol}://{proxy}"
                }
            elif protocol == 'socks4':
                proxies = {
                    "http": f"socks4://{proxy}",
                    "https": f"socks4://{proxy}"
                }
            elif protocol == 'socks5':
                proxies = {
                    "http": f"socks5://{proxy}",
                    "https": f"socks5://{proxy}"
                }
            
            start_time = time.time()
            
            try:
                response = requests.get(
                    self.test_url,
                    proxies=proxies,
                    timeout=self.timeout,
                    headers=self.headers
                )
                proxy_info["Response Time"] = round((time.time() - start_time) * 1000, 2)
                
                if response.status_code == 200:
                    proxy_info["Status"] = "Alive"
                    print(f"{COLOR_GREEN}✓ {protocol.upper()}://{proxy} ({proxy_info['Response Time']}ms){COLOR_RESET}")
                    
                    if not self.fast_mode:
                        if proxy_info["IP"] in response.text:
                            proxy_info["Anonymity"] = "Transparent"
                        else:
                            headers_test = requests.get(
                                self.headers_test_url,
                                proxies=proxies,
                                timeout=self.timeout,
                                headers=self.headers
                            )
                            if headers_test.status_code == 200:
                                headers_data = headers_test.json()
                                if "X-Forwarded-For" in headers_data["headers"]:
                                    proxy_info["Anonymity"] = "Anonymous"
                                else:
                                    proxy_info["Anonymity"] = "Elite"
                        
                        try:
                            ip_info = requests.get(
                                self.ipinfo_url.format(proxy_info["IP"]),
                                timeout=self.timeout
                            ).json()
                            proxy_info["Location"] = ip_info.get("city", "N/A")
                            proxy_info["Country"] = ip_info.get("country", "N/A")
                            proxy_info["ISP"] = ip_info.get("org", "N/A")
                            if proxy_info["Location"] == "N/A" and proxy_info["Country"] != "N/A":
                                proxy_info["Location"] = proxy_info["Country"]
                        except:
                            pass
                
                else:
                    print(f"{COLOR_RED}✗ {protocol.upper()}://{proxy} (Dead){COLOR_RESET}")
            
            except requests.exceptions.RequestException:
                print(f"{COLOR_RED}✗ {protocol.upper()}://{proxy} (Dead){COLOR_RESET}")
            
            return proxy_info
            
        except Exception as e:
            print(f"{COLOR_RED}Error checking {protocol.upper()}://{proxy}: {str(e)}{COLOR_RESET}")
            return None
    
    def check_proxies(self, proxies):
        """Check multiple proxies using threading"""
        print(f"\n{COLOR_YELLOW}Starting check for {len(proxies)} proxies...{COLOR_RESET}\n")
        valid_proxies = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(self.check_proxy, proxies)
            
            for result in results:
                if result and result["Status"] == "Alive":
                    valid_proxies.append(result)
        
        return valid_proxies
    
    def display_results(self, proxies):
        """Display the proxy information in appropriate format"""
        if not proxies:
            print(f"{COLOR_RED}No valid proxies found.{COLOR_RESET}")
            return
        
        if self.fast_mode:
            print(f"\n{COLOR_GREEN}Working proxies:{COLOR_RESET}")
            for proxy in proxies:
                print(f"{proxy['Protocol'].upper()}://{proxy['IP']}:{proxy['Port']} ({proxy['Response Time']}ms)")
        else:
            print(f"\n{COLOR_GREEN}Detailed results:{COLOR_RESET}")
            print("{:<15} {:<8} {:<20} {:<25} {:<10} {:<15} {:<12} {:<10} {:<15}".format(
                "IP", "Port", "Location", "ISP", "Status", "Anonymity", "Protocol", "Resp Time", "Last Checked"
            ))
            print("-" * 140)
            
            for proxy in proxies:
                print("{:<15} {:<8} {:<20} {:<25} {:<10} {:<15} {:<12} {:<10} {:<15}".format(
                    proxy["IP"],
                    proxy["Port"],
                    proxy.get("Location", "N/A"),
                    (proxy.get("ISP", "N/A")[:22] + "...") if len(proxy.get("ISP", "")) > 25 else proxy.get("ISP", "N/A"),
                    proxy["Status"],
                    proxy.get("Anonymity", "N/A"),
                    proxy["Protocol"].upper(),
                    f"{proxy['Response Time']}ms",
                    proxy.get("Last Checked", "N/A")
                ))

def main():
    parser = argparse.ArgumentParser(description="Proxy Checker with dual modes by TheSR")
    parser.add_argument("-f", "--fast", action="store_true", help="Enable fast checking mode")
    parser.add_argument("-i", "--input", help="Input file with proxies (one per line)")
    args = parser.parse_args()

    print(f"{COLOR_YELLOW}Proxy Checker - Dual Mode by TheSR{COLOR_RESET}")
    print(f"Mode: {COLOR_BLUE}{'FAST (minimal info)' if args.fast else 'VERBOSE (detailed info)'}{COLOR_RESET}")
    
    # Get proxies
    if args.input:
        try:
            with open(args.input, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"{COLOR_RED}Error: File '{args.input}' not found.{COLOR_RESET}")
            return
    else:
        proxy_source = input("Enter proxy list (comma separated): ").strip()
        proxies = [p.strip() for p in proxy_source.split(",") if p.strip()]
    
    if not proxies:
        print(f"{COLOR_RED}No proxies provided.{COLOR_RESET}")
        return
    
    start_time = time.time()
    
    checker = ProxyChecker(fast_mode=args.fast)
    valid_proxies = checker.check_proxies(proxies)
    
    print(f"\n{COLOR_GREEN}Found {len(valid_proxies)} working proxies out of {len(proxies)}{COLOR_RESET}")
    checker.display_results(valid_proxies)
    
    if not args.fast and valid_proxies:
        save = input("\nSave results to file? (y/n): ").lower()
        if save == 'y':
            filename = f"proxy_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(valid_proxies, f, indent=2)
            print(f"{COLOR_GREEN}Results saved to {filename}{COLOR_RESET}")
    
    print(f"\n{COLOR_YELLOW}Total execution time: {time.time() - start_time:.2f} seconds{COLOR_RESET}")

if __name__ == "__main__":
    main()