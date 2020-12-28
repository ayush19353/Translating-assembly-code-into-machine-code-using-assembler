import re
def opcode_true_false(s):
    opcode=['CLA', 'LAC', 'SAC', 'ADD', 'SUB', 'BRZ', 'BRN', 'BRP', 'INP', 'DSP', 'MUL', 'DIV', 'STP']
    if(s in opcode):
        return True
    else:
        return False
def opcode_check_and_number(x):
    h=x.split()
    c=0
    for i in h:
        if(opcode_true_false(i)):
            c+=1
    return c
'''
firstpass()-RETURN TYPE=>Dictionary
This function iterates over the text file "test.txt",through iterating it creates a suitable format for checking each line and then reports the errors as soon as they are caught.
While checking for errors it updates the location counter , keeps a marker on each line and updates the dictionary "symbol" for storing symbols as key and their address as value.
At the end it adds a new key into the ditionary,symbol,named "error" for counting the number of errors.

'''

def firstpass():
    error=0
    f=open("test.txt","r")
    comment=0           #initialising comment 
    marker=0            #initialising marker which helps to determine on which line an error is caught
    s=f.readlines()     #reading the lines
    length_lines=len(s)
    lines=[]
    h=[]
    loc=0               #initialising the location counter
    symbol={}           #initialising the ditionary symbol
    label={}
    #The for loop below creates a suitable format for iterating through all the line by splitting.
    
    for i in s:
        stp=i.strip();
        r=re.split('|\n',stp)
        k=""
        for i in r:
            k=k+i
        r=k+'\n'
        h.append(r)

    #This is where ERROR reporting starts.        
    for i in h:
        
        marker+=1                       #remembering which line of file.
        comment=i.find('#')            #searching for commented line.
        if(comment==-1):
            pass
        if(comment!=-1):                #removing comment and replacing i.
            i=i[:comment]
        full_line_comment=list(i.split())   #checking whether the whole line is commented or not
        if(len(full_line_comment)==0):
            length_lines=length_lines-1
            continue
            
        else:
            num_opcode=opcode_check_and_number(i)                             #Checking for the number of opcodes in i
            Str=i.split()
            if(i=='STP'):   #if STP then stop the process
                break
            if(num_opcode==0 and (Str[0]!="DS" and Str[0]!="DC")):
                print("ERROR on line "+Str[0]+str(marker)+" : No opcode given") #No opcode given.
                error+=1
                continue
            elif(num_opcode>1):
                print("ERROR on line "+str(marker)+" : Multiple opcodes given in a line")#Multiple instruction given in a line
                error+=1
                continue
            if(len(Str)==1):
                if(Str[0]!='STP' and Str[0]!='CLA'):
                    print("ERROR on line "+str(marker)+" : Label or Variable is incomplete")#only STP and CLA can be executed without any oprand given. 
                    error+=1
                    continue
            elif(len(Str)==2):
                if((Str[0]=="DS" or Str[0]=="DC")):
                    if(symbol[Str[1]]==-1):
                        symbol[Str[1]]=loc
                    else:
                        print("ERROR on line "+str(marker)+": Already declared")        #The Varible has already been declared.
                if(opcode_true_false(Str[0])==False and opcode_true_false(Str[1])==True and Str[1]!='CLA' and Str[1]!='STP'):
                    
                    print("ERROR on Line "+str(marker)+": ERROR in thhe FORMAT.")  #operand cant come before opcode 
                    error+=1
                    continue
            for k in range(len(Str)):
                if(opcode_true_false(Str[k])):
                    if(len(Str)-k-1>=2):
                        print("ERROR on Line "+str(i)+ ": More than one variable/label provided.") #Cant have multiple Variables/Labels.
                        error+=1
                        continue
            if(len(Str)>=3):
                if((Str[0]=="DS" or Str[0]=="DC")):
                    if(symbol[Str[1]]==-1):
                        symbol[Str[1]]=loc
                    else:
                        print("ERROR on line "+str(marker)+": Already declared")
                        error+=1
                        continue

                elif(opcode_true_false(Str[0])==False and opcode_true_false(Str[1])==False):
                    print(Str)
                    print("ERROR on Line "+str(marker)+": ERROR in thhe FORMAT.") #no instruction has been passed
                    error+=1
                    continue
            if(':' in i):                   #checking for Labels
                sym=i[:i.index(':')]        #Label found-removinge everything after ":" and storing it i.e storing the Label
                sym=sym.strip()
                if('STP' in i ):
                    break                       #break if stopped after branching
                if(opcode_true_false(sym)):
                    print("ERROR on Line "+str(marker)+": name of the symbol can't be an instruction.") #name of the symbol cant be an instruction.
                    error+=1
                    continue
                if(sym in symbol):
                    if(symbol[sym]==-1):
                        print("ERROR on Line "+str(marker)+": Variable with same name is already declared.") #Variable with same name is already declared.
                        error+=1
                        continue
                    elif(symbol[sym]==-2):
                        print("ERROR on Line "+str(j)+": A Label with the same name has already been declared.") #A Label with the same name has already been declared,i.e  a label can t be declared twice
                        error+=1
                        continue
                i=i[i.index(':')+1:]
                i=i.strip()
                symbol[sym]=loc
                label[sym]=loc
            elif('BRZ' in i or 'BRP' in i or 'BRN' in i):
                sym=Str[1]
                if(opcode_true_false(sym)):
                    print("ERROR on Line "+str(marker)+": symbol name can not be an instruction,can't branch to an opcode")
                    error+=1
                    continue
                if(sym in symbol):
                    if(symbol[sym]==-1):
                        print("ERROR on Line "+str(marker)+": Branching to a Variable is not possible.") #Example --> BRN A where A is a Varible
                        error+=1
                        continue
                    else:
                        continue
                else:
                    symbol[sym]=loc
            elif('INP' in i):
                if(opcode_true_false(Str[1])):
                    print("ERROR on Line "+str(marker)+": symbol name can not be an instruction.") #Example --> INP CLA
                    error+=1
                    continue
                elif(Str[1] in symbol):
                    if(symbol[Str[1]]!=-1):
                        print("ERROR on Line "+str(marker)+": "+Str[1]+" is a label type symbol.")
                        error+=1
                        continue
                symbol[Str[1]]=-1
            elif('SAC' in i):
                if(opcode_true_false(Str[1])):
                    print("ERROR on Line "+str(marker)+": symbol name can not be an instruction.")
                    error+=1
                    continue
                elif(Str[1] in symbol):
                 if(symbol[Str[1]]!=-1):
                    print("ERROR on Line "+str(marker)+": "+Str[1]+" is a label type symbol.")
                    error+=1
                    continue
                symbol[Str[1]]=-1
            elif('LAC' in i or 'ADD' in i or 'SUB' in i or 'DSP' in i or 'MUL' in i or 'DIV' in i):
                if(opcode_true_false(Str[1])):
                    print("ERROR on Line "+str(marker)+": symbol name can not be an instruction.")
                    error+=1
                    continue
                elif(Str[1] in symbol):
                 if(symbol[Str[1]]!=-1):
                    print("ERROR on Line "+str(marker)+": "+Str[1]+" is a label type symbol.")
                    error+=1
                    continue
                symbol[Str[1]]=-1
            loc+=1
            comment=0
    symbol["error"]=error  #Adding the errors to symbol and returning it.      
    
    return symbol,error,label
    

