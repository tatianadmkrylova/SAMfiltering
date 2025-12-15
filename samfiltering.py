#!/usr/bin/python3
#-*- coding : utf-8 -*-

import os, re, sys

base_name = os.path.splitext(os.path.basename(sys.argv[1]))[0] # name of file without the extension
output_dir = f"{base_name}_out" # directory for the saved files 
os.makedirs(output_dir, exist_ok=True) 

# check of presence a correct number of arguments
if len(sys.argv) != 2:
        print("\nYou need to have an argument\t")
        print("\nCondition: ./list.py <filename.sam>")
        sys.exit(1)
        
# verification if a file contains .sam
if not sys.argv[1].lower().endswith(".sam"):
        print("\nYou need a file with .sam")
        sys.exit(1)        
        
        
def filter_mapq(row, mapq_value = 30): # function for filtration (MAPQ)
        mapq_col = int(row[4]) # dp in 5 column (MAPQ)
        if mapq_col >= mapq_value:
                return 'pass'
        else:
                return 'filter'
        
def flag_binary(flag):     # function to convert flag to binary         
        flagB = bin(int(flag))[2:] 
        flagB = list(flagB)
        if len(flagB) < 12:
                add = 12 - len(flagB)
                for t in range(add):
                        flagB.insert(0, '0') # list
        return flagB

def cigar_stats(cigar, cigar_dict): # function to count CIGAR statistics
        if cigar == '*':
                return
        ops = set(re.findall(r'([MIDNSHP=X])', cigar))
        for op in ops:
                cigar_dict[op] += 1


bit_counts = {i: 0 for i in range(12)} # dictionnary for FLAG count
chr_counts = {} # dictionnary for read counts per chromosome
cigar_counts = {
        'M': 0, 'I': 0, 'D': 0, 'N': 0,
        'S': 0, 'H': 0, 'P': 0, '=': 0, 'X': 0
} # # dictionnary for CIGAR statistics counts, initiation to 0

with open(sys.argv[1], 'r') as f: # open the file
        data_present = False # "flag" that file is empty
        filtered = []
        unfiltered = []
        mapped_count = 0
        unmapped_count = 0
        mapped_cigar_count = 0
        unmapped_cigar_count = 0
        unmapped_sequences = [] 
        mapped_sequences = []
        unmapped_cigar_sequences = []

        for line in f:
                if line.startswith("@"):
                        continue # pass headers, continue with data
                data_present = True # file contains read, not empty
                row = line.rstrip().split('\t') # for columns view
                
                if filter_mapq(row) == 'pass':
                        filtered.append(row) # reads that passed MAPQ >30
                else:
                        unfiltered.append(row[9]) # unfiltered reads that did not pass MAPQ >30

        for row in filtered:
                        
                flag = row[1] # flag is in the 2nd column
                flagB = flag_binary(flag)
                
                if flagB[-3] == "1": # flag contains 4 --> unmapped
                        unmapped_count += 1
                        unmapped_sequences.append(row[9]) # extrait des reads unmapped
                else:			# flag does not contain 4 --> mapped	
                        mapped_count += 1
                        mapped_sequences.append(row[9])
                

                for pos in range(12): # to count every flag
                        if flagB[-1-pos] == '1':
                                bit_counts[pos] += 1

                chrom = row[2] # chromosome position is in the 3rd column
                if chrom in chr_counts:
                        chr_counts[chrom] += 1
                else:
                        chr_counts[chrom] = 1

                cigar = row[5]
                #print(len(cigar), cigar)

                cigar_stats(cigar, cigar_counts)

                if cigar == '*':
                        continue
                digitCig = re.findall("(\d+)\D", cigar) # to find all digits in the line
                #print(digitCig)
                sum = 0
                for digit in digitCig:
                        sum += int(digit)
                #print(sum)

                if sum == len(filtered):
                        mapped_cigar_count += 1
                else:
                        unmapped_cigar_count += 1
                        unmapped_cigar_sequences.append(row[9])
                
if not data_present:
        print("\nSam file is empty or contains just header")
        sys.exit(0)
else:	

#### STATISTICS ######

        print("\nStatistics for", sys.argv[1], "is:" )
        print("\nNumber of reads which pass MAPQ>30 is:", len(filtered))
        print("number of unmapped reads is : ", unmapped_count, "," , "number of mapped reads is: ",  mapped_count)
        print("number of unmapped reads is (in CIGAR): ", unmapped_cigar_count, "," , "number of mapped reads (in CIGAR): is", mapped_cigar_count)
        
        flag_descriptions = {
            0: "paired",
            1: "proper pair",
            2: "read unmapped",
            3: "mate unmapped",
            4: "read reverse strand",
            5: "mate reverse strand",
            6: "first in pair",
            7: "second in pair",
            8: "secondary alignment",
            9: "QC fail",
            10: "duplicate",
            11: "supplementary alignment"
        }
        print("\nFLags bits statistics :")
        for pos, description in flag_descriptions.items():
                print(f"{description:25s}: {bit_counts[pos]} reads") # line contains 25 caracters
                
        print("\nReads per chromosome :")
        for chrom, count in sorted(chr_counts.items()):
                print(f"{chrom}: {count} reads")

        total_reads = len(filtered)

        cigar_descriptions = {
        'M': 'alignment match (can be match or mismatch)',
        'I': 'insertion to the reference',
        'D': 'deletion from the reference',
        'N': 'skipped region from the reference',
        'S': 'soft clipping (clipped sequences present in SEQ)',
        'H': 'hard clipping (clipped sequences NOT present in SEQ)',
        'P': 'padding',
        '=': 'sequence match',
        'X': 'sequence mismatch'
        }

        print("\nCIGAR operations statistics (% of reads):")
        for op, count in cigar_counts.items():
                percent = (count / total_reads) * 100 if total_reads else 0
                desc = cigar_descriptions.get(op, 'unknown')
                print(f"{desc:45s}: {count:6d} reads ({percent:6.2f} %)")

#### FASTA output ######

        unfiltered_file = os.path.join(output_dir, f"{base_name}_unfiltered_reads.fasta")
        with open(unfiltered_file , "w") as out:
                for i, seq in enumerate(unfiltered):
                        out.write(f">unfiltered_{i}\n{seq}\n")
        print("Saved unfiltered sequences to", unfiltered_file)

        unmapped_file = os.path.join(output_dir, f"{base_name}_unmapped_reads.fasta")
        with open(unmapped_file, "w") as out:
                for i, seq in enumerate(unmapped_sequences):
                        out.write(f">unmapped_{i}\n{seq}\n")
        print("Saved unmapped sequences to", unmapped_file)


        mapped_file = os.path.join(output_dir, f"{base_name}_mapped_reads.fasta")
        with open(mapped_file, "w") as out:
                for i, seq in enumerate(mapped_sequences):
                        out.write(f">mapped_{i}\n{seq}\n")
        print("Saved mapped sequences to", mapped_file)


        unmapped_cigar_file = os.path.join(output_dir, f"{base_name}_unmapped_cigar_reads.fasta")
        with open(unmapped_cigar_file, "w") as out:
                for i, seq in enumerate(unmapped_cigar_sequences):
                        out.write(f">unmapped_cigar_{i}\n{seq}\n")
        print("Saved unmapped cigar sequences to", unmapped_cigar_file)

