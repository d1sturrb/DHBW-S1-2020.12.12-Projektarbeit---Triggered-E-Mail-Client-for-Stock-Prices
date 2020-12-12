# DHBW-S1-2020.12.12-Projektarbeit---Triggered-E-Mail-Client-for-Stock-Prices


Ich schreibe einen E-Mail-Client welcher von der API von Finnhub.io Daten über Aktienkurse abfragt.
Das Programm fragt alle 5 Minuten Aktienkurse von vorbestimmten Aktien ab und sendet eine E-Mail an den ausgewählten Empfänger, wenn bei Ausführung des Skripts der aktuelle Preis einer Aktie im Vergleich zum Preis bei Öffnung der Börse des jeweiligen Tages um mehr als den am Anfang ausgewählten Prozentbetrag abweicht oder der Preis gleich geblieben ist.
Dies wäre dann eine durch die externe API getriggerte E-Mail an mich, damit ich eine Warnung habe und entscheiden kann, ob ich meine Aktien verkaufe oder nicht.


Zu Beginn wird in eine unendliche Schleife gesprungen, anschließend werden die Daten der zuvor gewählten Aktie abgerufen und in einer Variable gespeichert.
Anschließend werden die erhaltenen Daten in der Methode ,,compare_data" verarbeitet und geprüft, wobei ein Teil der E-Mail-Nachricht generiert wird.
Anschließend wird in der Konsole die jetzige Zeit mit dem Datum ausgegeben und auch die Preisveränderung der Aktie an diesem Tag.
Danach wird geprüft, ob die ausgerechnete Aktienpreisänderung seit Börsenöffnung die vorgegebene Schwelle übertritt oter nicht.
Ob der Aktienpreis sinkt oder steigt ist hier nicht von Relevanz, es ist lediglich der Betrag der Preisänderung wichtig.
Wenn die Schwelle übertroffen ist, dann wird die Nachricht, die in der E-Mail-Nachricht sein soll, zu einer Nachricht zusammengefügt und als Parameter in der ,,send_mail"-Methode übergeben und dann die E-Mail mit dieser Nachricht versendet.
Dieser Prozess wird je nach Voreinstellung in Minuten, jedes Mal erneut wiederholt um zu sehen, ob eine Aktienkursänderung nach der Wiederholung dann die Schwelle übertreten hat oder nicht.



Einstellungen für die Benutzung:

=> API-Token = von Alexander Biber vorgegeben (Gratis API-Key von Finnhub.io)

=> Symbol = Symbol der Aktie auf der amerikanischen Börse
    - z.B. "TSLA" steht für Tesla Inc.
    - Symbole, die bei der deutschen Börse benutzt werden, funktionieren hier nicht
    - Symbole für die Aktien der Unternehmen werden z.B. gefunden auf http://de.marketscreener.com/ , wenn der Name der Aktie eingegeben und ausgewählt wird. Rechts neben dem Namen in der Klammer
        - z.B. bei der BMW AG (BMW) ist das Symbol BMW

=> delay_for_loop_in_minutes = Gewünschter Zeitabstand in Minuten, wie oft die Kursabfrage der Aktie geschehen soll
    - z.B. 0.1  (dann wird jede 0,1 Minuten, also jede 6 Sekunden der Kurs abgefragt)
    - z.B. 5    (dann wird jede 5 Minuten der Kurs abgefragt)

=> Currency_Pair = gewünschte Währung, in der die Preise gerechnet und angezeigt werden sollen.

=> Price_difference_percent = Zahl in Prozent, wie groß die Preisabweichung sein soll damit eine E-Mail versendet wird
    - z.B. 2    (dann wird eine E-Mail erst versendet, wenn der aktuelle Kurs einer Aktie um mindestens 2 Prozent im Gegensatz zum Preis bei Börsenöffnung abweicht)



=> sender_email = E-Mail-Adresse des Versenders
    - z.B. "maxmustermann@outlook.com"
    - bei den jetzigen SMTP-Einstellungen wird der Outlook-Server von Microsoft benutzt

=> receiver_email = E-Mail-Adresse des Empfängers
    - z.B. "maxmusterfrau@outlook.com"
    - z.B. sender_email     (um die E-Mail an den Versender zu schicken)


=> in der, im selben Ordner des Skripts zu findenen, Passwort.txt-Datei einfach das Passwort für den E-Mail-Account eingeben
    z.B. passwort12_3.4