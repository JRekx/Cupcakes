from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE = "https://www.freepik.com/free-vector/cute-cat-cupcake-cartoon-vector-icon-illustration-animal-food-icon-concept-isolated-premium-vector-flat-cartoon-style_18305543.htm#query=cartoon%20cupcake&position=3&from_view=keyword&track=ais"

class Cupcake(db.Model):
    """Cupcake model representing the 'cupcakes' table in the database."""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE)
    rating = db.Column(db.Float, nullable=False, default=0.0)

    def to_dict(self):
        """Converts Cupcake object to a dictionary."""
        return {
            "id": self.id,
            "image": self.image,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
        }

def connect_db(app):
    """Connects the database to the Flask app."""
    db.app = app
    db.init_app(app)
