# IntelX-Leak-Finder
* Extract credentials from IntelX leaks with smart parsing and JSON output 
* IntelX credential leak parser with URL-aware extraction 
* SOC-focused IntelX credential extractor


## What this tool does:

This tool searches IntelX for leaked data related to a specific domain and extracts credentials from raw leak files. 

Username and password types inside the IntelX leak file:

• URL + username + password

• Email + password

• Phone + password

• Username + password

• Space-separated credentials

• Pipe-separated formats

• CSV-like formats


## Features

• IntelX search automation

• Polling for result readiness

• Credential parsing

• URL extraction

• Deduplication

• Date range filtering

• JSON output


P.S.
This tool specifically targets the IntelX bucket "leaks.private.general", that means only Identity Portal or Enterprise accounts can use this tool. which aggregates private breach material, leaked credentials, and compromised account data relevant for threat intelligence and incident response workflows.

<img width="201" height="360" alt="Screenshot from 2026-01-13 15-32-52" src="https://github.com/user-attachments/assets/e3d7cf4f-27d5-42d3-b830-796cefeb7e70" />

## Requirements

• Python 3.10 or higher

• requests library

• An active IntelX API key (Identity Portal or Enterprise)

• Internet access (for IntelX API calls)


## Installation

1. Clone the repository:
```bash
https://github.com/h4nt3r039/IntelX-Leak-Finder
cd IntelX-Leak-Finder
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip3 install requests
```

## Usage 
```bash
python3 intelx_leaks.py -h
usage: intelx_leaks.py [-h] --from DATE_FROM --to DATE_TO domain

IntelX Leak Finder (JSON output)

positional arguments:
  domain

options:
  -h, --help        show this help message and exit
  --from DATE_FROM
  --to DATE_TO

```

## Example 

<img width="1836" height="419" alt="Screenshot 2026-01-13 160412" src="https://github.com/user-attachments/assets/1800c930-4ce8-413d-8308-fdd9f7049df3" />

