import zipfile
import argparse

def zipcrack(zipka,wordl):
    def extract_zip(zipfile_path, password):
        try:
            with zipfile.ZipFile(zipfile_path) as zip_file:
                zip_file.extractall(pwd=password.encode())
                print("Password found: " + password)
                return True

        except Exception as e:
            if "Bad password" in str(e):
                print("Incorrect password: " + password)
            else:
                print("Error occurred: " + str(e))

        return False


    def brute_force(zipfile_path, password_list):
        for password in password_list:
            if extract_zip(zipfile_path, password):
                break


    def main():

        with open(wordlist, "r") as f:
            password_list = f.read().splitlines()

        brute_force(zipfile_path, password_list)

    zipfile_path = zipka
    wordlist = wordl
    main()
    pass

