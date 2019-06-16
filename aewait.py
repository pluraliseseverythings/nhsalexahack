import json, urllib.request

def wait_time(hosp_simp):
    with urllib.request.urlopen("https://ae-waits.herokuapp.com") as url:
        data = json.loads(url.read().decode())
        for items in data:
            items['hosp_simp']=items['hospital'].split(' (')[0]
            if hosp_simp in items['hosp_simp']:
                if items['is_open']=='false':
                    print('This hospital is closed')
                else:
                    print('The waiting time at '+hosp_simp+' is up to '+items['waiting_time'])