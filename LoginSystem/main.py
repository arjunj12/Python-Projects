file = open('db.txt','r')
file_read = file.readlines()

details = {}
for line in file_read:
    det = line.split()
    details[det[0]]=det[1]

def logon():
    if username in details:
        password = input("Enter Password: ")
        if password == details[username]:
            print("Login Successfully")
        else:
            print("Wrong Password Entered")        
    else:
        print("User Name Not Found")

file.close()
file = open('db.txt','a')

def signup():
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    file.write("\n" + username + " " + password)
    print("Account Created Successfully")
    


def changePassword():
    username = input("Enter Username: ")
    if username in details:
        password = input("Enter Password: ")
        if password == details[username]:
             new_password = input("Enter new Password: ")
             details[username] = new_password
             with open('db.txt','w') as w:
                 for item in details.items():
                     w.write(item[0] + " " + item[1] + "\n")
        else:
            print("Wrong Password Entered")
    else:
        print("Username Not Found")  



print("\n******welcome To Login System******")
print("Enter Choice")
print("1.Login")
print("2.Sign Up")
print("3.Change Password")
value = int(input())

if value == 1:
    username = input("Enter Username: ")
    logon()
elif value == 2:
    signup()
elif value == 3:
    changePassword()

