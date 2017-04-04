import json,csv
import argparse
import os,argparse
from datetime import datetime
from datetime import timedelta
from pprint import pprint 

def time_normalizer(time,offset):
    """
    this is a helper function 
    converts time to a datetime object
    uses timeOffset to normalize the time to GMT time
    if the hour is >= 24, increment day by 1
    """
    
    in_time = datetime.strptime(time,'%m/%d/%Y %I:%M:%S%p')
    offset = float(offset.replace(':','.'))
    #offset = float(datetime.strptime(offset,'%I:%M').replace(':','.'))
    new_hr = in_time.hour-(offset)
    
    if new_hr >= 24:
        return in_time + timedelta(hours=1)
    else:
        return in_time
    
    
class StreamData(object):
    def __init__(
        self,
        json_file,
        csv_file,
        out_json_file,
        **kwargs
        ):

        """
        This class reads the JSON file,
        converts JSON to a dictionary,
        populates a CSV file based on certain conditions in the description
        populates a JSON file with analytics info.
        """

        self.json_file = json_file
        self.out_json_file = out_json_file
        self.csv_file = csv_file
        self.kwags = kwargs

        # Variables for data analysis
        self.line_count = 0 # counts the number of lines in the JSON file.
        self.dropped_lines = 0 # counts the number of dropped lines from the JSON file
        self.dup_count = 0 # counts the number of dups based on event_id
        self.no_action_mapping = 0 # counts the number of entries with invalid action mapping 
        self.event_id_list = [] # helper list to see if the event id is unique or not
        self.time_stamp_list = [] # helper list to collect timestamps
        self.unique_user_set = set() # helper set to get the number of unique users in the JSON file
        self.unique_file_set = set() # helper set to get the number of unique files in the JSON file
        self.add_count,self.del_count,self.acc_count = [0,0,0]
        if self.json_file:
            self.read_json()
            
    def read_json(self):
        self.data = []
        for _item in open(self.json_file,'r'):
            self.line_count += 1
            self.data.append(json.loads(_item))

    def write_to_csv(self):
        # `TIMESTAMP,ACTION,USER,FOLDER,FILENAME,IP`
        with open(self.csv_file,'w+') as csv_file:
            fields = ['TIMESTAMP','ACTION','USER','FOLDER','FILENAME','IP']
            writer = csv.DictWriter(csv_file, fieldnames=fields)
            writer.writeheader()
            _action_dict = {
                'createdDoc': 'ADD',
                'deletedDoc': 'REMOVE',
                'viewedDoc': 'ACCESSED',
                'addedText': 'ADD',
                'changedText': 'ADD',
                'deletedText': 'REMOVE',
                'hashed': None,
                'replicated': None,
                'archived': 'REMOVE',
                'restored': None,
                }

            for item in self.data:
                self.time_stamp_list.append(
                    time_normalizer(
                        item['timestamp'],
                        item['timeOffset'] if item.get('timeOffset') else '-05:00',
                        )
                    )

                if item['eventId'] not in self.event_id_list:
                    self.unique_file_set.add(item['file'])
                    self.unique_user_set.add(item['user'])
                    self.event_id_list.append(item['eventId'])
                    #self.time_stamp_list.append(item['timestamp'])
                    if _action_dict[item['activity']]:
                        _folder,_file_name = item['file'].rsplit('/',1)
                        writer.writerow(
                            {
                                'TIMESTAMP':item['timestamp'],
                                'ACTION': _action_dict[item['activity']],
                                'USER': item['user'].split('@')[0],
                                'FOLDER': _folder,
                                'FILENAME': _file_name,
                                'IP': item['ipAddr'],
                                }
                            )
                        if _action_dict[item['activity']] == 'ADD':
                            self.add_count += 1
                        elif _action_dict[item['activity']] == 'REMOVE':
                            self.del_count += 1
                        elif _action_dict[item['activity']] == 'ACCESSED':
                            self.acc_count += 1
                        else:
                            print ('None')
                    else:
                        self.dropped_lines += 1 
                        self.no_action_mapping += 1
                else:
                    self.dropped_lines += 1 
                    self.dup_count += 1 

    def write_to_json(self):
        out_dict = {}
        self.time_stamp_list.sort()        
        out_dict['linesRead'] = self.line_count
        out_dict['droppedEventsCounts'] = self.dropped_lines
        out_dict['droppedEvents'] = {}
        out_dict['droppedEvents']['No action mapping'] = self.no_action_mapping
        out_dict['droppedEvents']['Duplicates'] = self.dup_count
        out_dict['uniqueUser'] = len(self.unique_user_set)
        out_dict['uniqueFiles'] = len(self.unique_file_set)
        out_dict['startDate'] = str(self.time_stamp_list[0])
        out_dict['endDate'] = str(self.time_stamp_list[-1])
        out_dict['actions'] = {}
        out_dict['actions']['ADD'] = self.add_count
        out_dict['actions']['REMOVE'] = self.del_count
        out_dict['actions']['ACCESSED'] = self.acc_count
        pprint (out_dict)
        with open(self.out_json_file,'w') as file_handle:
            json.dump(out_dict,file_handle,indent=4)
            
                            
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument(
        '--in_json', 
        help='Input JSON file',
        required=False,
        default=os.getcwd()+'/metadataObjects.json'
        )
    parser.add_argument(
        '--out_json',
        help='Output JSON file',
        required=False,
        default=os.getcwd()+'/output.json',
        )
    parser.add_argument(
        '--out_csv',
        help='Output CSV file',
        required=False,
        default=os.getcwd()+'/output.csv',
        )
    args=parser.parse_args()    
    print (
        args.in_json,
        args.out_csv,
        args.out_json,
        )
    s1 = StreamData(
        args.in_json,
        args.out_csv,
        args.out_json,
        )
    s1.write_to_csv()
    s1.write_to_json()
    
       
