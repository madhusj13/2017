# Interset Solution
Interset Solution<br />
python json_to_csv.py --help<br />
usage: json_to_csv.py [-h] [--in_json IN_JSON] [--out_json OUT_JSON]<br />
                      [--out_csv OUT_CSV]<br />

optional arguments:<br />
  -h, --help           show this help message and exit<br />
  --in_json IN_JSON    Input JSON file<br />
  --out_json OUT_JSON  Output JSON file<br />
  --out_csv OUT_CSV    Output CSV file<br />


a) This python file provides StreamData class which,<br />
     1. reads a JSON file to a dictionary<br />
     2. massages the output based on the problem description<br />
     3. populates a CSV file 'output.csv' in the same directory<br />
     4. populates a JSON file 'output.json' with analytics info in the same directory. <br />

b) There is a helper function to normalize time based on offset and convert time to GMT.<br />
c) The code makes use of standard python libraries, so there is no need for an additional requirements file.<br />
d) Lists, sets and other variables are declared in the init section which are used to generate analytics. <br />
e) Assumption - All data from the JSON file is used to analyze start and end dates.






