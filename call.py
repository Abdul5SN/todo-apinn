#!flask/bin/python
import subp
from flask import Flask, jsonify
import json
from flask import request, make_response
from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

call = Flask(__name__)

@auth.get_password
def get_password(username):
	if username == 'abdullah':
		return 'bull'
	return None

@auth.error_handler
def unauthorized():
	return make_response(jsonify( {'Error': 'Unauthorized access'} ),403)

@call.errorhandler(400)
def not_found(error):
	return make_response(jsonify( {'Error': 'Bad Request'} ), 400)

@call.errorhandler(404)
def not_found(error):
	return make_response(jsonify( {'Error': 'Not Found'}), 404)

#-------------------------------------Bridge--------------------------------------

#Add A Bridge
@call.route('/addbridge', methods=['POST'])
@auth.login_required
def add_bri():
	bridge = request.json['bridge']
	subp.add_bridge(bridge)
	return jsonify ({'Bridge Created': bridge,
			'Port': bridge,
			'Interface':bridge,
			'Type': 'Internal'}),201
#Show All Bridge
@call.route('/showbridge', methods=['GET'])
@auth.login_required
def show_bri():
	return subp.show_bridge()

#Delete a bridge
@call.route('/deletebridge/<bridge>', methods=['DELETE'])
@auth.login_required
def del_bri(bridge):
	subp.del_bridge(bridge)
	return jsonify({'Bridge Deleted': bridge}),201
#---------------------------Port------------------------------------------------

#Add a Port for the particular bridge
@call.route('/addport/<bridge>', methods=['POST'])
@auth.login_required
def add_port(bridge):
	port = request.json['port']
	subp.add_port(bridge,port)
	return jsonify({'Bridge': bridge,
			'Port Added': port}),201

#Show port for the particular bridge
@call.route('/showport', methods=['GET'])
@auth.login_required
def show_port():
	return subp.show_port()

#Delete a port for the particular bridge
@call.route('/deleteport/<bridge>', methods=['DELETE'])
@auth.login_required
def del_port(bridge):
	port = request.json['port']
	subp.del_port(bridge,port)
	return jsonify({'Bridge': bridge,
			'Port Deleted': port}),201

#------------------------------------------QoS----------------------------------------

#Add a qos configuration for the particular interface
@call.route('/addqos/<interface>', methods=['POST'])
@auth.login_required
def add_qos(interface):
	qos = request.json['qos']
	subp.add_qos(interface,qos)
	return jsonify({'Interface': interface,
			'QoS': qos}),201

#Update QoS configuration for the particular interface
@call.route('/updateqos/<interface>', methods=['PUT'])
@auth.login_required
def update_qos(interface):
	qos = request.json['qos']
	subp.update_qos(interface,qos)
	return jsonify({'Interface': interface,
			'QoS': qos}), 201

#Get QoS configuration for the particular interface
@call.route('/showqos/<interface>', methods=['GET'])
@auth.login_required
def get_qos(interface):
	return subp.show_qos(interface)

#Get QoS ingress_policing_rate for the interface
@call.route('/showqosrate/<interface>', methods=['GET'])
@auth.login_required
def get_qosrate(interface):
	return subp.show_qosrate(interface)

#Get QoS ingress_policing_burst for the interface
@call.route('/showqosburst/<interface>', methods=['GET'])
@auth.login_required
def get_qosburst(interface):
        return subp.show_qosburst(interface)


#Delete QoS configuration for the particular interface
@call.route('/deleteqos/<interface>', methods=['DELETE'])
@auth.login_required
def del_qos(interface):
	subp.del_qosrate(interface)
	subp.del_qosburst(interface)
	return jsonify ({"Interface": interface,
			'QoS Ingress_policing_rate': '0',
			'QoS Ingress_policing_burst': '0'}),201

#-----------------------------------SSL---------------------------------------------

#Add SSL Configuration
@call.route('/addssl', methods=['POST'])
@auth.login_required
def add_ssl():
	privatekey = request.json['Private Key']
	certificate = request.json['Certificate']
	cacert = request.json['CA Certificate']
	subp.add_ssl(privatekey,certificate,cacert)
	return jsonify ({"Private Key" : privatekey,
			"Certificate" : certificate,
			"CA Certificate" : cacert}),201

