import numpy as np
import mysql.connector as connector
import os
from tkinter import *
from PIL import ImageTk, Image
from matplotlib import pyplot as plt
from tkinter import messagebox as mb


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

# main window=========================================================================================================
root = Tk()
root.title("COVID Vaccination Survey")
root.resizable(0,0) #disables maximise btn

bgimg1 = Image.open(r'{}'.format(str(os.getcwd())+"/vaccimg1.png"))# defining image and its path, and inserting it in a label (photolabel)
resized = bgimg1.resize((1000, 700))# resizing image to required size.
bgimg = ImageTk.PhotoImage(resized)# pillow command to get the image after applying changes
photolabel = Label(root, image=bgimg).place(x=0, y=0)
root.iconphoto(False, bgimg)#changing the tk symbol on top left of the window

root.geometry("1000x700")

heading = Label(root, text="COVID Vaccination Survey", font=("times", 25, "bold",), fg = "#3090C7",bg ="#d6e8ff" )
subheading = Label(root, text="Towards our health", font=("times", 17, "bold"),fg = "#3090C7", bg="#d6e8ff")
heading.place(relx=0.32, y=5)
subheading.place(relx=0.41, rely=0.94)

def exitroot():
    qn = mb.askquestion("Exit", "Are you sure, you want to exit?")
    if qn=='yes':
        root.destroy()
root.protocol("WM_DELETE_WINDOW", exitroot)# will execute exitroot fn on pressing X button

nameval=0
ageval=0
stateval=0
genderval=0
regnoval=0
sym1lst=0
sym2lst=0




