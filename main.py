from cProfile import run
import pstats
from pyobigram.utils import sizeof_fmt,get_file_size,createID,nice_time
from pyobigram.client import ObigramClient,inlineQueryResultArticle
from pyobigram.client import inlineKeyboardMarkup,inlineKeyboardMarkupArray,inlineKeyboardButton

from JDatabase import JsonDatabase
import shortener
import zipfile
import os
import infos
import xdlink
import mediafire
import datetime
import time
import youtube
from ProxyCloud import ProxyCloud
import ProxyCloud
import socket
import tlmedia
import S5Crypto
import asyncio
import aiohttp
from yarl import URL
import re
import random
import S5Crypto


import f2f

def sendTxt(name,files,update,bot):
                txt = open(name,'w')
                fi = 0
                for f in files:
                    separator = ''
                    if fi < len(files)-1:
                        separator += '\n'
                    try:
                        txt.write(f.url+separator)
                    except:
                        try:
                            txt.write(f + separator)
                        except:pass
                    fi += 1
                txt.close()
                bot.sendFile(update.message.chat.id,name)
                os.unlink(name)

def hook_state(state,args=None):
    try:
        filename = state.file
        current = state.current
        total = state.total
        speed = state.speed
        time = state.time
        status = state.state
        update = args[0]
        bot = args[1]
        message = args[2]
        if status==1:
            progresmsg = infos.createDownloading(filename,total,current,speed,time)
            bot.editMessageText(message,progresmsg)
        if status==2:
            progresmsg = infos.createUploading(filename,total,current,speed,time)
            bot.editMessageText(message,progresmsg)
    except:pass


