import json

default_map = {
    "minTransactionAmountForSurcharge": "1",
    "maxTransactionAmountForSurcharge": "0",
    "type": "4",
    "value": "0",
    "minSurchargeAmount": "0",
    "maxSurchargeAmount": "0"
}

default_map_nab = {
    "minTransactionAmountForSurcharge": "1",
    "maxTransactionAmountForSurcharge": "99999999",
    "type": "4",
    "value": "0",
    "minSurchargeAmount": "0",
    "maxSurchargeAmount": "99999999"
}

query = "db.terminal.update(json1 , {$set: json2} )"

print("starting process")
f1 = open('C:/Users/YusufZ1/Downloads/nab_31082023.txt', 'r')
data_json = json.load(f1)
lst = {}
provider = "NAB"
for data in data_json:
    id = data["did"]
    query_json1 = {"_id": "100723286800", "cardProducts.cardProduct.$ind$.productId": "AMEX"}
    query_json2 = {"cardProducts.cardProduct.$ind$.surcharge": {}}
    query_json1["_id"] = id
    query_json1["cardProducts.cardProduct.$ind$.productId"] = data["productId"]

    sur_data = data["surcharge"]
    if provider == "NAB":
        default_map_nab["minTransactionAmountForSurcharge"] = sur_data["minTransactionAmountForSurcharge"] \
            if "minTransactionAmountForSurcharge" in sur_data else "1"
        default_map_nab["maxTransactionAmountForSurcharge"] = sur_data["maxTransactionAmountForSurcharge"] \
            if "maxTransactionAmountForSurcharge" in sur_data else "99999999"
        default_map_nab["type"] = sur_data["type"] \
            if "type" in sur_data else "4"
        default_map_nab["value"] = sur_data["value"] \
            if "value" in sur_data else "0"
        default_map_nab["minSurchargeAmount"] = sur_data["minSurchargeAmount"] \
            if "minSurchargeAmount" in sur_data else "0"
        default_map_nab["maxSurchargeAmount"] = sur_data["maxSurchargeAmount"] \
            if "maxSurchargeAmount" in sur_data else "99999999"
        query_json2["cardProducts.cardProduct.$ind$.surcharge"] = default_map_nab
        query1 = query.replace("json1", json.dumps(query_json1).replace("$ind$", str(data["index"]))).replace(
            "json2", json.dumps(query_json2).replace("$ind$", str(data["index"])))

    else:

        default_map["minTransactionAmountForSurcharge"] = sur_data["minTransactionAmountForSurcharge"] \
            if "minTransactionAmountForSurcharge" in sur_data else "1"
        default_map["maxTransactionAmountForSurcharge"] = sur_data["maxTransactionAmountForSurcharge"] \
            if "maxTransactionAmountForSurcharge" in sur_data else "0"
        default_map["type"] = sur_data["type"] \
            if "type" in sur_data else "4"
        default_map["value"] = sur_data["value"] \
            if "value" in sur_data else "0"
        default_map["minSurchargeAmount"] = sur_data["minSurchargeAmount"] \
            if "minSurchargeAmount" in sur_data else "0"
        default_map["maxSurchargeAmount"] = sur_data["maxSurchargeAmount"] \
            if "maxSurchargeAmount" in sur_data else "0"
        query_json2["cardProducts.cardProduct.$ind$.surcharge"] = default_map
        query1 = query.replace("json1", json.dumps(query_json1).replace("$ind$", str(data["index"]))).replace(
            "json2", json.dumps(query_json2).replace("$ind$", str(data["index"])))

    if id not in lst:
        lst[id] = []
        lst[id].append(query1)
    else:
        lst[id].append(query1)

counter = 0
lower = 1
upper = 142627
with open('C:/Users/YusufZ1/Downloads/correctionQueries_' + str(lower) + '-' + str(upper) + '.txt', 'w') as filehandle:
    for dat in lst:
        print(dat)
        counter += 1
        if lower <= counter <= upper:
            for line in lst[dat]:
                filehandle.write('%s\n' % line)
            filehandle.write('\n')
