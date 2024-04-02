import json
import time
import pandas as pd

def manish_fun():
    input_csv_file = open(r"C:\Users\yusufz1\Downloads\data\12212.csv",'r')
    lines = input_csv_file.readlines()

    sponsor_ids = []

    for line in lines:
        if '""Sponsor"":""' in line:
            id = line.split('""Sponsor"":""')[1].split('""}')[0]
            sponsor_ids.append(id)
    print("Number of sponsor Ids from file 12212.csv: " + str(len(sponsor_ids)))

    input_csv_file = open(r"C:\Users\yusufz1\Downloads\data\12223.csv",'r')
    lines = input_csv_file.readlines()

    sponsor_ids2 = []
    for line in lines:
        if '""Sponsor"":""' in line:
            id = line.split('""Sponsor"":""')[1].split('""}')[0]
            sponsor_ids2.append(id)
    print("Number of sponsor Ids from file 12223.csv: " + str(len(sponsor_ids2)))

    total_ids = sponsor_ids + sponsor_ids2
    print("Total number of Ids: " + str(len(total_ids)))
    total_ids = list(set(total_ids))
    print("Total unique Ids: " + str(len(total_ids)))

    df = pd.DataFrame(total_ids)
    df.columns = ['Sponsor Id']
    df.to_excel('C:/Users/YusufZ1/Downloads/data/unique_sponsor_ids.xlsx', sheet_name='sponsorIds', index=False)
    #writer.save()


    

if __name__ == "__main__":
    start = time.process_time()
    print("Jo chacha hai wo hi bhatija hai.....")
    manish_fun()
    print("Execution Time: " + str(time.process_time() - start))
    print("Jo bhatija hai wo hi chacha hai.....")