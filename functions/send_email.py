#import necessaires
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

#fonction d'envoi du mail
def mailer():
    directory = "archives"
    date_str = datetime.now().strftime("%Y-%m-%d")
    senders = os.getenv("EMAIL")
    password = ""
    receivers = os.getenv("EMAIL")
    object = f"Rapport du {date_str}"
    name = os.getenv("NAME")
    body = f"Bonjour M. or Mme {name}"
    file_name = os.path.join(directory, f"news_letters_{date_str}.txt")
    password = os.getenv("PASSWORD")
    file_at_add = file_name
    file = os.path.basename(file_at_add)
    msg = MIMEMultipart()
    #creation de l'obejt msg
    msg['From'] = senders
    msg['To'] = receivers
    msg['Subject'] = object
    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(file_name, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {file}",
        )
        msg.attach(part)
    except FileNotFoundError:
        print(f"Erreur : Le fichier spécifié ({file_name}) n'a pas été trouvé.")
        return False 

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(senders, password)
        full_text = msg.as_string()
        server.sendmail(senders, receivers, full_text)
        print("\n✅ Email envoyé avec succès !")
        print(f" Destinataire : {senders}")
        print(f" Pièce jointe : {file}")
        return True 
        
    except smtplib.SMTPAuthenticationError:
        print("\n❌ Erreur d'authentification : Veuillez vérifier l'email/mot de passe.")
        print(" Si vous utilisez Gmail, assurez-vous d'utiliser un 'Mot de passe d'application'.")
        return False 
        
    except Exception as e:
        print(f"\n❌ Une erreur s'est produite lors de l'envoi : {e}")
        return False 
        
    finally:
        if 'server' in locals() and server:
            server.quit()