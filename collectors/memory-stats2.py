#!/usr/bin/python2.7
# encoding: utf-8

from subprocess import Popen, PIPE
import pprint,sys,simplejson,os,requests,time

def localConfig():
	# use default if need be
	configName = 'misc/osx-usages-stats-config.json'
	path = os.getcwd().split('/')[:-1]
	configPath = '/Users/johndebovis/workspace/osx-usages-stats'
	# configPath = '/'.join(path)
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

def postToTurbine(config,data=getMemoryUsage()):
	turbine = config['turbine']
	strange = "http://{0}:{1}/{2}".format(turbine['host'], turbine['port'], turbine['path'])
	resp = requests.post(strange,simplejson.dumps(data)).text
	print resp

if __name__ == '__main__':
	
	configLocation = sys.argv[1] if len(sys.argv) > 1 else localConfig()
	config = loadCfg(configLocation)
	postToTurbine(config)

