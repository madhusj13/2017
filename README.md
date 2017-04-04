# Interset Solution
Interset Solution\n
python json_to_csv.py --help\n
usage: json_to_csv.py [-h] [--in_json IN_JSON] [--out_json OUT_JSON]\n
                      [--out_csv OUT_CSV]\n

optional arguments:\n
  -h, --help           show this help message and exit\n
  --in_json IN_JSON    Input JSON file\n
  --out_json OUT_JSON  Output JSON file\n
  --out_csv OUT_CSV    Output CSV file\n


a) This python file provides StreamData class which,\n
     1. reads a JSON file to a dictionary\n
     2. massages the output based on the problem description\n
     3. populates a CSV file 'output.csv' in the same directory\n
     4. populates a JSON file 'output.json' with analytics info in the same directory. \n

b) There is a helper function to normalize time based on offset and convert time to GMT.\n
c) The code makes use of standard python libraries, so there is no need for an additional requirements file.\n
d) Lists, sets and other variables are declared in the init section which are used to generate analytics. \n







