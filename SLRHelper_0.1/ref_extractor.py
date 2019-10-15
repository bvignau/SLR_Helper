#!/bin/python2
from refextract import extract_references_from_file
from os import chdir, listdir, path, mkdir
from references import Reference
import argparse

# A class to get the main part of a reference and function to compare references

def Extract_From_Dir(path):
    chdir(path)
    all=[]
    i=0
    for d in listdir('.'):
        #print(str(d))
        chdir(d)
        for d2 in listdir('.'):
            #print(str(d2))
            if 'pdf' in d2.split('.'):
                print("dossier => "+d+" pdf "+str(i)+" => "+d2)
                i+=1
                all.extend(Extract_Ref_From_PDF(d2))
        chdir('../')
    chdir('../')
    return all

def Extract_Ref_From_PDF(path):
    references = extract_references_from_file(path)
    all=[]
    for r in references:
        ref=Reference()
        ref.create_Ref(r)
        all.append(ref)
    return all

def save_extract(L,file):
    with open(file,'w') as sf:
        for ref in L :
            sf.writelines([ref.CSV_Line(),'\n'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory')
    parser.add_argument('save')
    arg = parser.parse_args()
    if path.isdir(arg.directory) == False:
        print("erreur le dossier n'existe pas")
    else :
        all = Extract_From_Dir(arg.directory)
        save_extract(all,arg.save)
        print("creation du csv : "+arg.save)
        




if __name__ == '__main__':
    main()