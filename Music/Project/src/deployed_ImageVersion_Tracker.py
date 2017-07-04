#!//usr/local/bin/python3
json_string = """
{
  "app": "mabr",
  "description": "text description",
  "service": "restj",
  "version": "0.0.14",
  "env": "testing",
  "source": "kube",
  "details":{
    "name": "restj",
    "kind": "docker",
    "registry": "ctoregprod.arrisi.com",
    "namespace": "mabrtesting",
    "label": "0.0.14",
    "metadata":{
      "digest": "",
      "id": "236f88dd6019",
      "started": "Wed, 22 Mar 2017 21:07:35 +0000",
      "labels": "app=contentrouterj",
      "restart_count":  0
    }
  },
  "age": "21d",
  "message": "build message or runtime message - optional",
  "status": "Running/Crashloop",
  "timestamp": "Fri Apr 21 13:22:59 PDT 2017"
}"""
import time
from datetime import date
from datetime import datetime
import requests
import sys,json,getopt, errno
from pprint import pprint

environment = ""
headers = {'Content-type': 'application/json'}
json_input = ""
url = 'http://10.102.255.125:8080/deploy'
headers = {'Content-type': 'application/json'}
def process_data(data):
    if data['kind'] == 'Pod':
        namespace = data['metadata']['namespace']
        mylabels = data['metadata']['labels']
        for containers in data['spec']['containers']:
            cimage = containers['image']
        for containers in data['status']['containerStatuses']:
            containerid = containers['containerID']
            image = containers['image'].split("/")
            registry = image[0]
            dockernamespace = image[1]
            component = image[2].split(":")
            label = component[1]
            imagename = component[0]
            imagesha = containers['imageID'].split("@")
            imageid=imagesha[1]
            restarts = containers['restartCount']
            containerstatus = containers['ready']
            starttime = data['status']['startTime']
            containerstatus = data['status']['phase']
            service_name = data['metadata']['name'].split("-")
            if service_name[0] in ["zookeeper", "kafka", "redis"]:
                service1 = service_name[0]
            else:
                service1 = service_name[0]+"-"+service_name[1]
    if data['kind'] == 'ReplicationController':
        namespace = data['metadata']['namespace']
        mylabels = data['metadata']['labels']
        
        for containers in data['spec']['template']['spec']['containers']:
            containerid = ""
            image = containers['image'].split("/")
            registry = image[0]
            dockernamespace = image[1]
            component = image[2].split(":")
            label = component[1]
            restarts = 0
            containerstatus = 'unknown'
            starttime = data['metadata']['creationTimestamp']
    output = json.loads(json_string)

    output["app"] = "mabr"
    output["description"] = "auto generated"
    output["service"] = service1
    output["version"] = "v1.0.0"
    output["env"] = environment
    output["source"] = "kubectl"
    output["details"]['name'] = imagename
    output["details"]['kind'] = "docker"
    output["details"]['registry'] = registry
    output["details"]['namespace'] = dockernamespace
    output["details"]['label'] = label
    output["details"]['metadata']['digest']  = imageid
    output["details"]['metadata']['started']  = starttime
    output["details"]['metadata']['labels']  = mylabels
    output["details"]['metadata']['podname'] = data['metadata']['name']
    output["details"]['metadata']['restart_count']  = restarts
    output["age"] = ""
    output["message"] = ""
    output["status"] = containerstatus 
    output["timestamp"] = datetime.now().isoformat().rpartition('.')[0]
    #pprint (output)
    data_json = json.dumps(output, separators=(',',':'))
    print(data_json)
    response = requests.post(url, data=data_json, headers=headers)

try:
    myoptions, myargs = getopt.getopt(sys.argv[1:],"e:u:j:")
except getopt.GetoptError as e:
    print (str(e))
    print("Usage: cat <json-file>| %s -e <environment>" % sys.argv[0])
    sys.exit(2)
if myoptions == []:
   print("Usage: cat <json-file>| %s -e <environment> [ -u <post-url>]" % sys.argv[0])
   print("Usage: %s -e <environment> -j <pod definition in json format> [ -u <post-url>]" % sys.argv[0])
   sys.exit(2)
for o, a in myoptions:
    if o == '-e':
        environment = a
    elif o == '-u':
        url = a
    elif o == '-j':
        json_input =a
    else:
        print("Usage: %s -s" % sys.argv[0])
        sys.exit(2)
if json_input != "":
    json_data = open (json_input,'r',encoding='utf-8')
    bulkdata = json.load(json_data)
else:
    bulkdata = json.load(sys.stdin)
if 'items' in bulkdata:
    for data in bulkdata['items']:    
        process_data(data)
else:
    process_data(bulkdata)    
