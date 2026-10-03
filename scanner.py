import socket
import argparse
import requests
import json
import datetime
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
import logging
import errno
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
def resolve_target(target) :
    try :
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        logging.error("INVALID HOST NAME!")
        return None
def http_enum(ip , port):
    if port == 80:
        scheme = "http"
    elif port == 443:
        scheme = "https"
    else:
        return None
    url = f"{scheme}://{ip}:{port}"
    try:
        response = requests.get(url , timeout=2)
        return response
    except requests.RequestException:
        logging.warning("HTTP request failed!")
        return None
def grab_banner(sock):
    banner = None
    try : 
        data = sock.recv(1024)
        if data == b'':
            logging.info("No banner received!")
        else:
            banner = data.decode()
            logging.info("Banner : %s",banner)
    except UnicodeDecodeError:
        logging.warning("Banner could not be decoded as text!")
    except socket.timeout:
        logging.warning("Banner connection timeout!")
    return banner
def scan_port(ip , port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(4)
    try:
        connection_result = sock.connect_ex((ip , port))
        if connection_result == 0 :
            port_info = {"port": port, "status": "open", "banner": None, "http_status": None, "server": None,"content_type" : None}
            if port == 80 or port == 443:
                response = http_enum(ip, port)
                if response:
                    logging.info("Status : %s",response.status_code)
                    logging.info("Server : %s",response.headers.get('Server' , 'Not disclosed'))
                    logging.info("Content Type : %s",response.headers.get('Content-Type' , 'Not disclosed'))
                    port_info["http_status"] = response.status_code
                    port_info["server"] = response.headers.get('Server' , 'Not disclosed')
                    port_info["content_type"] = response.headers.get('Content-Type' , 'Not disclosed')
            else:
                banner = grab_banner(sock)
                port_info["banner"] = banner
            result = port_info
        elif connection_result == errno.ECONNREFUSED:
            result = {
                "port" : port,
                "status" : "closed",
                "banner" : None,
                "http_status" : None,
                "server" : None,
                "content_type" : None
            }
        else:
            logging.error(connection_result)
            result = {
                "port" : port,
                "status" : "error",
                "banner" : None,
                "http_status" : None,
                "server" : None,
                "content_type" : None
            }
    except socket.timeout:
        logging.warning("Connection timeout!")
        result = {"port" : port , "status" : "timeout", "banner": None, "http_status": None, "server": None, "content_type" : None}
    finally:
        sock.close()
    return result
def parse_ports(ports_str):
    if "-" in ports_str:
        ports = ports_str.split("-")
        if len(ports) != 2:
            logging.error("Invalid port format! Use start-end, example: 1-100")
            return
        try: 
            start = int(ports[0])
            end = int(ports[1])
        except ValueError :
            logging.error("Invalid ports - must be numbers")
            return
        if start < 1 or start > 65535 or end < 1 or end > 65535:
            logging.error("Ports must be between 1 and 65535!")
            return
        if start > end:
            logging.error("The start port must be less than the end port!")
            return
        ports_for_scan = range(start , end+1)
    elif "," in ports_str:
        try :
            ports_for_scan = [int(port) for port in ports_str.split(",")]
        except ValueError :
            logging.error("Invalid ports - must be numbers")
            return
        for port in ports_for_scan:
            if port < 1 or port > 65535:
                logging.error("Ports must be between 1 and 65535!")
                return
    else:
        try :
            ports_for_scan = [int(ports_str)]
        except ValueError :
            logging.error("Invalid ports - must be numbers")
            return
        if ports_for_scan[0] < 1 or ports_for_scan[0] > 65535:
            logging.error("Ports must be between 1 and 65535!")
            return
    return ports_for_scan
def main():
    parser = argparse.ArgumentParser(description="--HOST NAME SCANNER--")
    parser.add_argument("--target",help="--target HOST NAME (example.com)--", type=str , required= True)
    parser.add_argument("--ports",help="--PORTS to test(--ports 1-100)--", type=str , required=True)
    args = parser.parse_args()
    ip = resolve_target(args.target)
    if not ip:
        return
    logging.info("The IP of the host is : %s",ip)
    port_list = parse_ports(args.ports)
    t = datetime.datetime.now()
    time = t.strftime("%Y-%m-%d | %H:%M:%S")
    if port_list:
        result = {
            "target" : args.target,
            "ip" : ip,
            "ports" : [],
            "timestamp" : time
        }
        with ThreadPoolExecutor(max_workers=20) as ex:
            scanning = list(ex.map(scan_port , repeat(ip) , port_list))
        result["ports"].extend(scanning)
        filename = f"reports/scan_{args.target}_{t.strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename,"w") as file:
            json.dump(result, file , indent=4)
if __name__ == "__main__":
    main()