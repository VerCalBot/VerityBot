import os
import tkinter as tk
import configparser
import dotenv
import secrets
import base64




def init():

    def Save_Button():

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        #Get new values from the user entries
        newTo = inpTo.get()
        newFrom = inpFrom.get()
        newSubject = inpSubject.get()
        newMessage = inpMessage.get("1.0", "end-1c")
        newSendTime = inpSendTime.get()
        newFreq = freqVar.get()
        newEmailPass = inpEmailPass.get()
        newVerkAPI = inpApiKey.get("1.0", "end-1c")
        newElastPass = inpElastPass.get()
        newKibPass =inpKibPass.get()
        newKibEnc = inpKibEnc.get("1.0", "end-1c")

        #Updates config values
        co["Email"]["EMAIL_TO"] = newTo
        co["Email"]["EMAIL_FROM"] = newFrom
        co["Email"]["EMAIL_SUBJECT"] = newSubject
        co["Email"]["EMAIL_BODY_PREFIX"] = newMessage
        co["Email"]["EMAIL_SEND_TIME"] = newSendTime
        co["Verkada"]["TIME_DELTA_INSTALLATION"] = newFreq
        dotenv.set_key(dotenv_file, "EMAIL_PASSWORD", newEmailPass)
        dotenv.set_key(dotenv_file, "VERKADA_API_KEY", newVerkAPI)
        dotenv.set_key(dotenv_file, "ELASTIC_PASSWORD", newElastPass)
        dotenv.set_key(dotenv_file,"KIBANA_SYSTEM_PASSWORD", newKibPass)
        dotenv.set_key(dotenv_file,"KIBANA_ENCRYPTION_KEY", newKibEnc)

        #Writes new config values to file
        with open(os.path.join(BASE_DIR, '..', 'config.ini'), "w") as f:
            co.write(f)

        #Successful save message
        successfulSave = tk.Label(root, text="Saved Successfully!")
        successfulSave.grid(row = 12, column = 0, columnspan = 2, pady = 5)
        root.after(2000, successfulSave.destroy)

    def generate_kibana_key():
        key = base64.b64encode(secrets.token_bytes(32)).decode()
        inpKibEnc.delete("1.0", "end")
        inpKibEnc.insert("1.0", key or "")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    co = configparser.ConfigParser()
    co.read(os.path.join(BASE_DIR, '..', 'config.ini'))
    dotenv.load_dotenv()
    dotenv_file = ".env"

    root = tk.Tk(screenName=None, baseName='VerityBot', className='VerityBot', useTk=1)
    frame = tk.Frame(root)
    frame2 = tk.Frame(root)

    root.geometry("")

    #Title
    title = tk.Label(root, text="Welcome to VerityBot!")

    #Email_TO
    toLabel = tk.Label(root, text="Email Destination").grid(row=1, column=0)
    inpTo = tk.Entry(root, width=50)

    #EMAIL_FROM
    fromLabel = tk.Label(root, text="Email Sender").grid(row=2, column=0)
    inpFrom = tk.Entry(root, width=50)

    #EMAIL_SUBJECT
    subLabel = tk.Label(root, text="Email Subject").grid(row=3, column=0)
    inpSubject = tk.Entry(root, width=50)

    #EMAIL_BODY_PREFIX
    messageLabel = tk.Label(root, text="Email Message").grid(row=4, column=0)
    inpMessage = tk.Text(root, height=10, width=38)

    #EMAIL_SEND_TIME
    sendTimeLabel = tk.Label(root, text="Email Send Time (24HR)").grid(row=5, column=0)
    inpSendTime = tk.Entry(root, width = 7)

    #Email Password
    emailPassLabel = tk.Label(root, text="Email Password").grid(row=6, column=0)
    inpEmailPass = tk.Entry(root, width=50)

    #TIME_DELTA_INSTALLATION
    freqLabel1 = tk.Label(root, text="Update Verkada")
    freqVar = tk.StringVar()
    verkadaTimeInstallation = co.get("Verkada", "TIME_DELTA_INSTALLATION")
    freqVar.set(verkadaTimeInstallation)
    freqSpinbox = tk.Spinbox(frame, textvariable=freqVar, from_=1, to=60, width = 4)
    freqLabel2 = tk.Label(frame, text="time(s) per day")

    #Verkada API
    apiKeyLabel = tk.Label(root, text="Verkada API Key").grid(row=8, column=0)
    inpApiKey = tk.Text(root, height = 3, width=38)

    #Elastic Password
    elastPassLabel = tk.Label(root, text="Elastic Password").grid(row=9, column=0)
    inpElastPass = tk.Entry(root, width=50)

    #Kibana System Password
    kibPassLabel = tk.Label(root, text="Kibana Password").grid(row=10, column=0)
    inpKibPass = tk.Entry(root, width=50)

    #Kibana Encryption Key
    kibEncLabel = tk.Label(root, text="Kibana Encryption Key").grid(row=11, column=0)
    inpKibEnc = tk.Text(frame2, height = 2, width = 23)
    #Generate Encryption Key Button
    encButton = tk.Button(frame2, text="Generate Key", width=14, command=generate_kibana_key)

    #Title Insertion
    title.grid(row=0, column=0, columnspan=2, pady=10)

    #Email Entries
    inpTo.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    inpFrom.grid(row=2, column=1, padx=5, pady=5, sticky='w')
    inpSubject.grid(row=3, column=1, padx=5, pady=5, sticky='w')
    inpMessage.grid(row=4, column=1, padx=(5,15), pady=5, sticky='w')
    inpSendTime.grid(row=5, column=1, padx=5, pady=5, sticky='w')
    inpEmailPass.grid(row=6, column=1, padx=5, pady=5, sticky='w')

    #Verkada Entries
    freqLabel1.grid(row=7, column=0, padx=5, pady=5)
    frame.grid(row=7, column=1, padx=5, pady=5, sticky='w')
    freqSpinbox.grid(row=0, column=0)
    freqLabel2.grid(row=0, column=1)

    #ENV Entries
    inpApiKey.grid(row=8, column=1, padx=5, pady=5, sticky='w')
    inpElastPass.grid(row=9, column=1, padx=5, pady=5, sticky='w')
    inpKibPass.grid(row=10, column=1, padx=5, pady=5, sticky='w')
    frame2.grid(row=11, column=1, padx=5, pady=5, sticky='w')
    inpKibEnc.grid(row=0, column=0)
    encButton.grid(row=0, column=1, padx=5)

    #Getting existing config values
    emailTo = co.get("Email", "EMAIL_TO")
    emailFrom = co.get("Email", "EMAIL_FROM")
    emailSubject = co.get("Email", "EMAIL_SUBJECT")
    emailMessage = co.get("Email", "EMAIL_BODY_PREFIX")
    emailSendTime = co.get("Email", "EMAIL_SEND_TIME")
    emailPass = os.getenv("EMAIL_PASSWORD")
    verkAPIKey = os.getenv("VERKADA_API_KEY")
    elasticPass = os.getenv("ELASTIC_PASSWORD")
    kibanaPass = os.getenv("KIBANA_SYSTEM_PASSWORD")
    kibanaEncKey = os.getenv("KIBANA_ENCRYPTION_KEY")

    #Inserting existing config values
    inpTo.insert(0, emailTo)
    inpFrom.insert(0, emailFrom)
    inpSubject.insert(0, emailSubject)
    inpMessage.insert("1.0", emailMessage)
    inpSendTime.insert(0, emailSendTime)
    inpEmailPass.insert(0, emailPass or "")
    inpApiKey.insert("1.0", verkAPIKey or "")
    inpElastPass.insert(0, elasticPass or "")
    inpKibPass.insert(0, kibanaPass or "")
    inpKibEnc.insert("1.0", kibanaEncKey or "")

    #Save Button
    button = tk.Button(root, text="Save", width=20, command=Save_Button)
    button.grid(row = 12, column = 0, columnspan = 2, pady = 5)

    root.mainloop()

if __name__ == "__main__":
    init()
