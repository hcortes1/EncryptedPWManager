from cryptography.fernet import Fernet

class PasswordManager:
    # initializing constructor
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        # Key that can be used for encrpy/decrypt. generated using fernet.generate_key
        self.key = Fernet.generate_key()
        # open path write in bytes mode as f 
        with open(path, 'wb') as f:
            f.write(self.key)
    # function for loading 
    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()
    def create_pw_file(self, path, initial_values = None):
        self.password_file = path 

        if initial_values is not None:
            # can iterate using .items over list of tuples in dictionary 
            for key, values in initial_values.items():
                self.add_password(key, values)
    def load_pw_file(self, path): 
        self.password_file = path 

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":") # key value pair separated by a character in this case a colon 
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, site, password):
        self.password_dict[site] = password

        if self.password_file is not None:
            # w overwrites a file and a adds lines to the file
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")
    def get_password(self, site):
        return self.password_dict[site]

def main():
    #TODO: VALUES IN PASSWORD ARE TEST, FUTURE ADDITIONS TO THIS PROJECT WILL INCLUDE THE ADDITION OF A FULL EXECUTABLE GUI THAT STORES THESE PASSWORDS LOCALLY. 

    password = {"EMAIL": "FORTNITEGIGABALLS"
                }
    pm = PasswordManager()
    print(""" Encrypted Password Manager
    (1) Create a new key 
    (2) Load an existing key 
    (3) Create a new password file 
    (4) Load existing password file 
    (5) Add a new password 
    (6) Get a password 
    (q) Exit Password Manger 
    """)

    done = False
    while not done: 
        choice = input(" Enter your choice: ")
        if choice == "1":
            path = input("Enter path: ")
            pm.create_key(path)
        elif choice == "2":
            path = input("Enter path: ")
            pm.load_key(path)
        elif choice == "3":
            path = input("Enter path: ")
            pm.create_pw_file(path, password)
        elif choice == "4":
            path = input("Enter path: ")
            pm.load_pw_file(path)
        elif choice == "5":
            site = input("Enter the site: ")
            password = input("Enter the password: ")
            pm.add_password(site, password)
        elif choice == "6":
            site = input("Choose Site: ")
            print(f" Password for {site} is {pm.get_password(site)}")
        elif choice == "q":
            done = True
            print("Adios Crack!")
        else:
            print(" Invalid choice!")

            
if __name__ == "__main__":
    main()
