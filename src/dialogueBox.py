import tkinter as tk
import configparser
import tracemalloc

def Save_Button():

    #Get new values from the user entries
    newTo = inpTo.get()
    newFrom = inpFrom.get()
    newSubject = inpSubject.get()
    newMessage = inpMessage.get("1.0", "end-1c")
    newSendTime = inpSendTime.get()
    newFreq = freqVar.get()

    #Updates config values
    co["Email"]["EMAIL_TO"] = newTo
    co["Email"]["EMAIL_FROM"] = newFrom
    co["Email"]["EMAIL_SUBJECT"] = newSubject
    co["Email"]["EMAIL_MESSAGE"] = newMessage
    co["Email"]["EMAIL_SEND_TIME"] = newSendTime
    co["Verkada"]["TIME_DELTA_RECURRING"] = newFreq

    #Writes new config values to file
    with open("config.ini", "w") as f:
        co.write(f)

    #Successful save message
    successfulSave = tk.Label(root, text="Saved Successfully!")
    successfulSave.grid(row = 11, column = 0, columnspan = 2, pady = 5)
    root.after(2000, successfulSave.destroy)

co = configparser.ConfigParser()
co.read("config.ini")

root = tk.Tk(screenName=None, baseName='VerityBot', className='VerityBot', useTk=1)
frame = tk.Frame(root)

root.geometry("")

#Title
title = tk.Label(root, text="Welcome to VerityBot!")

#Email_TO
toLabel = tk.Label(root, text="Email Receiver").grid(row=1, column=0)
inpTo = tk.Entry(root, width=50)

#EMAIL_FROM
fromLabel = tk.Label(root, text="Email Sender").grid(row=2, column=0)
inpFrom = tk.Entry(root, width=50)

#EMAIL_SUBJECT
subLabel = tk.Label(root, text="Email Subject").grid(row=3, column=0)
inpSubject = tk.Entry(root, width=50)

#EMAIL_MESSAGE
messageLabel = tk.Label(root, text="Email Message").grid(row=4, column=0)
inpMessage = tk.Text(root, height=10, width=50)

#EMAIL_SEND_TIME
sendTimeLabel = tk.Label(root, text="Email Send Time").grid(row=5, column=0)
inpSendTime = tk.Entry(root)


#TIME_DELTA_RECURRING
freqLabel1 = tk.Label(root, text="Update Verkada data every")
freqVar = tk.StringVar()
verkadaTimeRecurring = co.get("Verkada", "TIME_DELTA_RECURRING")
freqVar.set(verkadaTimeRecurring)
freqSpinbox = tk.Spinbox(frame, textvariable=freqVar, from_=1, to=60)
freqLabel2 = tk.Label(frame, text="day(s)")

#Title Insertion
title.grid(row=0, column=0, columnspan=2, pady=10)

#Email Entries
inpTo.grid(row=1, column=1, padx=5, pady=5, sticky='w')
inpFrom.grid(row=2, column=1, padx=5, pady=5, sticky='w')
inpSubject.grid(row=3, column=1, padx=5, pady=5, sticky='w')
inpMessage.grid(row=4, column=1, padx=(5,15), pady=5, sticky='w')
inpSendTime.grid(row=5, column=1, padx=5, pady=5, sticky='w')

#Verkada Entries
freqLabel1.grid(row=6, column=0, padx=5, pady=5)
frame.grid(row=6, column=1, padx=5, pady=5, sticky='w')
freqSpinbox.grid(row=0, column=0)
freqLabel2.grid(row=0, column=1)

#Getting existing config values
emailTo = co.get("Email", "EMAIL_TO")
emailFrom = co.get("Email", "EMAIL_FROM")
emailSubject = co.get("Email", "EMAIL_SUBJECT")
emailMessage = co.get("Email", "EMAIL_MESSAGE")
emailSendTime = co.get("Email", "EMAIL_SEND_TIME")

#Inserting existing config values
inpTo.insert(0, emailTo)
inpFrom.insert(0, emailFrom)
inpSubject.insert(0, emailSubject)
inpMessage.insert("1.0", emailMessage)
inpSendTime.insert(0, emailSendTime)

#Save Button
button = tk.Button(root, text="Save", width=25, command=Save_Button)
button.grid(row = 7, column = 0, columnspan = 2, pady = 5)

root.mainloop()