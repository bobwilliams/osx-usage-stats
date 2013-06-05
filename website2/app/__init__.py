
from flask import Flask, request, render_template, Response, g, current_app,jsonify
import simplejson, cStringIO, gzip
from functools import wraps
import socket, requests,simplejson


def loadCfg(configFileLocation):
	config = None
	try:
		config = simplejson.load(open(configFileLocation, 'r'))

	except Exception,e:
		raise Exception('error loading configfile located at {0} {1}'.format(configFileLocation,e))

	return config

def postAppLoading(app):
	"""
		post app
	"""
	# app.conn = conn(app.config['CONFIG'])
	app.hostname = socket.gethostname()

	return app


def create_app(configFilePath):
	# create application, can not import routes until app is loaded
	app = Flask(__name__)
	app.config['CONFIG'] = loadCfg(configFilePath)



	####### ROUTES ########

	@app.route("/favicon.ico")
	def favicon():
		return app.send_static_file("favicon.ico")

	@app.route('/')
	def home():
		return render_template('home.html')

	@app.route('/memory')
	def memory():
		turbine = app.config['CONFIG']['turbine']
		memory = app.config['CONFIG']['memory']
		uri = "http://{0}:{1}/db/{2}/{3}".format( \
				turbine['host'], \
				turbine['port'], \
				memory['database'],\
				memory['collection'] \
				)

		print uri

		query = {
		 	"reduce" : [ 
					{"avg-wired" : 
						{"avg": "MEM_WIRED"} 
					}, 
					{"avg-active" : 
						{"avg": "MEM_ACTIVE"} 
					}, 
					{"avg-inactive" : 
						{"avg": "MEM_INACTIVE"}
					}, 
					{"avg-used" : 
						{"avg": "MEM_USED"}
					}, 
					{"avg-free" : 
						{"avg": "MEM_FREE"}
					} 
				]
			}
		# query = '{"group":[{"duration":"minute"}],"reduce":[{"avg-free":{"avg":"MEM_FREE"}}]}';

		url = uri + "?q=" + simplejson.dumps(query)
		req = requests.get(uri, params=)
		print req.url
		print req.text

		return jsonify({ "data" : req.text })

	##########


	# ability to add functions before and after requests

	def after_this_request(f):
		if not hasattr(g, 'after_request_callbacks'):
			g.after_request_callbacks = []
		g.after_request_callbacks.append(f)
		return f

	@app.after_request
	def call_after_request_callbacks(response):
		for callback in getattr(g, 'after_request_callbacks', ()):
			response = callback(response)
		return response

	@app.before_request
	def authen():
		pass

	@app.before_request
	def setCompression():
		"""
			http://flask.pocoo.org/mailinglist/archive/2010/6/14/gzip-compression/#13cd7c9498f74538f48d2a4e557c8148
		"""
		productionHeaders = ['User-Agent', 'X-Real-Ip', 'Host','X-Forwarded-For','Authorization']

		# if app.config['CONFIG']['productionCfg']["inProduction"]:
		# 	newDict = {}
		# 	for key,value in request.headers:
		# 		if key in productionHeaders:
		# 			if key == 'Authorization':
		# 				newDict[key] = 'u: {0} p: {1}'.format(request.authorization['username'], request.authorization['password'])
		# 			else:
		# 				newDict[key] = value
		# 	tempString = """url: {0}\nargs: {1}\nheaders: {2}"""
		# 	if socket.gethostname().find('127.0.0.1')==-1:
		# 		app.logger.warning(tempString.format(request.url,request.args,newDict ))


		@after_this_request
		def compressResponse(response):
		    # Compress the response
		    COMPRESSION_LEVEL=6
		    if response.status_code != 200 or len(response.data) < 500 or 'Content-Encoding' in response.headers:
		    	return response
		    
		    gzip_buffer = cStringIO.StringIO()
		    gzip_file = gzip.GzipFile(mode='wb', compresslevel=COMPRESSION_LEVEL, fileobj=gzip_buffer)
		    gzip_file.write(response.data)
		    gzip_file.close()
		    response.data = gzip_buffer.getvalue()
		    response.headers['Content-Encoding'] = 'gzip'
		    response.headers['Content-Length'] = str(len(response.data))
		    return response

	return postAppLoading(app)

