from csv import writer
from requests import post
from pyparsing import Combine, alphas, nums, SkipTo, Regex, Word, restOfLine, Suppress, ParseException


def from_json_to_csv(host: dict, keyname: str, UID: int, keys=() ):
    filename = f'{host["name"]}-{keyname}{UID}.csv'

    with open(f'{filename}', 'w', newline='') as csv_file:
        
        write_csv = writer(csv_file)
        if keys:
            write_csv.writerow(keys)
            for item in host[f"{keyname}"]:
                if item[keys[0]]:
                    write_csv.writerow([item.get(key) for key in keys])
                else:
                    return
        else:
            write_csv.writerow(host.get(f"{keyname}")[0].keys())
            for item in host[f"{keyname}"]:
                write_csv.writerow(item.values())
    
    # Write the data rows

            
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

# create list of logs from rsyslog.log and take in a sort_by parameter to sort by
def log_list(sort_by=""):

    rsyslog_logs_file = "/var/log/rsyslog.log"

    log_format = (Combine(Word(alphas + nums + '-_') + '.' + Word(alphas + nums + '-_') ) + 
              SkipTo(Regex('\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}')).suppress() + Regex('\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}') +
              Regex('\w+') + SkipTo(':') + Suppress(':') +
              restOfLine)

    log_file = []
    with open(rsyslog_logs_file, 'r') as f:
        for line in f.readlines()[::-1]:
            try:
                parsed_line = log_format.parseString(line.strip())
                # nothing to sort by
                if sort_by == "flip_timestamp" or sort_by == "":
                    log_file.append({
                        'hostname': parsed_line[2],
                        'syslogtag_pid': parsed_line[3],
                        'timestamp': parsed_line[1],
                        'log_level': parsed_line[0],
                        'log_message': parsed_line[4]
                    })
                # sort by specified host name
                elif sort_by == parsed_line[2]:
                    log_file.append({
                        'hostname': parsed_line[2],
                        'syslogtag_pid': parsed_line[3],
                        'timestamp': parsed_line[1],
                        'log_level': parsed_line[0],
                        'log_message': parsed_line[4]
                    })
                # sort by severity
                elif sort_by in parsed_line[0].split('.')[1]:
                        log_file.append({
                        'hostname': parsed_line[2],
                        'syslogtag_pid': parsed_line[3],
                        'timestamp': parsed_line[1],
                        'log_level': parsed_line[0],
                        'log_message': parsed_line[4]
                    })
            except ParseException:
                print(f"No match found for line: {line.strip()}")

    # sort by timestamp
    if sort_by == "flip_timestamp":
        sorted_file = sorted(log_file, key=lambda x: x['timestamp'], reverse=False)
        return sorted_file

    return log_file