#USER SIGN UP ===========================================================================================================
def usersignup():
    global nameval, ageval, stateval, genderval
    root.iconify()#minimises root window
    signupwin = Toplevel(root)# creating new subwindow
    signupwin.title("Sign up")
    signupwin.geometry("1000x700")
    signupwin.resizable(0,0)
    bgimg2 = Image.open(r'{}'.format(str(os.getcwd())+"/vaccimg2.png"))
    resized = bgimg2.resize((1000, 700))
    bgimg = ImageTk.PhotoImage(resized)
    photolabel = Label(signupwin, image=bgimg).place(x=0, y=0)
    signupwin.iconphoto(False, bgimg)

    #dropdown menu for state
    #stateval = StringVar() erase this after some time
    statelist = ["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana",
                 "Himachal Pradesh","Jammu and Kashmir","Ladakh","Jharkhand","Karnataka","Kerala","Madhya Pradesh",
                 "Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan",
                 "Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
                 "Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu",
                 "Lakshadweep","National Capital Territory of Delhi","Puducherry"]
    Label(signupwin, text="Select your State",font=("times", 17, "bold"),fg = "#3090C7", bg="#d9edf1").place(relx=0.34, rely=0.125)
    #scrollbar for statelistbox
    myframe = Frame(signupwin,height = 12, width = 15)
    scrollbar = Scrollbar(myframe, orient = VERTICAL)
    statelistbox = Listbox(myframe, yscrollcommand=scrollbar.set, width = 30, exportselection = False)#exportselection ensures that even when focus is not on the
    statelistbox.pack(side = LEFT)                                                                    #listbox, the selection(s) remain intact
    scrollbar.configure(command = statelistbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    myframe.place(relx=0.34, rely=0.175)
    for i in statelist:
        statelistbox.insert(END,i)

    #name
    name = StringVar# StringVar is a datatype defined for&by tkinter, it is similar to str
    nameentry = Entry(signupwin, textvariable = name, font=("times", 12), bg = "white", width = 24)
    nameentry.delete(0, END)
    nameentry.insert(0, "Enter your name")
    global a
    a = False
    def entryerase1(event):                     #this loop is for not deleting the default text on clicking the entry box the 2nd time
        global a
        if a!=True:
            nameentry.delete(0, END)
            a = True
        else:
            pass
    nameentry.bind('<Button-1>', entryerase1)   #on left clicking on the entrybox, entryerase1 fn is executed which on the 1st click erases the default text.
    nameentry.place(relx = 0.10, rely = 0.17)
    Label(signupwin, text="Name",font=("times", 17, "bold"),fg = "#3090C7", bg="#daf0f2").place(relx = 0.10, rely = 0.125)

    #age
    age = IntVar
    ageentry = Entry(signupwin, textvariable = age, font=("times", 12), bg = "white", width = 15)
    ageentry.delete(0, END)                                   # (0, END) in many tkinter entry commands is for pointer purpose, it starts the pointer at 0 ie 1st index
    ageentry.insert(0, "Enter your age")                      # and END is the index of the last entered character by the user.
    global b
    b = 1
    def entryerase2(event):
        global b
        if b<2:
            ageentry.delete(0, END)
            b+=1
        else:
            pass
    ageentry.bind('<Button-1>', entryerase2)
    ageentry.place(relx = 0.10, rely = 0.34)
    Label(signupwin, text="Age",font=("times", 17, "bold"),fg = "#3090C7", bg="#d9edf1").place(relx = 0.10, rely = 0.295)

    #gender
    gender = StringVar(signupwin, 4)
    gendervalues = {1:"Female", 2:"Male", 3:"Other", 4:"Prefer not to say"}
    for (num, value) in gendervalues.items():
        Radiobutton(signupwin, text = value, variable = gender, value = num, font=("times", 10, "bold"),
                    selectcolor = "#c7dae0", bg = "#cde0e6").place(relx=0.1, rely=(num/25+0.49))
    Label(signupwin, text="Gender",font=("times", 17, "bold"),fg = "#3090C7", bg="#d3e6ea").place(relx = 0.1, rely = 0.48)

    Label(signupwin, text="*All fields are compulsary to fill",font=("times", 12, "bold"),fg = "#ff0000", bg="#c7dae0").place(relx = 0.1, rely = 0.70)



    cursor.execute("select regno from userinfo")
    rows = cursor.fetchall()
    x = (rows)[cursor.rowcount-1][0]+1 # for getting the next regno, rowcount-1 will give the index of last entered regno, + 1 will give the next regno.



    #register button and regno label
    def registration():
        global nameval, ageval, stateval, genderval
        nameval = nameentry.get()
        stateval = statelistbox.get(ANCHOR)
        ageval = ageentry.get()
        genderval = int(gender.get())

        def userinfoquery():
            cursor.execute("select * from userinfo")
            list1 = cursor.fetchall()
            list2 = [a[1:] for a in list1] # creates a list without the regnos.

            genderlist = ["Female", "Male", "Other", "Prefer not to say"]
            tup = (str(nameval), ageval, str(genderlist[int(genderval)-1]), str(stateval))# genderval is 1,2,3 or 4 as per the dictionary defined before
            # -1 done as in mysql indexing starts from 1 while in python from 0

            if tup in list2: # validation for an already existing record
                mb.showinfo("Error", "This user has been already regestered.")
                regbtn['state']=ACTIVE
            else:
                try:
                    cursor.execute("insert into userinfo values('"+str(x)+"', '"+str(nameval)+"', '"+str(ageval)+"', '"+str(genderval)+"', '"+str(stateval)+"')")
                    Label(signupwin, text = "your registration number is :"+"{}".format(x),font=("times", 18, "bold"),
                          fg = "#014d4e", bg="#c7dae0").place(relx=0.3, rely=0.8)
                    mb.showinfo("Registration number", "Your registration number is: {}, login with this number to start the survey".format(x)) # x is defined on line 176
                except:
                    mb.showwarning("Error", "Please dont enter quotes or slashes in your name")
                conn.commit()
        try:
            ageval = int(ageentry.get())
            if ageval not in range(15, 121):
                mb.showwarning("Error", "Please enter a valid age between 15 and 120")
            else:
                if nameval == "Enter your name" or len(nameval)>255:
                    mb.showwarning("Error", "Please enter your name (max 255 characters and should not contain numbers )")
                else:
                    for i in nameval.split(" "):
                        if not i.isalpha():
                            mb.showwarning("Error", "Please enter a valid name (max 255 characters, no numbers or special characters.)")
                            break
                    else:
                        if stateval not in statelist:
                            mb.showwarning("Error", "Please select your state")
                        else:
                            regbtn['state']=DISABLED
                            userinfoquery()
        except ValueError:
            mb.showwarning("Error", "Please enter a valid age between 15 and 120 ")

    regbtn = Button(signupwin, text="Register", font=("times", 17, "bold"), fg="#3090C7", bg="#d9edf5", command = registration)
    regbtn.place(relx=0.1, rely=0.77)

    signupwin.protocol("WM_DELETE_WINDOW", lambda: [root.deiconify(), signupwin.destroy()]) # closes loginwin and expands root window on pressing x button

    signupwin.mainloop()


#USER LOGIN =============================================================================================================
def loginpwd():
    global regnoval, bgimg
    regnowin = Toplevel(root)# creates a child window for rootwindow
    regnowin.title("Registration no.")
    regnowin.geometry("320x82+400+360")# size, location
    regnowin.configure(bg = "#bedaec")# bg hex codes
    regnowin.resizable(0,0)# makes window resizable
    regnowin.iconphoto(False, bgimg)# puts bgimg as icon on topleft

    Label(regnowin, text = """Please enter your registration number""",font=("times", 13), fg = "#008080", bg = "#bedaec").pack()
    pressenterlbl = Label(regnowin, text = """Press enter""",font=("times", 13),fg = "#008080", bg = "#bedaec")

    regnopwd = StringVar# defining variable
    regentry = Entry(regnowin, textvariable = regnopwd, font=("times", 12), bg = "white", width = 24, show = "*")
    regentry.pack()

    cursor.execute("select regno from userinfo")
    rows1=cursor.fetchall()
    regnolist1 = []
    for i in rows1:                        #***# cursor.rowcount is the no of records
        regnolist1.append(str(i[0]))

    cursor.execute("select distinct regno from vaccination")   #***# no of ppl who have done the survey
    rows2=cursor.fetchall()
    regnolist2=[]
    for i in rows2:                         #***#
        regnolist2.append(str(i[0]))

    def enter(event):# event is necessary for the bind method to work
        global regnoval
        regnoval = regentry.get()
        def loginpwddestroy():
            regnowin.destroy()
        def invalidregno():
            mb.showwarning("Error", """Please enter your correct registration number
      no registration done with this number""")
        if regnoval in regnolist1 and regnoval not in regnolist2:# means the user has registered but not been surveyed
            regentry.delete(0, END)
            regentry.insert(0, "")
            loginpwddestroy()
            userlogin()

        elif  regnoval in regnolist2:# means the user has registered as well as been surveyed
            qn = mb.askquestion("Thank you","""Your response has been recorded, Thank you.
        Do you want to see your response?""")
            if qn=='yes':

                cursor.execute("select * from userinfo where regno = '"+regnoval+"'")
                vals = cursor.fetchone()
                nameval, ageval, genderval, stateval = vals[1], vals[2], vals[3], vals[4]

                cursor.execute("select vaccinebrand from vaccination where regno = '"+regnoval+"'")
                vaccval = cursor.fetchall()[0][0]

                cursor.execute("select symptoms from vaccination where regno = '"+regnoval+"'")
                vals2 = cursor.fetchall()
                sym1val = []
                sym2val = []
                for i in vals2:
                    if i[0][0]=="1":
                        sym1val.append(i[0][3:])#1st index is for the string in the tuple in vals2 list, 2nd index is for the string, ie, from 3rd posn, ie w/o 1. or 2.
                    else:
                        sym2val.append(i[0][3:])
                if sym1val == ["1. none"]:
                    sym1val = "none"
                if sym2val == ["2. none"]:
                    sym2val = "none"

                infowin = Toplevel(regnowin)
                infowin.title("Info")
                infowin.geometry("1000x313+400+360")
                infowin.configure(bg = "white")
                infowin.resizable(0,0)
                infowin.iconphoto(False, bgimg)
                Label(infowin, height = 20, width = 141, borderwidth = 5, relief = RIDGE, bg = "white").place(x = 0, y = 0)
                Label(infowin, text =
"""Registration no.:                     {}

Name:                                       {}

Age:                                          {}

Gender:                                     {}

State:                                         {}

Vaccine taken:                          {}

symptoms after 1st dose:        {}

symptoms after 2nd dose:       {}""".format(regnoval, nameval, ageval, genderval, stateval, vaccval , ", ".join(sym1val), ", ".join(sym2val)),
                font=("times", 13),fg = "#008080", bg = "white", justify = LEFT, wraplength = 1000).place(x = 5,y = 5)
                #wraplength enters a new line if a line exceeds a word limit.
                #join prints the contents of the list as csv
                infowin.protocol("WM_DELETE_WINDOW", regnowin.destroy)
            #regentry.delete(0, END)
            #regentry.insert(0, "")
            if qn=='no':
                regnowin.destroy()

        else:
            invalidregno()
            regnowin.deiconify()
            pressenterlbl.pack_forget()
            regentry.delete(0, END)
            regentry.insert(0, "")

    def pressenter(event):# event is necessary to mension for the bind method to work
        if len(regentry.get()) in range(3,5):     #when atleast 4 keys are pressed, pressenterlabel is placed
            pressenterlbl.pack(pady=4)

    regentry.bind('<Key>', pressenter)# when any key is pressed on the keyboard, pressenter command is executed.
    regnowin.bind('<Return>', enter)# when enter key is pressed on the keyboard, enter command is executed.

    regnowin.mainloop()


#SURVEY =================================================================================================================
def userlogin():
    global regnoval
    root.iconify()
    vaccval = 0
    sym1lst = 0
    sym2lst = 0
    symlist = 0
    loginwin = Toplevel(root)
    loginwin.title("Logged in")
    loginwin.geometry("1000x700")
    loginwin.resizable(0,0)

    bgimg3 = Image.open(r'{}'.format(str(os.getcwd())+"/vaccimg3.png"))
    resized = bgimg3.resize((1000, 700))
    bgimg = ImageTk.PhotoImage(resized)
    photolabel = Label(loginwin, image=bgimg).place(x=0, y=0)
    loginwin.iconphoto(False, bgimg)

    cursor.execute("select name from userinfo where regno ='"+str(regnoval)+"' ")                       #***#
    rows = cursor.fetchall()
    Label(loginwin, text = "{}{}{}{}".format("Hi ",rows[0][0],"! ","Welcome to the Survey "),
          font=("times", 20),fg = "#006151", bg = "#c1e1ec" ).place(relx = 0.28,rely = 0.1)
    rdlbl = Label(loginwin, text = "Have you been vaccinated for COVID?", font=("times", 17),fg = "#006151", bg = "#c4e3ef" )
    rdlbl.place(relx = 0.32,rely = 0.23)

    #defining main labels
    nodoselbl = Label(loginwin, text = """Please come after taking both the doses
Thank you.""", font = ('times', 22), fg = "#006151", bg = "#c6e3ee")

    onedoselbl = Label(loginwin, text = """Please select the symptoms you experienced
after taking the 1st dose. """, font = ('times', 18), fg = "#006151", bg = "#c6e3ee")

    twodoselbl = Label(loginwin, text = """Please select the symptoms you experienced
after taking the 2nd dose. """, font = ('times', 18), fg = "#006151", bg = "#c6e3ee")

    finsvlbl = Label(loginwin, text = """Thank you for your valuable responce.
Press submit to submit your responce""", font = ('times', 24), fg = "#006151", bg = "#c6e3ee")



    #vaccinebrandlist
    vacclbl = Label(loginwin, text = "Select the vaccine you took", font = ("times", 20), fg = "#006151", bg = "#c8e4f0")
    vaccbrandlist = Listbox(loginwin, height = 5, font = ("times", 18), fg = "#006151",
                            width = 15, selectmode = SINGLE, exportselection = False)# exportselection = false ensures that on clicking elsewhere after selecting any itme in the list box, the selection remains intact
    vaccbrands = ["Covishield", "Covaxin", "Sputnik V", "Moderna", "Pfizer"]

    for i in vaccbrands:
        vaccbrandlist.insert(END,i)

    #symptom list
    symlist = [" None", " Feeling sick (nausea)", " Feeling tired (fatigue)"," Fever"," Cough and/or cold"," Itching/rash/red bumps at injection site"," Pain in chest",
               " Breathlessness"," Persistent abdominal pain"," Seizures"," Severe and persistent headache",
               " Weakness/paralysis of limbs or any side of the body"," Persistent vomiting"," Blurred vision or pain in eyes",
               " Change in mental status, confusion"," Decreased appetite"," Other"]
    sym1frame = Frame(loginwin,height = 13, width = 45)
    sym2frame = Frame(loginwin,height = 13, width = 45)
    scrollbary1 = Scrollbar(sym1frame, orient = VERTICAL)
    scrollbary2 = Scrollbar(sym2frame, orient = VERTICAL)
    sym1listbox = Listbox(sym1frame, yscrollcommand=scrollbary1.set,font = ("times", 15), fg = "#006151",
                          width = 43, height = 7, selectmode = MULTIPLE, exportselection = False)
    sym2listbox = Listbox(sym2frame, yscrollcommand=scrollbary2.set,font = ("times", 15), fg = "#006151",
                          width = 43, height = 7, selectmode = MULTIPLE, exportselection = False)
    sym1listbox.pack(side = LEFT)
    sym2listbox.pack(side = LEFT)
    scrollbary1.configure(command = sym1listbox.yview)
    scrollbary2.configure(command = sym2listbox.yview)
    scrollbary1.pack(side = RIGHT, fill = Y)
    scrollbary2.pack(side = RIGHT, fill = Y)
    for i in symlist:
        sym1listbox.insert(END,i)
        sym2listbox.insert(END,i)



    sym1lst = 0
    sym2lst = 0

    def finalfin():
        finsvlbl.place_forget()
        finsvbtn.place_forget()
        backbtn3.place_forget()
        backbtn0.place_forget()
        Label(loginwin, text = """Your responce has been successfully recorded""", font = ('times', 24),
              fg = "#006151",bg = "#c6e3ee").place(relx = 0.26, rely = 0.35)
        Label(loginwin, text = """• You can login again to see your responce""", font = ('times', 17),
              fg = "#006151",bg = "#c6e3ee").place(relx = 0.27, rely = 0.45)
        Label(loginwin, text = """• Check out survey plots in survey analysis window""", font = ('times', 17),
              fg = "#006151",bg = "#c6e3ee").place(relx = 0.27, rely = 0.5)
        Button(loginwin, text = "Close", font = ("times", 18),fg = "#006151", bg = "#d9edf5",
               command = lambda: [loginwin.destroy(), root.deiconify()]).place(relx = 0.48, rely = 0.57)

#flow of control:
#both dose pressed - dose fn - back0 or next1 - sym1 - back1 or next2 - sym2 - back2 or next3 - finsvdose - back3 or finsvbtn(submit) - finalfin and enterdata


    def enterdata():
        #query
        global vaccval, sym1lst, sym2lst
        symlist = sym1lst+sym2lst
        for i in symlist:
            try:
                cursor.execute("insert into vaccination (regno, vaccinebrand, symptoms) values('"+str(regnoval)+"','"+str(vaccval)+"','"+str(i)+"')")
                conn.commit()
            except:
                conn.rollback()
                mb.showerror("Error", "Something went erong :( ")                 #Just in case of any unknown error occurs.

    def finsvdose():
        global sym2lst
        sym2val = sym2listbox.curselection()# sym2val will store a tuple with the index of all the selected items in sym2listbox
        if sym2val == ():
            mb.showwarning("Error", "Please select the syptoms you experienced after taking the second dose, if none, select none")
        elif 0 in sym2val and len(sym2val)>1:
            mb.showwarning("Error", "Please select none only if you had no symptoms")
        else:
            next3btn.place_forget()
            twodoselbl.place_forget()
            backbtn2.place_forget()
            sym2lst = []
            for i in sym2val:
                sym2lst.append("2."+str(sym2listbox.get(i)))
            sym2frame.place_forget()
            finsvlbl.place(relx = 0.26, rely = 0.35)
            finsvbtn.place(relx = 0.47, rely = 0.55)
            backbtn3.place(relx = 0.07,rely = 0.09)

    def sym2():
        global sym1lst
        sym1val = sym1listbox.curselection()# sym1val will store a tuple with all the selected items in sym1listbox
        if sym1val == ():
            mb.showwarning("Error", "Please select the syptoms you experienced after taking the first dose, if none, select none")

        #0 in sym1val means that 1st symptom in the list ie None is present, this elif is to ensure that user doesn't enter
        #none along with other symptoms.
        elif 0 in sym1val and len(sym1val)>1:
            mb.showwarning("Error", "Please select none only if you had no symptoms")
        else:
            next2btn.place_forget()
            onedoselbl.place_forget()
            backbtn1.place_forget()
            sym1lst=[]
            for i in sym1val:
                sym1lst.append("1."+str(sym1listbox.get(i)))
            sym1frame.place_forget()
            twodoselbl.place(relx = 0.3, rely = 0.29)
            sym2frame.place(relx=0.29, rely=0.41)
            next3btn.place(relx = 0.48, rely = 0.72)
            backbtn2.place(relx = 0.07, rely = 0.09)

    def sym1():
        global vaccval
        vaccval = vaccbrandlist.get(ANCHOR)
        if vaccval not in vaccbrands:
            mb.showwarning("Error", "Please select the vaccine you took")
        else:
            next1btn.place_forget()
            vacclbl.place_forget()
            vaccbrandlist.place_forget()
            onedoselbl.place(relx = 0.3, rely = 0.29)
            sym1frame.place(relx = 0.29, rely = 0.43)
            next2btn.place(relx = 0.48, rely = 0.72)
            backbtn1.place(relx = 0.07, rely = 0.09)

    def removerdbtns():
        rdlbl.place_forget()
        r1.place_forget()
        r2.place_forget()
        r3.place_forget()

    def nodose():
        removerdbtns()
        nodoselbl.place(relx = 0.28, rely = 0.33)
        Button(loginwin, text = "Close", font = ("times", 18),fg = "#006151", bg = "#d9edf5",
             command = lambda: [root.deiconify(), loginwin.destroy()]).place(relx = 0.46, rely = 0.48)

    def onedose():
        removerdbtns()
        nodoselbl.place(relx = 0.28, rely = 0.33)
        Button(loginwin, text = "Close", font = ("times", 18),fg = "#006151", bg = "#d9edf5",
             command = lambda: [root.deiconify(), loginwin.destroy()]).place(relx = 0.46, rely = 0.48)

    def dose():
        removerdbtns()
        vacclbl.place(relx = 0.35, rely = 0.3)
        vaccbrandlist.place(relx = 0.41, rely = 0.37)
        next1btn.place(relx = 0.47, rely = 0.6)
        backbtn0.place(relx = 0.07, rely = 0.09)

    def back0():
        vacclbl.place_forget()
        vaccbrandlist.place_forget()
        next1btn.place_forget()
        backbtn0.place_forget()
        r1.place(relx = 0.43, rely = 0.34)
        r2.place(relx = 0.43, rely = 0.39)
        r3.place(relx = 0.43, rely = 0.44)
        rdlbl.place(relx = 0.32,rely = 0.23)

    def back1():
        dose()
        next2btn.place_forget()
        onedoselbl.place_forget()
        sym1frame.place_forget()
        backbtn1.place_forget()

    def back2():
        sym1()
        next3btn.place_forget()
        twodoselbl.place_forget()
        sym2frame.place_forget()
        backbtn2.place_forget()

    def back3():
        sym2()
        finsvlbl.place_forget()
        finsvbtn.place_forget()
        backbtn3.place_forget()



    #next buttons
    next1btn = Button(loginwin, text = "Next", font = ("times", 18),fg = "#006151", bg = "#d9edf5", command = sym1)
    next2btn = Button(loginwin, text = "Next", font = ("times", 18),fg = "#006151", bg = "#d9edf5", command = sym2)
    next3btn = Button(loginwin, text = "Next", font = ("times", 18),fg = "#006151", bg = "#d9edf5", command = finsvdose)
    backbtn0 = Button(loginwin, text = "Back", font = ("times", 15),fg = "#006151", bg = "#d9edf5", command = back0)
    backbtn1 = Button(loginwin, text = "Back", font = ("times", 15),fg = "#006151", bg = "#d9edf5", command = back1)
    backbtn2 = Button(loginwin, text = "Back", font = ("times", 15),fg = "#006151", bg = "#d9edf5", command = back2)
    backbtn3 = Button(loginwin, text = "Back", font = ("times", 15),fg = "#006151", bg = "#d9edf5", command = back3)
    finsvbtn = Button(loginwin, text = "Submit", font = ("times", 18),fg = "#006151", bg = "#d9edf5", command = lambda: [finalfin(), enterdata()])

    #dose radiobuttons
    dosevar = StringVar(loginwin, 0)
    r1 = Radiobutton(loginwin, text = "Both the doses", variable = dosevar, value = 2, font = ("times", 13),
                      bg = "#c6e3ee", fg = "#006151", selectcolor = "#c6e3ee", command = dose)
    r1.place(relx = 0.43, rely = 0.34)
    r2 = Radiobutton(loginwin, text = "1st dose only", variable = dosevar, value = 1, font = ("times", 13),
                      bg = "#c6e3ee", fg = "#006151", selectcolor = "#c6e3ee", command = onedose)
    r2.place(relx = 0.43, rely = 0.39)
    r3 = Radiobutton(loginwin, text = "None", variable = dosevar, value = 3, font = ("times", 13),
                      bg = "#c6e3ee", fg = "#006151", selectcolor = "#c6e3ee", command = nodose)
    r3.place(relx = 0.43, rely = 0.44)

    loginwin.protocol("WM_DELETE_WINDOW", lambda: [root.deiconify(), loginwin.destroy()])

    loginwin.mainloop()


#SURVEY ANALYSIS ========================================================================================================
def surveyanalysis():
    global symlist, sym1list, regnos
    root.iconify()
    symlist = ["nausea", "fatigue","Fever","Cough/ cold","Itching/rash","Pain in chest",
               "Breathlessness","abdominal pain","Seizures","headache",
               "Weakness","vomiting","Blurred vision",
               "confusion","Decreased appetite","Other", "None"]
    sym1list = ["1. Feeling sick (nausea)", "1. Feeling tired (fatigue)","1. Fever","1. cough and/or cold",
                "1. itching/rash/red bumps at injection site","1. pain in chest","1. breathlessness","1. persistent abdominal pain","1. seizures",
                "1. severe and persistent headache","1. weakness/paralysis of limbs or any side of the body","1. persistent vomiting",
                "1. blurred vision or pain in eyes","1. change in mental status, confusion","1. Decreased appetite","1. Other", "1. none"]

    svanwin = Toplevel(root)
    svanwin.title("Stats")
    svanwin.geometry("1000x700")
    svanwin.resizable (0,0)

    bgimg4 = Image.open(r'{}'.format(str(os.getcwd())+"/vaccimg4.png"))
    resized = bgimg4.resize((1000, 700))
    bgimg = ImageTk.PhotoImage(resized)
    photolabel = Label(svanwin, image=bgimg).place(x=0, y=0)
    svanwin.iconphoto(False, bgimg)

    cursor.execute("select distinct regno from vaccination")
    regnos = len(cursor.fetchall())
    cursor.execute("select regno from userinfo")
    regnos_uns = len(cursor.fetchall())
    ageregno=[]

    for i in (18, 38, 58, 78):
        cursor.execute("select distinct regno from vaccination where regno in (select regno from userinfo where age between {} and {})".format(i, i+19))
        a = cursor.fetchall()
        ageregno.append(len(a))

    cursor.execute("select distinct regno from vaccination where regno in (select regno from userinfo where age between 15 and 17)")
    ageregno.insert(0, len(cursor.fetchall()))
    cursor.execute("select distinct regno from vaccination where regno in (select regno from userinfo where age between 98 and 120)")
    ageregno.insert(5, len(cursor.fetchall()))

    Label(svanwin, text = "Survey Statistics", font = ("times",22), bg = "#d3e6ff", fg = "#008080").place(relx = 0.4, rely = 0.02)
    Label(svanwin, text = "No. of people registered: {}".format(regnos_uns), font = ("times",18), bg = "#60cae0", fg = "#003232").place(relx = 0.1, rely = 0.1)
    Label(svanwin, text = "No. of people surveyed: {}".format(regnos), font = ("times",18), bg = "#50cae1", fg = "#003232").place(relx = 0.4, rely = 0.1)
    Label(svanwin, text = "Age 15-17:  {}".format(ageregno[0]), font = ("times",14), bg = "#5ecbdf", fg = "#003232").place(relx = 0.1, rely = 0.15)
    Label(svanwin, text = "Age 18-37:  {}".format(ageregno[1]), font = ("times",14), bg = "#5ecae3", fg = "#003232").place(relx = 0.23, rely = 0.15)
    Label(svanwin, text = "Age 38-57:  {}".format(ageregno[2]), font = ("times",14), bg = "#50cae1", fg = "#003232").place(relx = 0.36, rely = 0.15)
    Label(svanwin, text = "Age 58-77:  {}".format(ageregno[3]), font = ("times",14), bg = "#45c8e1", fg = "#003232").place(relx = 0.49, rely = 0.15)
    Label(svanwin, text = "Age 78-97:  {}".format(ageregno[4]), font = ("times",14), bg = "#4bc6de", fg = "#003232").place(relx = 0.62, rely = 0.15)
    Label(svanwin, text = "Age 98-120:  {}".format(ageregno[5]), font = ("times",14), bg = "#47c9e0", fg = "#003232").place(relx = 0.75, rely = 0.15)



    def sym_vs_freq():
        global sym1freq, sym2freq, regnos

        #y values for 1st bar (symptoms after dose 1)
        sym1freq = []
        sym2freq = []
        for i in sym1list:
            cursor.execute("select regno from vaccination where symptoms = '1. "+str(i[3:])+"'")#this query will make a table having one particular symptom only
            cursor.fetchall()# this will have the table
            sym1freq.append(cursor.rowcount)# this will count the number of rows in fetchall() i.e. the frequency of that symptom


        #y values for 2nd bar (symptoms after dose 2)
        for i in sym1list:
            cursor.execute("select regno from vaccination where symptoms = '2. "+str(i[3:])+"'")
            cursor.fetchall()
            sym2freq.append(cursor.rowcount)


        xindex = np.arange(len(symlist))# xindex will be the x values in the graph, which is contained in an array of length same as len of symlist ie 16
                                        # here xindex is the array with indexes of x, and values of y, ie indexes = symptoms, and values = their frequency

        figure, ax = plt.subplots(figsize = (12,7))# creates the window for graph

        sym1bar = ax.bar(xindex-0.21, sym1freq, color = "#008080", label = "Symptoms after 1st dose", width = 0.4)# creates bar graph for symptoms after 1st dose
        sym2bar = ax.bar(xindex+0.21, sym2freq, color = "#AEEEEE", label = "Symptoms after 2nd dose", width = 0.4)# Creates bar graph for symptoms after 2st dose

        ax.set_title("Frequency of various symptoms after taking vaccination")
        ax.set_xlabel("Symptoms")
        ax.set_ylabel("Frequency")
        ax.bar_label(sym1bar)# shows freq values on the top of the bars
        ax.bar_label(sym2bar)
        plt.xticks(ticks = xindex, labels = symlist, rotation = 70)# this sets x values as the symptoms mentioned,
        plt.legend()#displays the index to the graph
        figure.tight_layout()# fits the graph in the window
        plt.ylim([0, regnos-30])# limits the graphsize ie contracts it so as to fit the graph in the window as more data is entered.
        plt.show()

    def sym_vs_freq_vs_brand():
        global symlist, sym1list, regnos
        #yval
        vaccbrandlist = ['Covishield', 'Covaxin', 'Sputnik V', 'Moderna', 'Pfizer']
        #xval = symlist
        symcovifreq = np.array([])
        symcovaxfreq = np.array([])
        symsputfreq = np.array([])
        symmodfreq = np.array([])
        sympfifreq = np.array([])

        for i in sym1list:
            cursor.execute("select entryno from vaccination where symptoms like '__"+str(i)[2:]+"' and vaccinebrand = 'Covishield'")
            cursor.fetchall()
            symcovifreq = np.append(symcovifreq, cursor.rowcount)

            cursor.execute("select entryno from vaccination where symptoms like '__"+str(i)[2:]+"' and vaccinebrand = 'Covaxin'")
            cursor.fetchall()
            symcovaxfreq = np.append(symcovaxfreq, cursor.rowcount)

            cursor.execute("select entryno from vaccination where symptoms like '__"+str(i)[2:]+"' and vaccinebrand = 'Sputnik V'")
            cursor.fetchall()
            symsputfreq = np.append(symsputfreq, cursor.rowcount)

            cursor.execute("select entryno from vaccination where symptoms like '__"+str(i)[2:]+"' and vaccinebrand = 'Moderna'")
            cursor.fetchall()
            symmodfreq = np.append(symmodfreq,cursor.rowcount)

            cursor.execute("select entryno from vaccination where symptoms like '__"+str(i)[2:]+"' and vaccinebrand = 'Pfizer'")
            cursor.fetchall()
            sympfifreq = np.append(sympfifreq, cursor.rowcount)

        symfreq = symcovifreq+symcovaxfreq+symsputfreq+symmodfreq+sympfifreq
        plt.figure(figsize = (12,7))
        for i in range(0,17):
            plt.text(i, symfreq[i], symfreq[i], ha = CENTER)# displaying total frequency on the bars
        xindex = np.arange(len(symlist))
        plt.bar(symlist, symcovifreq, color = "#30b5c8", label = vaccbrandlist[0], clip_on=False, width = 0.6)# clip on = false means the bars will be stacked
        plt.bar(symlist, symcovaxfreq, bottom = symcovifreq, color = "#007FFF", label = vaccbrandlist[1], clip_on=False, width = 0.6)# bottom means the bar will be stacked on top of the given bar
        plt.bar(symlist, symsputfreq, bottom = symcovifreq+symcovaxfreq, color = "#302B54", label = vaccbrandlist[2], clip_on=False, width = 0.6)
        plt.bar(symlist, symmodfreq, bottom = symcovifreq+symcovaxfreq+symsputfreq, color = "#5781ff", label = vaccbrandlist[3], clip_on=False, width = 0.6)
        plt.bar(symlist, sympfifreq, bottom = symcovifreq+symcovaxfreq+symsputfreq+symmodfreq, color = "#236B8E", label = vaccbrandlist[4], clip_on=False, width = 0.6)
        plt.title("Frequency of various symptoms for different brands")
        plt.xlabel("Symptoms")
        plt.ylabel("Frequency")
        plt.xticks(rotation = 65)# rotating the symptoms labels so as to fit
        plt.ylim([0, regnos-15])#shrinks the graph, so that it does not exceed the window size.
        plt.legend()
        plt.tight_layout()# fits the graph in the window
        plt.show()

    def sym_vs_freq_vs_age():
        global regnos

        agelist1 = [["15-17"], ["18-37"], ["38-57"], ["58-77"], ["78-97"], ["98-120"]]

        symfreq = []
        for j in range(18, 100, 20):
            symage = []
            for i in sym1list:
                cursor.execute("""select u.regno, u.age from userinfo as u right join vaccination as v on u.regno = v.regno
                                  where v.symptoms like '___"""+str(i)[3:]+"""' and u.age between {} and {}""".format(j, j+20))#this query will make a table having one particular symptom only
                cursor.fetchall()# this will have the table
                symage.append(cursor.rowcount)
            symfreq.append(symage)

        l = []
        for i in sym1list:
            cursor.execute("""select u.regno, u.age from userinfo as u right join vaccination as v on u.regno = v.regno
                              where v.symptoms like '___"""+str(i)[3:]+"""' and u.age between 15 and 17""")
            cursor.fetchall()
            l.append(cursor.rowcount)
        symfreq.insert(0, l)


        figure, ax = plt.subplots(figsize = (12,7))
        xindex = np.arange(len(symlist))
        for i in range(0, 6):
            ax.scatter(xindex, 17*agelist1[i], s = 200*np.array(symfreq[i]), c = symfreq[i], alpha = 0.75)

        ax.set_title("Frequency of various symptoms after Vaccination with age ")
        ax.set_xlabel("Symptoms")
        ax.set_ylabel("Age groups")
        plt.xticks(ticks = xindex, labels = symlist, rotation = 70)
        figure.tight_layout()# fits the graph in the window
        plt.show()

    def states_vs_no():
        statelist = ["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana",
                         "Himachal Pradesh","Jammu and Kashmir","Ladakh","Jharkhand","Karnataka","Kerala","Madhya Pradesh",
                         "Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan",
                         "Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
                         "Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu",
                         "Lakshadweep","National Capital Territory of Delhi","Puducherry"]

        # x values for bar graph
        states = ['AP','AR','AS','BH','CT','GA','GJ','HR',"HP",
                  "JK","LA","JH","KA","KL","MP",'MH','MN',
                  "ML","MZ","NL","OD","PB","RJ", "SK",'TN','TG','TR','UP',
                  'UT','WB','AN','CH',"DH",'DD','LD','DL','PY']

        # y values (frequency of vaccine doses)
        statefreq=[]
        for i in statelist:
            cursor.execute("select distinct regno from vaccination where regno in (select regno from userinfo where state='" + str(i) + "')")
            cursor.fetchall()
            statefreq.append(cursor.rowcount)

        xindex = np.arange(len(statelist))
        plt.figure(figsize=(15, 7))
        plt.bar(xindex,statefreq, color="#008078", label="Vaccinated", width=0.5)
        plt.title("Patients vaccinated per state")
        plt.xlabel("State Name")
        plt.ylabel("No of Pateints Vaccinated")
        plt.xticks(ticks=xindex, labels=states)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def sym_vs_nosym():

        cursor.execute("""select regno from vaccination where symptoms = '1. none' and regno not in
                         (select regno from vaccination where symptoms = '2. none')""")# people who had no symptoms after 1st dose and had symptoms after 2nd
        cursor.fetchall()
        nosym1ct = cursor.rowcount

        cursor.execute("""select regno from vaccination where symptoms = '2. none' and regno not in
                         (select regno from vaccination where symptoms = '1. none' )""")# people who had no symptoms after 2nd dose and had symptoms after 1st
        cursor.fetchall()
        nosym2ct = cursor.rowcount

        cursor.execute("""select regno from vaccination where symptoms = '1. none' and regno in
                         (select regno from vaccination where symptoms = '2. none')""")# people who had no symptoms after both the doses
        cursor.fetchall()
        nosymct = cursor.rowcount

        cursor.execute("""select distinct regno from vaccination where regno not in
                         (select regno from vaccination where symptoms like '___none')""")# people who had symptoms after both the doses
        cursor.fetchall()
        symct = cursor.rowcount

        lbls = ["Symptoms only after 2nd dose", "Symptoms only after 1st dose", "No symptoms after both the doses",
                "Symptoms after both the doses"]
        plt.figure(figsize = (14,7))
        plt.pie([nosym1ct, nosym2ct, nosymct, symct], labels = lbls, explode=(0.01, 0.01, 0.01, 0.01),
                 autopct='%1.2f%%', colors = ["#236B8E", "#0276FD", "#82CFFD", "#008080"])
        #autopct shows percentages of the information displayed on the pie chart, explode will seperate out the slices by given amount
        plt.title("Symptoms vs no symptoms")
        plt.legend(loc = "lower right")
        plt.tight_layout()
        plt.show()



    Button(svanwin,text = "Symptoms vs Frequency", fg = "white",bg = "#007075", bd = 1, font = ("times", 17, "bold"),
           activebackground = "#3090C7", command = sym_vs_freq).place(relx = 0.1, rely = 0.25)
    Button(svanwin, text = "no. of people surveyed vs states", fg = "white",bg = "#007075", bd = 1, font = ("times", 17, "bold"),
           activebackground = "#3090C7", command = states_vs_no).place(relx = 0.1, rely = 0.35)
    Button(svanwin, text = "Symptoms vs no symptoms", fg = "white",bg = "#007075", bd = 1, font = ("times", 17, "bold"),
           activebackground = "#3090C7", command = sym_vs_nosym).place(relx = 0.1, rely = 0.45)
    Button(svanwin, text = "Symptoms vs Frequency vs age", fg = "white",bg = "#007075", bd = 1, font = ("times", 17, "bold"),
           activebackground = "#3090C7", command = sym_vs_freq_vs_age).place(relx = 0.1, rely = 0.55)
    Button(svanwin,text = "Symptoms vs Frequency with vaccine brands", fg = "white",bg = "#007075", bd = 1, font = ("times", 17, "bold"),
          activebackground = "#3090C7", command = sym_vs_freq_vs_brand).place(relx = 0.1, rely = 0.65)



    svanwin.protocol("WM_DELETE_WINDOW", lambda: [root.deiconify(), svanwin.destroy()])

    svanwin.mainloop()





#ROOT BUTTONS ================================================================================================================
usersignupbtn = Button(root,text = "  Sign up  ", bg = "white", fg = "#3090C7", bd = 3, font = ("times", 20, "bold"),
               activebackground = "#4E8975", command = usersignup).place(relx = 0.45, y = 170)

userloginbtn = Button(root,text = "  Login  ", bg = "white", fg = "#3090C7", bd = 3, font = ("times", 20, "bold"),
               activebackground = "#4E8975", command = loginpwd).place(relx = 0.46 , y = 270)

surveyanalysisbtn = Button(root,text = "  survey analysis  ", bg = "white", fg = "#3090C7", bd = 3,
                           font = ("times", 20, "bold"), activebackground = "#4E8975",
                           command = surveyanalysis).place(relx =0.405 , y = 370)

exitbtn = Button(root,text = " Exit ", fg = "white",bg = "#4E8975", bd = 1, font = ("times", 17, "bold"),
               activebackground = "#3090C7", command = exitroot ).place(relx=0.082, rely=0.85)

root.mainloop()

conn.close()
