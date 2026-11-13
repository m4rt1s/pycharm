from flask import session


class AuthService:
    def __init__(self, uzivatele):
        self.uzivatele = uzivatele

    def najdi_uzivatele(self, email):
        for uzivatel in self.uzivatele:
            if uzivatel.email == email:
                return uzivatel

        return None

    def prihlas(self, email, heslo):
        uzivatel = self.najdi_uzivatele(email)

        if uzivatel is None:
            return None

        if uzivatel.overit_heslo(heslo):
            return uzivatel


        #dodělat ověření hesla
        return None
