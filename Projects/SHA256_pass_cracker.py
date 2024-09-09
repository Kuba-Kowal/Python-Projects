from pwn import sha256sumhex, log
import sys

if len(sys.argv) != 2: # Checks if the number of objects parsed during execution is 2
    print(f"[X] Incorrect Number Of Arguments. [✓] {sys.argv[0]} <sha256sum>")
    sys.exit()

wanted_hash = sys.argv[1]
password_file = "rockyou.txt"
attempts = 0

with log.progress(f"Attempting to crack: {wanted_hash}") as p:  # Creates a line of text that outputs the hash we want to crack
    with open(password_file, "r", econding="latin-1") as password_list:
        for password in password_list:
            password = password.strip("\n").encode("latin-1") # Ensures any passwords that arent encoded in latin-1, now are
            password_hash = sha256sumhex(password)            # Converts the current password being checked into a sha256 format using hex
            p.status(f"[{attempts}] {password.decode("latin-1")} == {password_hash}") # Creats a seperate line that updates each time we check a hash
            if password_hash == wanted_hash:
                p.success(f"Password has found after {attempts} attempts. {password.decode("latin-1")} hashes to {password_hash}")
                exit()
            attempts += 1
        p.failure("Pass hash not found")