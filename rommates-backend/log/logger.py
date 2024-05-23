import json
import os
from datetime import datetime

class Logger(object):
    _instance = None
    _log_file = './log/log.json'
    
    def __new__(cls, log_file=_log_file):
        if cls._instance is None:
            cls._instance= super(Logger,cls).__new__(cls)
            # Creating the log file as part of the instance creation, if not already exists
            if not os.path.exists(log_file):
                with open(log_file, 'w') as file:
                    file.write('[]')
            cls._instance._log_file = log_file
            
        return cls._instance
    
    def __init__(self,  max_entries=1000):
        self.max_entries = max_entries


    @property
    def log_path(self):
        return self._log_file
       
        
    def log(self, class_name, func_name, func_input, func_output):
        entries = self._load_entries()
        id = len(entries) + 1
        log_entry = {
            'id': id,
            'datetime': str(datetime.now()),
            'class_name': str(class_name),
            'func_name': str(func_name),
            'func_input': str(func_input),
            'func_output': str(func_output)
        }
        
        try:
            self._add_entry(log_entry)
                
        except Exception as e:
            return str(e)
        
        
    def _add_entry(self, entry):
        entries = self._load_entries()
        entries.append(entry)
        if len(entries) > self.max_entries:
            entries = entries[self.max_entries:]
        self._save_entries(entries)


    def _load_entries(self):
        try:
            with open(self.log_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []


    def _save_entries(self, entries):
        with open(self.log_path, 'w') as file:
            json.dump(entries, file,indent=2)
        
        