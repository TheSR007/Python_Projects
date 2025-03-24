#!/bin/bash

# Proxy Checker in Bash
# Usage: ./proxycheck.sh [proxy_file.txt] or paste proxies directly

# Configuration
TIMEOUT=5  # seconds
TEST_URL="http://httpbin.org/ip"
THREADS=20  # concurrent checks
OUTPUT_FILE="working_proxies_$(date +%Y%m%d_%H%M%S).txt"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Check dependencies
if ! command -v curl &> /dev/null; then
    echo -e "${RED}Error: curl is required but not installed.${NC}"
    exit 1
fi

if ! command -v parallel &> /dev/null; then
    echo -e "${YELLOW}Warning: GNU parallel not found. Using slower sequential checking.${NC}"
    THREADS=1
fi

# Get proxies
if [ $# -ge 1 ]; then
    PROXIES=$(cat "$1" | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{1,5}')
else
    echo "Paste proxies (IP:PORT format, one per line, Ctrl+D to finish):"
    PROXIES=$(cat | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{1,5}')
fi

if [ -z "$PROXIES" ]; then
    echo -e "${RED}No valid proxies found.${NC}"
    exit 1
fi

TOTAL=$(echo "$PROXIES" | wc -l)
echo -e "Checking ${YELLOW}$TOTAL${NC} proxies..."

# Check function
check_proxy() {
    local proxy=$1
    local ip=$(echo $proxy | cut -d: -f1)
    local port=$(echo $proxy | cut -d: -f2)
    
    # Try SOCKS4
    if curl -s -m $TIMEOUT --socks4 "$ip:$port" $TEST_URL &> /dev/null; then
        echo -e "${GREEN}SOCKS4${NC} $proxy"
        echo "socks4://$proxy" >> $OUTPUT_FILE
        return
    fi
    
    # Try SOCKS5
    if curl -s -m $TIMEOUT --socks5 "$ip:$port" $TEST_URL &> /dev/null; then
        echo -e "${GREEN}SOCKS5${NC} $proxy"
        echo "socks5://$proxy" >> $OUTPUT_FILE
        return
    fi
    
    # Try HTTP
    if curl -s -m $TIMEOUT --proxy "http://$proxy" $TEST_URL &> /dev/null; then
        echo -e "${GREEN}HTTP${NC} $proxy"
        echo "http://$proxy" >> $OUTPUT_FILE
        return
    fi
    
    # Try HTTPS
    if curl -s -m $TIMEOUT --proxy "https://$proxy" $TEST_URL &> /dev/null; then
        echo -e "${GREEN}HTTPS${NC} $proxy"
        echo "https://$proxy" >> $OUTPUT_FILE
        return
    fi
    
    echo -e "${RED}DEAD${NC} $proxy"
}

# Make output file empty
> $OUTPUT_FILE

# Run checks
if [ "$THREADS" -gt 1 ]; then
    export -f check_proxy
    export TIMEOUT TEST_URL GREEN RED NC OUTPUT_FILE
    echo "$PROXIES" | parallel -j $THREADS check_proxy
else
    while read -r proxy; do
        check_proxy "$proxy"
    done <<< "$PROXIES"
fi

# Results
WORKING=$(wc -l < $OUTPUT_FILE)
echo -e "\nFound ${GREEN}$WORKING${NC} working proxies out of ${YELLOW}$TOTAL${NC}"
echo "Working proxies saved to: $OUTPUT_FILE"