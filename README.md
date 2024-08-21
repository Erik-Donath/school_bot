# school_bot
Dieser Discord Bot ermöglicht es, die Einträge eines Moodle Kalenders in einen Discord Channel zu schreiben.

# Requirements
Damit dieser Bot funktioniert, muss Python 3.12 zusammen mit den Paketen in ```requirements.txt``` installiert sein (Siehe: [Install](#install)).
Damit der Bot funktioniert müssen die Konfigurations-Dateien im Ordner ```config/``` angepasst werden (Siehe: [How to use](#how-to-use)).

# Install
Windows:<br>
    1. ```winget install Python.Python.3.12```<br>
    2. ```python -m pip install --upgrade pip```<br>
    3. ```pip3 install -r requirements.txt```<br>
Linux (debian):<br>
    1. ```sudo apt update```<br>
    2. ```sudo apt install python3 python3-pip```<br>
    3. ```pip3 install -r requirements.txt```<br>
Docker:<br>
    1. ```docker build . -t school_bot```<br>

# How to use
Für Linux und Windows muss folgender Command ausgeführt werden: ```python3 Run.py```<br>
Unter Docker muss folgender Command ausgeführt werden: ```docker run --rm -it -v ./config:/bot/config school_bot```.<br>
Beim ersten start wird das Programm den Ordner ```config``` erstellen und sich dann Beenden. In diesem werden die Dateien ```config.cfg``` und ```calender.cfg``` erstellt.<br>
<br>
Verändere folgende Felder nach der untenstehenden Beschreibung.
```
config.cfg:
    [Discord]
    activity = <Aktivitäts Nachricht des Bots>
    prefix = <Prefix des Bots (unused)>
    token = <Der Discord Bot Token>

calender.cfg:
    [Moodle]
    domain = <Die Domain (Webaddresse) deines Moodles. Beispiel: www.example.com>
    userid = <Die Userid des Moodle Nutzers>
    token = <Der Token des Moodle Nutzers>
    interval = <Wie lange dauert es, bis zum aktualisieren der Einträge. Entfohlen: 1 - 5 Minuten>
    enabled = true
    
    [Channel]
    title = <Titel der Nachricht des Bots>
    description = <Kurze Beschreibung der Nachricht>
    id = <Die Discord Channel Id des Kannals in dem die Nachrichten gesendet werden sollen>
    notfound = <Nachricht fals keine Einträge gefunden wurden>
    purge = <Soll der Kanal vor dem Senden der Wilkommensnachricht gelert werden>
    
    [Welcome]
    message = <Kurze Wilkommensnachricht>
    description = <Kurze Beschreibung unter der Wilkommensnachricht>
```

# Disclaimer
This project is licensed under the [MIT license](LICENSE). Use on own risk.