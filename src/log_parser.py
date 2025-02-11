
LOOKUP_FILE = "lookup.txt"
LOG_FILE = "log.txt"

SUPPORTED_VERSION = 2
TCP_PROTOCOL = 'tcp'
UDP_PROTOCOL = 'udp'
UDP_DECIMAL = 17


def loadLookupData(lookup_file=LOOKUP_FILE):
	lookup = {}
	with open(lookup_file, "r") as file:
		for line in file:
			line = line.strip()
			# Skip header
			if 'dst' in line:
				continue
		
			line_li = line.split(',')
			# Skip invalid lines
			if len(line_li) != 3:
				continue
			
			# Create a key from dstport and protocol
			dstport_protocol = line_li[0] + '_' + line_li[1]
			lookup[dstport_protocol] = line_li[2].strip()

	return lookup

def readLogFile(log_file=LOG_FILE):
    with open(log_file, "r") as file:
        for line in file:
            yield line.strip()  # Yield one line at a time

def initialize_tag_counts(lookup):
	res = {}
	for key, val in lookup.items():
		res[val] = 0
	res['Untagged'] = 0
	return res

def save_to_file_tag_counts(tag_counts):
	with open("tag_counts.txt", "w") as file:
		file.write("Tag, Count:\n")
		for key, val in tag_counts.items():
			file.write(f"{key}, {val}\n")

def save_to_file_port_protocol_counts(port_protocol_counts):
	with open("port_protocol_counts.txt", "w") as file:
		file.write("Port, Protocol, Count:\n")
		for key, val in port_protocol_counts.items():
			split_key = key.split('_')
			file.write(f"{split_key[0]}, {split_key[1]}, {val}\n")

def parseLog(log_file=LOG_FILE, lookup_file=LOOKUP_FILE):
	lookup = loadLookupData(lookup_file)
	if not lookup:
		print("Lookup data is empty.")
	
	tag_counts = initialize_tag_counts(lookup)
	port_protocol_counts = {}

	for line in readLogFile(log_file):
		parsed_list = line.split(" ")
		# Skip lines with less than 8 elements
		if len(parsed_list) <= 7:
			continue

		version = parsed_list[0]
		
		# Determine protocol
		protocol = TCP_PROTOCOL
		if parsed_list[7] == str(UDP_DECIMAL):
			protocol = UDP_PROTOCOL

		dstport = parsed_list[6]
	
		if version == str(SUPPORTED_VERSION):
			dstport_protocol = dstport + '_' + protocol
			# tag counts
			if dstport_protocol in lookup:
				tag_counts[lookup[dstport_protocol]] += 1
			else:
				tag_counts['Untagged'] += 1
		    
			# port protocol counts
			if dstport_protocol in port_protocol_counts:
				port_protocol_counts[dstport_protocol] += 1
			else:
				port_protocol_counts[dstport_protocol] = 1
	
	# Save results to files
	save_to_file_tag_counts(tag_counts)
	save_to_file_port_protocol_counts(port_protocol_counts)
	return



def main():
	parseLog()

if __name__ == "__main__":
	main()


