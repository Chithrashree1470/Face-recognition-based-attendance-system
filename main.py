############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
############################################# FUNCTIONS ################################################
def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
##################################################################################
def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)

###################################################################################

def contact():
    mess._show(title='Contact us', message="Please contact us on : 'xxxxxxxxxxxxx@gmail.com' ")

###################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

###################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

###################################################################################

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    Enter Old Password',bg='white',font=('times', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#3ece48", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#####################################################################################

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

#######################################################################################
def TakeImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImage/")
    assure_path_exists("StudentDetails/")
    Id = txt.get().strip()
    name = txt2.get().strip()

    if not Id.isdigit():
        message1.configure(text="Enter a valid numeric ID")
        return
    if not name.replace(" ", "").isalpha():
        message1.configure(text="Enter a valid name")
        return

    # Check duplicate ID
    student_file = "StudentDetails/StudentDetails.csv"
    if os.path.isfile(student_file):
        df_check = pd.read_csv(student_file)
        if int(Id) in df_check['ID'].values:
            message1.configure(text="ID already exists!")
            return

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        mess._show(title='Error', message='Cannot access camera')
        return

    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    sampleNum = 0
    serial = 1

    if os.path.isfile(student_file):
        with open(student_file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            serial = sum(1 for _ in reader) // 2 + 1

    while True:
        ret, img = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sampleNum += 1
            cv2.imwrite(f"TrainingImage/{name}.{serial}.{Id}.{sampleNum}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.imshow('Taking Images - Press q to exit', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if sampleNum >= 100:
            break
    cam.release()
    cv2.destroyAllWindows()

    with open(student_file, 'a+', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow([serial, '', Id, '', name])
    message1.configure(text=f"Images Taken for ID: {Id}")


########################################################################################

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))

############################################################################################3

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")

    # Clear old entries in table
    for k in tv.get_children():
        tv.delete(k)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if not os.path.isfile("TrainingImageLabel/Trainner.yml"):
        mess._show(title='Data Missing', message='Please click on Save Profile first!')
        return
    recognizer.read("TrainingImageLabel/Trainner.yml")

    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    df = pd.read_csv("StudentDetails/StudentDetails.csv")

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['ID', 'Name', 'Time']  # Only 3 columns for Excel
    attendance_data = []
    marked_ids = set()

    while True:
        ret, im = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])

            if conf < 50:
                ts = time.time()
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                name = df.loc[df['SERIAL NO.'] == serial]['NAME'].values[0]
                Id = df.loc[df['SERIAL NO.'] == serial]['ID'].values[0]

                if Id not in marked_ids:  # prevent duplicate marking
                    marked_ids.add(Id)
                    attendance_data.append([Id, name, timeStamp])

                    # Show in Treeview (with Date also)
                    tv.insert('', 'end', text=Id, values=(Id, name, date, timeStamp))

                cv2.putText(im, f"{name}", (x, y + h + 25), font, 0.8, (255, 255, 255), 2)
            else:
                cv2.putText(im, "Unknown", (x, y + h + 25), font, 0.8, (0, 0, 255), 2)

        cv2.imshow('Taking Attendance - Press Q to quit', im)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

    # Save attendance data (only 3 columns)
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    file_path = f"Attendance/Attendance_{date}.csv"
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a+', newline='') as csvFile:
        writer = csv.writer(csvFile)
        if not file_exists:
            writer.writerow(col_names)
        for row in attendance_data:
            writer.writerow(row)

    mess._show(title='Success', message='Attendance Recorded Successfully!')


######################################## USED STUFFS ############################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