def onmessage(update,bot:ObigramClient):
    try:
        thread = bot.this_thread
        username = update.message.sender.username
        tl_admin_user = os.environ.get('tl_admin_user')

        #set in debug
        #tl_admin_user = 'obidevel'

        jdb = JsonDatabase('database')
        jdb.check_create()
        jdb.load()

        user_info = jdb.get_user(username)
        #if username == tl_admin_user or user_info:
        if username in str(tl_admin_user).split(';') or user_info or tl_admin_user=='*':  # validate user
            if user_info is None:
                #if username == tl_admin_user:
                if username == tl_admin_user:
                    jdb.create_admin(username)
                else:
                    jdb.create_user(username)
                user_info = jdb.get_user(username)
                jdb.save()
        else:
            mensaje = "🚷 No tienes Acceso 🚷"
            reply_markup = inlineKeyboardMarkup(
                r1=[inlineKeyboardButton('⚙Contactar Soporte⚙',url='https://t.me/obidevel')]
            )
            bot.sendMessage(update.message.chat.id,mensaje,reply_markup=reply_markup)
            return

        msgText = ''
        try: msgText = update.message.text
        except:pass

        # comandos de admin
        if '/adduser' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                try:
                    user = str(msgText).split(' ')[1]
                    jdb.create_user(user)
                    jdb.save()
                    msg = '😃Genial @'+user+' ahora tiene acceso al bot👍'
                    bot.sendMessage(update.message.chat.id,msg)
                except:
                    bot.sendMessage(update.message.chat.id,'❌Error en el comando /adduser username❌')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        if '/addadmin' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                try:
                    user = str(msgText).split(' ')[1]
                    jdb.create_admin(user)
                    jdb.save()
                    msg = '😃Genial @'+user+' ahora es Admin del bot👍'
                    bot.sendMessage(update.message.chat.id,msg)
                except:
                    bot.sendMessage(update.message.chat.id,'❌Error en el comando /adduser username❌')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        if '/shorturl' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                try:
                    for user in jdb.items:
                        if jdb.items[user]['urlshort']==0:
                            jdb.items[user]['urlshort'] = 1
                            continue
                        if jdb.items[user]['urlshort']==1:
                            jdb.items[user]['urlshort'] = 0
                            continue
                    jdb.save()
                    bot.sendMessage(update.message.chat.id,'✅ShortUrl Cambiado✅')
                    statInfo = infos.createStat(username, user_info, jdb.is_admin(username))
                    reply_markup = None
                    if user_info['proxy'] != '':
                        reply_markup = inlineKeyboardMarkup(
                            r1=[inlineKeyboardButton('✘ Quitar Proxy ✘', callback_data='/deleteproxy ' + username)]
                        )
                    bot.sendMessage(update.message.chat.id, statInfo,reply_markup=reply_markup)
                except:
                    bot.sendMessage(update.message.chat.id,'❌Error en el comando /banuser username❌')
            return
        if '/banuser' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                try:
                    user = str(msgText).split(' ')[1]
                    if user == username:
                        bot.sendMessage(update.message.chat.id,'❌No Se Puede Banear Usted❌')
                        return
                    jdb.remove(user)
                    jdb.save()
                    msg = '🦶Fuera @'+user+' Baneado❌'
                    bot.sendMessage(update.message.chat.id,msg)
                except:
                    bot.sendMessage(update.message.chat.id,'❌Error en el comando /banuser username❌')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        if '/getdb' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                bot.sendMessage(update.message.chat.id,'Base De Datos👇')
                bot.sendFile(update.message.chat.id,'database.jdb')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        # end

        # comandos de usuario
        if '/tutorial' in msgText:
            tuto = open('tuto.txt','r')
            bot.sendMessage(update.message.chat.id,tuto.read())
            tuto.close()
            return
        if '/info' in msgText:
            getUser = user_info
            if getUser:
                statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                reply_markup = None
                bot.sendMessage(update.message.chat.id,statInfo,reply_markup=reply_markup)
                return
        if '/zips' in msgText:
            getUser = user_info
            if getUser:
                try:
                   size = int(str(msgText).split(' ')[1])
                   getUser['zips'] = size
                   jdb.save_data_user(username,getUser)
                   jdb.save()
                   msg = '😃Genial los zips seran de '+ sizeof_fmt(size*1024*1024)+' las partes👍'
                   bot.sendMessage(update.message.chat.id,msg)
                except:
                   bot.sendMessage(update.message.chat.id,'❌Error en el comando /zips size❌')
                return
        if '/account' in msgText:
            try:
                account = str(msgText).split(' ',2)[1].split(',')
                user = account[0]
                passw = account[1]
                getUser = user_info
                if getUser:
                    getUser['moodle_user'] = user
                    getUser['moodle_password'] = passw
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                    reply_markup = None
                    bot.sendMessage(update.message.chat.id,statInfo,reply_markup=reply_markup)
            except:
                bot.sendMessage(update.message.chat.id,'❌Error en el comando /account user,password❌')
            return
        if '/host' in msgText:
            try:
                cmd = str(msgText).split(' ',2)
                host = cmd[1]
                getUser = user_info
                if getUser:
                    getUser['moodle_host'] = host
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                    reply_markup = None
                    bot.sendMessage(update.message.chat.id,statInfo,reply_markup=reply_markup)
            except:
                bot.sendMessage(update.message.chat.id,'❌Error en el comando /host moodlehost❌')
            return
        if '/repo' in msgText:
            try:
                cmd = str(msgText).split(' ',2)
                repoid = int(cmd[1])
                getUser = user_info
                if getUser:
                    getUser['moodle_repo_id'] = repoid
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                    reply_markup = None
                    bot.sendMessage(update.message.chat.id,statInfo,reply_markup=reply_markup)
            except:
                bot.sendMessage(update.message.chat.id,'❌Error en el comando /repo id❌')
            return
        if '/crypt' in msgText:
            proxy_sms = str(msgText).split(' ')[1]
            proxy = S5Crypto.encrypt(f'{proxy_sms}')
            bot.sendMessage(update.message.chat.id, f'Crypt:\n{proxy}')
            return
        if '/decrypt' in msgText:
            proxy_sms = str(msgText).split(' ')[1]
            proxy_de = S5Crypto.decrypt(f'{proxy_sms}')
            bot.sendMessage(update.message.chat.id, f'Decrypt:\n{proxy_de}')
            return
        if '/parse' in msgText:
            try:
                type = str(msgText).split(' ')[1]
                doc = update.message.reply_to_message.document
                docfile = bot.downloadFile(doc.file_id,doc.file_name)
                odoc = open(docfile)
                urls = str(odoc.read()).split('\n')
                odoc.close()
                err, data = f2f.parse(host=user_info['moodle_host'],
                                        auth=user_info['moodle_user'],
                                        passw=user_info['moodle_password'],
                                        urls=urls,
                                        type=type)
                if err:
                    bot.sendMessage(update.message.chat.id, f'⭕{err}⭕')
                if data:
                    if len(data) > 0:
                        sendTxt(docfile,data, update, bot)
            except Exception as ex:
                bot.sendMessage(update.message.chat.id, f'⭕ERROR {str(ex)}⭕')

            return
        #end

        message = bot.sendMessage(update.message.chat.id,'⏳Procesando...')

        thread.store('msg',message)

        if '/start' in msgText:
            reply_markup = inlineKeyboardMarkup(
                r1=[inlineKeyboardButton('📊 Github Dev 📊', url='https://github.com/ObisoftDev'),
                    inlineKeyboardButton('⚙ Soporte ⚙', url='https://t.me/obidevel')]
            )
            bot.editMessageText(message,infos.dashboard(),parse_mode='html',reply_markup=reply_markup)
        elif 'http' in msgText:
            url = msgText
            filename = str(url).split('/')[-1]
            err, token = f2f.create(host=user_info['moodle_host'],
                                auth=user_info['moodle_user'],
                                passw=user_info['moodle_password'],
                                urls=[url],
                                repoid=user_info['moodle_repo_id'],zips=user_info['zips'])
            print(err)
            print(token)
            if token:
                try:
                    state = f2f.hook_state(token,hook_state,args=(update,bot,message))
                    if state:
                        txtname = filename.split('.')[0] + '.txt'
                        finishInfo = infos.createFinishUploading(filename)
                        filesInfo = infos.createFileMsg(filename, state.data.uploadlist)
                        bot.editMessageText(message,finishInfo+'\n'+filesInfo,parse_mode='html')
                        if len(state.data.uploadlist)>0:
                            sendTxt(txtname,state.data.uploadlist,update,bot)
                except Exception as ex:
                    print(str(ex))
                    reply_markup = inlineKeyboardMarkup(r1=[inlineKeyboardButton('⚗Recuperar Estado⚗', callback_data='/update '+token+' '+filename)])
                    bot.editMessageText(message,'🚫ERROR EN EL ESTADO🚫',reply_markup=reply_markup)
            else:
                bot.editMessageText(message,'🚫USTED NO PUEDE SUBIR!🚫')
        else:
            #if update:
            #    api_id = os.environ.get('api_id')
            #    api_hash = os.environ.get('api_hash')
            #    bot_token = os.environ.get('bot_token')
            #    
                # set in debug
            #    api_id = 7386053
            #    api_hash = '78d1c032f3aa546ff5176d9ff0e7f341'
            #    bot_token = '5124841893:AAH30p6ljtIzi2oPlaZwBmCfWQ1KelC6KUg'

            #    chat_id = int(update.message.chat.id)
            #    message_id = int(update.message.message_id)
            #    import asyncio
            #    asyncio.run(tlmedia.download_media(api_id,api_hash,bot_token,chat_id,message_id))
            #    return
            bot.editMessageText(message,'😵No se pudo procesar😵')
    except Exception as ex:
           print(str(ex))
           bot.sendMessage(update.message.chat.id,str(ex))

