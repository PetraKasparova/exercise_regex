import re

#TASK1
log_lines = [
    "2024-01-15 10:02:11 INFO Server started on port 8080",
    "2024-01-15 10:03:47 ERROR Failed to connect to database",
    "2024-01-16 08:15:00 WARNING Disk usage at 85%",
    "2024-01-16 14:22:39 ERROR Timeout while fetching https://example.com/api",
    "2024-01-17 09:00:05 INFO User admin logged in from 192.168.1.10",
    "2024-01-17 11:41:18 DEBUG Cache cleared successfully",
    "2024-01-18 03:12:56 ERROR Connection refused from 192.168.1.55",
    "2024-01-18 23:59:02 INFO Backup completed in 42s",
]

#1
result1 = []
for line in log_lines:
    if re.match("2024-01-16", line):
        result1.append(line)
#print(result1)

#2
result2 = []
for line in log_lines:
    if re.search("(ERROR|WARNING)", line):
        result2.append(line)
#print(result2)

#3
IPv4_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
result3 = []
for line in log_lines:
    result3.extend(re.findall(IPv4_pattern, line))
#print(result3)

#4
result4 = []
for line in log_lines:
   if re.search(r"\d.+s$", line):
       result4.append(line)
#print(result4)

#5
result5 = []
for line in log_lines:
    if re.search("(http://|https://)",line):
        result5.append(line)
#print(result5)

#TASK2
def reverse_complement(sequence):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    complemented = "".join(complement[base] for base in sequence)
    return complemented[::-1]

print

class SequencingRead:
    def __init__(self,read_id, sequence):
        self.sequence = sequence
        self.read_id = read_id

    def matches_mid_pair(self, forward_mid, reverse_mid) -> bool:



