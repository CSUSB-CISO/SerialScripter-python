from csv import writer
from requests import post

def from_json_to_csv(host: dict, keyname: str, UID: int):
    filename = f'{host["name"]}-{keyname}{UID}.csv'

    with open(f'{filename}', 'w', newline='') as csv_file:
        
        write_csv = writer(csv_file)
        write_csv.writerow(host.get(f"{keyname}")[0].keys())
    
    # Write the data rows
        for user in host[f"{keyname}"]:
            write_csv.writerow(user.values())
            
    return filename

def from_host_to_csv(host_list: list, UID: int):

    useful_keys = ("name", "ip", "OS", "hostname")
    filename = f'box-overview{UID}.csv'

    with open(f'{filename}', "w", newline='') as csv_file:
        write_csv = writer(csv_file)
        write_csv.writerow(useful_keys)

        for host in host_list:
            values = list()
            for key in host.keys():
                if key in useful_keys:
                    if host[key]:
                        values.append(host[key])
                    else:   
                        values.append("NULL")

            write_csv.writerow(values)
            
    return filename
            
# upload csv to web server
def upload_csv(url: str, port: str, filename: str):

    # specify url and port to go to upload endpoint of tonic server
    url = f"{url}:{port}/upload"
    files = [('file[]', open(f'{filename}', 'rb'))]
    post(url, files=files)