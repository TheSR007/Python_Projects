# Infinity IP Using Tor

## Usage
```
python3 infinity.py
```
(To run infinity IP and get new ip every 10 sec)

```
python3 install.py
```
(To install infinity IP as infinity which you can run thro terminal)

## Requirements
- GNU/Linux OS
- Tor
- Python 3.x 
- Python requests module
- Python socks module

## Tor Setup (Arch Linux)

```
pacman -Syu 
```
(Updating database)

```
pacman -S tor 
```
(downloading tor Service)

```
systemctl start tor 
```
(Starting Tor Service)

```
systemctl enable tor 
```
(Optional, makes tor run at startup)

```
systemctl status tor 
```
(Checking Status)


## Python Setup

```
pacman -S python
```
(downloading Python)

```
pacman -S python-requests
```
(dowloading python requests module)

```
pacman -S python-socks
```
(downloading python socks module)