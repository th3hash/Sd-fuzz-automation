import subprocess
import os

# Input file containing the list of domains
input_file = "domains.txt"

# Output file to store the results
output_file = "output.txt"

# Running sublist3r, subfinder, and amass to gather subdomains
with open(input_file, "r") as f:
    domains = f.read().splitlines()
    for domain in domains:
        subprocess.call(["sublist3r", "-d", domain, "-o", "sublist3r_output.txt"])
        subprocess.call(["subfinder", "-d", domain, "-o", "subfinder_output.txt"])
        subprocess.call(["amass", "enum", "-d", domain, "-o", "amass_output.txt"])

# Combining the results from sublist3r, subfinder, and amass into one file
with open("sublist3r_output.txt", "r") as f1, open("subfinder_output.txt", "r") as f2, open("amass_output.txt", "r") as f3:
    subdomains = set(f1.read().splitlines() + f2.read().splitlines() + f3.read().splitlines())

# Running waybackurls and ffuf on the combined subdomains list
with open(output_file, "w") as f:
    for subdomain in subdomains:
        wayback_output = subprocess.check_output(["waybackurls", subdomain]).decode("utf-8")
        ffuf_output = subprocess.check_output(["ffuf", "-u", subdomain + "/FUZZ", "-w", "wordlist.txt"]).decode("utf-8")
        f.write(subdomain + "\n" + wayback_output + "\n" + ffuf_output + "\n\n")

# Cleaning up intermediate files
os.remove("sublist3r_output.txt")
os.remove("subfinder_output.txt")
os.remove("amass_output.txt")
