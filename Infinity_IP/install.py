import os

def install_infinity():
    choice = input("To install press (Y) to uninstall press (N) >> ")
    
    if choice.upper() == 'Y':
        # Change permissions and copy the infinity.py script to the appropriate directory
        os.system('chmod 777 infinity.py')
        os.makedirs('/usr/share/infinityIP', exist_ok=True)
        os.system('cp infinity.py /usr/share/infinityIP/infinity.py')
        
        # Create a command to execute infinity.py from anywhere
        with open('/usr/bin/infinity', 'w') as f:
            f.write('#! /bin/sh\nexec python3 /usr/share/infinityIP/infinity.py "$@"\n')
        
        os.system('chmod +x /usr/bin/infinity')
        os.system('chmod +x /usr/share/infinityIP/infinity.py')
        
        print("infinity_IP (Tor IP Changer) is installed successfully.")
        print("From now just type 'infinity' in terminal.")

    elif choice.upper() == 'N':
        # Uninstalling
        os.system('rm -r /usr/share/infinityIP')
        os.system('rm /usr/bin/infinity')
        print("infinity_IP (Tor IP Changer) has been removed successfully.")
    else:
        print("Invalid choice, please enter 'Y' or 'N'.")

if __name__ == "__main__":
    install_infinity()
