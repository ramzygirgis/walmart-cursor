from functions.run_python_file import run_python_file
print("should print the calculator's usage instructions:")
print(run_python_file("calculator", "main.py"))

print("\nshould run the calculator... which gives a kinda nasty rendered result:")
print(run_python_file("calculator", "main.py", ["3 + 5"]))

print("\nshould run the calculator's tests successfully:")
print(run_python_file("calculator", "tests.py"))

print("\nthis should return an error:")
print(run_python_file("calculator", "../main.py"))

print("\nthis should return an error:")
print(run_python_file("calculator", "nonexistent.py"))

print("\nthis should return an error:")
print(run_python_file("calculator", "lorem.txt"))