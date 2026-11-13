# Ukázkové účty jsou v paměti, zatím nepoužíváme databázi.
# Restart obnoví jejich výchozí stav. Hesla slouží pouze pro místní výuku.
from models.user import User

# Složené závorky bez dvojic klíč: hodnota zde vytvářejí množinu (set).
# Pořadí argumentů: ID, jméno, příjmení, e-mail, heslo, přezdívka, role.
uzivatele = {
    User(1,"Radegast", "Modrý", "radegast.zalen@lulu.cz", "123", "radeg", "user"),
    User(2,"Radek","Hruška","hruskaradek@huhu.cz","1234", "hruska", "user"),
    User(3, "Martin", "Mlínek", "martinmlinek@kulu.cz", "12345", "mlin", "admin")
}
