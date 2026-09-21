import re
from Bio.Seq import Seq
from Bio import SeqIO
import csv
import gzip
import os

from Bio.SeqRecord import SeqRecord

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

class SequencingRead:
    def __init__(self, read_id, sequence):
        self.sequence = sequence
        self.read_id = read_id

    def matches_mid_pair(self, forward_mid, reverse_mid) -> bool:
        reverse_mid_rc = str(Seq(reverse_mid).reverse_complement())
        pattern = rf"^{re.escape(forward_mid)}.*{re.escape(reverse_mid_rc)}$"
        return bool(re.fullmatch(pattern, self.sequence))

    def trim_mid_pair(self, forward_mid, reverse_mid):
        if self.matches_mid_pair(forward_mid, reverse_mid):
            reverse_mid_rc = str(Seq(reverse_mid).reverse_complement())

            return self.sequence[len(forward_mid):-len(reverse_mid_rc)]

        return None

    def describe(self):
        return f"Sequencing read: {self.read_id} ({len(self.sequence)} bp)"


r1 = SequencingRead("demo_1", "AGCTTCGA" + "N" * 20 + str(Seq("TGCAGGTC").reverse_complement()))
print(r1.describe())
print(r1.matches_mid_pair("AGCTTCGA", "TGCAGGTC"))  # True
print(r1.matches_mid_pair("CGATCGAT", "GCTAGCTA"))  # False
print(r1.trim_mid_pair("AGCTTCGA", "TGCAGGTC"))     # 20 x "N"

#TASK3
class Demultiplexer:
    def __init__(self, fasta_path, mid_table_path):
        self.reads = []
        self.mid_pairs = []

        with gzip.open(fasta_path, 'rt') as handle:
            for record in SeqIO.parse(handle, 'fasta'):
                read = SequencingRead(record.id, str(record.seq))
                self.reads.append(read)

        with open(mid_table_path, 'r') as handle:
            reader = csv.DictReader(handle, delimiter=';')
            for row in reader:
                label = f"{row["SampleID"]}_{row["Description"]}"
                forward_mid = row["FBarcodeSequence"]
                reverse_mid = row["RBarcodeSequence"]
                self.mid_pairs.append((label, forward_mid, reverse_mid))

        self.assigned = {}
        for label, forward_mid, reverse_mid in self.mid_pairs:
            self.assigned[label] = []

        self.unassigned = []
    def assing_reads(self):
        for read in self.reads:
            matched = False

            for label, forward_mid, reversemid in self.mid_pairs:
                if read.matches_mid_pair(forward_mid, reversemid):
                    trimmed_sequence = read.trim_mid_pair(forward_mid, reversemid)
                    trimmed_read = SequencingRead(read.id, trimmed_sequence)
                    self.assigned[label].append(trimmed_sequence)
                    matched = True
                    break
                elif read.matches_mid_pair(forward_mid, reversemid):
                    trimmed_sequence = read.trim_mid_pair(forward_mid, reversemid)





    def report(self) -> str:

    def write_fasta(self, output_dir):


#demux = Demultiplexer("fishes.fna.gz", "fishes_MIDs.csv")




