#!/usr/bin/python2.5
# encoding: utf-8

from subprocess import Popen, PIPE
import pprint,sys,simplejson,os,requests,time

CONFIG_LOCATION = '/Users/bob/workspace/osx-usage-stats/misc/config.json'

def localConfig():
	# use default if need be
	configName = 'misc/config.json'
	path = os.getcwd().split('/')[:-1]
	configPath = '/'.join(path)
	configFilePath = "{0}/{1}".format(configPath,configName)
	return configFilePath

def loadCfg(configFileLocation):
	config = None
	try:
		configOpen = open(configFileLocation, 'r')
		config = simplejson.load(configOpen)
		configOpen.close()
		
	except Exception,e:
		raise Exception('error loading configfile located at {0} {1}'.format(configFileLocation,e))
	return config

def getMemoryUsage():
	output = Popen(['top', '-l 1'], stdout=PIPE)
	PhysMem = output.stdout.readlines()[6].strip('\n').split(',')

	data = {
			"timestamp" : 	int(round(time.time() * 1000)),
			"data" : {
				"MEM_WIRED" : 	PhysMem[0].split(':')[1].strip().split()[0][:-1],
				"MEM_ACTIVE" :  PhysMem[1].lstrip().split()[0][:-1],
				"MEM_INACTIVE": PhysMem[2].lstrip().split()[0][:-1],
				"MEM_USED" : 	PhysMem[3].lstrip().split()[0][:-1],
				"MEM_FREE" : 	PhysMem[4].lstrip().split()[0][:-1]
		}
	}
	return data

def postToTurbine(config):
	turbine = config['turbine']
	memory = config['memory']
	sleepInterval = int(config['sleepInterval'])
	while True:
		data = getMemoryUsage()
		url = "http://{0}:{1}/db/{2}/{3}".format(turbine['host'], turbine['port'], memory['database'], memory['collection'])
		resp = requests.post(url,simplejson.dumps(data)).text
		print resp

		#sleeeep
		time.sleep(sleepInterval)

if __name__ == '__main__':
	
	# configLocation = sys.argv[1] if len(sys.argv) > 1 else localConfig()
	config = loadCfg(CONFIG_LOCATION)
	postToTurbine(config)	

