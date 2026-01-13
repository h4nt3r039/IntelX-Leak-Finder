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
