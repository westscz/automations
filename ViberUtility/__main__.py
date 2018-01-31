import csv
import sys
csv.field_size_limit(sys.maxsize)

class CsvFileCreator:
    def __init__(self, file_name):
        self.file_name = file_name
        self.csvfile = open("{}.csv".format(file_name), 'w+', encoding='utf8', newline='')
        self.write = csv.writer(self.csvfile)

    def write_row(self, row):
        self.write.writerow(row)

    def close(self):
        self.csvfile.close()



d = dict()
data = None
csvf = CsvFileCreator("none")
last_data = None
with open('TMP.csv', 'rt', encoding='utf8') as csvfile:
    spamreader = csv.reader(csvfile, quotechar='|')
    for row in spamreader:
        if len(row):
            print(row[-1])
            if data!=row[0]:
                try:
                    # print("try")
                    csvf.close()
                finally:
                    data=row[0]
                    csvf = CsvFileCreator(data.replace('/', '-'))
                    csvf.write_row(row)
            else:
                csvf.write_row(row)






#             if word in d:
#                 d[word]=d[word]+1
#             else:
#                 d[word]=1
# for k, v in d.items():
#     print(k,v)