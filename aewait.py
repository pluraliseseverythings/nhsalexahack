def waiting_patients(hosp_simp):
    with urllib.request.urlopen("https://ae-waits.herokuapp.com") as url:
        data = json.loads(url.read().decode())
        for items in data:
            items['hosp_simp']=items['hospital'].split(' (')[0]
            if hosp_simp in items['hosp_simp']:
                if items['is_open']=='false':
                    return('This hospital is closed')
                else:
                    return('There are currently '+items['current_patients']+' patients waiting at '+hosp_simp)
