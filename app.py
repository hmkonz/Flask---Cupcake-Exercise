"""Flask app for Cupcakes"""

from flask import Flask, request, render_template,  redirect, session, jsonify

from models import db,  connect_db, Cupcake


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret-key"

app.app_context().push()


connect_db(app)


@app.route('/')
def homepage():
    """Renders html template with some JS - Not part of JSON API"""
    
    return render_template('homepage.html')

##############################################################################
# Restful Cupcakes JSON API
##############################################################################

@app.route('/api/cupcakes')
def list_cupcakes():
    """ Returns all cupcakes in database
    
    Returns JSON like:
    {cupcakes: [{id, flavor, size, rating, image}, ... ]}"""


    all_cupcakes=[cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


@app.route('/api/cupcakes', methods = ["POST"])
def create_cupcake():
    """ Creates a new cupcake and returns information in JSON about that newly created cupcake like:

    {cupcake: [{id, flavor, size,rating, image}]"""


    new_cupcake=Cupcake(
        flavor=request.json['flavor'], 
        size=request.json['size'], 
        rating=request.json['rating'], 
        image = request.json['image'])

    db.session.add(new_cupcake)
    db.session.commit()

    response_json=jsonify(cupcake=new_cupcake.serialize())

    #POST requests should return HTTP status code of 201 CREATED
    return (response_json, 201)


@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """ Returns data for one specific cupcake.
    
    Returns JSON like:
    {cupcake: [{id, flavor, size, rating, image}]}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify (cupcake=cupcake.serialize())




@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    """ Updates a particular cupcake and responds with JSON of updated cupcake like:
    
    {cupcake: [{id, flavor, size, rating, image}]
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor=request.json.get('flavor', cupcake.flavor)
    cupcake.size=request.json.get('size', cupcake.size)
    cupcake.rating=request.json.get('rating', cupcake.rating)
    cupcake.image=request.json.get('image', cupcake.image)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify (cupcake=cupcake.serialize())



@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Deletes a particular cupcake and returns a confirmation message
    
    Returns JSON of {message: 'Deleted'}"""

    cupcake=Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message='Deleted')