"""Třída User popisuje jednoho uživatele a jeho základní chování."""

from werkzeug.security import check_password_hash, generate_password_hash


class User:
    # __init__ se spustí při vytvoření uživatele pomocí User(...).
    # self označuje konkrétního uživatele, jehož údaje právě ukládáme.
    def __init__(self, id, jmeno, prijmeni, email, password, nickname, role):
        self.id = id
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.email = email
        # Ukládáme otisk hesla, nikoli čitelné heslo.
        self.password = generate_password_hash(password)
        self.nickname = nickname
        self.role = role
        # Dvojité podtržítko označuje vnitřní údaj této třídy.
        self.__aktivni = True

    def cele_jmeno(self):
        return f"{self.jmeno} {self.prijmeni}"

    def je_admin(self):
        # Porovnání vrací True (ano), nebo False (ne).
        return self.role == "admin"

    def je_aktivni(self):
        return self.__aktivni

    def deaktivovat(self):
        self.__aktivni = False

    def overit_heslo(self, password):
        # Stejný způsob ověření používá také přihlašovací stránka.
        return check_password_hash(self.password, password)
