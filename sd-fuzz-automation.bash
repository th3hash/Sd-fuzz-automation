#!/bin/bash

# Store the file name in a variable
file=$1

# Check if the file exists
if [ ! -f "$file" ]; then
  echo "Error: File not found."
  exit 1
fi

# Read each line of the file and store it in an array
declare -a domains
while IFS= read -r line; do
  domains+=( "$line" )
done < "$file"

# Use sublist3r, subfinder, and amass to grab all the domains
echo "Gathering domains..."
for domain in "${domains[@]}"; do
  sublist3r -d "$domain" >> domains.txt
  subfinder -d "$domain" >> domains.txt
  amass enum -d "$domain" >> domains.txt
done

# Sort and remove duplicates from the list of domains
echo "Removing duplicates..."
sort domains.txt | uniq > sorted_domains.txt

# Use waybackurls and ffuf to fuzz the domains and find endpoints
echo "Finding endpoints..."
while read -r domain; do
  waybackurls "$domain" >> endpoints.txt
  ffuf -u "$domain" -w /path/to/wordlist.txt -e .php,.html -t 100 -o ffuf_output.txt
done < sorted_domains.txt

# Store the results in an output file
echo "Storing results in output file..."
cat ffuf_output.txt >> output.txt

# Clean up
rm domains.txt
rm sorted_domains.txt
rm endpoints.txt
rm ffuf_output.txt

echo "Done!"
