import time

lines = ["Line 1", "Line 2", "Line 3"]

for line in lines:
    print(line, end='\r')
    time.sleep(1)  # Delay to simulate processing time

print()  # Print an empty line to move to the next line after the loop
