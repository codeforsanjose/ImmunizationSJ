

#!/usr/bin/python
# -*- coding: latin-1 -*-
# csv_to_json.py
# slurp in the csv file and output the results as JSON
#

from StringIO import StringIO
import csv, json, optparse

from db_utils import insert_school, insert_record

GRADES = ('PK','K','1','2','3','4','5','6','7','8','9','10','11','12')

def csvfile_in(csvfilename):
    csv_dump = []
    with open(csvfilename, 'rb') as csvfile:
        raw_dump = csv.DictReader(csvfile)
        # raw_dump = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in raw_dump:
            csv_dump.append(dict((k, v.decode('utf-8', 'replace')) for k, v in row.items()))
    return csv_dump

def sql_insert_csvdump(csv_dump, grade, year):
    for row in csv_dump[1:]:    # Skip first row, which is the column headers
        insert_school(row)
        insert_record(row, grade, year)


import sys, doctest
def main():
    doctest.testmod()
    parser = optparse.OptionParser()
    parser.add_option('-i', '--in-file', help='input file name (.csv)')
    parser.add_option('-g', '--grade', help='The grade applicable to the given data (K-12)')
    parser.add_option('-y', '--year', help='The four-digit school year when the data was collected')
    (options, args) = parser.parse_args()

    if not options.in_file:
        parser.print_help()
        parser.error("an input file must be given")
    if not options.year or len(options.year) is not 4 or not 1900 < int(options.year) < 2200:
        parser.print_help()
        parser.error("a valid four-digit year must be given")
    if not options.grade or options.grade not in GRADES:
        parser.print_help()
        parser.error("a valid grade must be given, one of: "+str(GRADES))

    print("Inserting the CSV data into the SQLite database")
    parsed_data = csvfile_in(options.in_file)
    sql_insert_csvdump(parsed_data, options.grade, options.year)
    print('done')


if __name__ == '__main__':
    main()
