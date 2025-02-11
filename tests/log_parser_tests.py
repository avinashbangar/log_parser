import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from log_parser import parseLog

# Test Cases:
TEST_LOG_FILE = "log_test.txt"
TEST_LOOKUP_FILE = "lookup_test.txt"

# Test Case 1: Basic Functionality
def test_basic_functionality():
	# Assuming the lookup.txt and log.txt files are set up correctly
	parseLog(log_file=TEST_LOG_FILE, lookup_file=TEST_LOOKUP_FILE)
	with open("tag_counts.txt", "r") as file:
		content = file.read()
		assert "Tag, Count:" in content
	with open("port_protocol_counts.txt", "r") as file:
		content = file.read()
		assert "Port, Protocol, Count:" in content

# Test Case 2: Empty Log File
def test_empty_log_file():
	# Create an empty log.txt file
	with open("empty_log.txt", "w") as file:
		pass
	parseLog(log_file="empty_log.txt", lookup_file=TEST_LOOKUP_FILE)
	with open("tag_counts.txt", "r") as file:
		content = file.read()
		assert "Untagged, 0" in content

# Test Case 3: Invalid Log Format
def test_invalid_log_format():
	# Create a log.txt file with invalid format
	with open("invalid_log.txt", "w") as file:
		file.write("Invalid log entry")
	parseLog(log_file="invalid_log.txt", lookup_file=TEST_LOOKUP_FILE)
	with open("tag_counts.txt", "r") as file:
		content = file.read()
		assert "Untagged, 0" in content


# Test Case 4: Mixed Protocols
def test_mixed_protocols():
	# Create a log.txt file with mixed protocols
	with open("mixed_protocol_log.txt", "w") as file:
		file.write("2 tcp 0 0 0 0 993 6\n")
		file.write("2 udp 0 0 0 0 31 17\n")
	parseLog(log_file="mixed_protocol_log.txt", lookup_file=TEST_LOOKUP_FILE)
	with open("tag_counts.txt", "r") as file:
		content = file.read()
		assert "SV_P3, 1" in content
		assert "email, 1" in content

# Test Case 5: Large Log File
def test_large_log_file():
	# Create a large log.txt file
	with open("test_large_log.txt", "w") as file:
		for i in range(10000):
			file.write("2 tcp 0 0 0 0 80 6\n")
	parseLog(log_file="test_large_log.txt", lookup_file=TEST_LOOKUP_FILE)
	with open("tag_counts.txt", "r") as file:
		content = file.read()
		assert "Untagged, 10000" in content

# Test Case 6: Different Versions
def test_different_versions():
	# Create a log.txt file with different versions
	with open("different_version_log.txt", "w") as file:
		file.write("1 tcp 0 0 0 0 80 6\n")
		file.write("2 tcp 0 0 0 0 80 6\n")
	parseLog(log_file="different_version_log.txt", lookup_file=TEST_LOOKUP_FILE)
	with open("tag_counts.txt", "r") as file:
		content = file.read()
		assert "Untagged, 1" in content

# Test Case 7: Empty Lookup File
def test_empty_lookup_file():
	# Create an empty lookup.txt file
	with open("empty_lookup.txt", "w") as file:
		pass
	parseLog(log_file=TEST_LOG_FILE, lookup_file="empty_lookup.txt")
	with open("tag_counts.txt", "r") as file:
		content = file.read()
		assert "Untagged, 14" in content


def run_tests():

	# Run all test cases
	test_basic_functionality()
	test_empty_log_file()
	test_invalid_log_format()
	test_mixed_protocols()
	test_large_log_file()
	test_different_versions()
	test_empty_lookup_file()

run_tests()