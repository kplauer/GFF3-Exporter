#!/usr/bin/env python3
# Kim Lauer
# Computer Concepts Final Question #5
# 8/22/15
# Extracts info from GFF3 files (version 1.23) described by Lincoln Stein

import re, argparse

# creates dict of options used at command prompt
command_line = {}

# list created to use keys in dict
key_list = []

# list created for ouput
output_list = []

# list created to store matching chromosome seq
# to find seq start and stop points
chromosome_match = []

# parses the command line and finds options
parser = argparse.ArgumentParser()
parser.add_argument('--source_gff')
parser.add_argument('--seqid', default="null")
parser.add_argument('--source', default="null")
parser.add_argument('--type', default="null")
parser.add_argument('--start', default="null")
parser.add_argument('--end', default="null")
parser.add_argument('--score', default="null")
parser.add_argument('--strand', default="null")
parser.add_argument('--phase', default="null") 
parser.add_argument('--attribute', default="null")
parser.add_argument('--value', default="null")
args = parser.parse_args()

# adds options to list only if entered at command prompt
seqid = args.seqid
if seqid != 'null':
    command_line[1] = seqid
    key_list.append(1)

source = args.source
if source != 'null':
    command_line[2] = source
    key_list.append(2)

vtype = args.type
if vtype != 'null':
    command_line[3] = vtype
    key_list.append(3)

vstart = args.start
if vstart != 'null':
    command_line[4] = vstart
    key_list.append(4)

vend = args.end
if vend != 'null':
    command_line[5] = vend
    key_list.append(5)

score = args.score
if score != 'null':
    command_line[6] = score
    key_list.append(6)

strand = args.strand
if strand != "null":
    command_line[7] = strand
    key_list.append(7)

phase = args.phase
if phase != 'null':
    command_line[8] = phase
    key_list.append(8)

# combines the key=value pair in 9th column
attribute = args.attribute
value = args.value
if attribute != "null" and value != "null":
    command_line[9] = (attribute + "=" + value)
    key_list.append(9)

# used if not enough info included in command line
if len(command_line) < 2:
    print("Please enter at least one search option")
    exit()

# count used to see if more than one match
count = 0

# True/False variables used in for loop below
in_fasta_section = False
found_match = False

# opens GFF3 file
gff_file = open(args.source_gff)

# removes the first item from the command_line dict
# because it would be the most specific (assuming it
# is col 9) rather than having to break up every line.
# this elimates most lines
search_for = command_line[key_list.pop()]

# adds to output list
output_list.append(search_for)

# loops thru each line
for line in gff_file:

    # using command_line{} created above loops thru each
    # one till it finds a line that has all variable(s)
    # This search is limited to only matching two columns
    if re.search(re.escape(search_for), line, re.I) and len(key_list) > 0:

        # splits line up so can compare column #s for match
        inital_table = line.split()
        column_num = key_list.pop()
        # adds back in for more than one match
        key_list.append(column_num)
        if inital_table[column_num-1] == command_line[column_num]:
            count = count + 1
            found_match = True
            # makes sure to show correct line match of first match
            if count == 1:
                output_list.append(command_line[column_num])
                table = inital_table           
        else:
            continue

    # finds the line before the FASTA seq for the chromosome match
    # i.e. finds >chrI
    elif found_match == True and re.match('>' + table[0] + r'\b', line):
        in_fasta_section = True

    # finds end of chromosome match, by find next '>'
    elif found_match == True and re.match('>', line) and not re.match(table[0] + r'\b', line):
        in_fasta_section = False

    # while in the matching FASTA chromosome sequence, stripping each 
    # line of it's new line characters, storing each line into a list 
    # and appending a second list.  
    elif in_fasta_section == True:
        line = line.rstrip()
        split_line = list(line)
        chromosome_match.extend(split_line)
    else:
        continue 

# prints out answer if a match was found
if found_match == True:

    # if search has matched more than once
    if count > 1:
        print("More than one match found, only one shown below")

    # initializes output statement
    output_statement = ""
    
    # reverses output list to print in correct order
    output_list.reverse()

    # loops thru command option list for final output
    while len(output_list) > 0:
        output_statement = output_list.pop().replace("=",":") + ":" + output_statement

    # prints out output statement
    print(">" + output_statement)

    # removes one integer because table values start at 0
    start = int(table[3])-1
    end = int(table[4])-1

    # creates a list with matching sequence
    seq_match = []
    seq_end = start
    while seq_end <= end:
        seq_match.append(chromosome_match[seq_end])
        seq_end = seq_end + 1

    # finds complement if on negative strand
    if table[6] == '-':
        list_len = len(seq_match)
        complement = []
        while list_len > 0:

            # removes one char from list, finds it complement
            # and adds to the complement list
            nuc = seq_match.pop()
            if nuc == 'A':
                complement.extend('T')
                list_len = len(seq_match)
                continue
            elif nuc == 'T':
                complement.extend('A')
                list_len = len(seq_match)
                continue
            elif nuc == 'C':
                complement.extend('G')
                list_len = len(seq_match)
                continue
            elif nuc == 'G':
                complement.extend('C')
                list_len = len(seq_match)
                continue

        # prints out complement dna sequence
        # print("length of seq_match is " + str(len(seq_match)))
        line_start = 0
        line_end = line_start + 60
        while line_start < len(complement):
            print("".join(complement[line_start:line_end]))
            line_start = line_end
            line_end = line_end + 60

    # prints out dna sequence if on + or . strand
    else:
        line_start = 0
        line_end = line_start + 60
        while line_start < len(seq_match):
            print("".join(seq_match[line_start:line_end]))
            line_start = line_end
            line_end = line_end + 60

# message if there were no hits
else:
    # initializes output statement
    output_statement = ""
    
    # reverses output list to print in correct order
    output_list.reverse()

    # loops thru command option list for final output
    while len(output_list) > 0:
        output_statement = output_list.pop().replace("=",":") + ":" + output_statement

    # prints out output statement
    print(">" + output_statement)
    print("No matches")
