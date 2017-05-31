Extracts Information from GFF3 files (version 1.23) as described by Lincoln Stein 
    Description of file format can be found at -
    https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md 

Project created for Computer Concepts Final Question #5

Originally Created: August 22, 2015

Tested using Python 3.4.0

Example:
        $ export_gff3_feature.py --source_gff=/path/to/some.gff3 --type=gene --attribute=ID --value=YAR003W
        This will parse the gff3 file to find a gene with the ID YAR003W and print out the corresponding sequence
        Outputs to screen:              
		>gene:ID:YAR003W
		....sequence....		

    Required Command Line Arguments: --source_gff=/path/to/some.gff3 and at least one other search feature
                                     
    Command Line Arguments (for more information on the term definitions please see website above):
        --source_gff:	The gff3 file
        --seqid:        1st column in GFF3 
        --source:       2nd column
        --type:         3rd column
        --start:        4th column
        --end:          5th column
        --score:        6th column
        --strand:       7th column
        --phase:        8th column
        --attribute + --value:	9th column which has a key=value pair description

AUTHOR: Kim Lauer

FURTHER INSTRUCTIONS:

	outputs (+) strand sequence (if seq on (-) strand, determines complement and prints it out)
	
	**Will ONLY OUTPUT ONE MATCH**
