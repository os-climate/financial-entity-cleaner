import csv


def read_test_file(filename, list_obj):
    file_obj = open(filename, "r")
    csv_reader = csv.reader(file_obj, delimiter=",")
    next(csv_reader)  # skip header
    for row in csv_reader:
        list_obj.append(row)
    file_obj.close()
