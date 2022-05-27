"""                          EKİM 2020 TALPAY
                     ÇOK FONKSİYOLU GÜVENLİK SİSTEMİ
    ********************************************************************
    BAĞLANTI PİNLERİ:
    GSM TETİKLEME 32 NUMARALI PİNE
    PIR SENSÖR 7 NUMARALI PİNE
    RFID SOLDAN SAĞA DOGRU 2-21-5-17-22-20-24-23 NOLU PİNE
    1 NUMARALI LED 31 NUMARALI PİNE
    2 NUMARALI LED 33 NUMARALI PİNE
    3 NUMARALI LED 35 NUMARALI PİNE
    4 NUMARALI LED 37 NUMARALI PİNE
    
    ********************************************************************
    GEREKLİ KÜTÜPHANELER: 
    RFID KUTUPHANESİNİ İNDİREBİLMEK İÇİN TERMİNALE
    PYOTHON 2.*.* SERİSİ:sudo pip install pi-rc522
    PYOTHON 3.*.* SERİSİ:sudo pip3 install pi-rc522
    
"""

import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
from gpiozero import MotionSensor
from datetime import datetime
import time
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
global server
from pirc522 import RFID
import signal

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(32, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)

rdr = RFID()
util = rdr.util()
util.debug = True

camera = PiCamera()
pir = MotionSensor(4)

i = 0
j = 0
k = 0

filename = "Date:{0:%d}-{0:%m}-{0:%y} Time:{0:%H}-{0:%M}-{0:%S}".format(datetime.now())

#************FOTO DOSYALAMA FONKSİYONU*****************************
def foto():
    camera.start_preview()
    sleep(1)
    camera.capture('/home/pi/Desktop/foto/%s.jpg' % filename)
    camera.stop_preview()

#************VİDEO DOSYALAMA FONKSİYONU*****************************
def video():
    camera.start_preview()
    camera.start_recording('/home/pi/Desktop/video/%s.h264' % filename)
    sleep(10)
    camera.stop_recording()
    camera.stop_preview()
    
#************SABİT İSİMLE FOTO KAYDETME FONKSİYONU*******************  
def foto1():
    camera.start_preview()
    sleep(1)
    camera.capture('/home/pi/Desktop/foto.jpg')
    camera.stop_preview()

#************SABİT İSİMLE VİDEO KAYDETME FONKSİYONU*******************
def video1():
    camera.start_preview()
    camera.start_recording('/home/pi/Desktop/video.h264')
    sleep(10)
    camera.stop_recording()
    camera.stop_preview() 

#***************** MAİL FOTO GÖNDERME FONKSİYONU********************** 
def mailfoto():
    username = "tahiralpay98@gmail.com"
    password = "161101045t."
    mail_adress_to_send = "tahiralpay.mdbf16@iste.edu.tr"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    
    def send_mail( send_from, send_to, subject, text, file, isTls=True):
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = "".join(send_to)
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = subject
        msg.attach( MIMEText(text) )
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(file,"rb").read() )
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(file)))
        msg.attach(part)  
        server.sendmail(send_from, send_to, msg.as_string())
   
    send_from = ""
    subject = "UYARI"
    text = """
    Hareket Algılandı.
    """

    fileName = "/home/pi/Desktop/foto.jpg"
    send_mail(send_from, mail_adress_to_send, subject, text, fileName, isTls = True)
    print("mail foto başarıyla gönderildi")
    server.quit()

#*****************MAİL VİDEO GÖNDERME FONKSİYONU******************** 
def mailvideo():
    username = "tahiralpay98@gmail.com"
    password = "161101045t."
    mail_adress_to_send = "tahiralpay.mdbf16@iste.edu.tr"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    
    def send_mail( send_from, send_to, subject, text, file, isTls=True):
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = "".join(send_to)
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = subject
        msg.attach( MIMEText(text) )
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(file,"rb").read() )
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(file)))
        msg.attach(part)  
        server.sendmail(send_from, send_to, msg.as_string())
   
    send_from = ""
    subject = "UYARI"
    text = """
    Hareket Algılandı.
    """
    
    fileName = "/home/pi/Desktop/video.h264"
    send_mail(send_from, mail_adress_to_send, subject, text, fileName, isTls = True)
    print("MAİL VİDEO BAŞARIYLA GÖNDERİLDİ")
    server.quit()
    
               
while True:
    GPIO.output(32, GPIO.LOW)
    GPIO.output(31, GPIO.LOW)
    GPIO.output(33, GPIO.LOW)
    GPIO.output(35, GPIO.LOW)
    GPIO.output(37, GPIO.LOW)

