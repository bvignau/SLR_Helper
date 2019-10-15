import configparser
#from refextract import extract_references_from_file
import argparse
import shutil
import sys
import subprocess
from os import path, mkdir

BASE_DIR="./Results/"
pathname = path.dirname(sys.argv[0]) 
SOURCE_DIR=pathname = path.abspath(pathname)+"/"
#####################################################
#
# To extract all ref in all pdf in a directory
# all = Extract_From_Dir(BASE_DIR)              
# save_extract(all,"save_ref.csv")
#
#####################################################


#####################################################
#
# To load all ref in a CSV
# all = dump_extract("save_ref.csv")
# print("all => "+str(len(all)))        
#
#####################################################

def ConfigParse():
    config = configparser.ConfigParser()
    config.read('SLR.conf')
    requests=[]
    for i in range(len(config['Request'])):
        r="r"+str(i)
        requests.append(config['Request'][r].split(','))
    CSV=config['RQ']['CSV'].split(',')
    TEXTE=config['RQ']['Text'].split(',')
    COMPARISON=int(config['Filter']['comparison'])
    APPEARANCE=int(config['Filter']['appearance'])
    NKWORDS=int(config['Filter']['NKwords'])
    KWORDS=config['Filter']['Kwords'].split(',')
    print("Requests = "+str(requests))
    print("CSV = "+str(CSV))
    print("Texte = "+str(TEXTE))
    print("COMPARISON = "+str(COMPARISON))
    print("APPEARANCE = "+str(APPEARANCE))
    print("KWORDS = "+str(KWORDS))
    return requests,CSV,TEXTE, COMPARISON, APPEARANCE, KWORDS, NKWORDS



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    arg = parser.parse_args()
    if arg.command not in ["snowball","mergeBib","start"]:
        print("Error, unknow command")
        print("Use : 'SRLHelper start' to create a directory and a empty config file")
        print("Use : 'SRLHelper mergeBib' to merge all the bib file in the 'bib' folder, print some stats about the bib files merged, and create folders for each paper to analyse.")
        print("Use : 'SRLHeper snowball' to dump all references from all PDF in all sub folders of the 'Results' folder, create a CSV file with all extracted references, and a bib file with all the filtered references.")
    else : 
        if arg.command == "start":
            if path.isdir(BASE_DIR) == False:
                mkdir(BASE_DIR)
                srcConf=SOURCE_DIR+"empty.conf"
                shutil.copyfile(srcConf,"SLR.conf")
                mkdir("./bib")
            else :
                print("Error folder already exist")
        if arg.command == "mergeBib":
            requests,CSV,TEXTE, COMPARISON, APPEARANCE, KWORDS, NKWORDS = ConfigParse()
            r = GenRequest(requests)
            print("r => "+str(r))
            path=path.abspath(path.split(__file__)[0])
            ida,db = recupID(r,path)
            print("\n\n R2 = "+str(r))
            idt=sort(ida)
            ShowBar(idt)
            #GenGraph(ida,r)
            GenDirectories(ida,r,idt,path,CSV,TEXTE,db)
        if arg.command == "snowball":
            requests,CSV,TEXTE, COMPARISON, APPEARANCE, KWORDS,NKWORDS = ConfigParse()
            cmd=subprocess.run(["./ref_extractor.py",BASE_DIR,"ref.csv"],capture_output=True)
            all = dump_extract("ref.csv")
            snowball=Merge_All_List(all,COMPARISON)
            final=filtre(snowball,APPEARANCE)
            final=Filtre_title(final,KWORDS,NKWORDS)
            genBib(final,"snowball.bib")


if __name__ == '__main__':
    main()