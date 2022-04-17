
from xml.etree.ElementTree import QName
from numpy import true_divide
import numpy as np


def initArrays(sudoku, domains):
    lines = []
    with open('sudoku1.txt') as f:
        lines = f.readlines()

    count = 0
    for line in lines:
        sudoku[count] = line.split(" ")[:-1]  # Διαβάζει γραμμη γραμμη το αρχείο, την σπαει στα κενα, και αγνωεί τα \n
        sudoku[count] = [int(x) for x in sudoku[count]]  # Μετατρέπει ολα τα στοιχεία της γραμμης σε int
        # print(sudoku[count])
        count += 1

    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                pass
            else:
                # (9*i)+j αντιστοιχεί την δυσδιάστατη θέση του sudo στην μονοδιάστατη γραμμή του domains
                domains[(9*i)+j] = [-2 for x in domains[(9*i)+j]]  # κάθε -1 στην γραμμή του domains το κάνει -2
                domains[(9*i)+j][sudoku[i][j]-1] = sudoku[i][j]
                # ----------------------------> **Βαλε counter εδω!** <-----------------------------------




def NC(sudoku, domains):

    for row in range(9):
        for col in range(9):

            if sudoku[row][col] == 0:
                continue

            # Για την ιδια γραμμη
            # Replace left
            for k in range(col + (row * 9) - 1, row * 9 - 1, -1):
                domains[k][sudoku[row][col]-1] = -3
                # ----------------------------> **Βαλε counter εδω!** <-----------------------------------

            # Replace right
            for k in range(col + (row * 9) + 1, row * 9 + 9):
                domains[k][sudoku[row][col]-1] = -3
                # ----------------------------> **Βαλε counter εδω!** <-----------------------------------

            # #   (9*i)+j
            # if row < 3:
            #     box_row = 1
            # elif row > 2 and row < 6:
            #     box_row = 2
            # else:
            #     box_row = 3
            #
            # if col < 3:
            #     box_col = 1
            # elif col > 2 and col < 6:
            #     box_col = 2
            # else:
            #     box_col = 3
            #
            # for w in range(box_row * 3 - 3, box_row * 3):
            #     for y in range(box_col * 3 - 3, box_col * 3):
            #         domains[k] = -10




            # Σβηνουμε την τιμη απο τις στειλες και γραμμες του sudoku


def printBox(sudoku):

    #for block in range(9):
     #   print(block * 3)

      #  for row in range(3):
       #     for col in range(3):
        #        print(sudoku[row][(block*3+col)%9], end="")
         #   print()
       # print()
    k=0
    block=0
    j=3
    for block in range(9):
        i=k
        for i in range(3):
            for j in range(3):
                print(sudoku[i][j], end="")
            print()
        print()
        j=j*block
        if block%2==0:
            k=i+3
            j=0
        

def CHECK(xi,a,xj,b):
    print("xi",xi)
    print("a",a)
    print("xj",xj)
    print("b",b)
    if C[xi][xj]==1:
        if a!=b:
            return True
    elif C[xi][xj]==2:
        if a>b:
            return True
    elif C[xi][xj]==3:
        if a<b:
            return True
    return False

def SUPPORTED(xi,a,xj,domains):
    support=False
    for j in range(len(domains[xj])):
        if domains[xj][j]!=-2:
            print("supported")
            if CHECK(xi,a,xj,j)==True:
                support=True
                return support
    return support

def REVISE(xi,xj,domains):
    revised=False
    for i in range(len(domains[xi])):
        if domains[xi][i]!=-2:
            found=SUPPORTED(xi,i,xj,domains)
            print("found....",found)
            if found==False:
                print("false..")
                revised=True 
                domains[xi][i]=-2
                print("xs..................",domains[xi][i])
    return revised

def CONSTRAIN(C):
    row=0
    column=0
    r=0
    c=0
    for k in range(81):
        for i in range(9):
            for j in range(9):
                if r==i: #αν είναι στην ίδια γραμμή να είναι διαφορετικοί αριθμοί
                    C[row][(9*i)+j]=1
                if c==j: # αν είναι στην ίδια στηλη να είναι διαφορετικοί αριθμοί
                    C[row][(9*i)+j]=1
                if i%3==1: #για να βρεί την σωστή γραμμή
                    tr=i
                    tr=tr-1
                if i%3==2:
                    tr=i
                    tr=tr-2
                if i%3==0:
                    tr=i
                if j%3==1:# για να βρεί την σωστή στήλη
                    tj=j
                    tj=tj-1
                if j%3==2:
                    tj=j
                    tj=tj-2
                if j%3==0:
                    tj=j
                for tr in range(3): #για να βρει το block που πρεπει να είναι διαφορετικά μεταξύ τους
                    for tj in range(3):
                        C[row][(9*tr)+tj]=1
        if k%9==0:# αν το κ φτασει σε 9,18...κλπ τοτε αυξανουμε μια γραμμή γιατι στο πινακα sudoko θα πρεπει να πάμε στην επόμενη γραμμή
            if k!=0:
                r=r+1
                #column=0
        c=c+1
        if c%9==0:#αν το c ειναι 9 τοτε μηδενιζουμε για να πάμε ξανα απο την αρχή για τις στηλες 
            c=0
        row=row+1 #αυξανουμε το row για να αποθηκευουμε σωστά στον πινακα C [ROW] αν εχει περιοσρισμο με κάποια απο τις επομενες στήλες 
        column=column+1
                    
def AC3NEW(C,domains):
    Q=[i for i in range(81)]
    print("Q is ")
    k=0
    while len(Q)!=0:
        #print(len(Q))
        j=1
        for i in range(81):
            for j in range(81):
                if i!=j:
                    if C[i][j]!=0:
                        #print(len(Q))
                        updated=REVISE(i,j,domains)
                        count=9
                        for ch in range(9):
                            if domains[k][ch]==-2:
                                count=count-1
                                print("domainsss",domains[k][ch])
                                if count==0:
                                    return False
                        if updated==True:
                            Q.append(1)
                        else:
                            if len(Q)!=0:
                                Q.pop(0)
                                print("pop",len(Q))
                            else:
                                break
            k=k+1
            print("k",k)
    





def AC3(sudoku, domains):
    NC(sudoku, domains)
    # node consistency
    #printBox(sudoku)




    pass


if (__name__ == "__main__"):

    # Δημηουργία πίνακα εισοδου
    sudoku = [[-1, -1, -1, -1, -1, -1, -1, -1, -1] for i in range(9)]
    # έχει την μορφη:
    # (1) [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    # (2) [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    # (3) [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    # ...

    domains = [[-1, -1, -1, -1, -1, -1, -1, -1, -1] for i in range(81)]
    C = np.zeros((81,81), int)
    initArrays(sudoku, domains)

    #AC3(sudoku, domains)
    #printBox(sudoku)

    # prints Sudoku
    print("sudoku array")
    for i in range(len(sudoku)):
        print(i+1, sudoku[i])


    # prints Domains
    print("domains array")
    for i in range(len(domains)):
        print(i, domains[i])

    print("constrain")
    CONSTRAIN(C)
    for i in range(81):
            print(i,C[i])

    AC3NEW(C,domains)
    print("domains array")
    for i in range(len(domains)):
        print(i, domains[i])
    
    
