import os
import unittest
import tempfile
from app import app, db, Cupcake

class CupcakeAppTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client and a temporary database."""
        self.app = app.test_client()
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_path
        app.config['TESTING'] = True
        db.create_all()

    def tearDown(self):
        """Close the temporary database."""
        db.session.remove()
        db.drop_all()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_index(self):
        """Test the home page."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cupcake App', response.data)

    def test_add_cupcake(self):
        """Test adding a new cupcake."""
        response = self.app.post('/api/cupcakes', json={
            'flavor': 'Chocolate',
            'size': 'Medium',
            'rating': 4.5,
            'image': 'https://example.com/chocolate-cupcake.jpg'
        })
        self.assertEqual(response.status_code, 201)

        # Check if the cupcake was added to the database
        cupcake = Cupcake.query.first()
        self.assertEqual(cupcake.flavor, 'Chocolate')
        self.assertEqual(cupcake.size, 'Medium')
        self.assertEqual(cupcake.rating, 4.5)
        self.assertEqual(cupcake.image, 'https://example.com/chocolate-cupcake.jpg')

    def test_get_cupcakes(self):
        """Test getting the list of cupcakes."""
        # Add some cupcakes to the database
        cupcakes_data = [
            {'flavor': 'Vanilla', 'size': 'Small', 'rating': 4.2, 'image': 'https://example.com/vanilla.jpg'},
            {'flavor': 'Strawberry', 'size': 'Large', 'rating': 4.8, 'image': 'https://example.com/strawberry.jpg'}
        ]
        for data in cupcakes_data:
            Cupcake(**data).save_to_db()

        response = self.app.get('/api/cupcakes')
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the cupcakes added
        expected_response = {
            'cupcakes': [
                {'flavor': 'Strawberry', 'size': 'Large', 'rating': 4.8, 'image': 'https://example.com/strawberry.jpg'},
                {'flavor': 'Vanilla', 'size': 'Small', 'rating': 4.2, 'image': 'https://example.com/vanilla.jpg'}
            ]
        }
        self.assertEqual(response.get_json(), expected_response)

if __name__ == '__main__':
    unittest.main()
