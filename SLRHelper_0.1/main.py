import configparser
#from refextract import extract_references_from_file
from bib_parser import GenRequest, recupID, ShowBar, GenDirectories, sort, ShowBar, Mergefinal
from references import dump_extract, Merge_All_List, filtre, Filtre_title, genBib
import argparse
import shutil
import sys
import subprocess
import os as os

#TODO VERBOSE COMMAND

BASE_DIR="./Results/"
pathname = os.path.dirname(sys.argv[0]) 
SOURCE_DIR=pathname = os.path.abspath(pathname)+"/"

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
    #print("Requests = "+str(requests))
    #print("CSV = "+str(CSV))
    #print("Texte = "+str(TEXTE))
    #print("COMPARISON = "+str(COMPARISON))
    #print("APPEARANCE = "+str(APPEARANCE))
    #print("KWORDS = "+str(KWORDS))
    return requests,CSV,TEXTE, COMPARISON, APPEARANCE, KWORDS, NKWORDS



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    arg = parser.parse_args()
    if arg.command not in ["snowball","mergeBib","start","final"]:
        print("Error, unknow command")
        print("Use : 'slrh start' to create a directory and a empty config file")
        print("Use : 'slrh mergeBib' to merge all the bib file in the 'bib' folder, print some stats about the bib files merged, and create folders for each paper to analyse.")
        print("Use : 'slrh snowball' to dump all references from all PDF in all sub folders of the 'Results' folder, create a CSV file with all extracted references, and a bib file with all the filtered references.")
    else : 
        if arg.command == "start":
            if os.path.isdir(BASE_DIR) == False:
                os.mkdir(BASE_DIR)
                print("[+] The Results Folder will contain later the folders for the pdf to analyse")
                srcConf=SOURCE_DIR+"empty.conf"
                if os.path.isfile("SLR.conf"):
                    print("[!] Error SLR.conf already created")
                    print("[!] Please complete it")
                else :
                    shutil.copyfile(srcConf,"SLR.conf")
                if os.path.isdir("./bib") :
                    print("[!] Error bib folder already created")
                else :
                    os.mkdir("./bib")
                    print("[+] SLRHelper create a folder 'bib' to put your bibfile in")
                print("[+] NOW COMPLETE THE SLR.conf FILE FOR FURTHER USE !")
            else :
                print("Error Results folder already exist")
        if arg.command == "mergeBib":
            requests,CSV,TEXTE, COMPARISON, APPEARANCE, KWORDS, NKWORDS = ConfigParse()
            r = GenRequest(requests)
            print("[+] The request have been generated")
            path=os.getcwd()
            ida,db = recupID(r,path)
            idt=sort(ida)
            ShowBar(idt)
            GenDirectories(ida,r,idt,path,CSV,TEXTE,db)
            print("[+] Directories created in the Results folder. Please fill them with the rigth pdf paper")
        if arg.command == "snowball":
            requests,CSV,TEXTE, COMPARISON, APPEARANCE, KWORDS,NKWORDS = ConfigParse()
            print("[*] Reference extraction from all pdf (may take severals minutes)")
            cmd=subprocess.run(["/usr/bin/SLRHelper_0.1/ref_extractor.py",BASE_DIR,"ref.csv"])
            # TODO VERIF
            print("[+] extraction complete, results in 'ref.csv'")
            all = dump_extract("ref.csv")
            print("[*] Snowball strating (may take severals minutes)")
            snowball=Merge_All_List(all,COMPARISON)
            #TODO VERIF
            print("[*] Merge completed")
            print("[*] "+str(len(snowball))+" differents references extracted")
            final=filtre(snowball,APPEARANCE)
            final=Filtre_title(final,KWORDS,NKWORDS)
            print("[*] "+str(len(final))+" references add after filter")
            genBib(final,"snowball.bib")
            print("[+] BibFile 'snowball.bib' created with all the references to add")
            print("[*] Please check the file and change the unknow ref")
        if arg.command == "final":
            if not os.path.isfile("final.bib"):
                print("[!] Error, missing final.bib")
            else :
                if not os.path.isfile("snowball.bib"):
                    print("[!] Error, missing snowball.bib")
                else:
                    db=Mergefinal("final.bib","snowball.bib")


if __name__ == '__main__':
    main()
