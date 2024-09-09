binary_value = input("Please input your binary value: ")
place_value = 1
denary_total = 0
counter = 0
denary_to_hex = []

denary_format = binary_value.strip().replace(" ", "")
binary_list = binary_value.split(" ")

# Calculates denary value from binary number
for digit in denary_format[::-1]:
  denary_value = int(digit) * place_value # Assigns the place value it is currently calculating its corresponding binary value
  denary_total += denary_value 
  place_value *= 2

# Calculate the hex value from binary number
for section in binary_list:
    place_value = 1
    hex_total = 0
    # For each place value within a byte give it, its corresponding denary value
    for digit in section[::-1]:
      hex_value = int(digit) * place_value
      hex_total += hex_value
      place_value *= 2

    denary_to_hex.append(hex(hex_total))

print(f"The hex value of your binary input is: {denary_to_hex}")
print(f"The denary value of your binary input is: {denary_total}")
