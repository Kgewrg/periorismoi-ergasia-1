import numpy as np


def initArrays(sudoku, domains):
    lines = []
    with open('sudoku1.txt') as f:
        lines = f.readlines()

    count = 0
    for line in lines:
        sudoku[count] = line.split(" ")  # Διαβάζει γραμμη γραμμη το αρχείο, την σπαει στα κενα, και αγνωεί τα \n
        sudoku[count][-1] = sudoku[count][-1].replace('\n', '')
        # Κάτι γινόταν και χρείαστηκε να προσθέσω αυτήν την γραμμή
        sudoku[count] = [int(x) for x in sudoku[count]]  # Μετατρέπει ολα τα στοιχεία της γραμμης σε int
        # print(sudoku[count])
        count += 1

    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                pass
            else:
                # (9*i)+j αντιστοιχεί την δυσδιάστατη θέση του sudo στην μονοδιάστατη γραμμή του domains
                domains[(9 * i) + j] = [-2 for x in domains[(9 * i) + j]]  # κάθε -1 στην γραμμή του domains το κάνει -2
                domains[(9 * i) + j][sudoku[i][j] - 1] = sudoku[i][j]
                # ----------------------------> **Βαλε counter εδω!** <-----------------------------------


def NC(sudoku, domains):
    """
        Αφαιρεί όλες τι τιμες απο το Domain καποιο κελιου που δεν είναι συμβατές με οποιοδηποτε κελι.
    """
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] == 0:
                continue
            # Για την ιδια γραμμη
            for i in range(9):  # τρέχει για τα στοιχεία γραμμής
                if (i == col):  # αγνωόντας το στοιχείο που είμαστε τώρα
                    continue
                # συντεταγένες γραμμής sudoku=[row][i]
                domains[(9 * row) + i][sudoku[row][col] - 1] = -2
                # "(9 * row) + i" αντιστοιχεί θέση sudoku με γραμμή Domains
                # ----------------------------> **Βαλε counter εδω!** <-----------------------------------

            # Για την ίδια στήλη
            for i in range(9):
                if (i == row):
                    continue
                # συντεταγένες στήλης sudoku=[i][col]
                domains[(9 * i) + col][sudoku[row][col] - 1] = -2
                # ----------------------------> **Βαλε counter εδω!** <-----------------------------------

            # για το block
            startRow = row - row % 3
            startCol = col - col % 3
            # δείχνουν στο πανω αριστερα στοιχείο του block
            for i in range(3):
                for j in range(3):
                    if (((startRow + i) == row) and ((startCol + j) == col)):
                        continue
                    # Διάσχιση του block: sudoku[(startRow+i)][(startCol+j)]
                    domains[(9 * (startRow + i)) + (startCol + j)][sudoku[row][col] - 1] = -2
                    # ----------------------------> **Βαλε counter εδω!** <-----------------------------------


def CHECK(xi, a, xj, b):
    print("xi", xi)
    print("a", a)
    print("xj", xj)
    print("b", b)
    if C[xi][xj] == 1:
        if a != b:
            return True
    elif C[xi][xj] == 2:
        if a > b:
            return True
    elif C[xi][xj] == 3:
        if a < b:
            return True
    else:
        return False


def SUPPORTED(xi, a, xj, domains):
    support = False
    for i in range(9):
        if domains[xi][i] == -1:
            print("supported")
            if CHECK(xi, a, xj, i) == True:
                support = True
                return support
    return support


def REVISE(xi, xj, domains):
    revised = False
    for i in range(9):
        print(i)
        if domains[xi][i] == -1:
            found = SUPPORTED(xi, i, xj, domains)
            if found == False:
                revised = True
                domains[xi][i] = -2
    return revised


