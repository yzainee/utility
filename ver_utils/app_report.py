import json
import csv
import time

def manish_fun():
    input_csv_file = open(r"C:\Users\yusufz1\Downloads\allApps24hours.csv",'r')
    lines = input_csv_file.readlines()
    fields = ['serial', 'appLabel', 'appName', 'fgMs', 'fgMm', 'model', 'os', 'evdate', 'tag']
    unwanted = ["Android System", "Base Control", "Camera", "Files", "InstallPolicyUI", "Launcher3", "Media Storage", "ModemConfig", "Package installer", 
        "PeripheralsService", "Quickstep", "Screen Saver", "Settings", "Setup", "Shift Totals", "Verifone Update Service", "VhqConfig"]
    final_data = []
    line_num = 0
    for line in lines:
        insertFlag = True
        if line_num == 0:
            line_num = line_num + 1            
            continue
        sr_num =  line.split('""Host"":""')[1].split('"",')[0]
        line = line.split('VLS_DataDictionary: ')[1].split('"""')[0]
        json_text = line.replace('\\', "").replace('""', '"')
        json_data = json.loads(json_text)
        
        wanted_data={
            "serial": sr_num
        }       
        for key in json_data:            
            if key in fields:
                wanted_data[key] = json_data[key]
                if key == "fgMs":
                    wanted_data["fgMm"] = round(json_data["fgMs"]/60000)
                if key == "appLabel" and json_data[key] in unwanted:
                        insertFlag = False
            elif key == "appData":
                app_data = json_data["appData"][0]
                for app_key in app_data:
                    if app_key == "fgMs":
                        wanted_data["fgMm"] = round(app_data["fgMs"]/60000)
                    if app_key == "appLabel" and app_data[app_key] in unwanted:
                        insertFlag = False
                    wanted_data[app_key] = app_data[app_key]
        if insertFlag:
            final_data.append(wanted_data)
    
    with open('C:/Users/YusufZ1/Downloads/required_fields_appusage_report_generated.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fields)            
        writer.writeheader()            
        writer.writerows(final_data) 

if __name__ == "__main__":
    start = time.process_time()
    print("Jo chacha hai wo hi bhatija hai.....")
    manish_fun()
    print(time.process_time() - start)
    print("Jo bhatija hai wo hi chacha hai.....")
