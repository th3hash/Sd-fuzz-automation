import os

# List of domains
domains = [
    "example.com",
    "example2.com",
    "example3.com"
]

# Output file
output_file = "output.txt"

# Remove output file if it already exists
if os.path.exists(output_file):
    os.remove(output_file)

# Run sublist3r, subfinder, and amass on each domain
for domain in domains:
    os.system(f"sublist3r -d {domain} >> {output_file}")
    os.system(f"subfinder -d {domain} >> {output_file}")
    os.system(f"amass enum -d {domain} >> {output_file}")

# Remove duplicates from the output file
with open(output_file, "r") as f:
    lines = set(f.readlines())

with open(output_file, "w") as f:
    for line in lines:
        f.write(line)

# Run waybackurls and ffuf on each domain
with open(output_file, "r") as f:
    lines = f.readlines()

for line in lines:
    line = line.strip()
    os.system(f"waybackurls {line} >> {output_file}")
    os.system(f"ffuf -w {line} -u {line} >> {output_file}")
