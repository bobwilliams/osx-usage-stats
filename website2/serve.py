from app import create_app
from flask import Config,current_app
import os,sys,simplejson

configName = 'config.json'
configFilePath = "{0}/{1}".format(os.getcwd(),configName)

if len(sys.argv)>1:
	configFilePath = sys.argv[1]

app = create_app(configFilePath)

# run app on different host if on linux server vs mac
if len(os.listdir('/home'))>0:
	app.run(host="0.0.0.0",debug=False)
else:
	app.run(port=5000,debug=True)
