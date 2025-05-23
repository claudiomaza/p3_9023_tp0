from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/jardineria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#MODELOS (clientes (get), productos (herramientas get), oficinas (put), pedidos entregados y pendientes (get), endpoint para consultar (get) estado pedido y forma de pago), endpoint para obtener ciudad y telefono oficina de EEUU y españa)

class clientes(db.Model):
        CodigoCliente = db.Column(db.Integer, primary_key=True)
        NombreCliente = db.Column(db.String(50), nullable=True)
        NombreContacto = db.Column(db.String(50), nullable=True)
        ApellidoContacto = db.Column(db.String(50), nullable=True)
        Telefono = db.Column(db.String(50), nullable=True)
        Fax = db.Column(db.String(50), nullable=True)
        LineaDireccion1 = db.Column(db.String(50), nullable=True)
        LineaDireccion2 = db.Column(db.String(50), nullable=True)
        Ciudad = db.Column(db.String(50), nullable=True)
        Region = db.Column(db.String(50), nullable=True)
        Pais = db.Column(db.String(50), nullable=True)
        CodigoPostal = db.Column(db.String(50), nullable=True)
        CodigoEmpleadoRepVentas = db.Column(db.String(50), nullable=True)
        LimiteCredito = db.Column(db.Float, nullable=True)

class productos(db.Model):
        CodigoProducto = db.Column(db.Integer, primary_key=True)
        Nombre = db.Column(db.String(50), nullable=True)
        Gama = db.Column(db.String(50), nullable=True)
        Dimensiones = db.Column(db.String(50), nullable=True)
        Proveedor = db.Column(db.String(50), nullable=True)
        Descripcion = db.Column(db.String(50), nullable=True)
        CantidadEnStock = db.Column(db.Integer, nullable=True)
        PrecioVenta = db.Column(db.Float, nullable=True)
        PrecioProveedor = db.Column(db.Float, nullable=True)

class oficinas(db.Model):

        CodigoOficina = db.Column(db.String(50), primary_key=True)
        Ciudad = db.Column(db.String(50), nullable=True)
        Pais = db.Column(db.String(50), nullable=True)
        Region = db.Column(db.String(50), nullable=True)
        CodigoPostal = db.Column(db.String(50), nullable=True)
        Telefono = db.Column(db.Integer, nullable=True)
        LineaDireccion1 = db.Column(db.String(50), nullable=True)
        LineaDireccion2 = db.Column(db.String(50), nullable=True)

class pedidos(db.Model):

        CodigoPedido = db.Column(db.Integer, primary_key=True)
        FechaPedido = db.Column(db.Date, nullable=True)
        FechaEsperada = db.Column(db.Date, nullable=True)
        FechaEntrega = db.Column(db.Date, nullable=True)
        Estado = db.Column(db.String(50), nullable=True)
        Comentarios = db.Column(db.String(50), nullable=True)
        CodigoCliente = db.Column(db.Integer, db.ForeignKey('clientes.CodigoCliente'), nullable=True)

class pagos(db.Model):
       
        CodigoCliente = db.Column(db.Integer, db.ForeignKey('clientes.CodigoCliente'), primary_key=True)
        FormaPago = db.Column(db.String(50), nullable=True)
        IDTransaccion = db.Column(db.Integer, primary_key=True)
        FechaPago = db.Column(db.Date, nullable=True)
        Cantidad = db.Column(db.Float, nullable=True)

with app.app_context():
    db.create_all()

#RUTAS

@app.route('/clientes/pais/<pais>', methods=['GET'])
def get_clientes_por_pais(pais):
    clientes_list = clientes.query.filter_by(Pais=pais).all()
    result = []
    for cliente in clientes_list:
        result.append({
            'NombreCliente': cliente.NombreCliente,
        })
    return jsonify(result)

@app.route('/productos/<gama>', methods=['GET'])
def get_productos_herramientas(gama):
    productos_list = productos.query.filter_by(Gama=gama).all()
    result = []
    for producto in productos_list:
        result.append({
            'Nombre': producto.Nombre,
        })
    return jsonify(result)      

@app.route('/oficinas/', methods=['PUT'])
def update_oficinas():
    data = request.json
    nueva_oficina = oficinas(
        CodigoOficina=data['CodigoOficina'],
        Ciudad=data['Ciudad'],
        Pais=data['Pais'],
        Region=data['Region'],
        CodigoPostal=data['CodigoPostal'],
        Telefono=data['Telefono'],
        LineaDireccion1=data['LineaDireccion1'],
        LineaDireccion2=data['LineaDireccion2']
    )
    db.session.add(nueva_oficina)
    db.session.commit()
    return jsonify({"mensaje": "Oficina creada correctamente"})

@app.route('/pedidos/<estado>', methods=['GET'])
def get_pedidos_por_estado(estado):
    pedidos_list = pedidos.query.filter_by(Estado=estado).all()
    result = []
    for pedido in pedidos_list:
        result.append({
            'CodigoPedido': pedido.CodigoPedido,
            'FechaPedido': pedido.FechaPedido,
            'FechaEsperada': pedido.FechaEsperada,
            'FechaEntrega': pedido.FechaEntrega,
            'Estado': pedido.Estado,
            'Comentarios': pedido.Comentarios
        })
    return jsonify(result)

@app.route('/pedidos/estados_mediospago', methods=['GET'])
def get_estados_y_medios_pago():
    # Obtener estados únicos de pedidos
    estados = db.session.query(pedidos.Estado).distinct().all()
    estados_list = [estado[0] for estado in estados if estado[0] is not None]

    # Obtener formas de pago únicas de pagos
    medios_pago = db.session.query(pagos.FormaPago).distinct().all()
    medios_pago_list = [medio[0] for medio in medios_pago if medio[0] is not None]

    return jsonify({
        "estados_pedidos": estados_list,
        "medios_pago": medios_pago_list
    })

@app.route('/oficinas/caso6', methods=['GET'])
def get_oficinas_caso6():
    oficinas_usa_spain = oficinas.query.filter(oficinas.Pais.in_(['EEUU', 'España'])).all()
    resultado = []
    for oficina in oficinas_usa_spain:
        resultado.append({
            "Ciudad": oficina.Ciudad,
            "Telefono": oficina.Telefono,
        })
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
