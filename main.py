""" Imports """     """ Alle benötigten Module werden hier importiert """
import email, smtplib, ssl, json, os, requests, time, datetime
from pathlib import Path
from email.message import EmailMessage
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep



""" Attributes """      """ Alle globalen Attribute (Variablen) für den Programmablauf werden in diesem Bereich gespeichert """

# Aktien-Daten
api_token = "bus50cf48v6t07kq4lug"  # API-Token für die Benutzung der API von finnhub.io (API-Token ist von Alexander Biber vorgegeben)
symbol="TSLA"   # Das Symbol der Aktie - Ausschliesslich Symbole der amerikanischen Börse möglich
currency_base = "USD"   # Basis für Währungskursumrechnung
currency_pair = "EUR"   # Währungspaar zur Währungskursumrechnung
price_difference_percent = 0    # Angabe, bei wie viel Preisunterschied in % zum Öffnungskurs des Tages der Trigger eine E-Mail senden soll
price_change_since_last_open_in_percent = None  # die Preisdifferenz seit Börsenöffnung des Tages wird bei compare_data(current_stock_data) geändert und hier gespeichert
price_change_since_last_open_in_percent_for_printing = None # Speicherung der Preisänderung in Prozent mit dem eventuellen Minuszeichen, zur Ausgabe in der Konsole

# E-Mail-Daten
sender_email = "d1sturrb@outlook.com" # E-Mail mit der gesendet werden soll (bitte nur Outlook/Hotmail-Emailadresse)
receiver_email = sender_email # Empfänger-Emailadresse (hier wird an sich selbst gesendet)

path_to_password = os.path.dirname(os.path.abspath(__file__)) + r"\password.txt" # Pfad zu Passwortdatei im Ordner dieses ausgeführten Python-Skripts
sender_password = open(path_to_password, "r").read() # Passwort zum Versenden der E-Mail wird aus passwort.txt ausgelesen

current_time = datetime.datetime.now().strftime("Current time: "'%Y-%m-%d %H:%M:%S') # aktueller Zeitpunkt wird aus dem Modul ,,datetime" gelesen und lesbar umformatiert
subject = f"Stonk-Alarm | {symbol} | {current_time}" # E-Mail Betreff als Formatstring, also { und } Verwendung möglich um Werte direkt darzustellen



""" Methods """

""" In der Main-Methode läuft alle 5 Minuten eine Schleife durch, die prüft, ob eine E-Mail anhand von den Aktienkursdaten gesendet werden soll oder nicht """
def main():
    """ """ """ MEHRERE SYMBOLE EINGEBEN """ """ """
    
    while 1:    # unendliche Schleife (Wert 1 bedeutet True), da der Wert auf True gesetzt ist und die Bedingung für die Schleife immer erfüllt ist
        current_stock_data = get_stock_data() # Rückgabewert der Methode ,,get_stock_data()" speichern
        compare_text = compare_data(current_stock_data)
        
        # Trigger when current price fell 1% or less since last open price
        print(datetime.datetime.now().strftime("Current time: "'%Y-%m-%d %H:%M:%S'))    # Ausgabe des Datums mit Uhrzeit in der Konsole
        print("Price Change: " + str(price_change_since_last_open_in_percent_for_printing) + "%")   # Ausgabe der Kursänderung in Prozent (mit Minuszeichen) in der Konsole
        if price_change_since_last_open_in_percent > price_difference_percent:  # wenn Kursänderung die ausgewählte Triggerschwelle übertritt, dann wird die E-Mail gesendet
            msg = format_mail(compare_text, current_stock_data)   # zu sendende Nachricht wird in der Methode ,,format_mail" mit den Parametern für den E-Mail-Text formatiert
            send_mail(msg)  # Methode zum E-Mail senden wird mit der zu sendenden Nachricht aufgerufen
        
        time.sleep(60 * 5)   # Skript um 5 Minuten bis zum nächsten Durchgang verzögern und so jede 5 Minuten erneut abzuprüfen, ob eine E-Mail gesendet werden soll


"""
In dieser Methode werden Daten zu den gewählten Aktienkursen von der Finnhub.io-API abgefragt.
Anschließend werden diese Daten lesbarer formatiert, in die gewünschte Währung mit dem Echtzeitkurs umgewandelt und in einer Datei gespeichert.
"""
def get_stock_data():
    url_finnhub = "https://finnhub.io/api/v1/"  # statischer Teil der API-URL
    url_quote = url_finnhub + f'quote?symbol={symbol}&token={api_token}'    # Symbol der Aktie und API-Tokens wird zur URL hinzugefügt
    request = requests.get(url_quote).json()    # Anfrage und Speicherung der Daten im .json-Format
    """ request =  oder requests.get(url=url_link, params=params_for_request) """
    data_of_url_quote = request # übersichtshalbe Umbenennung der Daten

    data_for_output_file = convert_data_for_output(data_of_url_quote) # Aufruf der Methode zum Konvertieren der erhaltenen Daten und Speicherung dieser in einer Variable
    
    print(data_for_output_file) # Ausgabe der konvertierten Daten in die Konsole
    return data_for_output_file # Rückgabe der konvertierten Daten


