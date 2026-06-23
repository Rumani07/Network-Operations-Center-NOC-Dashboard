from django.contrib.auth import user_logged_in
from django.http import FileResponse
from django.shortcuts import render
import json
from datetime import datetime, timedelta



def ping_dashboard(request):
    from .models import Sensing
    import requests
    import json

    
    departments = {}
    total_sensors = 0
    on_count = 0
    off_count = 0
    
    user_logged_in= False
    if request.user.is_authenticated:
        user_logged_in= True

    # Process each Sensing object and group by Type (Department)
    for sensing_obj in Sensing.objects.all():
        dept = sensing_obj.Type
        if dept not in departments:
            departments[dept] = {'id': sensing_obj.id, 'sensors': []}
            
        URL = f"http://{sensing_obj.ip}/api/table.json?content=sensors&columns=objid,device,sensor,status,lastvalue&output=json&username={sensing_obj.username}&passhash={sensing_obj.passhash}"
        try:
            response = requests.get(URL, verify=False, timeout=3.0)
            if response.status_code == 200:
                data = response.json()
                for s in data.get('sensors', []):
                    # Only include sensors saved in DB
                    if s.get('objid') in sensing_obj.SensorID:
                        status_str = s.get('status', 'Unknown')
                        is_on = status_str in ['Up', 'Warning']
                        
                        raw_val = s.get('lastvalue', '0')
                        cleaned_val = "0"
                        for char in raw_val.split():
                            if char.replace('.', '', 1).isdigit():
                                cleaned_val = char
                                break
                                
                        if is_on and float(cleaned_val) == 0.0:
                            cleaned_val = "15.0"
                            
                        sensor_data = {
                            "id": s.get('objid'),
                            "name": s.get('device', 'Unknown Device'),
                            "type": s.get('sensor', 'Ping'),
                            "status": "on" if is_on else "off",
                            "avgLatency": cleaned_val if is_on else "0",
                            "latencyHistory": []
                        }
                        departments[dept]['sensors'].append(sensor_data)
                        
                        total_sensors += 1
                        if is_on:
                            on_count += 1
                        else:
                            off_count += 1
        except Exception as e:
            print(f"Error fetching sensors for {sensing_obj.ip}: {e}")
            
    online_pct = int((on_count / total_sensors) * 100) if total_sensors > 0 else 0
    
    # Flatten all sensors for the gauge chart and javascript
    all_sensors = []
    for d in departments.values():
        all_sensors.extend(d['sensors'])
        
    context = {
        'user_logged_in': user_logged_in,
        'departments': departments,
        'sensors_json': json.dumps(all_sensors),
        'total_sensors': total_sensors,
        'on_count': on_count,
        'off_count': off_count,
        'online_pct': online_pct,
        'ErrorGettingSensorData': False,
    }
    
    from django.shortcuts import render
    return render(request, 'dashboards-analytics-NetworkRuma.html', context)
    



def sensor_graphs_view(request):
    from .fetch import get_historic_data_api, get_sensor_details

    sensor_id = request.GET.get('sensorID')
    server_id = request.GET.get('serverID')
    start_raw = request.GET.get('start')
    end_raw = request.GET.get('end')
    interval_raw = request.GET.get('interval')
    
    end_dt = datetime.now()
    start_dt = end_dt - timedelta(hours=12)
    interval_secs = 3600 # default 1 hour
    
    if start_raw:
        try:
            start_dt = datetime.strptime(start_raw, "%Y-%m-%d %H:%M")
        except:
            pass
    if end_raw:
        try:
            end_dt = datetime.strptime(end_raw, "%Y-%m-%d %H:%M")
        except:
            pass
    if interval_raw:
        try:
            interval_secs = int(interval_raw)
        except:
            pass
    from .models import Sensing
    sensing = Sensing.objects.get(id=server_id) 
    sensor_details = get_sensor_details(sensor_id,sensing.ip,sensing.username,sensing.passhash)
    sensor_details['Location'] = sensing.Site_name
    historic_data = get_historic_data_api(sensor_id, start_dt, end_dt, interval_secs,sensing.ip,sensing.username,sensing.passhash)
    
    # Process historic data for charts
    ping_data = []
    traffic_data = []
    
    for row in historic_data:
        dt_str = row.get("datetime")
        if not dt_str:
            continue
            
        # PRTG sometimes returns datetime as a range, e.g. "14-06-2026 11:30:00 - 12:30:00"
        # We take the first part for graphing
        if " - " in dt_str:
            dt_str = dt_str.split(" - ")[0]
            
        ping = row.get("Ping Time", row.get("Health", row.get("Ping", row.get("Response Time", row.get("value_raw", row.get("value"))))))
        traffic = row.get("Traffic Total", row.get("System CPU Load", row.get("Traffic In", row.get("Packet Loss", row.get("Downtime", row.get("value_raw", row.get("value")))))))
        
        # If the value is an empty string from PRTG mock, treat as 0 or ignore
        if ping == '':
            ping = 0
        if traffic == '':
            traffic = 0
            
        if ping is not None:
            try:
                ping_data.append({"x": dt_str, "y": float(ping)})
            except ValueError:
                pass
        if traffic is not None:
            try:
                traffic_data.append({"x": dt_str, "y": float(traffic)})
            except ValueError:
                pass
            
    context = {
        "sensor_id": sensor_id,
        "server_id":server_id,
        "sensor_details": sensor_details,
        "ping_data": json.dumps(ping_data),
        "traffic_data": json.dumps(traffic_data),
        "start_dt": start_dt.strftime("%Y-%m-%d %H:%M"),
        "end_dt": end_dt.strftime("%Y-%m-%d %H:%M"),
        "interval_secs": interval_secs
    }
    return render(request, 'graphs.html', context)




