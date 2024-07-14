#proj w/o tkinter:
import mysql.connector as connector
import mysql.connector as connector
conn = connector.connect(user="root",
                         password="root",
                         host = "localhost",
                         database="computer")
cursor = conn.cursor(buffered = True)
#To prevent unread result found error
#buffering -> temporary storage, the whole db data is fetched and stored temporarily.

#table creation (userinfo and vaccination)
#userinfo table creation
"""
cursor.execute('''create table IF NOT EXISTS userinfo(
                regno integer AUTO_INCREMENT PRIMARY KEY,
                name varchar(255),
                age integer NOT NULL DEFAULT 18,
                gender enum ('Female', 'Male', 'Other', 'Prefer not to say'),
                state enum ("Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana",
                             "Himachal Pradesh","Jammu and Kashmir","Ladakh","Jharkhand","Karnataka","Kerala","Madhya Pradesh",
                             "Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan",
                             "Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
                             "Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu",
                             "Lakshadweep","National Capital Territory of Delhi","Puducherry"))''')
cursor.execute('alter table userinfo AUTO_INCREMENT=1001')

#vaccination table creation
cursor.execute('''create table IF NOT EXISTS vaccination(
               entryno integer AUTO_INCREMENT PRIMARY KEY,
               regno integer REFERENCES userinfo (regno) ON DELETE CASCADE ON UPDATE CASCADE,
               vaccinebrand enum ('Covaxin', 'Covishield', 'Sputnik V', 'Moderna', 'Pfizer') NOT NULL,
               symptoms enum ("1. Feeling sick (nausea)", "1. Feeling tired (fatigue)","1. Fever","1. cough and/or cold",
                          "1. itching/rash/red bumps at injection site","1. pain in chest","1. breathlessness","1. persistent abdominal pain","1. seizures",
                          "1. severe and persistent headache","1. weakness/paralysis of limbs or any side of the body","1. persistent vomiting",
                          "1. blurred vision or pain in eyes","1. change in mental status, confusion","1. Decreased appetite","1. Other","1. none",
                          "2. Feeling sick (nausea)","2. Feeling tired (fatigue)","2. Fever","2. cough and/or cold",
                          "2. itching/rash/red bumps at injection site","2. pain in chest","2. breathlessness","2. persistent abdominal pain","2. seizures",
                          "2. severe and persistent headache","2. weakness/paralysis of limbs or any side of the body","2. persistent vomiting",
                          "2. blurred vision or pain in eyes","2. change in mental status, confusion","2. Decreased appetite","2. Other", "2. none"))''')
# 1. means symptoms after 1st dose, 2. means symptoms after 2nd dose
cursor.execute('alter table vaccination AUTO_INCREMENT=1')
cursor.execute('''alter table vaccination add foreign key(regno) references userinfo(regno) on delete cascade on update cascade''')

#initiating table userinfo with sample data.
cursor.execute("insert ignore into userinfo (regno, name, age, gender, state) values(1001,'Yash Bhake',18,'Male','Maharashtra')")
cursor.execute("insert ignore into userinfo (regno, name, age, gender, state) values(1002,'Ajinkya Deshpande',18,'Male','Maharashtra')")
cursor.execute("insert ignore into userinfo (regno, name, age, gender, state) values(1003,'Rashmi Banerjee',25,'Female','West Bengal')")
conn.commit()
"""

print("____________________Welcome to COVID Vaccination Survey________________________    \n")
print("1. Sign up       2. Login       3. Survey Analysis       4. exit ")
try:
    windowch = int(input("Enter your choice: (1, 2, 3, 4) "))
    print("\n")
except:
    print("Please ennter a valid choice among 1,2,3,4")


def usersignup():
    global nameval, ageval, stateval, genderval
    try:
        nameval = input("Enter your name: ")
    except:
        print("Enter a valid name")
    try:
        def age():
            age = int(input("Enter your age (b/w 18 and 120)"))
        if age in range(18, 121):
            ageval = age
        else:
            print("Enter a valid age b/w 18 and 120")
    except():
        print("Enter a valid age b/w 18 and 120")





def loginpwd():
    pass

def userlogin():
    pass

def surveyanalysis():
    pass

if windowch == 1:
    usersignup()
if windowch == 2:
    loginpwd()
if windowch == 3:
    surveyanalysis()
if windowch == 4:
    quit()
