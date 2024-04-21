import json

def check(sciezka_do_pliku: str):
    try:
        with open(sciezka_do_pliku, 'r') as plik:
            dane = json.load(plik)

        if not dane:
            return "Plik JSON jest pusty."

        if not (1 <= len(dane["PolicyName"]) <= 128):
            return "Zła długość wartości (PolicyName)"

        if "PolicyDocument" in dane and "Statement" in dane["PolicyDocument"]:
            statements = dane["PolicyDocument"]["Statement"]

            if not statements:
                return "Brak instrukcji (Statement) w pliku JSON."

            first_statement = statements[0]
            resource = first_statement.get("Resource",None)
            if resource is None:
                return "Klucz 'Resource' nie został znaleziony w pierwszej instrukcji."

            # check resource
            if resource == "*":
                return False
            else:
                return True
        else:
            if not "PolicyDocument" in dane:
                return "Brak (PolicyDocument) w pliku JSON"
            else:
                return "Brak instrukcji (Statement) w pliku JSON."

    except FileNotFoundError:
       return "Plik nie został znaleziony."
    except json.decoder.JSONDecodeError:
        return "Błąd dekodowania JSON. Plik JSON ma niepoprawny format."
