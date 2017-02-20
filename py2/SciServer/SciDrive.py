import json
from io import StringIO

import requests

from SciServer import Config, Authentication


def createContainer(path, token=""):
    if (token == ""):
        userToken = Authentication.getToken()
    else:
        userToken = token;

    containerBody = ('<vos:node xmlns:xsi="http://www.w3.org/2001/thisSchema-instance" '
                     'xsi:type="vos:ContainerNode" xmlns:vos="http://www.ivoa.net/xml/VOSpace/v2.0" '
                     'uri="vos://' + Config.SciDriveHost + '!vospace/' + path + '">'
                                                                                '<vos:properties/><vos:accepts/><vos:provides/><vos:capabilities/>'
                                                                                '</vos:node>')
    url = Config.SciDriveHost + '/vospace-2.0/nodes/' + path
    data = str.encode(containerBody)
    headers = {'X-Auth-Token': userToken, 'Content-Type': 'application/xml'}
    try:
        res = requests.put(url, data=data, headers=headers)
        if res.status_code != 200:
            raise Exception("Http Response returned status code " + str(res.status_code) + ":\n" + res.content.decode());

    except Exception as error:
        if (Config.executeMode == "debug"):
            print error, error.read().decode()
        raise


def upload(path, data, token=""):
    if (token == ""):
        userToken = Authentication.getToken()
    else:
        userToken = token;

    url = Config.SciDriveHost + '/vospace-2.0/1/files_put/dropbox/' + path
    data = data
    headers = {'X-Auth-Token': userToken}
    try:
        res = requests.put(url, data=data, headers=headers)
        if res.status_code != 200:
            raise Exception("Http Response returned status code " + str(res.status_code) + ":\n" + res.content.decode());

        if (Config.executeMode == "debug"):
            print(res.content.decode())
    except Exception as error:
        if (Config.executeMode == "debug"):
            print error, error.read().decode()
        raise error

def publicUrl(path, token):
    """
    retrieve public URL for file identified by path
    """
    if (token == ""):
        userToken = Authentication.getToken()
    else:
        userToken = token;

    url = Config.SciDriveHost + '/vospace-2.0/1/media/sandbox/' + path
    headers={'X-Auth-Token': userToken}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            raise Exception("Http Response returned status code " + str(res.status_code) + ":\n" + res.content.decode());

        jsonRes = json.loads(res.content.decode())
        fileUrl = jsonRes["url"]
        return fileUrl

    except Exception as error:
        if (Config.executeMode == "debug"):
            print error, error.read().decode()
        raise error

def download(path, token=""):
    """
    Download the file identified by the path as a read()-able stream.
    I.e. to get contents call read() on the resulting object
    """
    fileUrl=publicUrl(path,token)
    try:
        res = requests.get(fileUrl,stream=True)
        if res.status_code != 200:
            raise Exception("Http Response returned status code " + str(res.status_code) + ":\n" + res.content.decode());

        return StringIO(res.content.decode())
    except Exception as error:
        if (Config.executeMode == "debug"):
            print error, error.read().decode()
        raise error
  