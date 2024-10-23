#!/usr/bin/env python3
import requests
import argparse
import time

login = ("admin", "admin")

def configure_interfaces(dest, dport, source, sport, current):
    url_serial_and_dport = f"http://{current}/config.cgi"
    params_serial_and_dport = {
        "port": "0",
        "br": "115200",
        "bc": "8",
        "parity": "1",
        "stop": "1",
        "tlp": dport,
        "trp": sport,
        "tnmode": "1",
        "multicasten": "0",
        "url1": dest,
        "srf": "1",
        "srh": "1",
    }
    response = requests.get(url_serial_and_dport, params=params_serial_and_dport, auth=login)
    url_source_networking = f"http://{current}/ip.cgi"
    octets = source.split('.')
    params_network = {
        "staticip": "1",
        "sip1": octets[0],
        "sip2": octets[1],
        "sip3": octets[2],
        "sip4": octets[3],
        "mip1": "255",
        "mip2": "255",
        "mip3": "255",
        "mip4": "0",
        "gip1": "192",
        "gip2": "168",
        "gip3": "0",
        "gip4": "1",
        "dip1": "0",
        "dip2": "0",
        "dip3": "0",
        "dip4": "0",
    }
    response = requests.get(url_source_networking, params=params_network, auth=login)
    response = requests.get(f"http://{current}/login.cgi?restart", auth=login)

def configure_rs232():
    parser = argparse.ArgumentParser(description='Configure RS232 to ETH adapters.')
    parser.add_argument(
        "-d",
        "--dest",
        type=str,
        default="192.168.0.201",
        help="Destination listener IP address to communicate to",
    )
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        default="192.168.0.7",
        help="Source IP address (ignore to leave the same as default)",
    )
    parser.add_argument(
        "-dpt",
        "--dport",
        type=str,
        default="1337",
        help="Destination listener port to communicate to",
    )
    parser.add_argument(
        "-spt",
        "--sport",
        type=str,
        default="8045",
        help="Source port",
    )
    parser.add_argument(
        "-c",
        "--current",
        type=str,
        default="192.168.0.7",
        help="Current device IP address",
    )
    args = parser.parse_args()
    configure_interfaces(args.dest, args.dport, args.source, args.sport, args.current)

if __name__ == '__main__':
    configure_rs232()