""" In dieser Methode werden die Preise der ausgewählten Aktie zum derzeitigen Moment und zur Börsenöffnung des Tages verarbeitet.
    Es wird errechnet um wie viel Prozent der derzeitige Aktienkurs vom Aktienkurs bei Börsenöffnung abweicht, dann wird abfragt, ob
    diese Abweichung größer oder gleich der vorgegebenen Triggerschwelle ,,price_difference_percent" ist und wenn die Abweichung größer oder gleich ist,
    dann wird je nach Ausfall der Abweichung ein Teil der E-Mail-Nachricht sofort generiert."""
def compare_data(current_stock_data):
        
    current_stock_price = round(current_stock_data["Current Price"], 3) # der derzeitige Aktienkurs wird auf 3 Nachkommastellen gerundet
    current_stock_open = round(current_stock_data["Open Price"], 3) # der Öffnungskurs wird auf 3 Nachkommastellen gerundet
    
    global price_change_since_last_open_in_percent, price_change_since_last_open_in_percent_for_printing    # in dieser Methode werden von den beiden Variablen die globalen Attribute/Variablen benutzt
    price_change_since_last_open_in_percent = round((current_stock_price / current_stock_open - 1) * 100, 2)    # Berechnung der Kursänderung seit Kursöffnung in Prozent und Rundung auf 2 Nachkommastellen
    price_change_since_last_open_in_percent_for_printing = price_change_since_last_open_in_percent  # Speicherung der Preisänderung in Prozent mit dem eventuellen Minuszeichen, zur Ausgabe in der Konsole
    if "-" in str(price_change_since_last_open_in_percent): # Wenn die Kursänderung negativ ist, also ein "-" enthält
        price_change_since_last_open_in_percent = float(str(price_change_since_last_open_in_percent).replace("-", ""))  # dann wird hier das "-" durch "" ersetzt, also quasi entfernt und anschließend der Wert wieder als float-Zahl gespeichert
    
    if price_change_since_last_open_in_percent >= price_difference_percent: # unterer Codeblock wird ausgeführt wenn die Preisänderung seit Öffnung größer oder gleich der ausgewählten Preisdifferenz-Triggerschwelle ist.
        if current_stock_price > current_stock_open:    # Wenn jetziger Aktienpreis höher ist als bei Börsenöffnung,
            compare_text = ("The Stock Price rose " + str(price_change_since_last_open_in_percent) + " % today")    # dann wird in ,,compare_text" der folgende String gespeichert
            
        elif current_stock_price < current_stock_open:  # Wenn jetziger Aktienpreis niedriger ist als bei Börsenöffnung,
            compare_text = ("The Stock Price fell " + str(price_change_since_last_open_in_percent).replace("-", "") + " % today")    # dann wird in ,,compare_text" der folgende String gespeichert, aber davor das Minuszeichen "-" aus dem String entfernt
        else:   # Wenn jetziger Aktienpreis gleich wie bei Börsenöffnung ist
            compare_text = ("The price didn't change today")
            
        return compare_text # Rückgabe des nun ausgewählten Teils der E-Mail-Nachricht


    
""" In dieser Methode werden die erhaltenen API-Daten schöner formatiert.
    Die Datenfelder werden einleuchtend umbenannt und mit dem aktuellen Währungskurs verrechnet."""
def convert_data_for_output(data_of_request):
    global currency_base, currency_pair # In dieser Methode werden die globalen Variablen ,,currency_base" und ,,currency_pair" verwendet
    current_currency_exchange_rate = get_current_currency_exchange_rate(currency_base, currency_pair)   # Abfrage des Echtzeit-Währungsumrechnungskurses mit Währungsbasis- und paar als Parameter
    
    # Umbenennung der Datenfelder und anschließend die Verrechnung mit dem Währungskurs
    data_of_request["Current Price"] = data_of_request.pop('c')   # Daten von Feld "c" werden im neuen Feld "Current Price" gespeichert und anschließend wird "c" quasi gelöscht
    data_of_request["Current Price"] *= current_currency_exchange_rate # Daten vom Feld "Current Price" werden mit dem Echtzeit-Währungskurs multipliziert
    data_of_request["Highest price of the day"] = data_of_request.pop('h')
    data_of_request["Highest price of the day"] *= current_currency_exchange_rate
    data_of_request["Lowest price of the day"] = data_of_request.pop('l')
    data_of_request["Lowest price of the day"] *= current_currency_exchange_rate
    data_of_request["Open Price"] = data_of_request.pop('o')
    data_of_request["Open Price"] *= current_currency_exchange_rate
    data_of_request["Previous Close Price"] = data_of_request.pop('pc')
    data_of_request["Previous Close Price"] *= current_currency_exchange_rate
    data_of_request["Unix-Timestamp"] = data_of_request.pop('t')
    return data_of_request # Rückgabe der konfigurierten Daten


