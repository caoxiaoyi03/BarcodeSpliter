import argparse
import textdistance

levenshtein = textdistance.Levenshtein()

parser = argparse.ArgumentParser(
  description='Find and group some sequences by tag.')
parser.add_argument('input', type=str, help='Input file name')
parser.add_argument('nonTag1', type=str, help='First non-barcode tag')
parser.add_argument('nonTag2', type=str, help='Second non-barcode tag')
parser.add_argument('barcodeA', type=str, help='Barcode A list file')
parser.add_argument('barcodeB', type=str, help='Barcode B list file')
parser.add_argument('--maxDistance', type=int, default=2, help='Maximum distance (Levenshtein) allowed for barcodes')
args = parser.parse_args()

barcodeADict = dict()
barcodeBDict = dict()
seqsCount = 0
barcodeASize = 0
barcodeBSize = 0

with open(args.barcodeA, 'r') as fin:
  for line in fin:
    if line.strip() and not line.strip().startswith('#'):
      barcodeADict[line.strip().lower()] = True
      if barcodeASize <= 0:
        barcodeASize = len(line.strip())
print('Barcode A varieties:', len(barcodeADict.keys()), '| Size:', barcodeASize)

with open(args.barcodeB, 'r') as fin:
  for line in fin:
    if line.strip() and not line.strip().startswith('#'):
      barcodeBDict[line.strip().lower()] = True
      if barcodeBSize <= 0:
        barcodeBSize = len(line.strip())
print('Barcode B varieties:', len(barcodeBDict.keys()), '| Size:', barcodeBSize)

numOfUnparseable = 0 # Cannot split tag
matchedA = dict()
nonMatchedA = dict()

def findClosestBarcode(value, dictionary, levDistance):
  if value in dictionary:
    return value
  else:
    # find the dictionary value
    for barcode in dictionary.keys():
      if levenshtein(value, barcode) <= levDistance:
        return barcode
  return None

def processSeq(sequence):
  # find matched nonTag1 and nonTag2
  # compare barcode A1 and A2
  # find barcode dictionary entry
  # add count for barcode A and B
  global numOfUnparseable
  tagASplit = sequence.split(args.nonTag1.lower(), 1)
  if len(tagASplit) < 2:
    numOfUnparseable += 1
  else:
    barcodeA1Candidate = tagASplit[0][-barcodeASize:]
    tagBSplit = tagASplit[1].split(args.nonTag2.lower(), 1)
    if len(tagBSplit) < 2:
      numOfUnparseable += 1
    else:
      barcodeBCandidate = tagBSplit[0][-barcodeBSize:]
      barcodeA2Candidate = tagBSplit[1][:barcodeASize]
      barcodeA1Entry = None
      if barcodeA1Candidate in barcodeADict:
        barcodeA1Entry = barcodeA1Candidate
      else:
        # find the dictionary value
        for barcodeA in barcodeADict.keys():
          if levenshtein(barcodeA1Candidate, barcodeA) <= 2:
            barcodeA1Entry = barcodeA
            break
      barcodeA1Entry = findClosestBarcode(barcodeA1Candidate, barcodeADict, args.maxDistance)
      barcodeA2Entry = findClosestBarcode(barcodeA2Candidate, barcodeADict, args.maxDistance)
      barcodeBEntry = findClosestBarcode(
          barcodeBCandidate, barcodeBDict, args.maxDistance)
      if barcodeA1Entry is None or barcodeA2Entry is None or barcodeBEntry is None:
        numOfUnparseable += 1
      else:
        # now everything is there
        if barcodeA1Entry == barcodeA2Entry:
          # matched
          if barcodeA1Entry not in matchedA:
            matchedA[barcodeA1Entry] = dict()
          if barcodeBEntry not in matchedA[barcodeA1Entry]:
            matchedA[barcodeA1Entry][barcodeBEntry] = 1
          else:
            matchedA[barcodeA1Entry][barcodeBEntry] += 1
        else:
          # mismatch
          if barcodeA1Entry not in nonMatchedA:
            nonMatchedA[barcodeA1Entry] = dict()
          if barcodeA2Entry not in nonMatchedA[barcodeA1Entry]:
            nonMatchedA[barcodeA1Entry][barcodeA2Entry] = dict()
          if barcodeBEntry not in nonMatchedA[barcodeA1Entry][barcodeA2Entry]:
            nonMatchedA[barcodeA1Entry][barcodeA2Entry][barcodeBEntry] = 1
          else:
            nonMatchedA[barcodeA1Entry][barcodeA2Entry][barcodeBEntry] += 1


with open(args.input, 'r') as fin:
  line = fin.readline()
  while line:
    if line.startswith('@'):
      line = fin.readline()  # read sequence
      processSeq(line.strip().lower())
      seqsCount += 1
      line = fin.readline()  # skip +
      line = fin.readline()  # skip quality
    line = fin.readline()  # next line
print('Total number of sequences:', seqsCount)

# now everything should be done
print('Unparseable reads:', numOfUnparseable)
print('\n******* Matched Barcode A entries *******\n')
print('Barcode A\tBarcode B\tCount')
for barcodeA, bDict in matchedA.items():
  for barcodeB, count in bDict.items():
    print(barcodeA, barcodeB, count, sep='\t')

print('\n******* Non-matched Barcode A1/A2 entries *******\n')
print('Barcode A1\tBarcode A2\tBarcode B\tCount')
for barcodeA1, a2Dict in nonMatchedA.items():
  for barcodeA2, bDict in a2Dict.items():
    for barcodeB, count in bDict.items():
      print(barcodeA1, barcodeA2, barcodeB, count, sep='\t')
