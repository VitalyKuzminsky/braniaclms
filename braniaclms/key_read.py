def get_key():
    with open("key.pyc", "r") as file1:
        for line in file1:
            return line.strip()

