from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carros.db'
db = SQLAlchemy(app)

class Carro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    transmission = db.Column(db.String(50), nullable=False)
    mileage = db.Column(db.Float, nullable=False)
    fueltype = db.Column(db.String(50), nullable=False)
    tax = db.Column(db.Float, nullable=False)
    mpg = db.Column(db.Float, nullable=False)
    enginesize = db.Column(db.Float, nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)

def criar_tabelas():
    with app.app_context():
        db.create_all()

@app.cli.command()
def init_db():
    criar_tabelas()

@app.route('/carros', methods=['GET'])
def get_carros():
    carros = Carro.query.all()
    output = []
    for carro in carros:
        carro_data = {}
        carro_data['id'] = carro.id
        carro_data['model'] = carro.model
        carro_data['year'] = carro.year
        carro_data['price'] = carro.price
        carro_data['transmission'] = carro.transmission
        carro_data['mileage'] = carro.mileage
        carro_data['fueltype'] = carro.fueltype
        carro_data['tax'] = carro.tax
        carro_data['mpg'] = carro.mpg
        carro_data['enginesize'] = carro.enginesize
        carro_data['manufacturer'] = carro.manufacturer
        output.append(carro_data)
    return jsonify({'carros': output})

@app.route('/carros/<int:id>', methods=['GET'])
def get_carro_by_id(id):
    carro = Carro.query.get_or_404(id)
    carro_data = {
        'id': carro.id,
        'model': carro.model,
        'year': carro.year,
        'price': carro.price,
        'transmission': carro.transmission,
        'mileage': carro.mileage,
        'fueltype': carro.fueltype,
        'tax': carro.tax,
        'mpg': carro.mpg,
        'enginesize': carro.enginesize,
        'manufacturer': carro.manufacturer
    }
    return jsonify({'carro': carro_data})

@app.route('/carros', methods=['POST'])
def add_carro():
    data = request.get_json()
    novo_carro = Carro(model=data['model'], year=data['year'], price=data['price'], transmission=data['transmission'], mileage=data['mileage'], fueltype=data['fueltype'], tax=data['tax'], mpg=data['mpg'], enginesize=data['enginesize'], manufacturer=data['manufacturer'])
    db.session.add(novo_carro)
    db.session.commit()
    return jsonify({'message': 'Carro adicionado com sucesso'})

@app.route('/carros/<int:id>', methods=['PUT'])
def update_carro(id):
    carro = Carro.query.get_or_404(id)
    data = request.get_json()
    carro.model = data['model']
    carro.year = data['year']
    carro.price = data['price']
    carro.transmission = data['transmission']
    carro.mileage = data['mileage']
    carro.fueltype = data['fueltype']
    carro.tax = data['tax']
    carro.mpg = data['mpg']
    carro.enginesize = data['enginesize']
    carro.manufacturer = data['manufacturer']
    db.session.commit()
    return jsonify({'message': 'Carro atualizado com sucesso'})

@app.route('/carros/<int:id>', methods=['DELETE'])
def delete_carro(id):
    carro = Carro.query.get_or_404(id)
    db.session.delete(carro)
    db.session.commit()
    return jsonify({'message': 'Carro deletado com sucesso'})

if __name__ == '__main__':
    app.run(debug=True)
