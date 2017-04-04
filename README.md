# Interset Solution
Interset Solution
python json_to_csv.py --help
usage: json_to_csv.py [-h] [--in_json IN_JSON] [--out_json OUT_JSON]
                      [--out_csv OUT_CSV]

optional arguments:
  -h, --help           show this help message and exit
  --in_json IN_JSON    Input JSON file
  --out_json OUT_JSON  Output JSON file
  --out_csv OUT_CSV    Output CSV file


a) This python file provides StreamData class which,
     1. reads a JSON file to a dictionary
     2. massages the output based on the problem description
     3. populates a CSV file 'output.csv' in the same directory
     4. populates a JSON file 'output.json' with analytics info in the same directory. 

b) There is a helper function to normalize time based on offset and convert time to GMT.
c) The code makes use of standard python libraries, so there is no need for an additional requirements file.
d) Lists, sets and other variables are declared in the init section which are used to generate analytics. 







