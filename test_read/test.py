import sys

FILE_NAME = 'raw_data.txt'
NEW_FILE = 'newfile.csv'

def retrieve_stored_data(file_name):
        f_read = open(file_name, 'r')
        raw_data = str(f_read.read().split(","))
        f_read.close()
        return raw_data

def store_raw_data(raw_data, file_name):
        f_write = open(file_name, 'w')
        f_write.write(str(raw_data))
        f_write.close()
        return raw_data


answer = retrieve_stored_data(FILE_NAME)
written = store_raw_data(answer, NEW_FILE)

print(type(answer))