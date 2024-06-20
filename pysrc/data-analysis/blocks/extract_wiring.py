import re

index_file = r"D:\Data\CF900\SA40458.20240606\01 - IV\SA40458.20240606.000000.tdms_index"
# Read the content from the index file
with open(index_file, 'r') as file:
    data = file.read()

# Define a regex pattern to extract the wiring information block
pattern = re.compile(r'Wiring:\s*(.*?)\s*Lockin:', re.DOTALL)
match = pattern.search(data)

if match:
    # Extract the wiring information block
    wiring_block = match.group(1).strip()
    
    # Split the block into individual lines
    wiring_lines = wiring_block.split('\n')
    
    # Define a pattern to extract Lockin number and the text after the last comma
    line_pattern = re.compile(r'Lockin (\d+), (.+)$')
    
    extracted_info = []
    
    # Process each line to extract the required details
    for line in wiring_lines:
        match_line = line_pattern.search(line.strip())
        if match_line:
            lockin_number = match_line.group(1)
            label = match_line.group(2)
            extracted_info.append((label, lockin_number))
    print(extracted_info)
    # Print the extracted information
    for lockin_number, label in extracted_info:
        print(f"Lockin {lockin_number}: {label}")
else:
    print("Wiring information not found.")
