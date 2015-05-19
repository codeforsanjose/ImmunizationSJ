#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# intended for SQLite 3
#

import sqlite3

IMMUNIZATION_DATABASE_NAME = 'immune.db'

SQL_CREATE_TABLE_SCHOOLS = "CREATE TABLE schools (\
        school_code                          INTEGER NOT NULL PRIMARY KEY,\
        school_name                                         TEXT NOT NULL,\
        district                                            TEXT NOT NULL,\
        is_public    BOOLEAN NOT NULL CHECK (is_public IN (0,1)) NOT NULL,\
        address                                                      TEXT,\
        city                                                TEXT NOT NULL,\
        zip                                                          TEXT,\
        county                                              TEXT NOT NULL\
    );"

SQL_CREATE_TABLE_RECORDS = "CREATE TABLE records (\
        ID                      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
        school                     INTEGER references schools(school_code),\
        grade                                                         TEXT,\
        year                                                       INTEGER,\
        reported       BOOLEAN NOT NULL CHECK (reported IN (0,1)) NOT NULL,\
        enrollment                                                 INTEGER,\
        num_conditional                                            INTEGER,\
        num_DTP                                                    INTEGER,\
        num_health_care_practitioner_counseled_PBE                 INTEGER,\
        num_HEPB                                                   INTEGER,\
        num_MMR                                                    INTEGER,\
        num_PBE                                                    INTEGER,\
        num_PME                                                    INTEGER,\
        num_polio                                                  INTEGER,\
        num_pre_Jan_PBE                                            INTEGER,\
        num_religious_PBE                                          INTEGER,\
        num_up_to_date                                             INTEGER,\
        num_vari                                                   INTEGER\
    );"

SQL_DROP_TABLE_SCHOOLS = "DROP TABLE IF EXISTS schools;"
SQL_DROP_TABLE_RECORDS = "DROP TABLE IF EXISTS records;"

def create_tables():
    conn = sqlite3.connect(IMMUNIZATION_DATABASE_NAME)
    cur = conn.cursor()
    
    cur.execute(SQL_CREATE_TABLE_SCHOOLS)
    cur.execute(SQL_CREATE_TABLE_RECORDS)

    conn.commit()
    cur.close()
    conn.close()
    print("tables created")

def drop_tables():
    # TODO: get confirmation before dropping.
    conn = sqlite3.connect(IMMUNIZATION_DATABASE_NAME)
    cur = conn.cursor()
    
    cur.execute(SQL_DROP_TABLE_RECORDS)
    cur.execute(SQL_DROP_TABLE_SCHOOLS)

    conn.commit()
    cur.close()
    conn.close()
    print("tables dropped")

def load_dummy_schools():
    conn = sqlite3.connect(IMMUNIZATION_DATABASE_NAME)
    cur = conn.cursor()
    
    cur.execute("INSERT INTO schools VALUES (123, 'Test School', 'Farmington', 1, 'Camarillo', 'Ventura');")
    cur.execute("INSERT INTO schools VALUES (124, 'Test School 2', 'Farmington', 0, 'Camarillo', 'Ventura');")

    cur.execute("INSERT INTO records (school, grade, year, reported) VALUES (123, 'K', '2014', 1);")

    conn.commit()
    cur.close()
    conn.close()
    print("row(s) inserted")


def insert_school(school):
    school_code = int(school['SCHOOL CODE'])
    if school_exists(school_code):
        return

    conn = sqlite3.connect(IMMUNIZATION_DATABASE_NAME)
    cur = conn.cursor()

    school_row = {
        'school_code' : school_code,
        'school_name' : school['SCHOOL NAME'],
        'district' : school['PUBLIC SCHOOL DISTRICT'],
        'is_public' : 1 if school['PUBLIC/  PRIVATE'] == 'PUBLIC' else 0,
        'city' : school['CITY'],
        'county' : school['COUNTY'],
        'address' : None,
        'zip' : None
    }

    cur.execute("""
        INSERT INTO schools (school_code, school_name, district, is_public, address, city, zip, county) 
        VALUES (:school_code, :school_name, :district, :is_public, :address, :city, :zip, :county);""", 
        school_row)
    
    conn.commit()
    cur.close()
    conn.close()
    return 1

