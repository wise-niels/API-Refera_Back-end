from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
import datetime as dt

app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/referaimovel'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

#data_actual = dt.datetime.strftime('%d/%m/%y')




#Criacao da Tabela Category ##################################################

class Category(db.Model):
    __tablename__= 'category'

    cat_id = db.Column (db.Integer, primary_key = True)
    cat_name = db.Column(db.String(100))


    def __init__(self, cat_name):
        self.cat_name = cat_name

class CategorySchema(ma.Schema):
    class Meta:
        fields= ('cat_id', 'cat_name')


#Para uma so resposta
category_schema = CategorySchema()

#Para muitas requisicoes/ respostas
categories_schema = CategorySchema(many=True)


###################### Criacao da Tabela Order ##########################################################

class Order(db.Model):
    __tablename__= 'order'

    order_id = db.Column (db.Integer, primary_key = True)
    order_contact_name= db.Column(db.String(100))
    order_agency_name = db.Column(db.String(100))
    order_company = db.Column(db.String(100))
    order_description = db.Column(db.String(250))
    order_deadline = db.Column(db.DateTime)
    cat_fk = db.Column(db.Integer, db.ForeignKey('category.cat_id'))


    def __init__(self,order_contact_name,order_agency_name, order_company, order_description, order_deadline, cat_fk):
        self.order_contact_name = order_contact_name
        self.order_agency_name=order_agency_name
        self.order_company=order_company
        self.order_description=order_description
        self.order_deadline=order_deadline
        self.cat_fk = cat_fk

db.create_all()

class OrderSchema(ma.Schema):
    class Meta():
        fields= ('order_id','order_contact_name', 'order_agency_name','order_company', 'order_description', 'order_deadline', 'cat_fk')



#Para uma so resposta 
order_schema = OrderSchema()

#Para muitas requisicoes/ respostas
orders_schema = OrderSchema(many=True)




# METO #############################################CRUD PARA CATEGORIA #######################################

# Endpoit to list categories

#GET -PARA OBTER TODOS
@app.route('/category', methods= ['GET'])

def get_category():
    all_categories = Category.query.all()
    result = categories_schema.dump(all_categories)
    return jsonify(result)



#GEt (OBTER DADOS DE UM NOME POR ID)

@app.route('/category/<id>',methods= ['GET'])

def get_category_id(id):
    one_category = Category.query.get(id)
    return category_schema.jsonify(one_category)



#ENDPOIT TO CREATE CATEGORY 
#POST - Metodo para adicionar na tabela do banco de dados

@app.route('/category', methods =['POST'])

def inserir_category():
    data = request.get_json(force=True)
    cat_name = data['cat_name']

    novo_registo = Category(cat_name)

    db.session.add(novo_registo)
    db.session.commit()
    return category_schema.jsonify(novo_registo)

#ENDPOINT TO UPDATE
#PUT _ Actualizar

@app.route('/category/<id>',methods = ['PUT'])


def update_catefory(id):
    actualizarcategoria= Category.query.get(id)
    data= request.get_json(force=True)
    cat_name = data['cat_name']
    

    actualizarcategoria.cat_name= cat_name
   

    db.session.commit()
    return category_schema.jsonify(actualizarcategoria)


#ENDPOPINT TO DELETE CATEGORY
#DELETE  #######################################################################

@app.route('/category/<id>',methods = ['DELETE'])

def detele_category(id):

    eliminarcategoria = Category.query.get(id)
    db.session.delete(eliminarcategoria)
    db.session.commit()
    return category_schema.jsonify(eliminarcategoria)

    
########################FINALIZANDO CRUD PARA CATEGORY ##########################################



##3###########################INICIANDO O CRUD PARA ORDER ##########################################


# Endpoit to list ORDER

#GET -PARA OBTER TODOS
@app.route('/order', methods= ['GET'])

def get_order():
    all_categories = Order.query.all()
    result = orders_schema.dump(all_categories)
    return jsonify(result)


#GEt (OBTER DADOS DE UM NOME POR ID) ####################

@app.route('/order/<id>',methods= ['GET'])

def get_order_id(id):
    one_order = Order.query.get(id)
    return order_schema.jsonify(one_order)


#ENDPOINT TO CREATE NEW ORDER

#POST - Metodo para adicionar na tabela do banco de dados

@app.route('/order', methods =['POST'])

def inserir_order():
    data = request.get_json(force=True)
    order_contact_name = data['order_contact_name']
    order_agency_name = data['order_agency_name']
    order_company = data['order_company']
    order_description = data['order_description']
    order_deadline = data['order_deadline']
    cat_fk = data['cat_fk']

    

    novo_registo =Order(order_contact_name, order_agency_name, order_company, order_description, order_deadline, cat_fk)

    db.session.add(novo_registo)
    db.session.commit()
    return category_schema.jsonify(novo_registo)


#PUT _ Actualizar

@app.route('/order/<id>',methods = ['PUT'])


def update_order(id):

    actualizarorder= Order.query.get(id)
    data= request.get_json(force=True)

    order_contact_name = data['order_contact_name']
    order_agency_name = data['order_agency_name']
    order_company = data['order_company']
    order_description = data['order_description']
    order_deadline = data['order_deadline']
    cat_fk = data['cat_fk']


    actualizarorder.order_contact_name= order_contact_name
    actualizarorder.order_agency_name= order_agency_name
    actualizarorder.order_company= order_company
    actualizarorder.order_description= order_description
    actualizarorder.order_deadline= order_deadline
    actualizarorder.cat_fk= cat_fk
  

    db.session.commit()
    return order_schema.jsonify(actualizarorder)

#ENDPOINT TO DELETE ORDER
#DELETE  #######################################

@app.route('/order/<id>',methods = ['DELETE'])

def detele_order(id):

    eliminarorder = Order.query.get(id)
    db.session.delete(eliminarorder)
    db.session.commit()
    return order_schema.jsonify(eliminarorder)



# BOAS VINDAS #######################################################

    
@app.route('/', methods=['GET'])

def index():
    return jsonify({'Mensagem':'API DA Refera'})

if __name__=="__main__":
    app.run(debug=True)