# Network Security Scanner
## Overview
Mini Network Security Scanner is a Python-based tool for authorized network scanning and reconnaissance.
The tool resolves a given hostname or IP address, allows the user to specify ports to scan, and checks whether those ports are open or closed. It also performs basic service/banner detection and HTTP enumeration, then saves the scan results in JSON reports.
The project uses Python libraries such as argparse for command-line arguments, socket for hostname resolution and TCP connections, requests for HTTP enumeration, Logging for errors and warnings, json for generating scan reports.
I built this project to practice Python and networking concepts in a cybersecurity context, use it as a practical scanning tool in authorized environments, and develop it further through future versions. It is also intended to demonstrate my Python and cybersecurity skills as part of my portfolio.
## Features
- Target resolution
- TCP Port scanning 
- Port range validation
- Banner/service detection
- HTTP enumeration 
- Concurrent port scanning
- JSON reports 
- Logging
- Unit tests
## Technologies
- Python
- argparse
- socket
- requests
- logging
- json
- concurrent.futures
- unittest
## Installation
- Clone the repository: 
```bash
git clone https://github.com/F4Lc0n-0x/network-security-scanner
cd network-security-scanner
```
- Install the required dependency: 
```bash
pip install -r requirements.txt
```
## Usage
- Scan multiple specific ports: 
```bash
python scanner.py --target example.com --ports 22,80,443
```
- Scan range of ports: 
```bash
python scanner.py --target example.com --ports 1-100
```
- Scan a single port:
```bash
python scanner.py --target example.com --ports 22
```
## Example 
- command
```bash
python scanner.py --target scanme.nmap.org --ports 80
```
- Example for the result
```json
    {
        "target": "scanme.nmap.org",
        "ip": "45.33.32.156",
        "ports": 
        [
           {
                "port": 80,
                "status": "open",
                "banner": null,
                "http_status": 200,
                "server": "Apache/2.4.7 (Ubuntu)",
                "content_type": "text/html"
            }
        ]
    }
    ```
## Project Structure 
```text
network-security-scanner/
├── scanner.py
├── requirements.txt
├── README.md
├── .gitignore
├── reports/
│   └── .gitkeep
└── tests/
    └── test_scanner.py
```
## Testing 
The project uses python's built-in unittest framework.
Run the test suite with:
```bash
python3 -m unittest discover -s tests
```
-- The current test suite covers:
- port parsing
- Port range validation
- Invalid port input
- Target resolution
- Invalid target handling
- Open port detection
- Closed port detection
## Limitations
This project is intended as a learning-focused network scanner and is not designed to replace professional tools such as Nmap
-- Current limitations include: 
- Basic TCP connection scanning 
- Basic banner detection
- HTTP enumeration is currently limited to ports 80 and 443
- Banner detection may not work with every service
- HTTPS requests to IP addresses may fail because of TLS certificate validation
- The scanner currently focuses on IPv4 targets
- Service detection is basic and does not perform comprehensive version detection
## Authorized Use 
This tool is intended for educational purposes and authorized security testing only.
Only scan systems, networks and services that you own or have explicit permission to test.
Do not use this tool against unauthorized targets.
## Future Improvements
Planned improvements for future versions include: 
- More flexible port parsing
- Improved service and version detection
- Support for additional HTTP ports
- Better HTTPS handling
- More detailed JSON reports
- Additional unit tests
- Improved command-line options
- Better error handling
- More advanced scanning techniques
- Improved documentation and reporting