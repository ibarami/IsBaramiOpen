import configparser
from httplib2 import Http
from urllib.parse import urlencode

configExist = False
configHeartbeatUrl = ''
configLogUrl = ''


def parseConfigure():
    global configExist, configHeartbeatUrl, configLogUrl

    config = configparser.ConfigParser()
    config.read('config.ini')
    if not 'Common' in config:
        configExist = False
    else:
        configHeartbeatUrl = config['Common'].get('configLogUrl', '')
        configLogUrl = config['Common'].get('LogUrl', '')
        if configLogUrl == '' or configHeartbeatUrl == '':
            configExist = False
        else:
            configExist = True
            print("log url={0}, hb url={1}".format(configLogUrl, configHeartbeatUrl))
    print("config exist: {0}".format(configExist))
    return


def uploadHeartbeat():
    h = Http()
    if not configExist:
        return
    h.request(configHeartbeatUrl, "PUT")
    print("heartbeat sent to {0}".format(configHeartbeatUrl))
    return

def uploadErrorLog(level, str):
    h = Http()
    if not configExist:
        return
    data = {'level': level, 'data': str}
    h.request(configLogUrl, "PUT", urlencode(data))
    print("log sent to {0}".format(configLogUrl))
    return
