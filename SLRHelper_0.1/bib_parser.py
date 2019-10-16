import os
import bibtexparser
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

#from pygraphviz import *
BASE_DIR="./Results/"

def autolabel(rects,ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width(), height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

# Function to generate the list of all requests 
def GenRequest(req):
    requests=[]
    for r1 in req[0]:
        for r2 in req[1]:
            request=r1+" "+r2
            requests.append(request)
    return requests

# To create all the ID of the folders within the Results folder.
# Each one is created as : Number_1stAuthor_Year_1stTitleWord
def recupID(requests,path):
    ida={}
    if not os.path.isdir("bib") :
        print("[!] Error bib folder missing")
        sys.exit()
    else :
        os.chdir("bib")
        db = bibtexparser.bibdatabase.BibDatabase()
        for r in requests:
            file=r+".bib"
            with open(file) as bibtex_file:
                #print("open :"+str(file))
                bib_database = bibtexparser.load(bibtex_file)
                # Merge ref by ID
                for ref in bib_database.entries:
                    if ref['ID'] not in ida:
                        ida[ref['ID']]=[r]
                        db.entries.append(ref) # to generate the final bib file
                    else :
                        ida[ref['ID']].append(r)
        print("[*] Total of differents references = "+str(len(ida)))
        os.chdir(path)
        with open("final.bib",'w') as bibtex_file :
            writer= bibtexparser.bwriter.BibTexWriter()
            bibtex_file.write(writer.write(db))
        #print(str(ida))
        return ida, db

def CheckFile(file, abort):
    if not os.path.isfile(file):
        print("[!] Error the file "+file+" doesn't exist")
        if abort :
            print("[!] Abort")
            sys.exit()
        else :
            return False
    else :
        return True

def Mergefinal(base,snow):
    if CheckFile(base,True) and CheckFile(snow,True):
        db = bibtexparser.bibdatabase.BibDatabase()
        with open(base) as baseFile:
            with open(snow) as snowFile:
                base_bib=bibtexparser.load(baseFile)
                snow_bib=bibtexparser.load(snowFile)
                # check all ref in base file
                for bref in base_bib.entries:
                    add = True
                    # compare to all ref in snow file
                    for sref in snow_bib.entries:
                        # if their are identical, we can add one of them to the final bib and stop the loop
                        if bref['ID'] == sref['ID'] :
                            add = False
                            db.entries.append(bref)
                            break
                    if add :
                        db.entries.append(bref)
                        db.entries.append(sref)
        return db



# To generate a txt file and a CSV file for each request where the paper appears
def GenDoc(directory,request,path,CSV,TEXTE,title):
    os.chdir(directory)
    fname="analyse.txt"
    with open(fname,"w") as f:
        f.writelines([title,'\n'])
        for t in TEXTE:
            f.writelines([t,'\n'])
        f.close()
    for r in request:
        fname=r+".csv"
        with open(fname,"w",newline='\n') as csvfile:
            csvwrite=csv.writer(csvfile, delimiter=';',quotechar="'")
            csvwrite.writerow(CSV)
    os.chdir(path)


def GetTitleFromRef(ref, db):
    for r in db.entries:
        if r['ID'] == ref :
            return r['title']

# To create all the directories with the good number
def GenDirectories(ida,request,idt,path,CSV,TEXTE,db):
    if not os.path.exists(BASE_DIR):
        os.mkdir(BASE_DIR)
    i=0
    for t in idt:
        if i < 10:
            num="00"
            num+=str(i)
        elif i < 100 :
            num="0"
            num+=str(i)
        else :
            num=str(i)
        os.chdir(BASE_DIR)
        directory=num+"_"+str(t[0])
        os.mkdir(directory)
        finalR=[]
        for r in ida[t[0]] :
            if r in request and r not in finalR:
                finalR.append(r)

        title=GetTitleFromRef(t[0], db)
        GenDoc(directory,finalR,path,CSV,TEXTE,title)
        i+=1

def GenGraph(ida,requests):
    name="Relation articles - requetes"
    G=AGraph(strict=False,directed=True, size="100,100", overlap="scalexy",ranksep="1.2",nodesep="1.5",fontsize="80")
    for r in requests:
        n={'name':r,'fontsize':12,'size':15}
        G.add_node(r,shape='circle', fixedsize=True, width="15", height = "15",fontsize="12", penwidth="2")
    #print(str(nodes))
    for i,v in ida.items():
        n={'name':i,'fontsize':8*len(v),'size':len(v)*4}
        G.add_node(i,shape='circle', fixedsize=True, width=str(4*len(v)), height = str(4*len(v)),fontsize=str(4*len(v)), penwidth="2")
        for r in v:
            G.add_edge(i,r, style="bold", penwidth=5.5,arrowtail="none", labeldistance=20, labelfloat=True)
    G.write("test.dot")
    G.layout(prog='dot')
    G.draw('test.png')
    G.draw('test.ps',prog='circo')
    # nx.draw(G, pos=nx.circular_layout(G), with_labels=True, font_weight='bold',node_size =[500 * v for v in nodeSize])
    # nx.drawing.nx_pydot.write_dot(G,"test.dot")
    # plt.show()

def sort(ida):
    d={}
    for ref,req in ida.items():
        d[ref]=len(req)
    idt=sorted(d.items(), key=lambda t: t[1])
    idt.reverse()
    #print(str(idt))
    return idt

def ShowBar(idt):
    labels=[]
    values=[]
    width=0.35
    fig, ax = plt.subplots()
    for t in idt:
        labels.append(t[0])
        values.append(t[1])
    #print(str(values))
    x=np.arange(len(labels))
    rects=ax.bar(x, values)
    ax.set_ylabel("nombre d'apparitions")
    ax.set_title("nombre d'apparitions par article")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    autolabel(rects,ax)
    fig.autofmt_xdate()
    plt.show()



