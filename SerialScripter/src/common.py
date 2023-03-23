from csv import writer
from requests import post
from pyparsing import Combine, alphas, nums, SkipTo, Regex, Word, restOfLine, Suppress, ParseException
from os import path
from json import load
from datetime import datetime

def get_current_time():
    current_time = datetime.now()
    timestamp = current_time.strftime("%I:%M:%S %p")
    return timestamp

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

# return number of lines in log file
def get_log_lines(log_file: str):

    with open(log_file, 'r') as f:
        line_count = len(f.readlines())
    
    return line_count

# create list of logs from rsyslog.log from a given offset
def get_rsyslog_list(offset=slice(None, None)):

    rsyslog_logs_file = "/var/log/rsyslog.log"

    log_format = (Combine(Word(alphas + nums + '-_') + '.' + Word(alphas + nums + '-_') ) + 
              SkipTo(Regex('\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}')).suppress() + Regex('\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}') +
              SkipTo(Regex('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}')).suppress() + Regex('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}') + 
              Regex('\w+') + SkipTo(':') + Suppress(':') +
              restOfLine)
    
    log_file = []

    # open log file and grab up to 5000 lines
    with open(rsyslog_logs_file, 'r') as f:

        # read the file bottom up as newest lines will append to the end of the file
        reversed_list = f.readlines()[::-1]

        # iterate through specified lines in log file to reduce overhead 
        for line in reversed_list[offset]:
            try:

                # parse line and return list of key value pairs containing necessary field
                parsed_line = log_format.parseString(line.strip())
                # nothing to sort by
                
                log_file.append({
                    'hostname': parsed_line[3],
                    'syslogtag_pid': parsed_line[4],
                    'timestamp': parsed_line[1],
                    'IP': parsed_line[2],
                    'log_level': parsed_line[0],
                    'log_message': parsed_line[5]
                })
            
            except:
                print(f"No match found for line: {line.strip()}")

    return log_file

def filter_log_list(sort_by: str, offset=slice(None, None)):

    rsyslog_logs_file = "/var/log/rsyslog.log"

    log_format = (Combine(Word(alphas + nums + '-_') + '.' + Word(alphas + nums + '-_') ) + 
              SkipTo(Regex('\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}')).suppress() + Regex('\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}') +
              SkipTo(Regex('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}')).suppress() + Regex('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}') + 
              Regex('\w+') + SkipTo(':') + Suppress(':') +
              restOfLine)
    
    log_file = []

    # open log file and grab up to 5000 lines
    with open(rsyslog_logs_file, 'r') as f:

        # read the file bottom up as newest lines will append to the end of the file
        reversed_list = f.readlines()[::-1]

        # iterate through specified lines in log file to reduce overhead 
        for line in reversed_list[offset]:
            try:
                # parse line and return list of key value pairs containing necessary field
                parsed_line = log_format.parseString(line.strip())

                # append lines containing specified host name
                if sort_by == parsed_line[3]:
                    log_file.append({
                        'hostname': parsed_line[3],
                        'syslogtag_pid': parsed_line[4],
                        'timestamp': parsed_line[1],
                        'IP': parsed_line[2],
                        'log_level': parsed_line[0],
                        'log_message': parsed_line[5]
                    })

                # append lines containing specified severity
                elif sort_by in parsed_line[0].split('.')[1]:
                        log_file.append({
                        'hostname': parsed_line[3],
                        'syslogtag_pid': parsed_line[4],
                        'timestamp': parsed_line[1],
                        'IP': parsed_line[2],
                        'log_level': parsed_line[0],
                        'log_message': parsed_line[5]
                    })
            
            except:
                print(f"No match found for line: {line.strip()}")

def logging_serial(message: str, err_succ: bool, module: str):
    
    timestamp = get_current_time()
    # check if file exists
    if not path.exists("serial_logs.log"):
        with open("serial_logs.log", "x") as f:
            f.write(f"{timestamp} {err_succ} {module} | {message}\n")
    else:
        with open("serial_logs.log", 'a') as f:
            f.write(f"{timestamp} {err_succ} {module} | {message}\n")

def get_serial_log_list(offset=slice(None, None)):

    log_format = (Regex('\d{2}:\d{2}:\d{2}\s+\w{2}') + Word(alphas + nums + '-_') + 
                  Word(alphas + nums + '-_') + SkipTo(Regex('\w{1}')).suppress() + restOfLine)
    
    log_list = []
    with open("serial_logs.log", 'r') as f:
        reversed_log = f.readlines()[::-1]

        for line in reversed_log[offset]:
            try:
                parsed_line = log_format.parseString(line.strip())
                log_list.append({
                    "timestamp": parsed_line[0],
                    "err_succ": parsed_line[1],
                    "module": parsed_line[2],
                    "log_content": parsed_line[3]
                })
            except Exception as e:
                logging_serial(e, False, "get-logs")
    return log_list

# depending on if password has been changed or not the password will be generated
def get_password(host: dict):
    with open("config.json") as config:
        config = load(config)
        if host.get("changed_password"):
            password = config.get("configs").get("scheme") + str(int(host.get("ip").split(".")[-1])*config.get("configs").get("magic-number"))
        else:
            password = config.get("configs").get("starting-pass")

    return password