def CONSTRAIN(C):
    row = 0
    column = 0
    r = 0
    c = 0
    for k in range(81):
        for i in range(9):
            for j in range(9):
                if r == i:  # αν είναι στην ίδια γραμμή να είναι διαφορετικοί αριθμοί
                    C[row][(9 * i) + j] = 1
                if c == j:  # αν είναι στην ίδια στηλη να είναι διαφορετικοί αριθμοί
                    C[row][(9 * i) + j] = 1
                if i % 3 == 1:  # για να βρεί την σωστή γραμμή
                    tr = i
                    tr = tr - 1
                if i % 3 == 2:
                    tr = i
                    tr = tr - 2
                if i % 3 == 0:
                    tr = i
                if j % 3 == 1:  # για να βρεί την σωστή στήλη
                    tj = j
                    tj = tj - 1
                if j % 3 == 2:
                    tj = j
                    tj = tj - 2
                if j % 3 == 0:
                    tj = j
                for tr in range(3):  # για να βρει το block που πρεπει να είναι διαφορετικά μεταξύ τους
                    for tj in range(3):
                        C[row][(9 * tr) + tj] = 1
        if k % 9 == 0:  # αν το κ φτασει σε 9,18...κλπ τοτε αυξανουμε μια γραμμή γιατι στο πινακα sudoko θα πρεπει να πάμε στην επόμενη γραμμή
            if k != 0:
                r = r + 1
                # column=0
        c = c + 1
        if c % 9 == 0:  # αν το c ειναι 9 τοτε μηδενιζουμε για να πάμε ξανα απο την αρχή για τις στηλες
            c = 0
        row = row + 1  # αυξανουμε το row για να αποθηκευουμε σωστά στον πινακα C [ROW] αν εχει περιοσρισμο με κάποια απο τις επομενες στήλες
        column = column + 1


def AC3NEW(C, domains):
    # Q=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
    Q = [i for i in range(81)]
    print("Q is ")
    # for count in range(81):
    #   for i in range(9):
    #      if domain[count][i]==-1:
    #          Q.append(i)
    #     Q.pop(0)
    # for k in range(81):
    #   for j in range(81):
    #      if C[k][j]!=0:
    #         updated=REVISE(k,j)
    #        for ch in range(9):
    #           if domain[count][ch]==-2:
    #              return False
    # if updated==true:
    #    Q.append()
    # for i in range(81):
    #   if i==0:
    #      Q.pop(0)
    #     Q.append(i+1)
    # Q.appened(i+1)
    k = 0
    while len(Q) != 0:
        # print(len(Q))
        for i in range(81):
            for j in range(81):
                if C[i][j] != 0:
                    # print(len(Q))
                    updated = REVISE(i, j, domains)
                    for ch in range(9):
                        valueCounter = 9
                        if domains[k][ch] == -1:
                            print("domainsss", domains[k][ch])
                            valueCounter -= 1
                        if valueCounter == 0:
                            return False
                if updated == True:  # True οταν έχει γίνει αφαίρεση
                    print("befpreeee", len(Q))
                    Q.append(1)
                    print("afterrrrr", len(Q))
                else:
                    if len(Q) != 0:
                        Q.pop(0)
                        print("pop", len(Q))
                    else:
                        break
            k = k + 1
            print("k", k)

    print("domains array")
    for i in range(len(domains)):
        print(i, domains[i])

    # Προσπαθει να αφαιρέσει μη συμβατες τιμες


def AC3(sudoku, domains):
    NC(sudoku, domains)
    # node consistency
    # printBox(sudoku)

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
    C = np.zeros((81, 81), int)
    initArrays(sudoku, domains)

    # AC3(sudoku, domains)
    # printBox(sudoku)

    # prints Sudoku
    print("sudoku array")
    for i in range(len(sudoku)):
        print(i + 1, sudoku[i])

    # prints Domains
    print("domains array")
    for i in range(len(domains)):
        print(i, domains[i])

    print("constrain")
    CONSTRAIN(C)
    for i in range(81):
        print(i, C[i])

    AC3NEW(C, domains)