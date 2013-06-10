try:
    import json
except ImportError:
    import simplejson as json 

import time,urllib2,urllib,logging

CONFIG_LOCATION = "/Users/bob/workspace/osx-usage-stats/misc/config.json"


def loadCfg(configFileLocation):
    config = None
    try:
        configOpen = open(configFileLocation, 'r')
        config = json.load(configOpen)
        configOpen.close()
        
    except Exception,e:
        print e
        raise Exception("error loading configfile located at " + configFileLocation )
    return config

def post(env):
    try:
        post_turbine(env)

    except Exception:
        import traceback
        logging.error('generic exception in posting to turbine: ' + traceback.format_exc())

def post_turbine(env):
    """ posts our event data to turbinedb """

    config = loadCfg(CONFIG_LOCATION)
    turbine = config['turbine']
    notifications = config['notification']

    # boiler plate build for REST call
    url =   "http://" + \
            turbine['host'] + \
            ":" + turbine['port'] + \
            "/db/" + notifications['database'] + \
            "/" + notifications['collection']
    
    # print url
    # url = 'http://localhost:8080/db/macbookair/nsworkspace'
    headers = {"Content-Type": "application/json"}

    # build data to pass
    data = {
        "timestamp" : int(time.time()*1000),
        "data"  : {}
        }
    # loop through for nested data
    for k in env:
        data['data'][k] = env[k]

    dataNew = json.dumps(data)

    # echo the Request
    print url
    print dataNew

    # build request
    req = urllib2.Request(url, dataNew, headers)

    # make the call
    try: 
         f = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        logging.error('HTTPError = ' + str(e.code))
    except urllib2.URLError, e:
        logging.error('URLError = ' + str(e.reason))
    except httplib.HTTPException, e:
        logging.error('HTTPException')
    except Exception:
        import traceback
        logging.error('generic exception: ' + traceback.format_exc())

    res = f.read()
    f.close()

    # echo the response
    print res 

