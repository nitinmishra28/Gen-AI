import sys
import os

print("Python Path:")
for path in sys.path:
    print(path)

print("\nCurrent Directory Contents:")
print(os.listdir('.'))