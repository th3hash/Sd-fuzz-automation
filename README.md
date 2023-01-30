# Sd-fuzz-automation
Automation of grabbing all the subdomains and fuzzing the resultant.

This script takes a file name as the first argument and reads each line of the file as a domain. It uses the sublist3r, subfinder, and amass tools to gather all the domains associated with the input domains. The results are sorted and duplicates are removed. The script then uses waybackurls and ffuf to fuzz the domains and find endpoints, and stores the results in an output file. The script also cleans up the intermediate files created during the process.
