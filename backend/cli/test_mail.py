from smtplib import SMTP, SMTP_SSL, SMTPException
import sys

smtp = 'smtp.u-picaride.fr'
user = 'hartra'
passw = 'f4BJYH'

#smtp = 'smtp.gmail.com'
user = 'harold@insset.fr'
passw = 'Googledrive&2018'

try:
    server = SMTP()
    server.connect(host='smtp.u-picardie.fr', port=587)
    #server.ehlo()
    #server.login(user, passw)
except:
    print('Something went wrong...')
sys.exit()


with SMTP() as smtp:
       smtp.set_debuglevel(1)
       smtp.connect(host='smtp.gmail.com', port=465)
       smtp.login(user='harold@insset.fr', password='Googledrive&2018')

       fromaddr = 'harold@insset.fr'
       toaddrs = ['harold@trannois.eu'] # On peut mettre autant d'adresses que l'on souhaite
       sujet = "test"
       msg = """\
From: %s\r\n\
To: %s\r\n\
Subject: %s\r\n\
\r\n\
%s
       """ % (fromaddr, ", ".join(toaddrs), sujet, 'test')
       try:
              smtp.sendmail(fromaddr, toaddrs, msg.encode('utf-8'))
       except SMTPException as e:
              print(e)
       smtp.quit()