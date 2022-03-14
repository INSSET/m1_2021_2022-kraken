import subprocess


result = subprocess.check_output(["userdel", "-f", "--remove", "toto"], stderr=subprocess.STDOUT, text=True)

print(result)
