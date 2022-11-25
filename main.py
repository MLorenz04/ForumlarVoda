# Důležité importy
from flask import Flask, request, render_template
import re, json

# Nový Flask server
server = Flask(__name__)

@server.route('/')
def index():
    '''
    Metoda ukazující základní stránku s odkazem na registraci
    :return: Vyrendrovaná stránka index.html
    '''
    return render_template("index.html")

@server.route('/register')
def registration():
    '''
    Metoda ukazující formulář s registračními údaji
    :return: Vyrendrovaný formulář s registrací
    '''
    return render_template("registrace.html")

@server.route('/list', methods=['GET', 'POST'])
def list():
    '''
    Metoda vypisující všechny informace o registrovaných uživatelích

    :return: Vrací template s výpisem všech uživatelů
    '''
    list_lines = []
    f = open("static/students.txt")
    Lines = f.readlines()
    for line in Lines:
        list_lines.append(line.split("/-/"))
    return render_template("list.html", Lines = list_lines)


@server.route('/restapi/v1/validate/<nick>/<je_plavec>/<kanoe_kamarad>/<trida>', methods=['GET', 'POST'])
def validation(nick, je_plavec,kanoe_kamarad, trida):
    '''
    API Metoda na validaci formuláře

    nick = přezdívka uživatele
    je_plavec = informace, jestli je uživatel plavec
    kanoe_kamarad = informace o příteli, kterého chce mít spolu v kanoi
    :return: Vrací chybovou hlášku v případě chyby, jinak vrací hlášku o úspěšném vložení
    '''
    error_class = "Třída " + str(trida) + " neexistuje..."
    error_name_duplicity = "Toto jméno je již obsazeno!"
    error_name_mistake = "Vaše jméno nesplňuje požadavky!"
    error_swimmer = "Pokud neumíte plavat, co tady vlastně děláte?"
    error_friend = "Jméno vašeho kamaráda je špatně"
    regex_name = "^[A-Za-z0-9\s]{2,20}$";

    if not (re.match("^([c,a,eC,A,E]{1}[1-4]{1}[a-dA-D]?)$", trida)):
        return error_class

    if not (je_plavec == "1"):
       return error_swimmer

    if(str(nick)=="not_ok"):
        return error_name_duplicity

    if ((nick=="") or not (re.match(regex_name,nick))):
        return error_name_mistake
    if kanoe_kamarad != "" and not re.match(regex_name,kanoe_kamarad):
        return error_friend

    if (kanoe_kamarad == "none"): #Tady je "none" kvůli API - musí něco být, jinak url adresa nebude splňovat požadavky.
        kanoe_kamarad=""

    # Otevření souboru s metodou append
    f = open('static/students.txt', 'a')
    string = nick + "/-/" + kanoe_kamarad + "/-/" + trida + "\n"
    f.write(string)
    f.close()
    return "OK"

@server.route('/restapi/v1/check_name/<name>')
def check_name(name):
    '''
    Restapi metoda, která kontroluje, jestli není duplicitně zadáno jméno.

    :param name: Jméno uživatele, které kontrolujeme na duplicitu
    :return: Správnost výsledku - True vrací duplicitu, False vrací nenalezený výsledek
    '''
    f = open("static/students.txt")
    Lines = f.readlines()
    list_of_lines = []
    # Rozdělím nejdříve každou řádku na list tří proměnných - jméno, kamaráda a třídu.
    for line in Lines:
        list_of_lines.append(line.split("/-/"))
    for line in list_of_lines:
        if (str(line[0]) == str(name)): #Pokud se jméno na začátku řádku rovná zadanému jménu, hodím chybu
            return "false"
    f.close()
    return "true"

if __name__ == "__main__":
    server.run(host="0.0.0.0", port = 666)