def count_classes_for_student(student_name):
    total_classes = 0
    working_days = 0
    student_name = student_name.strip().lower()
    current_month = datetime.datetime.now().strftime("%m-%Y")
    folder = "Attendance"
    if not os.path.exists(folder):
        return -1, 0
    for file in os.listdir(folder):
        if file.endswith(".csv") and current_month in file:
            working_days += 1
            with open(os.path.join(folder, file), "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if any(student_name == cell.strip().lower() for cell in row):
                        total_classes += 1
                        break
    return total_classes, working_days
waiting_for_name = {"active": False}
######################################## GUI FRONT-END ###########################################
def open_chatbot():
    chatbot_win = tk.Toplevel(window)
    chatbot_win.title("Help Chatbot 🤖")
    chatbot_win.geometry("400x500")
    chatbot_win.configure(bg="#1e1e1e")

    chat_display = tk.Text(chatbot_win, bg="#2c2c2c", fg="white", font=("Arial", 12), wrap='word')
    chat_display.pack(padx=10, pady=10, fill='both', expand=True)
    chat_display.insert('end', "🤖 Chatbot: Hello! How can I help you?\n")
    chat_display.config(state='disabled')

    user_entry = tk.Entry(chatbot_win, font=("Arial", 12))
    user_entry.pack(side='left', padx=10, pady=10, fill='x', expand=True)

    def bot_reply(user_text):
        user_text = user_text.lower().strip()
        if waiting_for_name["active"]:
            name = user_text
            total, working_days = count_classes_for_student(name)
            waiting_for_name["active"] = False
            if total == -1:
                return "⚠ Attendance folder not found."
            if working_days == 0:
                return "❌ No attendance records found this month."
            percentage = (total / working_days) * 100
            return f"🧮 {name.capitalize()} attended {total}/{working_days} classes.\n📊 Attendance: {percentage:.2f}%."
        if "register" in user_text:
            return "\n->Step 1: Enter ID & Name \n→ Step 2: Take Images \n→ Step 3: Save Profile."
        elif "take attendance" in user_text:
            return "\n->Click 'Take Attendance' and \n->look at the camera."
        elif "password" in user_text:
            return "\n->Go to Help \n→ Change Password."
        elif "contact" in user_text:
            return "\n->📩 Contact: chithra@gmail.com"
        elif "exit" in user_text or "bye" in user_text:
            return "\n->👋 Thank you....!"
        elif "attendance percentage" in user_text:
            waiting_for_name["active"] = True
            return "\n->✍ Please enter your name."
        elif "developer" in user_text:
            return "\n->Developed by Chithra."
        else:
            return "\n->🤖 Try asking about attendance or percentage."

    def send_message(event=None):
        user_text = user_entry.get()
        if user_text.strip() == "":
            return
        chat_display.config(state='normal')
        chat_display.insert('end', f"🧑 You: {user_text}\n")
        reply = bot_reply(user_text)
        chat_display.insert('end', f"🤖 Chatbot: {reply}\n")
        chat_display.config(state='disabled')
        chat_display.see('end')
        user_entry.delete(0, 'end')

    send_btn = tk.Button(chatbot_win, text="Send", bg="#3ece48", fg="black", font=("Arial", 12, 'bold'), command=send_message)
    send_btn.pack(side='right', padx=10, pady=10)
    user_entry.bind("<Return>", send_message)


window = tk.Tk()
window.state('zoomed')  # makes the window full screen 
window.title("Attendance System")
window.configure(background='#262523')

frame1 = tk.Frame(window, bg="#626567")
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="#626567")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="                Face Recognition Based Attendance System" ,fg="white",bg="#262523" ,width=55 ,height=1,font=('times', 29, ' bold '))
message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year+"  |  ", fg="orange",bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
datef.pack(fill='both',expand=1)

clock = tk.Label(frame3,fg="orange",bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
clock.pack(fill='both',expand=1)
tick()

head2 = tk.Label(frame2, text="                       For New Registrations                       ", fg="black",bg="#3ece48" ,font=('times', 17, ' bold ') )
head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="                       For Already Registered                       ", fg="black",bg="#3ece48" ,font=('times', 17, ' bold ') )
head1.place(x=0,y=0)

lbl = tk.Label(frame2, text="Enter your ID :",width=20  ,height=1  ,fg="black"  ,bg="#626567" ,font=('times', 17, ' bold ') )
lbl.place(x=100, y=55)

txt = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold '))
txt.place(x=50, y=88)

lbl2 = tk.Label(frame2, text="Enter your Name :",width=20  ,fg="black"  ,bg="#626567" ,font=('times', 17, ' bold '))
lbl2.place(x=100, y=140)

