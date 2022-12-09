import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


def sendEmailAlert(imagePath):
    #Address data
    sender = 'cse525.group9fall2022@gmail.com'
    senderPassword = 'ezsorenzegvutpta'
    sendTo = 'jacobohcr@gmail.com'
    
    #Create message
    msg = MIMEMultipart()
    msg["Subject"] = "[PI SECURITY] INTRUDER ALERT"
    msgText = "Pi Security has detected an intruder!!!"
    msg.attach(MIMEText(msgText, 'plain'))
    msg["From"] = sender
    msg["To"] = sendTo
    msg.preamble = "INTRUDER ALERT"
    
    #Attach image
    attachment = open(imagePath, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    
    p.add_header('Content-Disposition', "attachment; filename= %s" % "capture.jpg")
    
    msg.attach(p)
    
    
    
    #with open(imagePath, 'rb') as fp:
    #    img = MIMEImage(fp.read())
    #    img.add_header('Content-Disposition', 'attachment', filename="image.jpg")
    #    msg.attach(img)
    
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender, senderPassword)
    text = msg.as_string()
    session.sendmail(sender, sendTo, text)
    session.quit()
    ##try:
    #    s = smtplib.SMTP("localhost")
    #    s.sendmail(sender, sendTo, msg.as_string())
    #    s.quit()
    #except smtplib.SMTPException:
    #    print("ERROR: Failed to send email alert " + imagePath)
    
    return

#Test Code
#sendEmailAlert("/home/Hat/ECE525/FinalProject/SecurityCam/img2022-12-07 14:54:44.002068.jpg")
    