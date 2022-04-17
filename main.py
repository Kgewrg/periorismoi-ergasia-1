import numpy as np

sudoku = []
domains = []
occupiedArray = []
C = []
removedCounter = 0


class node():
    global sudoku

    def __init__(self, sudokuCordinate=(-1, -1)):
        self.sudokuCordinate = sudokuCordinate
        self.domainsRow = self.sudokuCordinate[0] * 9 + self.sudokuCordinate[1]
        self.value = sudoku[self.sudokuCordinate[0]][self.sudokuCordinate[1]]

    def print(self):
        print(self.sudokuCordinate, self.domainsRow, self.value)


def initArrays():
    global occupiedArray, sudoku, domains, removedCounter
    lines = []
    with open('sudoku2.txt') as f:
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
                occupiedArray.append((9 * i) + j)
                # (9*i)+j αντιστοιχεί την δυσδιάστατη θέση του sudo στην μονοδιάστατη γραμμή του domains
                domains[(9 * i) + j] = [-2 for x in domains[(9 * i) + j]]  # κάθε -1 στην γραμμή του domains το κάνει -2
                removedCounter += 8  # --------> ΙΣΩΣ ΔΕΝ ΧΡΕΙΑΖΕΤΑΙ ΕΔΩ
                # += 8 γιατι απο τα κελια που έχουν προκαθοισμένες τιμές, αφαιρεί τις άλλες 8.
                domains[(9 * i) + j][sudoku[i][j] - 1] = sudoku[i][j]


def CHECK(xi, a, xj, b):
    """
    Ελέγχει την τιμή a της μεταβλητή xi με την τιμή b της xj
    :param xi: Μεταβλητή 1
    :param a: τιμή της μεταβλητής 1
    :param xj: Μεταβλητή 2
    :param b: τιμή της μεταβλητής 2
    :return: true/false ανάλογα με το είδος του περιορισμού
    """
    if C[xi][xj] == 1:
        if a != b:
            return True
    elif C[xi][xj] == 2:
        if a > b:
            return True
    elif C[xi][xj] == 3:
        if a < b:
            return True
    return False


def SUPPORTED(xi, a, xj):
    """
    Ελέγχει αν για την τιμή a της xi υπάρχουν συνεπής στην xj
    :param xi: Μεταβλητή 1 (1-81)
    :param a: τιμή της μεταβλητής 1
    :param xj: Μεταβλητή 2
    :return: True αν υπάρχει κάποια διαφορετική τιμή
    """
    global domains
    support = False
    for j in range(len(domains[xj])):
        if domains[xj][j] != -2:
            # print("supported")
            if CHECK(xi, a, xj, j):
                support = True
                return support
    return support


def REVISE(xi, xj):
    """
    Ελέγχει για τις τιμές του xi, αν υπάρχουν συνεπής στην xj
    :param xi: γραμμη του domains για την μεταβλητή 1
    :param xj: γραμμη του domains για την μεταβλητή 2
    :return: False αν δεν γίνει κάποια αλλαγή
    """
    global domains, removedCounter
    print("checking: xi=", xi, ",xj=", xj)
    revised = False
    for i in domains[xi]:
        if i > 0:
            return revised
    for i in range(len(domains[xi])):
        if domains[xi][i] != -2:
            found = SUPPORTED(xi, i, xj)
            # print("found....", found)
            if not found:
                # print("false..")
                revised = True
                domains[xi][i] = -2
                removedCounter += 1
                print("changed domain:", xi, ", value:,", i + 1, "to", domains[xi][i])
    return revised


def CONSTRAIN():
    global C
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

                startRow = r - r % 3
                startCol = c - c % 3
                # δείχνουν στο πανω αριστερα στοιχείο του block
                for t in range(3):
                    for y in range(3):
                        C[row][(9 * (startRow + t)) + (startCol + y)] = 1

        if k % 9 == 0:  # αν το κ φτασει σε 9,18...κλπ τοτε αυξανουμε μια γραμμή γιατι στο πινακα sudoko θα πρεπει να πάμε στην επόμενη γραμμή
            if k != 0:
                r = r + 1
                # column=0
        c = c + 1
        if c % 9 == 0:  # αν το c ειναι 9 τοτε μηδενιζουμε για να πάμε ξανα απο την αρχή για τις στηλες
            c = 0
        row = row + 1  # αυξανουμε το row για να αποθηκευουμε σωστά στον πινακα C [ROW] αν εχει περιοσρισμο με κάποια απο τις επομενες στήλες
        column = column + 1


def neigh(row):
    """
    Βρίσκει τους γείτωνες της μεταβλητής
    :param row: κάποια μεταβλητή του sudoku (γραμμη απο πίνακα domains)
    :return: neighbours(array): πίνακας με τους γείτωνες του row, (γραμμη απο πίνακα domains)
    """
    neighbours = []
    for i in range(len(C[row])):
        if C[row][i] == 1:
            neighbours.append(i)
    return neighbours


def AC3():
    """
    Υλοποιήση του αλγορίθμου AC3
    :return: False, αν κάποιο domain μήνει άδειο
    """
    global sudoku, domains, C
    # Φτίαχνουμε μια ουρά μέ ολα τα κελιά του Sudoku
    Q = []
    for row in range(9):
        for col in range(9):
            Q.append(node((row, col)))

    while (len(Q) > 0):
        # Σε κάθε επανάληψη αφαιρούμε μια μεταβλητή
        tmpNode_i = Q.pop(0)
        i = tmpNode_i.domainsRow  # μας νοιάζει η "θέση" της στην domains
        neighbours = neigh(i)  # εξετάζουμε τους γείτωνες του i
        for j in neighbours:
            # print("i=", i, "j=", j)
            if i == j:  # για να μην εξετάσουμε τον εαυτό του
                continue

            updated = REVISE(i, j)  # αν έχει κάνει αλλαγή επιστρέφει true
            count = 9
            for ch in range(9):  # Ελέγχουμε αν κάτι μείνει κενό
                if domains[i][ch] == -2:
                    count = count - 1
                    # print("domainsss", domains[k])
                    if count == 0:
                        print("Found empty domain", i, domains[i])
                        return False
            if updated:
                Q.append(tmpNode_i)  # Αν έχει αφαιρεθεί κάτι απο το domain που εξετάσαμε,
                # το ξαναβάζουμε στην ουρά

    # print("breaking, len(Q):", len(Q), "i =", i)


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
    initArrays()

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
    CONSTRAIN()

    # for i in range(81):
    #     print(i, C[i])

    AC3()
    print("ac3 removed:", removedCounter)
    print("domains array")
    for i in range(len(domains)):
        print(i, domains[i])

    for i in range(len(domains)):
        if (i in occupiedArray):
            continue
        available = 0
        for j in domains[i]:
            if (j == -1):
                available += 1
        print("available for variable", i, ":", available)

        # TODO:
        #   1. Να γίνει χρονομέτρηση,
        #   2. Να καθαρίσει λίγο ο κώδικας και να συμμαζευτεί
        #   3. Να μπεί print για το αν κάποια μεταβλητή έχει μονο μία τιμή

