#!/usr/bin/python2.7
# encoding: utf-8

from subprocess import Popen, PIPE
import pprint,sys,simplejson,os,requests,time,re

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
	# http://apple.stackexchange.com/questions/4286/is-there-a-mac-os-x-terminal-version-of-the-free-command-in-linux-systems
	
	# Get process info
	ps = Popen(['ps', '-caxm', '-orss,comm'], stdout=PIPE).communicate()[0]
	vm = Popen(['vm_stat'], stdout=PIPE).communicate()[0]

	# Iterate processes
	processLines = ps.split('\n')
	sep = re.compile('[\s]+')
	rssTotal = 0 # kB
	for row in range(1,len(processLines)):
	    rowText = processLines[row].strip()
	    rowElements = sep.split(rowText)
	    try:
	        rss = float(rowElements[0]) * 1024
	    except:
	        rss = 0 # ignore...
	    rssTotal += rss

	# Process vm_stat
	vmLines = vm.split('\n')
	sep = re.compile(':[\s]+')
	vmStats = {}
	for row in range(1,len(vmLines)-2):
	    rowText = vmLines[row].strip()
	    rowElements = sep.split(rowText)
	    vmStats[(rowElements[0])] = int(rowElements[1].strip('\.')) * 4096

	memWired = float(vmStats["Pages wired down"]/1024/1024)
	memActive = float(vmStats["Pages active"]/1024/1024)
	memInactive = float(vmStats["Pages inactive"]/1024/1024)
	memFree = float(vmStats["Pages free"]/1024/1024)

	data = {
			"timestamp" : 	int(round(time.time() * 1000)),
			"data" : {
				"MEM_WIRED" 		:	memWired,
				"MEM_ACTIVE" 		: memActive,
				"MEM_INACTIVE"	:	memInactive,
				"MEM_USED" 			:	memWired + memActive + memInactive,
				"MEM_FREE" 			:	memFree
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
		print url
		print data
		print resp

		#sleeeep
		time.sleep(sleepInterval)

if __name__ == '__main__':
	
	# configLocation = sys.argv[1] if len(sys.argv) > 1 else localConfig()
	config = loadCfg(CONFIG_LOCATION)
	postToTurbine(config)	