#*****************RFID ANAHTARLAMA********************  
    (error, data) = rdr.request()
        
    if not error:
        #print("\nKart Algilandi!")
        (error, uid) = rdr.anticoll()
           
        if not error:
            rdr.wait_for_tag()

            kart_uid = str(uid[0])+" "+str(uid[1])+" "+str(uid[2])+" "+str(uid[3])+" "+str(uid[4])
            #print(kart_uid)
                
            if kart_uid == "151 182 254 26 197":
                j += 1
                print("switch:", j, "aktif")
                time.sleep(0.1)
                if j > 4:
                    i = 0
                    j = 0
                    k = 0
   
  #*****************KESİNTİSİZ DOSYALAMA************************** 
    if j == 1:
        GPIO.output(31, GPIO.HIGH)
        GPIO.output(33, GPIO.LOW)
        GPIO.output(35, GPIO.LOW)
        GPIO.output(37, GPIO.LOW)
        
        if pir.wait_for_no_motion:
            print("hareket_yok=", k)
            k += 1
            time.sleep(1)

            if k>60:
                k = 0
                i = 0
            
        if pir.motion_detected:
            print("hareket_var=", i)
            i += 1
            time.sleep(1)
            
            if i == 1:
                GPIO.output(32,GPIO.HIGH)
                foto()

            if i == 7:
                GPIO.output(32,GPIO.HIGH)                
                video()
                i = 0
                k = 0
 
 #*****************KESİNTİSİZ MAİL GÖNDERME************************** 
    if j == 2:
        GPIO.output(31, GPIO.LOW)
        GPIO.output(33, GPIO.HIGH)
        GPIO.output(35, GPIO.LOW)
        GPIO.output(37, GPIO.LOW)
        
        if pir.wait_for_no_motion:
            print("hareket_yok=", k)
            k += 1
            time.sleep(1)
            
            if k>60:
                k = 0
                i = 0
            
        if pir.motion_detected:
             print("hareket_var=", i)
             i += 1
             time.sleep(1.7)
            
             if i == 1:
                 GPIO.output(32,GPIO.HIGH)
                 foto1()
                 mailfoto()

             if i == 7:
                 GPIO.output(32,GPIO.HIGH)
                 video1()
                 time.sleep(5)
                 i = 0
                 k = 0
                 mailvideo()

#*****************RFID DOSYALAMA******************************** 
    if j == 3:
        GPIO.output(31, GPIO.LOW)
        GPIO.output(33, GPIO.LOW)
        GPIO.output(35, GPIO.HIGH)
        GPIO.output(37, GPIO.LOW)
        
        (error, data) = rdr.request()
        
        if not error:
            #print("\nKart Algilandi!")
            (error, uid) = rdr.anticoll()
            
            if not error:
                kart_uid = str(uid[0])+" "+str(uid[1])+" "+str(uid[2])+" "+str(uid[3])+" "+str(uid[4])
                #print(kart_uid)
                
                if kart_uid == "226 230 220 27 195":                   
                    if pir.wait_for_no_motion:
                        print("hareket_yok=", k)
                        k += 1
                        time.sleep(1)

                        if k>60: 
                            k = 0
                            i = 0
                            
                    if pir.motion_detected:
                        print("hareket_var=", i)
                        i += 1
                        time.sleep(1)
                                
                        if i == 1:
                            GPIO.output(32,GPIO.HIGH) 
                            foto()
                                    
                        if i == 7:
                            GPIO.output(32,GPIO.HIGH)
                            video()
                            i = 0
                            k = 0
 
#*****************RFID MAİL GÖNDERME************************** 
    if j == 4:
        GPIO.output(31, GPIO.LOW)
        GPIO.output(33, GPIO.LOW)
        GPIO.output(35, GPIO.LOW)
        GPIO.output(37, GPIO.HIGH
                    )
        (error, data) = rdr.request()
        
        if not error:
            #print("\nKart Algilandi!")
            (error, uid) = rdr.anticoll()
            
            if not error:
                kart_uid = str(uid[0])+" "+str(uid[1])+" "+str(uid[2])+" "+str(uid[3])+" "+str(uid[4])
                #print(kart_uid)
                
                if kart_uid == "226 230 220 27 195":                 
                    if pir.wait_for_no_motion:
                        print("hareket_yok=", k)
                        k += 1
                        time.sleep(1)
                                
                        if k>60:
                            k = 0
                            i = 0
                            
                    if pir.motion_detected:
                        print("hareket_var=", i)
                        i += 1
                        time.sleep(1)
                                
                        if i == 1:
                            GPIO.output(32,GPIO.HIGH)
                            foto1()
                            mailfoto()
                      
                        if i == 7:
                            GPIO.output(32,GPIO.HIGH)
                            video1()
                            time.sleep(5)
                            i = 0
                            k = 0
                            mailvideo()