def sensor_csv_data(request):
    from .fetch import get_historic_data_api, get_sensor_details

    sensor_id = request.GET.get('sensorID')
    server_id = request.GET.get('serverID')
    start_raw = request.GET.get('start')
    end_raw = request.GET.get('end')
    interval_raw = request.GET.get('interval')
    
    end_dt = datetime.now()
    start_dt = end_dt - timedelta(hours=12)
    interval_secs = 3600 # default 1 hour
    
    if start_raw:
        try:
            start_dt = datetime.strptime(start_raw, "%Y-%m-%d %H:%M")
        except:
            pass
    if end_raw:
        try:
            end_dt = datetime.strptime(end_raw, "%Y-%m-%d %H:%M")
        except:
            pass
    if interval_raw:
        try:
            interval_secs = int(interval_raw)
        except:
            pass
    from .models import Sensing
    sensing = Sensing.objects.get(id=server_id) 
    sensor_details = get_sensor_details(sensor_id,sensing.ip,sensing.username,sensing.passhash)
    sensor_details['Location'] = sensing.Site_name
    historic_data = get_historic_data_api(sensor_id, start_dt, end_dt, interval_secs,sensing.ip,sensing.username,sensing.passhash)
    
    import csv
    fieldnames=["datetime","datetime_raw","value","value_raw","coverage","coverage_raw"]
    with open("data.csv","w") as f:
        writer=csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        for i in historic_data:
            writer.writerow(i)
    return FileResponse(open("data.csv", 'rb'), content_type='text/csv')

    




from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Sensing
from django.db.models import Max

@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if data.get('action') == 'logout':
                logout(request)
                return JsonResponse({'success': True})
                
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid username or password.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required(login_url='/')
def add_ip_view(request):
    return render(request, 'AddIP.html')

@csrf_exempt
@login_required(login_url='/')
def submit_add_ip(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ip = data.get('ip', '127.0.0.1')
            username = data.get('username', 'prtgadmin')
            passhash = data.get('passhash', '3657463105')
            site_name = data.get('site_name', 'Rumanikapc')
            department = data.get('department', 'localhost')
            sensors = data.get('sensors', [])
            
            # Find next ID
            max_id = Sensing.objects.aggregate(Max('id'))['id__max']
            next_id = 1 if max_id is None else max_id + 1
            
            Sensing.objects.create(
                id=next_id,
                ip=ip,
                username=username,
                passhash=passhash,
                Site_name=site_name,
                Type=department,
                SensorID=sensors
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@csrf_exempt
def get_sensors_by_ip_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'edit':
                # Edit functionality
                db_id = data.get('db_id')
                new_ip = data.get('new_ip')
                sen = Sensing.objects.get(id=db_id)
                # Attempt to fetch to verify IP is valid
                from dashboard.fetch import get_all_sensors_grouped
                sensors = get_all_sensors_grouped(new_ip, sen.username, sen.passhash)
                if sensors:
                    # Successfully fetched, save IP
                    sen.ip = new_ip
                    sen.save()
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'message': 'Could not verify PRTG credentials on new IP.'})
            else:
                ip = data.get('ip')
                if data.get('id'):
                    sen=Sensing.objects.get(id=data.get('id'))
                    username=sen.username
                    passhash=sen.passhash
                else:
                    username=data.get('username')
                    passhash=data.get('passhash')
                from dashboard.fetch import get_all_sensors_grouped
                sensors = get_all_sensors_grouped(ip, username, passhash)
                return JsonResponse({'success': True, 'sensors': sensors})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

