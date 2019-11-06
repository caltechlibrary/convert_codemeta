from pyld import jsonld
import csv,os,json

def build_context():
    '''Build up dictionary of contextx from crosswalk table'''
    with open(os.path.dirname(__file__)+'/crosswalk.csv',newline='') as infile:
        reader = csv.reader(infile, delimiter=',')
        context = {}
        crosswalks = next(reader)
        #Initialize context for each known crosswalk
        for cross in crosswalks:
            context[cross] = {}
        #Now add context for every row
        for row in reader:
            index = 0
            for value in row:
                if value != '':
                    context[crosswalks[index]][value] = {"@id":row[0]}
                index = index + 1

def crosswalk(json,from_format,to_format='codemeta',trim=True):
    context = build_context()
    print(context)

