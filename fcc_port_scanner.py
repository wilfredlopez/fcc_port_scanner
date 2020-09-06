import socket
# https://repl.it/repls/TeemingGaseousRecovery#main.py

# CONFIG
TIME_OUT = 5
HOST_ERROR = "Error: Invalid hostname"
IP_ERROR = 'Error: Invalid IP address'

# UTILS
ports_and_services = {
    7: 'echo',
    20: 'ftp',
    21: 'ftp',
    22: 'ssh',
    23: 'telnet',
    25: 'smtp',
    43: 'whois',
    53: 'dns',
    67: 'dhcp',
    68: 'dhcp',
    80: 'http',
    110: 'pop3',
    123: 'ntp',
    137: 'netbios',
    138: 'netbios',
    139: 'netbios',
    143: 'imap4',
    443: 'https',
    513: 'rlogin',
    540: 'uucp',
    554: 'rtsp',
    587: 'smtp',
    873: 'rsync',
    902: 'vmware',
    989: 'ftps',
    990: 'ftps',
    1194: 'openvpn',
    3306: 'mysql',
    5000: 'unpn',
    8080: 'https-proxy',
    8443: 'https-alt'
}
numbers = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}


def isNotHost(target):
    if target[-1] in numbers:
        return True
    return False


def isInvalidTarget(target: str):
    if target == None or not isinstance(target, str):
        return HOST_ERROR
    if isNotHost(target):
        return IP_ERROR
    return HOST_ERROR


def get_host_name(target):
    host_str = None
    hostipv4 = target
    try:
        hostname, _, listipv4 = socket.gethostbyaddr(target)
        hostipv4 = listipv4[0]
        host_str = hostname
        if host_str == target:
            hostipv4 = hostipv4
        host_str = host_str + " ("+hostipv4+")"
    except:
        host_str = target
    return (host_str, hostipv4)


def print_report(open_ports, host_str):
    portsservice = ''
    for p in open_ports:
        match = ports_and_services[p]
        pstr = str(p)
        totalSpace = 9 - len(pstr)
        space = " " * totalSpace
        portsservice += '\n' + pstr + space + match

    ouput = f'Open ports for {host_str}\nPORT     SERVICE'
    if portsservice != '':
        ouput += portsservice
    return ouput


### MAIN FUNCTION #######
def get_open_ports(target: str, port_range: list, Verbose=False):
    error = isInvalidTarget(target)
    port_range[-1] = port_range[-1] + 1
    open_ports = []
    host_str, hostipv4 = get_host_name(target)
    for port in range(*port_range):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIME_OUT)
        try:
            s.connect((hostipv4, port))
            open_ports.append(port)
        except Exception as ex:
            if ex.errno == 10049:
                return HOST_ERROR
            if ex.errno == 11001:
                return IP_ERROR
            if len(ex.args) > 1 and ex.args[1] == 'Name or service not known':
                return error
            continue
        except:
            continue
        finally:
            s.close()

    if Verbose:
        return print_report(open_ports, host_str)
    return(open_ports)


# print(get_open_ports("104.26.10.78", [440, 450], True))
