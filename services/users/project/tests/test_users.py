# services/users/project/tests/test_users.py


import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import User


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Tests para el servicio Users."""

    def test_users(self):
        """Asegurando que la ruta /ping  se comporta correctamente."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Asegurar que un nuevo usuario pueda ser agregado a la db."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'kevin',
                    'email': 'kevinmogollon@upeu.edu.pe'
                }),
                content_type='application/json',

            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('kevinmogollon@upeu.edu.pe ha sido agregado!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Asegurar que se produzca un error si el objeto json está vacío."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Carga invalida.', data['message'])
            self.assertIn('falló', data['status'])

    def test_add_user_invalid_json_keys(self):
        """Asegurarse si el objeto json no tiene una clave username."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'kevinmogollon@upeu.edu.pe'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Carga invalida.', data['message'])
            self.assertIn('falló', data['status'])

    def test_add_user_duplicate_email(self):
        """Asegurar que se produzca un error si el email exite."""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'kevin',
                    'email': 'kevinmogollon@upeu.edu.pe'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'kevin',
                    'email': 'kevinmogollon@upeu.edu.pe'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Lo siento. El email ya existe.', data['message'])
            self.assertIn('falló', data['status'])

    def test_single_user(self):
        """ Asegurando q el usuario individual se comporte correctamente."""
        user = add_user('kevin', 'kevinmogollon@upeu.edu.pe')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('kevin', data['data']['username'])
            self.assertIn('kevinmogollon@upeu.edu.pe', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Arrojar un error si no se proporciona una identificación."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El usuario no existe', data['message'])
            self.assertIn('fallo', data['status'])

    def test_single_user_incorrect_id(self):
        """Arrojar un error si la identificación no existe."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El usuario no existe', data['message'])
            self.assertIn('fallo', data['status'])

    def test_all_users(self):
        """ Asegurando de que todos los usuarios se comporten correctamente."""
        add_user('kevin', 'kevinmogollon@upeu.edu.pe')
        add_user('fredy', 'abelthf@gmail.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('kevin', data['data']['users'][0]['username'])
            self.assertIn(
                'kevinmogollon@upeu.edu.pe', data['data']['users'][0]['email'])
            self.assertIn('fredy', data['data']['users'][1]['username'])
            self.assertIn(
                'abelthf@gmail.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        """ La ruta principal funciona? con usuarios añadidos a la db."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Todos los usuarios', response.data)
        self.assertIn(b'<p>No hay usuarios!</p>', response.data)

    def test_main_with_users(self):
        """ La ruta principal funciona? cuando un usuario es add ."""
        add_user('kevin', 'kevinmogollon@upeu.edu.pe')
        add_user('fredy', 'abelthf@gmail.com')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Todos los usuarios', response.data)
            self.assertNotIn(b'<p>No hay usuarios!</p>', response.data)
            self.assertIn(b'kevin', response.data)
            self.assertIn(b'fredy', response.data)

    def test_main_add_users(self):
        """ Un nuevo usuario puede add a la db mediante un POST request? ."""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='kevin', email='kevinmogollon@upeu.edu.pe'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Todos los usuarios', response.data)
            self.assertNotIn(b'<p>No hay usuarios!</p>', response.data)
            self.assertIn(b'kevin', response.data)


if __name__ == '__main__':
    unittest.main()
