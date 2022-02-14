from smtplib import SMTP, SMTPException
import os

def sendAccesViaEmail(msg='../conf/email/htpasswd.txt', info=None):
       if info is None:
              info = {'adr': '', 'domain': '', 'user': '', 'password': ''}
       try:
              smtpPass = os.environ['SMTP_PASS']
              smtpUser = os.environ['SMTP_USER']
              smtpEmail = os.environ['SMTP_EMAIL']
       except KeyError:
              print("Fixer la variable d'environnement SMTP_PASS SMTP_USER SMTP_EMAIL avec vos identifiant smtp")
              return


       with open(msg, 'r') as file:
              message = file.read()
              message = message.replace("{DOMAIN}", info['domain'])
              message = message.replace("{USER}", info['user'])
              message = message.replace("{PASSWORD}", info['password'])

       with SMTP() as smtp:
              #smtp.set_debuglevel(1)
              smtp.connect(host='smtp.u-picardie.fr', port=587)
              smtp.login(user=smtpUser, password=smtpPass)

              fromaddr = smtpEmail
              toaddrs = [info['adr']] # On peut mettre autant d'adresses que l'on souhaite
              sujet = "Vos acces pour votre projet"
              msg = """\
From: %s\r\n\
To: %s\r\n\
Subject: %s\r\n\
\r\n\
%s
              """ % (fromaddr, ", ".join(toaddrs), sujet, message)
              try:
                     print("From:%s\nTo:%s\nSujet:%s\nCorps:%s" % (fromaddr, ", ".join(toaddrs), sujet, message ))
                     smtp.sendmail(fromaddr, toaddrs, msg.encode('utf-8'))
                     print("\n===> Envoyer\n")
              except SMTPException as e:
                     print(e)
              smtp.quit()