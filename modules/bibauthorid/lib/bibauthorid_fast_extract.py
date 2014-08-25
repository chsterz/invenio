#!/usr/bin/python

import invenio.bibauthorid_name_utils as name_utils
import invenio.dbquery as db
import time


def retrieve_author_data(fields=["100__a","100__u","100__i"]):
    """ performs the Database-Query based on the fields specified in the list 'fields' """

    dbquery_prefix = 'SELECT b.tag, b.value FROM bib10x AS b, bibrec_bib10x AS bb WHERE b.id=bb.id_bibxxx AND '

    dbquery_fields = '(b.tag LIKE '
    #fill in the fields
    for field in fields[:-1]: dbquery_fields += '"' + field + '"' + ' or b.tag LIKE '
    dbquery_fields += '"' + fields[-1] + '"' + ') '

    dbquery_postfix =  'ORDER BY bb.id_bibrec, bb.field_number, b.tag ASC;'

    dbquery = dbquery_prefix + dbquery_fields + dbquery_postfix
    return db.run_sql(dbquery)

def retrieve_coauthor_data(fields=["700__a","700__u","700__i"]):
    """ performs the Database-Query based on the fields specified in the list 'fields' """

    dbquery_prefix = 'SELECT b.tag, b.value FROM bib70x AS b, bibrec_bib70x AS bb WHERE b.id=bb.id_bibxxx AND '

    dbquery_fields = '(b.tag LIKE '
    #fill in the fields
    for field in fields[:-1]: dbquery_fields += '"' + field + '"' + ' or b.tag LIKE '
    dbquery_fields += '"' + fields[-1] + '"' + ') '

    dbquery_postfix =  'ORDER BY bb.id_bibrec, bb.field_number, b.tag ASC;'

    dbquery = dbquery_prefix + dbquery_fields + dbquery_postfix
    return db.run_sql(dbquery)


def postprocess_and_collate_authors():
    """ puts together the given fields and transforms names Puts all in a set"""
   
    print "[*] Performing database query..."

    t0 = time.time() 
    print "[*] Getting Author Information"
    author_result = retrieve_author_data()
    print "[*] Done," , len(author_result), "fields fetched"
    print "[*] Getting Coauthor Information"
    coauthor_result = retrieve_coauthor_data()
    print "[*] Done," , len(coauthor_result), "fields fetched"
    sql_result = author_result + coauthor_result
    t1 = time.time() 

    print "[*] Database Query OK. Took:", t1-t0, "seconds"
 
    name_set = set()

    #ATTENTION: assuming the 3 standard datafields here. If you include more
    #           you have to change the following code.
   
    #everytime we see a new author we add the last processed dataset to the set. 
    t0 = time.time()
    print "[*] Creating Matchable Authornames"
    author_tuple_proto = ["", "", ""]
    for index, row in enumerate(sql_result):
        if (index and index % 1000000 == 0): print "[*] Processed", index/1000000 ,"M Entries"
        subfield = row[0][-1]
        if  (subfield == "a"):
            if(author_tuple_proto != ["","",""]): name_set.add(tuple(author_tuple_proto));
            author_tuple_proto = ["","",""]
            author_tuple_proto[0] = name_utils.create_matchable_name(row[1])
        elif(subfield == "u"):
            author_tuple_proto[1] = row[1]
        elif(subfield == "i"):
            author_tuple_proto[2] = row[1]
    
    t1 = time.time()
    print "[*] Done Preprocessing Data. Took:", t1-t0, "seconds"
    print "[*] Number of distinct Author Records left after this step:", len(name_set)

    return name_set

postprocess_and_collate_authors()
