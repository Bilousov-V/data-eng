import json
import csv
from glob import glob

def flatten_json(y):
    out = {}
 
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x
 
    flatten(y)
    return out

def main():
    file_list = glob("**/*.json", recursive=True)
    for file in file_list:
        with open(file) as f:
            data = [flatten_json(json.load(f))]
            fieldnames = [key for key in data[0]]
            with open(file.replace(".json", ".csv"), 'w', newline='') as f:
                w = csv.DictWriter(f, fieldnames=fieldnames)
                w.writeheader()
                w.writerows(data)
    pass


if __name__ == "__main__":
    main()