""" In dieser Methode wird der Echtzeit-Währungskurs mit den zu Beginn angegebenen Attributen abgefragt und als Rückgabewert zurückgegeben """
def get_current_currency_exchange_rate(base, pair):
    r_currency = requests.get(f'https://finnhub.io/api/v1/forex/rates?base={currency_base}&token=bus50cf48v6t07kq4lug').json() # Daten zu Echtzeit-Währungskursen abfragen mit der Währungsbasis als Parameter und Umformung zu .json()
    return r_currency["quote"][pair]    # Rückgabe des gewünschten Währungskurses (z.B. USD/EUR = 0.86)


""" In dieser Methode wird die zu sendende E-Mail-Nachricht aus mehreren Teilen zusammengesetzt und zum versenden bereit gemacht """
def format_mail(compare_text, current_stock_data):
    
    # Der erste Teil der E-Mail-Nachricht   # {symbol} und {currency_pair} werden hier automatisch aus den Attributen eingesetzt, da das hier ein f-String ist.
    body = f"""\
            ==============================
            ==============================
            Stock: {symbol}
            Currency: {currency_pair}
            ==============================
            ==============================
                """
    
    # Absatz, der resultierende Text aus der Methode ,,compare_data()" und alle aktuellen Kursdaten werden dem body-String hinzugefügt und mit der Replace-Methode werden unwichtige Zeichen, wie ein "{" entfernt, da es so in der E-Mail schöner aussieht.
    body += "\n" + str(compare_text) + "\n \n \n \n \n Alle Daten: \n ============================== \n " + str(current_stock_data).replace(",", "\n").replace("{", "").replace("}", "").replace("'", "")
    
    message = MIMEMultipart() # eine MIME-Nachricht aus dem Modul/der Klasse MIMEMultipart wird erstellt
    message["Subject"] = subject    # der Betrett der E-Mail-Nachricht wird festgelegt, es wird der Text aus dem Attribut ,,subject" benutzt
    message.attach(MIMEText(body, "plain")) # Die zuvor formatierte E-Mail-Nachricht ,,body" wird an die E-Mail zu sendende angehängt
    return message  # Rückgabe der nun vorbereiteten E-Mail als Rückgabewert ,,message"


""" In dieser Methode ,,send_mail" mit dem Parameter ,,msg" wird der Mailserver als Variable benutzt und Versenden einer E-Mail vorbereitet.
    Das E-Mail-Protokoll SMTP wird hier benutzt und danach loggt sich der Mailserver mit der Methode .login(email, passwort) in die E-Mail ein.
    Anschließend wird die zuvor übergebene und fertig formatierte Email an den Empfänger gesendet und der Mailserver beendet"""
def send_mail(msg):
    mailserver = smtplib.SMTP("SMTP.office365.com",587) # SMTP-Protokoll wird ausgewählt
    mailserver.ehlo()
    mailserver.starttls()   # Wechselt das SMTP-Protokoll in den TLS-Modus
    mailserver.login(sender_email, sender_password) # Einloggen in den Mailserver mit E-Mail und Passwort
    
    mailserver.sendmail(sender_email,receiver_email, str(msg))  # Versenden der E-Mail mit Senderadresse, Empfängeradresse und der zuvor vorbereiteten E-Mail-Nachricht
    mailserver.quit()   # Beenden des genutzten Mailservers
    
    
""" Das Skript fängt hier an, jedoch die main()-Methode ganz oben
    so hat der Compiler bereits alle Zeilen von oben nach unten geladen und aus der main()-Methode heraus
    kann mit Variablen und Methoden gearbeitet werden, bei denen es egal ist, ob diese ober- oder unterhalb der Methode main() stehen """
if __name__ == "__main__":  # sobald der __main__-Konstruktor hier ankommt
    main()  # wird die Methode ,,main()" ausgeführt, die weit am Anfang des Skripts steht