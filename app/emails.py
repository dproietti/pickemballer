import requests
import os

print 'OS ENV: %s' % os.environ

def send_email(subject, sender, recipients, text_body, html_body):
    MAILGUN_DOMAIN = None
    MAILGUN_KEY = None

    if 'C9_HOSTNAME' in os.environ:
        MAILGUN_DOMAIN = 'sandbox77b45b303fab46b29c4578f629213ca9.mailgun.org'
        MAILGUN_KEY = 'key-e3e61696dc0a78667e9fbf0639a7b26b'
    elif 'HOST_NAME' in os.environ and os.environ['HOST_NAME'] == 'www.pickemballer.com' or 'VIRTUAL_ENV' in os.environ and os.environ['VIRTUAL_ENV'] == '/home/dproietti/.virtualenvs/baller-beta':
        MAILGUN_DOMAIN = "pickemballer.com"
        MAILGUN_KEY = "key-e3e61696dc0a78667e9fbf0639a7b26b"


    request=requests.post(
        'https://api.mailgun.net/v2/%s/messages' % MAILGUN_DOMAIN,
        auth=("api", MAILGUN_KEY),
        #files=[("attachment", open("test.jpg"))],
        data={"from" : sender,
            "to": recipients,
            #"to": 'daniel.proietti@gmail.com',
            "subject": subject,
            "text": text_body,
            "html": html_body})

    if 'C9_HOSTNAME' in os.environ:
        print 'email - begin'
        print 'to: %s' % recipients
        print 'from: %s' % sender
        print 'subject: %s' % subject
        print 'body -----------------------------------'
        print text_body
        print 'body -----------------------------------'

        print 'Status: {0}'.format(request.status_code)
        print 'Body:   {0}'.format(request.text)

    if request.status_code == 200:
        return True
    else:
        print "MAILGUN_DOMAIN: %s" % MAILGUN_DOMAIN
        print 'email - begin'
        print 'to: %s' % recipients
        print 'from: %s' % sender
        print 'subject: %s' % subject
        print 'body -----------------------------------'
        print text_body
        print 'body -----------------------------------'

        print 'Status: {0}'.format(request.status_code)
        print 'Body:   {0}'.format(request.text)

