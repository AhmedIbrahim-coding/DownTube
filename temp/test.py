import os

dir = input("Enter the directory path: ")

while os.path.isfile(dir):
    print("File exists.")
else:
    print("File does not exist.")