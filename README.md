SAMfiltering is a code writing in Python to analyse input SAM file for detecting unmapped reads and statistics of FLAGs and CIGAR. User can find all files containing mapped/unmapped/filtered/unfiltered reads in FASTA format in the directory "output" which has the same name like an input file without an extention .sam.

##  Requirements

- Python ≥ 3.6
- Standard Python libraries only (`os`, `sys`, `re`)

No external dependencies required.

## Usage
The input file must be a valid SAM file as specified in the SAM/BAM specification.

Command line in bash : 
```bash
python3 samfiltering.py input.sam
```
## The script creates an output directory:

<input_filename>_out/

and contains the following files:

*_unfiltered_reads.fasta	           Reads with MAPQ < 30
*_mapped_reads.fasta	                   Mapped reads (FLAG-based)
*_unmapped_reads.fasta	           Unmapped reads (FLAG-based)
*_unmapped_cigar_reads.fasta	   Reads with inconsistent CIGAR


## Example output:
```bash
Statistics for input.sam is:

Number of reads which pass MAPQ>30 is: 310367
number of unmapped reads is :  0 , number of mapped reads is:  310367
number of unmapped reads is (in CIGAR):  310367 , number of mapped reads (in CIGAR): is 0

FLags bits statistics :
paired                   : 310367 reads
proper pair              : 310352 reads
read unmapped            : 0 reads
mate unmapped            : 13 reads
read reverse strand      : 155180 reads
mate reverse strand      : 155182 reads
first in pair            : 155186 reads
second in pair           : 155181 reads
secondary alignment      : 0 reads
QC fail                  : 0 reads
duplicate                : 0 reads
supplementary alignment  : 0 reads

Reads per chromosome :
Reference: 310367 reads

CIGAR operations statistics (% of reads):
alignment match (can be match or mismatch)   : 310367 reads (100.00 %)
insertion to the reference                   :     17 reads (  0.01 %)
deletion from the reference                  :     54 reads (  0.02 %)
skipped region from the reference            :      0 reads (  0.00 %)
soft clipping (clipped sequences present in SEQ):     38 reads (  0.01 %)
hard clipping (clipped sequences NOT present in SEQ):      0 reads (  0.00 %)
padding                                      :      0 reads (  0.00 %)
sequence match                               :      0 reads (  0.00 %)
sequence mismatch                            :      0 reads (  0.00 %)
Saved unfiltered sequences to mapping_out/input_unfiltered_reads.fasta
Saved unmapped sequences to mapping_out/input_unmapped_reads.fasta
Saved mapped sequences to mapping_out/input_mapped_reads.fasta
Saved unmapped cigar sequences to mapping_out/input_unmapped_cigar_reads.fasta
```
## License

MIT License

Copyright (c) 2025 <Tatiana Krylova>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Author

Tatiana Krylova
University of Montpellier (Université de Montpellier), Montpellier, France, Bioinformatics department 
tatiana.krylova@etu.umontpellier.fr

