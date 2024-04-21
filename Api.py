from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/carros'
mongo = PyMongo(app)

@app.route('/carros', methods=['GET'])
def get_carros():
    carros = list(mongo.db.carros.find({}, {'_id': 0}))  
    return jsonify({'carros': carros})

@app.route('/carros/<int:id>', methods=['GET'])
def get_carro_by_id(id):
    carro = mongo.db.carros.find_one({'id': id}, {'_id': 0})
    if carro:
        return jsonify({'carro': carro}), 200
    else:
        return jsonify({'message': 'Carro não encontrado'}), 404

@app.route('/carros', methods=['POST'])
def add_carro():
    data = request.get_json()
    mongo.db.carros.insert_one(data)
    return jsonify({'message': 'Carro adicionado com sucesso'}), 201

@app.route('/carros/<int:id>', methods=['PUT'])
def update_carro(id):
    data = request.get_json()
    result = mongo.db.carros.update_one({'id': id}, {'$set': data})
    if result.modified_count > 0:
        return jsonify({'message': 'Carro atualizado com sucesso'}), 200
    else:
        return jsonify({'message': 'Carro não encontrado'}), 404

@app.route('/carros/<int:id>', methods=['DELETE'])
def delete_carro(id):
    result = mongo.db.carros.delete_one({'id': id})
    if result.deleted_count > 0:
        return jsonify({'message': 'Carro deletado com sucesso'}), 200
    else:
        return jsonify({'message': 'Carro não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