txt2 = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold ')  )
txt2.place(x=50, y=173)

message1 = tk.Label(frame2, text=">>> Continue with registration process >>>" ,bg="#626567" ,fg="black"  ,width=39 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
message1.place(x=20, y=230)
message1 = tk.Label(frame2, text=">>> Proceed further >>>" ,bg="#626567" ,fg="black"  ,width=39 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
message1.place(x=20, y=260)

message = tk.Label(frame2, text="" ,bg="#626567" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="Attendence Details:",width=20  ,fg="black"  ,bg="#626567"  ,height=1 ,font=('times', 20, ' bold '))
lbl3.place(x=100, y=115)

res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message1 = tk.Label(frame2, text=">>> Needed help? Ask for Chatbot! >>>" ,bg="#626567" ,fg="black"  ,width=39 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
message1.place(x=35, y=450)
chatbotButton = tk.Button(frame2, text="Chatbot help 🤖", command=open_chatbot, fg="white", bg="#3ece48", width=34, height=1, activebackground="white", font=('times', 15, 'bold'))
chatbotButton.place(x=50, y=500)



##################### MENUBAR #################################

menubar = tk.Menu(window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='Change Password', command = change_pass)
filemenu.add_command(label='Contact Us', command = contact)
filemenu.add_command(label='Exit',command = window.destroy)
menubar.add_cascade(label='Help',font=('times', 29, ' bold '),menu=filemenu)

################## TREEVIEW ATTENDANCE TABLE ####################

style = ttk.Style()
style.theme_use("clam")

# Table styling
style.configure("Treeview",
                background="#f0f0f0",
                foreground="black",
                rowheight=30,
                fieldbackground="#f0f0f0",
                font=('Times New Roman', 12))
style.configure("Treeview.Heading",
                font=('Times New Roman', 13, 'bold'),
                background="#0a0a0a",
                foreground="white",
                borderwidth=1)
style.map('Treeview', background=[('selected', '#99e699')])

# Alternate row colors
tv = ttk.Treeview(frame1, height=13, columns=('ID', 'Name', 'Date', 'Time'), show='headings')
tv.tag_configure('oddrow', background="#ffffff")
tv.tag_configure('evenrow', background="#e6ffe6")

tv.heading('ID', text='ID')
tv.heading('Name', text='NAME')
tv.heading('Date', text='DATE')
tv.heading('Time', text='TIME')

tv.column('ID', anchor='center', width=80)
tv.column('Name', anchor='center', width=160)
tv.column('Date', anchor='center', width=130)
tv.column('Time', anchor='center', width=130)

tv.grid(row=2, column=0, padx=(10, 0), pady=(150, 0), columnspan=4)

# Add frame border
frame1.config(highlightbackground="black", highlightthickness=2)



###################### SCROLLBAR ################################

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

###################### BUTTONS ##################################

clearButton = tk.Button(frame2, text="Clear", command=clear  ,fg="black"  ,bg="#ea2a2a"  ,width=11 ,activebackground = "white" ,font=('times', 11, ' bold '))
clearButton.place(x=355, y=86)
clearButton2 = tk.Button(frame2, text="Clear", command=clear2  ,fg="black"  ,bg="#ea2a2a"  ,width=11 , activebackground = "white" ,font=('times', 11, ' bold '))
clearButton2.place(x=355, y=172)    
takeImg = tk.Button(frame2, text="Take Images", command=TakeImages  ,fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
takeImg.place(x=50, y=300)
trainImg = tk.Button(frame2, text="Save Profile", command=psw ,fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trainImg.place(x=50, y=380)
trackImg = tk.Button(frame1, text="TAKE ATTENDANCE", command=TrackImages  ,fg="orange"  ,bg="black"  ,width=35  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trackImg.place(x=40,y=50)
quitWindow = tk.Button(frame1, text="Quit", command=window.destroy  ,fg="black"  ,bg="red"  ,width=35 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
quitWindow.place(x=40, y=530)

##################### END ######################################

window.configure(menu=menubar)
window.mainloop()

####################################################################################################