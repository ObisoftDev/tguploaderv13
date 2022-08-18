import os
import requests
import json
try:
    from types import SimpleNamespace as Namespace
except ImportError:
    from argparse import Namespace

HOST = 'https://file2freeapi.herokuapp.com/file2free/'
PARSE_CALENDAR = 'calendar'
PARSE_BLOG = 'blog'
PARSE_EVIDENCE = 'evidence'

def create(host='',auth='auth',passw='',repoid=4,urls=[],parse='',zips=100):
    err = None
    jsondata = {'auth':auth,'urls':urls,'host':host,'clave':passw,'repoid':str(repoid),'parse':parse,'zips':zips}
    resp = requests.get(HOST+'create',json=jsondata)
    try:
        jsondata = json.loads(resp.text)
        if 'token' in jsondata:return err,jsondata['token']
        err = jsondata['state']
    except Exception as ex:
        err = str(ex)
        pass
    return err,None
def parse(host='',auth='auth',passw='',urls=[],type=''):
    err = None
    jsondata = {'auth':auth,'urls':urls,'host':host,'clave':passw,'type':type}
    resp = requests.get(HOST+'parse',json=jsondata)
    try:
        jsondata = json.loads(resp.text)
        if 'data' in jsondata:return err,json.loads(resp.text, object_hook = lambda d : Namespace(**d)).data
        err = jsondata['state']
    except Exception as ex:
        err = str(ex)
        pass
    return err,None
def state(token):
    err = None
    jsondata = {'token': token}
    try:
        resp = requests.get(HOST + 'state', json=jsondata)
        return None,json.loads(resp.text, object_hook = lambda d : Namespace(**d))
        err = jsondata['state']
    except Exception as ex:
        err = str(ex)
        pass
    return err, None

def hook_state(token,hookfunc=None,args=()):
    wait = True
    stat = None
    if token:
        while wait:
            err,stat = state(token)
            try:
                if stat.state != 'OK':
                   wait = False
                try:
                   if stat.data:
                      if stat.data.state == 0 or stat.data.state == 3:
                          wait = False
                      data = stat.data
                      if hookfunc:
                         hookfunc(data,args)
                except:pass
            except:
                pass
    return stat

#err,token = create(host='https://aulavirtual.elacm.sld.cu/',
#                   auth='obysoft',
#                   passw='Obysoft2001@',
#                   urls=['https://linksas.herokuapp.com/dl/7975/file2free.rar'],
#                   parse=PARSE_CALENDAR)
#print(err)
#print(token)
#def hook(state):
#    print(f'{state.auth} {state.file} {state.current} {state.total} {state.speed} {state.time}')

#state = hook_state(token,hook)
#print(state)