def cancel_task(update,bot:ObigramClient):
    try:
        cmd = str(update.data).split(' ', 2)
        tid = cmd[0]
        tcancel = bot.threads[tid]
        msg = tcancel.getStore('msg')
        tcancel.store('stop', True)
        time.sleep(3)
        bot.deleteMessage(update.message)
    except Exception as ex:
        print(str(ex))
    return
    pass

def update_state(update,bot:ObigramClient):
    try:
        cmd = str(update.data).split(' ')
        token = cmd[0]
        filename = cmd[1]
        if token:
                try:
                    state = f2f.hook_state(token,hook_state,args=(update,bot,update.message))
                    if state:
                        txtname = filename.split('.')[0] + '.txt'
                        finishInfo = infos.createFinishUploading(filename)
                        filesInfo = infos.createFileMsg(filename, state.data.uploadlist)
                        bot.editMessageText(update.message,finishInfo+'\n'+filesInfo,parse_mode='html')
                        if len(state.data.uploadlist)>0:
                            sendTxt(txtname,state.data.uploadlist,update,bot)
                except Exception as ex:
                    print(str(ex))
                    reply_markup = inlineKeyboardMarkup(r1=[inlineKeyboardButton('⚗Recuperar Estado⚗', callback_data='/update '+token+' '+filename)])
                    bot.editMessageText(message,'🚫ERROR EN EL ESTADO🚫',reply_markup=reply_markup)
    except Exception as ex:
        print(str(ex))
    return
    pass

def main():
    bot_token = os.environ.get('bot_token')
    print('init bot.')
    #set in debug
    #bot_token = '5437096479:AAFc8sK6pNhlsZTywFXxt-LBk9ApDWbp9t8'
    bot = ObigramClient(bot_token)
    bot.onMessage(onmessage)
    bot.onCallbackData('/cancel ',cancel_task)
    bot.onCallbackData('/update ',update_state)
    bot.run()

if __name__ == '__main__':
    try:
        main()
    except:
        main()
