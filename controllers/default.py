# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################
import requests, json

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to DisRes!!!")
    if session.user is None:
        response.flash = "Please Login!"
    elif session.user == "admin":
        redirect(URL(c="default", f="admin"))
#    elif session.user == "user":
#        redirect(URL(c="default", f="user"))
        
    return dict()

def admin():
    # Send HTTP request to the REST server
    url = "http://127.0.0.1:9000/disasters/"
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    list_organisations = json.loads(r.text)

    t = TABLE(TR(TH("Created"), TH("Disaster Type"), TH("Latitude"), TH("Longitude")),
              _class="table")
    for i in list_organisations:
        t.append(TR(TD(A(i["created"]), _href=URL(c="default", f="disaster_details")),
                    TD(A(i["dis_type"]), _href=URL(c="default", f="disaster_details")),
                    TD(A(i["latitude"]), _href=URL(c="default", f="disaster_details")),
                    TD(A(i["longitude"], _href=URL(c="default", f="disaster_details")))
                    )
                 )
    return dict(t=t)

def user():
    return dict()

def disaster_details():
    # Send HTTP request to the REST server
    url = "http://127.0.0.1:9000/disasters/"
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    return dict()

def email():

    if session.user is None:
        response.flash = "Please Login!"
        redirect(URL(c="login", f="index"))

    form = FORM(TABLE(TR(TD('Username: '), TD(INPUT(_name='name', requires=IS_NOT_EMPTY()))),
                      TR(TD('Password: '), TD(INPUT(_name='password', _type='password', requires=IS_NOT_EMPTY()))), 
                      TR(TD('Send To: '), TD(INPUT(_name='sendto', requires=IS_NOT_EMPTY()))),
                      TR(TD('Subject: '), TD(INPUT(_name='Subject', requires=IS_NOT_EMPTY()))),
                      TR(TD('Message: '), TD(TEXTAREA(_name='Message', requires=IS_NOT_EMPTY()))),
                      TR(INPUT(_type='submit', _value='SEND')),
                      ))

    if form.accepts(request,session):
        email = str(request.vars['name']) + "@students.iiit.ac.in"
        password = str(request.vars['password'])
        from gluon.tools import Mail
        mail = Mail()
        mail.settings.server = "students.iiit.ac.in:25"
        mail.settings.sender = email
        mail.settings.login = str(request.vars['name']) + ":" + password
        mail.send(to=[str(request.vars['sendto'])],
                  subject=str(request.vars['Subject']),
                  # If reply_to is omitted, then mail.settings.sender is used
                  message=str(request.vars['Message']))
        response.flash = 'Message sent'
    elif form.errors:
        response.flash = 'Error Occured'
    else:
        response.flash = 'Please fill the form'
    return dict(form=form)

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