'''
machine_code_of_opcode(x)-->RETURN TYPE-String
This function takes in a String and checks if it is an opcode.
If it is an opcode then it returns its machine code as String. 
'''
def machine_code_of_opcode(x):
    opcode={'CLA':"0000",'LAC':"0001",'SAC':"0010",'ADD':"0011",'SUB':"0100",'BRZ':"0101",'BRN':"0110",'BRP':"0111",'INP':"1000",'DSP':"1001",'MUL':"1010",'DIV':"1011",'STP':"1100"}
    for i in opcode.keys():
        if(x==i):
            return opcode[i]
'''
secondpass(symbol)-->RETURN TYPE-void
This function takes in a dictionary,assigns the binary address and makes the "output.txt" file which contains the required oputput as per the file "test.txt.
It also creates "Symbol.txt" to display the Symbol table.
'''
def secondpass(symbol,lab):
    #This for loop is used to convert address to its binary equivalent.
    for j in lab.keys():
        numb=lab[j]
        bina=bin(numb)[2:]
        pq='0'*(8-len(bina))+bina
        lab[j]=pq

    for i in symbol.keys():
        num=symbol[i]
        binary=bin(num)[2:]
        p='0'*(8-len(binary))+binary
        symbol[i]=p

    file=open("output.txt","w") #opening a new file in write mode.
    a=[]
    h=[]
    comment=0
    f=open("test.txt","r")
    s=f.readlines()
    length_lines=len(s)    
    #This for loop creates an appropriate format to check all the lines.
    for i in s:
        stp=i.strip();
        r=re.split('|\n',stp)
        k=""
        for i in r:
            k=k+i
        r=k+'\n'
        h.append(r)

    for i in h:
        comment=i.find('#')            #if commented line is found then skip it.
        if(comment==-1):
            pass
        if(comment!=-1):
            i=i[:comment]
        full_line_comment=list(i.split())
        if(len(full_line_comment)==0):
            length_lines=length_lines-1
            continue
        if(':' in i):
            i=i[i.index(':')+1:]
        Str=i.split()
        if(len(Str)==1):
            a.append(machine_code_of_opcode(Str[0])+" 00000000")            #if an instruction doesn't have any symbol attached it will add 8 zeros in front
            file.write(a[-1])                                                   #then adding ot to file.
            file.write("\n")
        elif(Str[0]=="DS" or Str[0]=="DC"):
            x=1
        else:
            a.append(machine_code_of_opcode(Str[0])+" "+symbol[Str[1]]) #String concantenation (of opcode and address).
            file.write(a[-1])                                                   #then adding ot to file.
            file.write("\n")
    file.close()
    file=open("Symbol.txt",'w')
    a=[]
    file.write("SYMBOL\t\tTYPE\t\tADDRESS")
    file.write('\n')
    for i in symbol.keys():
        if(int(symbol[i],2)<=length_lines):
            a.append((str(i)+'\t\t'+"Label"+'\t\t'+symbol[i]))
        else:
            a.append(str(i)+'\t\t'+"Variable"+'\t'+symbol[i])
        file.write(a[-1])
        file.write('\n')
    file.close()


    file=open("label.txt",'w')
    ab=[]
    file.write("LABEL\t\tADDRESS")
    file.write('\n')
    for i in lab.keys():
            ab.append((str(i)+'\t\t'+lab[i]))
            file.write(ab[-1])
            file.write('\n')
    file.close()
dj,qw,lab=firstpass()
cv={}
if(qw==0):
 if(dj["error"]==0):
    for i in dj.keys():
        if(i!="error"):
            cv[i]=dj[i]
    secondpass(cv,lab)
                    