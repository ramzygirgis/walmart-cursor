from functions.get_file_content import get_file_content

print("Result for 'calculator', main.py:")
print(get_file_content("calculator", "main.py"))

print("Result for 'calculator', pkg/calculator.py:")
print(get_file_content("calculator", "pkg/calculator.py"))

print("Result for 'calculator', /bin/cat:")
print(get_file_content("calculator", "/bin/cat"))

print("Result for 'calculator', pkg/does_not_exist.py:")
print(get_file_content("calculator", "pkg/does_not_exist.py"))