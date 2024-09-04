import tkinter as tk
from tkinter import ttk, Message, Label, Entry, Button
import dframe as df
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

# Global variable to store the verification code
verification_code = None

def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_email(recipient_email, name):
    global verification_code
    verification_code = generate_verification_code()
    try:
        # SMTP server configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 465
        smtp_username = 'azimmustafa786@gmail.com'
        smtp_password = 'cvyd neuy jqoa tlje'

        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = recipient_email
        msg['Subject'] = 'Voter Registration Verification Code'

        # Email body
        body = f"""
        <html>
        <body>
            <h4>Dear {name},</h4>
            <p>Thank you for registering as a voter. Your verification code is:</p>
            <h2>{verification_code}</h2>
            <p>Please enter this code in the registration form to complete your registration.</p>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, recipient_email, msg.as_string())
        server.quit()

        print("Verification email sent successfully.")
        return True
    except Exception as e:
        print(f"Error sending verification email: {e}")
        return False

def reg_server(root, frame1, name, sex, zone, city, passw, email, verification_input):
    global verification_code
    if passw == '' or passw == ' ' or verification_input == '':
        msg = Message(frame1, text="Error: Missing Fields", width=500)
        msg.grid(row=12, column=0, columnspan=5)
        return -1

    if verification_input != verification_code:
        msg = Message(frame1, text="Error: Invalid Verification Code", width=500)
        msg.grid(row=12, column=0, columnspan=5)
        return -1

    vid = df.taking_data_voter(name, sex, zone, city, passw)
    for widget in frame1.winfo_children():
        widget.destroy()
    txt = "Registered Voter with\n\n VOTER I.D. = " + str(vid)
    Label(frame1, text=txt, font=('Helvetica', 18, 'bold')).grid(row=2, column=1, columnspan=2)

def send_code(email, name, frame1):
    if send_verification_email(email, name):
        msg = Message(frame1, text="Verification code sent to your email", width=500)
        msg.grid(row=12, column=0, columnspan=5)
    else:
        msg = Message(frame1, text="Error sending verification code", width=500)
        msg.grid(row=12, column=0, columnspan=5)

def Register(root, frame1):
    root.title("Register Voter")
    for widget in frame1.winfo_children():
        widget.destroy()

    Label(frame1, text="Register Voter", font=('Helvetica', 18, 'bold')).grid(row=0, column=2, rowspan=1)
    Label(frame1, text="").grid(row=1, column=0)
    Label(frame1, text="Name:         ", anchor="e", justify=tk.LEFT).grid(row=3, column=0)
    Label(frame1, text="Sex:              ", anchor="e", justify=tk.LEFT).grid(row=4, column=0)
    Label(frame1, text="Zone:           ", anchor="e", justify=tk.LEFT).grid(row=5, column=0)
    Label(frame1, text="City:             ", anchor="e", justify=tk.LEFT).grid(row=6, column=0)
    Label(frame1, text="Password:   ", anchor="e", justify=tk.LEFT).grid(row=7, column=0)
    Label(frame1, text="Email:           ", anchor="e", justify=tk.LEFT).grid(row=8, column=0)
    Label(frame1, text="Verification Code:", anchor="e", justify=tk.LEFT).grid(row=9, column=0)

    name = tk.StringVar()
    sex = tk.StringVar()
    zone = tk.StringVar()
    city = tk.StringVar()
    password = tk.StringVar()
    email = tk.StringVar()
    verification_input = tk.StringVar()

    Entry(frame1, textvariable=name).grid(row=3, column=2)
    Entry(frame1, textvariable=zone).grid(row=5, column=2)
    Entry(frame1, textvariable=city).grid(row=6, column=2)
    Entry(frame1, textvariable=password).grid(row=7, column=2)
    Entry(frame1, textvariable=email).grid(row=8, column=2)
    Entry(frame1, textvariable=verification_input).grid(row=9, column=2)

    e4 = ttk.Combobox(frame1, textvariable=sex, width=17)
    e4['values'] = ("Male", "Female", "Transgender")
    e4.grid(row=4, column=2)
    e4.current()

    send_code_button = Button(frame1, text="Send Code", command=lambda: send_code(email.get(), name.get(), frame1), width=10)
    send_code_button.grid(row=10, column=2)

    reg = Button(frame1, text="Register", command=lambda: reg_server(root, frame1, name.get(), sex.get(), zone.get(), city.get(), password.get(), email.get(), verification_input.get()), width=10)
    Label(frame1, text="").grid(row=11, column=0)
    reg.grid(row=11, column=3, columnspan=2)

    frame1.pack()
    root.mainloop()

# Uncomment to run the application
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.geometry('500x500')
#     frame1 = tk.Frame(root)
#     Register(root, frame1)