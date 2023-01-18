import smtplib
import imghdr
from email.message import EmailMessage
import env
def send_email(image_path):
    email_message= EmailMessage()
    email_message["Subject"]="ALERT !!! Something happening. "
    email_message.set_content("ALERT !!! Something happening, require attention !! ")
    with open(image_path,"rb") as file:
        content=file.read()
    email_message.add_attachment(content,maintype="image",subtype=imghdr.what(None, content))
    gmail= smtplib.SMTP("smtp.gmail.com",587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(env.SENDER,env.password)
    gmail.sendmail(env.SENDER,env.RECEVER,email_message.as_string())
    gmail.quit()


if __name__=="__main__":
    send_email(image_path="images/20.png")
