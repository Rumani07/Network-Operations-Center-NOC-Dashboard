import requests 
import urllib3
import time
import random
# Suppress insecure request warnings if verify=False is used
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def get_historic_data_api(sensorID, startDT, endDT, interval,PRTG_HOST,USERNAME,PASSHASH):

    prtg_s=startDT.strftime("%Y-%m-%d-%H-%M-%S")
    prtg_e=endDT.strftime("%Y-%m-%d-%H-%M-%S")
    URL = f"http://{PRTG_HOST}/api/historicdata.json?id={sensorID}&avg={interval}&sdate={prtg_s}&edate={prtg_e}&username={USERNAME}&passhash={PASSHASH}"
    try:
        response = requests.get(URL, verify=False, timeout=3.0)
        response.raise_for_status()
        data = response.json()
        return data.get('histdata', [])
    except Exception as e:
        return {f"{e}"}

def get_sensor_details(sensorID, PRTG_HOST, USERNAME, PASSHASH):

    URL = f"http://{PRTG_HOST}/api/table.json?content=sensors&columns=objid,device,sensor,status,lastvalue,location,group&filter_objid={sensorID}&output=json&username={USERNAME}&passhash={PASSHASH}"
    
    try:
        response = requests.get(URL, verify=False, timeout=3.0)
        response.raise_for_status()
        data = response.json()
        sensors = data.get('sensors', [])
        if sensors:
            s = sensors[0]
            return {
                "SensorID": s.get("objid", sensorID),
                "SensorName": s.get("sensor", "Unknown Sensor"),
                "SensorLocation": s.get("location", "Unknown Location"), 
                "RouterName": s.get("device", "Unknown Device"),
                "Status": s.get("status", "Unknown"),
                "LastPingLatency": s.get("lastvalue", "Unknown")
            }
    except Exception as e:
        print(f"Error fetching sensor details: {e}")
    
    return {
        "SensorID": sensorID,
        "SensorName": f"Sensor {sensorID}",
        "SensorLocation": "Data Center",
        "RouterName": "Core Switch",
        "Status": "Up",
        "LastPingLatency": "15 ms"
    }



from datetime import datetime, timedelta
import time



def get_all_sensors_grouped(prtgIp,UserName,PassHash):
    
    PRTG_HOST = f"http://{prtgIp}"
    USERNAME = f"{UserName}"
    PASSHASH = f"{PassHash}"
    URL = f"{PRTG_HOST}/api/table.json?content=sensors&columns=objid,device,sensor,status,lastvalue&output=json&username={USERNAME}&passhash={PASSHASH}"
    
    try:
        response = requests.get(URL, verify=False, timeout=3.0)
        response.raise_for_status()
        data = response.json()
        sensors = data.get('sensors', [])
        print("fetching done")
        grouped = {}
        for s in sensors:
            device = s.get('device', 'Unknown Device')
            if device not in grouped:
                grouped[device] = []
            grouped[device].append({
                'id': s.get('objid'),
                'name': s.get('sensor', 'Unknown Sensor'),
                'status': s.get('status', 'Unknown'),
                'lastvalue': s.get('lastvalue', '')
            })
        print("Grouping done")
        print(grouped)
        return grouped
    except Exception as e:
        print(f"Error fetching grouped sensors: {e}")
        # Return mock data if server is unreachable

