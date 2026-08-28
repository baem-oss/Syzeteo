import sqlite3
import unittest

from auth import create_admin, authenticate, change_password, change_username


class AuthTest(unittest.TestCase):
    def setUp(self):
        self.conn=sqlite3.connect(':memory:')
        self.conn.row_factory=sqlite3.Row

    def tearDown(self):
        self.conn.close()

    def test_admin_login_and_changes(self):
        ok,_=create_admin(self.conn,'admin','abcdefghijkl','abcdefghijkl')
        self.assertTrue(ok)
        self.assertTrue(authenticate(self.conn,'ADMIN','abcdefghijkl')[0])
        ok,_,new_name=change_username(self.conn,'admin','abcdefghijkl','syzeteo-admin')
        self.assertTrue(ok)
        self.assertEqual(new_name,'syzeteo-admin')
        ok,_=change_password(self.conn,'syzeteo-admin','abcdefghijkl','mnopqrstuvwx','mnopqrstuvwx')
        self.assertTrue(ok)
        self.assertTrue(authenticate(self.conn,'syzeteo-admin','mnopqrstuvwx')[0])

    def test_auth_returns_language_neutral_message_keys(self):
        ok,msg=create_admin(self.conn,'a','short','short')
        self.assertFalse(ok)
        self.assertTrue(msg.startswith('auth.'))
        ok,msg=create_admin(self.conn,'admin','abcdefghijkl','abcdefghijkl')
        self.assertTrue(ok)
        self.assertEqual(msg,'auth.success.account_created')
        ok,msg,_=authenticate(self.conn,'admin','wrong')
        self.assertFalse(ok)
        self.assertEqual(msg,'auth.error.invalid_credentials')

if __name__=='__main__':
    unittest.main()
