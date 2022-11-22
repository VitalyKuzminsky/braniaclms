def get_secret():
    with open("secret.pyc", "r") as file1:
        for line in file1:
            return line.strip()