def school_exists(school_code):
    """
    >>> school_exists(109835)
    True
    >>> school_exists(999)
    False
    """
    conn = sqlite3.connect(IMMUNIZATION_DATABASE_NAME)
    cur = conn.cursor()
    
    cur.execute("Select exists (select 1 from schools where school_code=?);", (school_code,))
    res = bool(cur.fetchone()[0])

    conn.commit()
    cur.close()
    conn.close()
    return res

def insert_record(record, grade, year):
    """
    """

    conn = sqlite3.connect(IMMUNIZATION_DATABASE_NAME)
    cur = conn.cursor()

    row =  (
                record['SCHOOL CODE'],
                grade,
                int(year), 
                1 if record['REPORTED'] in ('Y','y') else 0,
                cleanInt(record['ENROLLMENT']),
                cleanInt(record['# CONDITIONAL']),
                cleanInt(record['# DTP']),
                cleanInt(record['# HEALTH CARE PRACTITIONER COUNSELED PBE']),
                cleanInt(record['# HEPB']),
                cleanInt(record['# MMR']),
                cleanInt(record['# PBE']),
                cleanInt(record['# PME']), 
                cleanInt(record['# POLIO']),
                cleanInt(record['# PRE-JAN PBE']),
                cleanInt(record['# RELIGIOUS PBE']),
                cleanInt(record['# UP-TO-DATE']),
                cleanInt(record['# VARI'])
            )

    # TODO: change from '?' to named placeholders
    ret = cur.execute("INSERT INTO records "
            + "(school, grade, year, reported, enrollment, num_conditional, num_DTP, num_health_care_practitioner_counseled_PBE, num_HEPB, num_MMR, num_PBE, num_PME, num_polio, num_pre_Jan_PBE, num_religious_PBE, num_up_to_date, num_vari ) "
            + "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
           row
        )

    conn.commit()
    cur.close()
    conn.close()


def select_all():
    conn = sqlite3.connect(IMMUNIZATION_DATABASE_NAME)
    cur = conn.cursor()
    
    print("SCHOOLS:")
    print("="*80)
    for row in cur.execute("SELECT * FROM schools;"):
        print(str(row)+"\n")

    print("RECORDS:")
    print("="*80)
    for row in cur.execute("SELECT * FROM records;"):
        print(str(row)+"\n")

    conn.commit()
    cur.close()
    conn.close()

def select_top():
    conn = sqlite3.connect(IMMUNIZATION_DATABASE_NAME)
    cur = conn.cursor()
    
    print("SCHOOLS (10):")
    print("="*80)
    for row in cur.execute("SELECT * FROM schools LIMIT 10;"):
        print(str(row)+"\n")

    print("RECORDS (10):")
    print("="*80)
    for row in cur.execute("SELECT * FROM records LIMIT 10;"):
        print(str(row)+"\n")

    conn.commit()
    cur.close()
    conn.close()


def select_count():
    conn = sqlite3.connect(IMMUNIZATION_DATABASE_NAME)
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM schools;")
    res = cur.fetchone()[0]
    print("SCHOOLS COUNT: "+str(res))

    cur.execute("SELECT COUNT(*) FROM records;")
    res = cur.fetchone()[0]
    print("RECORDS COUNT: "+str(res))

    conn.commit()
    cur.close()
    conn.close()

def cleanInt(dirty):
    return int(0 if dirty in ('', ' ') else dirty)

import sys, doctest, argparse
def main():
    # doctest.testmod()
    parser = argparse.ArgumentParser(prog='db_utils')
    parser.add_argument('action', choices=['create', 'count', 'drop', 'dummy', 'select', 'top'])
    args = parser.parse_args()
    if args.action == 'create':
        create_tables()
    if args.action == 'count':
        select_count()
    elif args.action == 'drop':
        drop_tables()
    elif args.action == 'dummy':
        load_dummy_schools()
    elif args.action == 'select':
        select_all()
    elif args.action == 'top':
        select_top()


if __name__ == '__main__':
    main()