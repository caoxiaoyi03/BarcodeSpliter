## Split barcode and aggregate results

### Prerequisites

Python 3 with package `textdistance` is needed. If PIP is not installed with
Python 3, [please follow these instructions to install PIP](https://pip.pypa.io/en/stable/installing/).

With Python 3 and PIP, the following command can be used to install `textdistance`.

```bash
pip install textdistance
```

### Usage

```bash
python findSeq.py <input FASTQ file> <first non-barcode segment> <second non-barcode segment> <barcode A choices file> <barcode B choices file> [--maxDistance <max allowedlevenshtein distance, default = 2>]
```

Example:

```bash
python findSeq.py Sample_S1_L001_R1_001.fastq tctgcac tcgagtc barcodeA.txt barcodeB.txt --maxDistance 2
```

The choices files are text files with each choice on its own line. Lines
starting with `#` are ignored. For example:

```
# barcodeB.txt
CACCTGTAGT
TGTCGCGGAA
CTTCGGCGAA
GTCAGGTGAA
ACAACGACAA
GATAAGGCAA
AAGCCACCAA
CACGACTCAA
AGATGTAGGA
TTCCTTACGA
CCTCAGATGA
GTGAGATTGA
AGCTGTTACA
GGTAGCTGCA
TATCCATCCA
CCAACCGTCA
CAGTCCTATA
ACGAGTCGTA
CCTCAATCTA
GGCGATCTTA
TCCGTGATAG
GGCATAACGG
ATACATCCGG
TAGAACATGG
GTTGACCTGG
AGAGTTGGCG
TGGCAGATCG
GTGGTCGATG
ACAGAGGCTG
TCGGCTGTTG
CCATATAGGC
TTAGTTCACC
```

All sequences are case insensitive.
