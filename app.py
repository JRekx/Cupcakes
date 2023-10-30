from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

@app.route("/")
def root():
    """Homepage - Renders the index.html template."""
    return render_template("index.html")

@app.route("/api/cupcakes")
def list_cupcakes():
    """Returns a list of all cupcakes in the database."""
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Creates a new cupcake and adds it to the database."""
    data = request.json

    cupcake = Cupcake(
        image=data.get('image', None),
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating']
    )

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict()), 201

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Returns details of a specific cupcake by ID."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Updates details of a specific cupcake by ID."""
    data = request.json
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.image = data.get('image', cupcake.image)
    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)

    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    """Deletes a specific cupcake by ID."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="DELETED")