#Get SSL Configuration
@call.route('/getssl', methods=['GET'])
@auth.login_required
def get_ssl():
	return subp.get_ssl()

#Update SSL Configuration
@call.route('/updatessl', methods=['PUT'])
@auth.login_required
def update_ssl():
	privatekey = request.json['Private Key']
        certificate = request.json['Certificate']
        cacert = request.json['CA Certificate']
	subp.update_ssl(privatekey,certificate,cacert)
        return jsonify ({"Private Key" : privatekey,
                        "Certificate" : certificate,
                        "CA Certificate" : cacert}),201

#Delete SSL Configuration
@call.route('/deletessl', methods=['DELETE'])
@auth.login_required
def del_ssl():
	subp.del_ssl()
	return jsonify ({"SSL Configuration": "Cleared" }),201

#------------------------------------STP-----------------------------------------

#Add STP Configuration for Bridge
@call.route('/addstppriority/<bridge>', methods=['POST'])
@auth.login_required
def add_stpp(bridge):
	subp.en_stp(bridge)
	priority = request.json['priority']
	subp.add_stppri(bridge,priority)
	return jsonify ({'STP Enabled on bridge': bridge,
			'STP Priority': priority}),201

#Add STP Configuration for Port
@call.route('/addstpcost/<port>', methods=['POST'])
@auth.login_required
def add_stpc(port):
	cost = request.json['cost']
	subp.add_stpcost(port,cost)
	return jsonify ({'Port': port,
			'STP Cost': cost}),201


#Update STP Configuration for Bridge
@call.route('/updatestppriority/<bridge>', methods=['PUT'])
@auth.login_required
def update_stpp(bridge):
	priority = request.json['priority']
	subp.update_stppri(bridge,priority)
	return jsonify({'Bridge': bridge,
			'STP Priority Updated': priority}),201

#Update STP Configuration for Port
@call.route('/updatestpcost/<port>', methods=['PUT'])
@auth.login_required
def update_stpcost(port):
	cost = request.json['cost']
	subp.update_stpcost(port,cost)
	return jsonify({'Port': port,
			'STP Cost Updated': cost}),201

#Get STP Configuration for Bridge Priority
@call.route('/getstppriority/<bridge>', methods=['GET'])
@auth.login_required
def get_stppri(bridge):
	return subp.get_stppriority(bridge)

#Get STP Configuration for Port Cost
@call.route('/getstpcost/<port>', methods=['GET'])
@auth.login_required
def get_stpcost(port):
	return subp.get_stpcost(port)

#Delete STP Configuraton for Birdge
@call.route('/deletestppriority/<bridge>', methods=['DELETE'])
@auth.login_required
def del_stppri(bridge):
	subp.del_stpbridge(bridge)
	return jsonify({'STP Config(Priority) for Bridge': 'Cleared',
			'Bridge': bridge}),201

#Delete STP Configruation for Port
@call.route('/deletestpcost/<port>', methods=['DELETE'])
@auth.login_required
def del_stpcost(port):
	subp.del_stpport(port)
	return jsonify({'STP Config(Cost) for Port': 'Cleared',
			'Port': port}),201

#--------------------------------------------------------------------------
#Add OpenFlowVersion
@call.route('/addopenflowversion/<bridge>', methods=['POST'])
def add_openflowversion(bridge):
	protocol = request.json['protocol']
	subp.add_openflowv(bridge,protocol)
	return jsonify({'Bridge': bridge,
			'OpenFlow Version Added':protocol}),201

#Update OpenFlowVersion
@call.route('/updateopenflowversion/<bridge>', methods=['PUT'])
def update_openflowversion(bridge):
        protocol = request.json['protocol']
        subp.add_openflowv(bridge,protocol)
        return jsonify({'Bridge': bridge,
                        'OpenFlow Version Updated':protocol}),201

@call.route('/delopenflowversion/<bridge>', methods=['DELETE'])
def delete_openflowversion(bridge):
	subp.del_openflowv(bridge)
	return jsonify ({'Bridge':bridge,
			'OpenFlow  Version': 'CLEARED'}),201


@call.route('/getopenflowversion/<bridge>', methods=['GET'])
def get_openflowversion(bridge):
	return subp.get_openflowv(bridge)

if __name__ == '__main__':
	call.run(debug=True)
