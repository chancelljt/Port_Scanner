import socket
import time

def port_scanner(target, port):
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set timer for the connection
        s.settimeout(5)
        
        # Attempt to connect to the target IP and Port
        s.connect((target, port))
        
        # Close the socket
        s.close()
        return True
    except:
        return False
    
user_target = input("Please enter the target IP address using the following guide (xx.xx.xx.xx): ")
user_ports = input("Please enter the ports you would like to scan for: ")

print("Target IP: "+ user_target)
print("Target Port(s): " + user_ports)

# Split the entered ports by commas and convert to integers
ports_to_scan = [int(port.strip()) for port in user_ports.split(',')]

for port in ports_to_scan:
    result = port_scanner(user_target, port)
    if result:
        print(f"Port {port} is open on {user_target}.")
    else:
        print(f"Port {port} is closed on {user_target}.")