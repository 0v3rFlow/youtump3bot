#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import telepot
import youtube_dl
import os
from telepot.loop import MessageLoop

texti01 = "Ciao & 😊, per iniziare a scaricare il video in formato mp3 basta inviarmi il link di youtube 🧲, al resto ci penso io ✌️😎."\
          "Sei libero di salvare il file tra le tue canzoni oppure lasciarlo su telegramm."\
          "Se apri l'audio rimarrà attivo anche se apri altre applicazioni."\
          "Buon divertimento 😁"

texti02 = "Ho recuperato tutte le informazioni del video👍🤓.Inizio a scaricare e convertire..."
texti03 = "Download effettuato!😈"
texte01 = "⚠️⚠️ C'è un problema nel link 😭. RIprova e assicurati che sia corretto 🥺."
texte02 = "⚠️⚠️ Problema nell'invio audio 😭. File troppo grande. Scegliere un video con una minor durata 🥺."
texte03 = "⚠️⚠️ Non hai inserito un testo. Riprova e passami il link. 😊"
texte04 = "Mi dispiace 😔 ma il video è superiore hai 10 minuti, scegline un altro più breve. 😊"

def recupero_info_link(input_text):
          
    # Setto le variabili link e title
    link = ''
    title = ''

    ydl_opts = {'quiet': 'X', 'noplaylist': 'X'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(input_text, download=False)
        duration = meta['duration']
        minuti = duration / 60
        # se il video ha una dura più di 10 minuti non vado avanti
        if minuti < 10.05:
            # Recupero il link originale
            link = meta['webpage_url']
            # Recupero il titolo
            title = meta['title']
            return link, title
        else:
            return link, title


def youtube_to_mp3(link, title, chat_id, name):

    filename = title + '.%(ext)s'
    ydl_opts = {
        'writethumbnail': True,
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'quiet': 'X',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320', },
            {'key': 'EmbedThumbnail', }, ],
        'noplaylist': 'X',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
        # Invio l'audio con il file appena scaricato
        try:
            # Nome del file
            filename = title + '.mp3'
            bot.sendAudio(chat_id, audio=open(filename, 'rb'))
            # Messaggio dowload effettuato con successo
            bot.sendMessage(chat_id, texti03)
            print(name + ' ' + 'ha scaricato correttamente' + ' ' + title)
            # Cancello file.
            os.remove(filename)
        except:
            bot.sendMessage(chat_id, texte02)
            os.remove(filename)


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    input_text = ''
    # Prelevo il messaggio inserito dall'utente e controllo che sia un testo
    try:
        input_text = msg['text']
    except:
        bot.sendMessage(chat_id, texte03)

    if input_text:
        # Prende l'username
        name = msg['from']['first_name']
        print(content_type, chat_type, chat_id, name, input_text)

        if input_text == '/start':
            # Se l'utente digita /start
            messaggio = texti01
            messaggio = messaggio.replace('&', name)
            bot.sendMessage(chat_id, messaggio)
        else:
            try:
                # Recupero le informazioni dal link. N
                link, title = recupero_info_link(input_text)
                if link:
                    # Messaggio per info stato
                    bot.sendMessage(chat_id, texti02)
                else:
                    bot.sendMessage(chat_id, texte04)
            except:
                # Se ho qualsiasi tipo di errore durante il recuper delle informazioni o durante il download
                bot.sendMessage(chat_id, texte01)
                link = ''
                title = ''

            if link:
                # Se sono riuscito ad ottenere il link
                youtube_to_mp3(link, title, chat_id, name)

TOKEN = os.environ.get('API_TOKEN', None)
if __name__ == "__main__":
    # Recuper il TOKEN
    bot = telepot.Bot(TOKEN)
    # Avvio il loop dei messaggi
    MessageLoop(bot, {'chat': on_chat_message, }).run_as_thread()
    print('Listening ...')
    while 1:
        time.sleep(10)
