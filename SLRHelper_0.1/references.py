class Reference():
    def __init__(self):
        self.title = " "
        self.url = " "
        self.author = " "
        self.misc = " "
        self.year = " "
        self.appearance=0
    
    def Populate_with_dic(self,rdict):
        self.title = rdict['title'].lower()
        self.url = rdict['url']
        self.author = rdict['author'].lower()
        self.misc = rdict['misc'].lower()
        self.year = rdict['year']
        self.appearance=1

    def create_Ref(self,ref):
        if 'title' in ref:
            self.title = str(ref['title']).split("'")[1].lower()
        else :
            self.title="unknow title"
        if 'url' in ref:
            self.url = str(ref['url']).split("'")[1]
        else :
            self.url="unknow url"
        if 'author' in ref:
            self.author = str(ref['author']).split("'")[1].lower()
        else :
            self.author="unknow author"
        if 'misc' in ref:
            self.misc = str(ref['misc']).split("'")[1].lower()
        else :
            self.misc="unknow misc"
        if 'year' in ref:
            self.year = str(ref['year']).split("'")[1].lower()
        else :
            self.year="unknow year"
        self.appearance=1
    
    def get_ID(self):
        return self.author.split()[0]+self.year+self.title.split()[0]

    def __str__(self):
        return self.title+" authored by "+self.author+" in "+self.misc
    
    def CSV_Line(self):
        return self.title+";"+self.url+";"+self.author+";"+self.misc+";"+self.year+";"


def RefCompare(R1, R2, lvl):
    score=0
    if R1.title == R2.title and R1.title != "unknow title":
        score+=8
    else :
        if R1.title != R2.title :
            if R1.title == "unknow title" :
                if R2.title in R1.misc :
                    score += 8
            if R2.title == "unknow title" :
                if R1.title in R2.misc :
                    score+=8
            
    if  R1.author != "unknow author" and R1.author != "unknow author":
        auth1=R1.author.split(',')
        auth2=R2.author.split(',')
        if len(auth1) == len(auth2) :
            for a1 in auth1 :
                if a1 in auth2 :
                    score+=int((5/len(auth1)))
    if R1.title == "unknow title" and R1.author == "unknow author"  and R2.title == "unknow title" and R2.author == "unknow author":
        w1=R1.misc.split('.')
        w2=R2.misc.split('.')
        for w in w1 :
            if w in w2 :
                score+=5
    if R1.url == R2.url and R1.url != "unknow url":
        score+=3
    if R1.misc == R2.misc and R1.misc != "unknow misc":
        score+=2
    if R1.year == R2.year and R1.year != "unknow year" :
        score+=1
    if str(R1) == str(R2):
        score += 5
    if score >= lvl :
        return True
    else:
        return False

def MergeRef(R1,R2, lvl):
    if RefCompare(R1,R2,lvl) :
        R1.appearance+=1
        return [R1]
    else :
        return [R1,R2]

def Merge_List_Ref(R1,L2,lvl):
    add = True
    for r in L2 :
        if RefCompare(R1,r,lvl):
            r.appearance+=R1.appearance
            add = False
            break
    if add :
        L2.append(R1)
    return L2

def Filtre_title(Ref,Kwords,lvl):
    filtre=[]
    for r in Ref :
        total=0
        for w in r.title.split(' '):
            if w in Kwords :
                total+=1
        for w in r.misc.split(' '):
            if w in Kwords :
                total+=1
        if total >= lvl :
            filtre.append(r)
    return filtre


def MergeList(L1,L2,lvl):
    final=[]
    if isinstance(L2,list):
        #L2 = List
        if isinstance(L1,list):
            #L1 & L2 = List
            for r2 in L2:
                add = True
                for r1 in L1 :
                    if RefCompare(r1,r2,lvl) == True:
                        r1.appearance+=r2.appearance 
                        add = False
                        break
                if add == True :
                    final.append(r2)
            final.extend(L1)
        else :
            #R1 & L2
            final=Merge_List_Ref(L1,L2,lvl)
    else:
        # R2
        if isinstance(L1,list):
            #L1 & R2 = List
            final=Merge_List_Ref(L2,L1,lvl)
        else :
            #R1 & R2
            final=MergeRef(L1,L2,lvl)
    return final

def dump_extract(file):
    L=[]
    with open(file,'r') as sf:
        for line in sf:
            ref={}
            fields=line.split(";")
            ref['title'] = fields[0]
            ref['url'] = fields[1]
            ref['author'] = fields[2]
            ref['misc'] = fields[3]
            ref['year'] = fields[4]
            r = Reference()
            r.Populate_with_dic(ref)
            L.append(r)
    return L


def Merge_All_List(L,lvl):
    if len(L) > 2:
        # Divide by 2 and recursive
        L1=[]
        L2=[]
        for i in range(int(len(L)/2)):
            L1.append(L[i])
        for j in range(i+1,len(L)):
            L2.append(L[j])
        return MergeList(Merge_All_List(L1,lvl),Merge_All_List(L2,lvl),lvl)
    else :
        if len(L) == 1 :
            return L
        else :
            #print("L0 = "+str(L[0]))
            #print("L1 = "+str(L[1]))
            return MergeList(L[0],L[1],lvl)

def filtre(L,app):
    final=[]
    for r in L :
        if r.appearance >= app :
            final.append(r)
    return final

def genBib(L, file):
    with open(file,'w') as bibFile:
        for ref in L:
            bibref="@MISC{"+ref.author.split(' ')[1]+ref.year+ref.title.split(' ')[0]+",\n"
            bibref+="author = {"+ref.author+"},\n"
            bibref+="misc = {"+ref.misc+"},\n"
            bibref+="title = {"+ref.title+"},\n"
            bibref+="year = {"+ref.year+"},\n"
            if ref.url != "unknow url" :
                bibref+="url = {"+ref.url+"},\n}"
            else :
                bibref+="}\n"
            bibFile.writelines([bibref,'\n'])