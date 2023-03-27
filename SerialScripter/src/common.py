from csv import writer
from requests import post
from pyparsing import Combine, alphas, nums, SkipTo, Regex, Word, restOfLine, Suppress, ParseException
from os import path
from json import load
from datetime import datetime
from subprocess import check_output

def get_current_time():
    current_time = datetime.now()
    timestamp = current_time.strftime("%I:%M:%S %p")
    return timestamp

def from_json_to_csv(host: dict, keyname: str, UID: int, keys=() ):

    if host.get('hostname'):
        filename = f'{host["hostname"]}-{keyname}{UID}.csv'
    else:
        filename = f'{host["name"]}-{keyname}{UID}.csv'

    with open(f'{filename}', 'w', newline='') as csv_file:
        
        write_csv = writer(csv_file)
        if keys:
            write_csv.writerow(keys)
            for item in host[keyname]:
                if item[keys[0]]:
                    write_csv.writerow([item.get(key) for key in keys])
                else:
                    return
        else:
            write_csv.writerow(host.get(keyname)[0].keys())
            write_csv.writerow(item.values() for item in host[keyname])
    
    # Write the data rows

            
    return filename

def from_host_to_csv(host_list: list, UID: int):

    useful_keys = ("ip", "OS", "hostname", "port", "service")
    filename = f'network-enumerated{UID}.csv'

    with open(f'{filename}', "w", newline='') as csv_file:
        write_csv = writer(csv_file)
        write_csv.writerow(useful_keys)

        for host in host_list:
            values = []
            for key in host.keys():
                if key in useful_keys or key == "services":
                    if key == "services":
                        if "windows" in host.get("OS").lower():
                            port = ""
                            service_name = ""
                            for item in host[key]:
                                if item.get('port') != 0:
                                    port += (f"{item.get('port')}, ")
                                    service_name += (f"{item.get('DisplayName')}, ")
                            values.append(port)
                            values.append(service_name)
                        else:
                            port = ""
                            service_name = ""
                            for item in host[key]:
                                port += (f"{item.get('port')}, ")
                                service_name += (f"{item.get('service')}, ")
                            values.append(port)
                            values.append(service_name)

                    elif key in useful_keys:
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
        reversed_list =  list(reversed(f.readlines()))

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

# filter a log file 
def filter_log_list(filename: str, filter: str, start:int, end: int, page_num: int, max: int, per_page: int, log_format, mode=0, filtered_log=[], iterate=1, in_message=False):
    
    # open log file and grab lines
    with open(filename, 'r') as f:

        # read the file 
        reversed_list = f.readlines()
        # simply reverses order of list without creating a copy
        reversed_list.reverse()

        increment = end-start

        # iterate through specified lines in log file to reduce overhead 
        for line in reversed_list[start:end]:
            if filter in line:
                if mode == 0:
                    try:
                        # parse line and return list of key value pairs containing necessary field
                        parsed_line = log_format.parseString(line.strip())

                        # append lines containing specified host name
                        if filter == parsed_line[3]:
                            filtered_log.append({
                                'hostname': parsed_line[3],
                                'syslogtag_pid': parsed_line[4],
                                'timestamp': parsed_line[1],
                                'IP': parsed_line[2],
                                'log_level': parsed_line[0],
                                'log_message': parsed_line[5]
                            })
                        # append lines containing specified severity
                        elif filter == parsed_line[0].split('.')[1]:
                            filtered_log.append({
                                'hostname': parsed_line[3],
                                'syslogtag_pid': parsed_line[4],
                                'timestamp': parsed_line[1],
                                'IP': parsed_line[2],
                                'log_level': parsed_line[0],
                                'log_message': parsed_line[5]
                            })
                        # append lines containing logged commands from remote host
                        elif filter in parsed_line[5] and in_message:
                            filtered_log.append({
                                'hostname': parsed_line[3],
                                'syslogtag_pid': parsed_line[4],
                                'timestamp': parsed_line[1],
                                'IP': parsed_line[2],
                                'log_level': parsed_line[0],
                                'log_message': parsed_line[5]
                            })
                    except Exception as e:
                        print(e)

                elif mode == 1:
                    try:
                        parsed_line = log_format.parseString(line.strip())

                        if filter == parsed_line[2]:
                            filtered_log.append({
                                "timestamp": parsed_line[0],
                                "err_succ": parsed_line[1],
                                "module": parsed_line[2],
                                "log_content": parsed_line[3]
                            })
                        elif filter in parsed_line[3]:
                            filtered_log.append({
                                "timestamp": parsed_line[0],
                                "err_succ": parsed_line[1],
                                "module": parsed_line[2],
                                "log_content": parsed_line[3]
                            })
                    except Exception as e:
                        logging_serial(e, False, "get-serial-logs")

                    except:
                        pass
        # if in the splice of log file the string doesn't exist move to next splice
        try:
            # prevent index error
            if end < max:
                # if occurrences are found but there aren't enough matches to fill up the page then continue incrementing to acquire more matches 
                if len(filtered_log) < per_page:
                    filtered_log = filter_log_list(filename, filter=filter, start=start+increment, end=end+increment, page_num=page_num, max=max, filtered_log=filtered_log, per_page=per_page, log_format=log_format, mode=mode, in_message=in_message, iterate=iterate)
                
                # if len is met, but it does not match the current page number then call the function again and clear the existing log list
                elif page_num != iterate:
                    filtered_log = filter_log_list(filename, filter=filter, start=start+increment, end=end+increment, page_num=page_num, max=max, filtered_log=[], per_page=per_page, log_format=log_format, mode=mode, in_message=in_message, iterate=iterate+1)

                # if there were no matches for given offset, increment offset and try again
                elif not filtered_log:
                    filtered_log = filter_log_list(filename, filter=filter, start=start+increment, end=end+increment, page_num=page_num, max=max, filtered_log=filtered_log, per_page=per_page, log_format=log_format, mode=mode, in_message=in_message) 
        
        # catch exception to prevent from crashing
        except Exception as e:
            print(str(e))

    return filtered_log

def get_filtered_line_count(filename: str, filter: str, index_occurred=0, mode=1):
    
    line_count = 0
    with open(filename, 'r') as f:

        for line in f.readlines():
            # mode 1 is looking for filter in severity
            if mode == 1 and filter in line.split('.')[index_occurred]:
                line_count += 1
            # mode 2 is looking for filter occurrence throughout line
            elif filter in line and mode == 2:
                line_count +=1
            
            # mode 3 is for serial logs
            if mode == 3:
                if filter in line.split()[index_occurred]:
                    line_count += 1
        
    return line_count

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
        reversed_log = f.readlines()
        reversed_log.reverse()

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
                logging_serial(e, False, "get-serial-logs")
    return log_list



# depending on if password has been changed or not the password will be generated
def get_password(host: dict):
    with open("config.json") as config:
        config = load(config)
        if host.get("isChanged") :
            password = config.get("configs").get("scheme") + str(int(host.get("ip").split(".")[-1])*config.get("configs").get("magic-number"))
        else:
            password = config.get("configs").get("starting-pass")

    return password