# IntelX-Leak-Finder
* Extract credentials from IntelX leaks with smart parsing and JSON output 
* IntelX credential leak parser with URL-aware extraction 
* SOC-focused IntelX credential extractor


What this tool does:

This tool searches IntelX for leaked data related to a specific domain and extracts credentials from raw leak files. 

Username and password types inside the IntelX leak file:

• URL + username + password

• Email + password

• Phone + password

• Username + password

• Space-separated credentials

• Pipe-separated formats

• CSV-like formats

• Weird real-world dumps

It outputs structured JSON files ready for SOC ingestion, automation, or alerting.


P.S.
This tool specifically targets the IntelX bucket "leaks.private.general", which aggregates private breach material, leaked credentials, and compromised account data relevant for threat intelligence and incident response workflows.

<img width="201" height="360" alt="Screenshot from 2026-01-13 15-32-52" src="https://github.com/user-attachments/assets/e3d7cf4f-27d5-42d3-b830-796cefeb7e70" />




Features
• IntelX search automation
• Polling for result readiness
• Credential parsing
• URL extraction
• Deduplication
• Date range filtering
• JSON output
