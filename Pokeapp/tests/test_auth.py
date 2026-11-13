"""Kontrola aplikace bez spouštění serveru a otevírání prohlížeče."""

import unittest
from unittest.mock import patch

from app import app
from data_uzivatel import uzivatele


class AuthTests(unittest.TestCase):
    def setUp(self):
        # Před každým testem vytvoříme nového návštěvníka s vlastními cookies.
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def login(self, identity='radeg', password='123'):
        # Nejprve načteme formulář, abychom získali jeho skutečný CSRF kód.
        self.client.get('/auth/login')
        with self.client.session_transaction() as session:
            token = session['csrf_token']
        return self.client.post('/auth/login', data={
            'identity': identity, 'password': password, 'csrf_token': token,
        })

    def test_pages_and_script(self):
        for path in ('/', '/auth/login', '/static/effects.js'):
            with self.subTest(path=path):
                with self.client.get(path) as response:
                    self.assertEqual(response.status_code, 200)

    def test_login_by_nickname_and_logout(self):
        self.assertEqual(self.login().status_code, 302)
        page = self.client.get('/').get_data(as_text=True)
        self.assertIn('Trenér radeg', page)
        self.assertIn('Odhlásit se', page)
        with self.client.session_transaction() as session:
            token = session['csrf_token']
            self.assertEqual(session['user_id'], 1)
            self.assertNotIn('password', session)
        self.assertEqual(self.client.get('/auth/logout').status_code, 405)
        self.assertEqual(self.client.post('/auth/logout', data={'csrf_token': token}).status_code, 302)
        with self.client.session_transaction() as session:
            self.assertNotIn('user_id', session)

    def test_email_is_case_insensitive(self):
        self.assertEqual(self.login(' RADEGAST.ZALEN@LULU.CZ ').status_code, 302)

    def test_invalid_credentials(self):
        cases = [
            ('radeg', 'wrong', 'Nesprávné heslo.'),
            (' RADEGAST.ZALEN@LULU.CZ ', 'wrong', 'Nesprávné heslo.'),
            ('radeg', '', 'Nesprávné heslo.'),
            ('missing', '123', 'Nesprávná přezdívka.'),
            ('missing@example.com', '123', 'Nesprávný e-mail.'),
            ('', '', 'Vyplň e-mail nebo přezdívku.'),
            ('   ', '123', 'Vyplň e-mail nebo přezdívku.'),
        ]
        for identity, password, error in cases:
            with self.subTest(identity=identity, password=password):
                response = self.login(identity, password)
                self.assertEqual(response.status_code, 401)
                self.assertIn(
                    f'<div class="alert alert-danger" role="alert">{error}</div>',
                    response.get_data(as_text=True),
                )
                with self.client.session_transaction() as session:
                    self.assertNotIn('user_id', session)

    def test_csrf_required(self):
        for path in ('/auth/login', '/auth/logout'):
            self.assertEqual(self.client.post(path, data={}).status_code, 400)

    def test_inactive_account(self):
        user = next(user for user in uzivatele if user.id == 1)
        with patch.object(user, 'je_aktivni', return_value=False):
            response = self.login()
            self.assertEqual(response.status_code, 401)
            self.assertIn('Účet není aktivní.', response.get_data(as_text=True))
            with self.client.session_transaction() as session:
                self.assertNotIn('user_id', session)

    def test_removed_account_session(self):
        user = next(user for user in uzivatele if user.id == 1)
        self.assertEqual(self.login().status_code, 302)
        original_users = set(uzivatele)
        try:
            # Napodobíme smazání účtu v době, kdy má uživatel stále session.
            uzivatele.remove(user)
            self.assertNotIn('Odhlásit se', self.client.get('/').get_data(as_text=True))
        finally:
            uzivatele.update(original_users)


if __name__ == '__main__':
    unittest.main()
