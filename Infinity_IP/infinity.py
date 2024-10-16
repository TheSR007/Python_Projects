import os
import requests
import time

def change_ip():
    os.system("systemctl reload tor")  # Reloading the Tor service to get new IP
    
    # Using a SOCKS5 proxy to get the external IP
    proxies = {
        "http": "socks5://127.0.0.1:9050",
        "https": "socks5://127.0.0.1:9050",
    }
    
    # Fetching the external IP address
    response = requests.get("https://api.ipify.org/", proxies=proxies)
    print("[*] Your IP has been changed to: " + response.text)  # Display the new IP address

if __name__ == "__main__":
    while True:
        change_ip()  # Change IP every 10 seconds
        time.sleep(10)  # Wait for 10 seconds
