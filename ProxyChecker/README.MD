# ProxyChecker

## Usage
```
python3 ProxyChecker.py [-h] [-f] [-i INPUT]
```
### Options
- -h /help
- -f -i input_file // Fast Mode + proxyfile
- -i (input file)  // Verbose Mode + proxyfile
- -f               // Fast Mode + individual proxy separated by comma
- Nothing          // Verbose Mode + individual proxy separated by comma

## Requirements
- Python 3.x 
- Python requests module

### Note: A bash Script is also provided for testing which requires curl + GNU parallel