import json, requests
url = 'https://raw.githubusercontent.com/Alnasser0/COVID19/master/SAU-geo.json'
file = requests.get(url).json()
file['features'][0]['properties']['NAME_1'] = 'Aseer'
file['features'][1]['properties']['NAME_1'] = 'Al Bahah'
file['features'][2]['properties']['NAME_1'] = 'Northern Borders'
file['features'][3]['properties']['NAME_1'] = 'Al Jawf'
file['features'][4]['properties']['NAME_1'] = 'Al Madinah Al Munawwarah'
file['features'][5]['properties']['NAME_1'] = 'Al Qaseem'
file['features'][6]['properties']['NAME_1'] = 'Ar Riyad'
file['features'][7]['properties']['NAME_1'] = 'Eastern Region'
file['features'][8]['properties']['NAME_1'] = 'Hail'
file['features'][9]['properties']['NAME_1'] = 'Jazan'
file['features'][10]['properties']['NAME_1'] = 'Makkah Al Mukarramah'
file['features'][11]['properties']['NAME_1'] = 'Najran'
file['features'][12]['properties']['NAME_1'] = 'Tabuk'
with open("SAU-geo.json", "w") as write_file:
    json.dump(file, write_file)