
try:

    import unittest
    from ..config import create_app
    from src.models import Usuario
    from src.db.database import get_db, close_db
    from src.schema import UsuarioDao

except Exception as e:
    print('Some modules are missing {}'.format(e))


class TestUsuarioDao(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app.run(debug=True)
        self.client = self.app.test_client()
        self.db, self.c = get_db()

    def tearDown(self):
        """Executed after each test."""
        close_db()

    def test_insert(self):
        with self.app.app_context():
            user = Usuario()
            user.nombre = 'testing'
            user.email = 'test@gmail.com'
            user.fecha_nacimiento = '2003/05/05'
            user.pais = 'ecuador'
            user.ciudad = 'quito'
            user.telefono = '0987654321'
            with open('public/static/img/profile.jpg', 'rb') as file:
                user.image_perfil = file
            user.contrasena = 'password'
            user.generateEstado()
            user.generateHashId()
            user.generateHashPassword()

            user_dao = UsuarioDao(self.db, self.c)
            user_dao.insert(user)

            # Verify that the user was inserted correctly
            self.c.execute(
                "SELECT * FROM USUARIOS WHERE EMAIL = 'test@gmail.com'")
            result = self.c.fetchone()
            self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
