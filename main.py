import time
import copy

class node():
    def __init__(self, sudokuCordinate=(-1, -1), sudoku=[]):
        self.sudokuCordinate = sudokuCordinate
        self.domainsRow = self.sudokuCordinate[0] * 9 + self.sudokuCordinate[1]
        self.value = sudoku[self.sudokuCordinate[0]][self.sudokuCordinate[1]]

    def print(self):
        print(self.sudokuCordinate, self.domainsRow, self.value)

def initArrays(sudoku=[], domains=[], filename=""):
    """
    Διαβάζει απο αρχείο και αποθυκεύει στους πίνακες:
    :param sudoku: array[9][9], αναπαράσταση του sudoku,
    :param domains: array[81][9], domain για κάθε κελί του sudoku
    :param filename: string, όνομα του αρχείου απο το οποίο θα διαβάσει
    :return:
    """
    with open(filename) as f:
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
                # += 8 γιατι απο τα κελια που έχουν προκαθοισμένες τιμές, αφαιρεί τις άλλες 8.
                domains[(9 * i) + j][sudoku[i][j] - 1] = sudoku[i][j]


def CHECK(xi, a, xj, b, constraints=[]):
    """
    Ελέγχει τον περιορισμό ανάμεσα στις τιμές a της μεταβλητή xi και την τιμή b της xj
    :param xi: Μεταβλητή 1
    :param a: τιμή της μεταβλητής 1
    :param xj: Μεταβλητή 2
    :param b: τιμή της μεταβλητής 2
    :param constraints: array[81][81], πίνακας των constraint
    :return: true/false ανάλογα με το είδος του περιορισμού
    """
    if constraints[xi][xj] == 1:
        if a != b:
            return True
    elif constraints[xi][xj] == 2:
        if a > b:
            return True
    elif constraints[xi][xj] == 3:
        if a < b:
            return True
    return False


def SUPPORTED(xi, a, xj, domains=[], constraints=[]):
    """
    Ελέγχει αν για την τιμή a της xi υπάρχουν συνεπής στην xj
    :param xi: Μεταβλητή 1 (1-81)
    :param a: τιμή της μεταβλητής 1
    :param xj: Μεταβλητή 2
    :param domains: array[81][9], πίνακας των domains
    :param constraints: array[81][81], πίνακας των constraint
    :return: True αν υπάρχει κάποια διαφορετική τιμή
    """
    support = False
    for j in range(len(domains[xj])):
        if domains[xj][j] == -2:  # Αγνούμε τις τιμές που αφαιρέθηκαν
            continue
        # print("supported")
        if CHECK(xi, a, xj, j, constraints):
            support = True
            return support
    return support


def REVISE(xi, xj, removedCounter, domains=[], constraints=[]):
    """
    Ελέγχει για τις τιμές του xi, αν υπάρχουν συνεπής στην xj
    :param xi: γραμμη του domains για την μεταβλητή 1
    :param xj: γραμμη του domains για την μεταβλητή 2
    :param domains: array[81][9], πίνακας των domains
    :param constraints: array[81][81], πίνακας των constraint
    :return: False αν δεν γίνει κάποια αλλαγή
    """
    # print("checking: xi=", xi, ",xj=", xj)
    revised = False
    for i in domains[xi]:
        if i > 0:
            return revised, removedCounter

    for i in range(len(domains[xi])):
        if domains[xi][i] != -2:
            found = SUPPORTED(xi, i, xj, domains, constraints)
            # print("found....", found)
            if not found:
                # print("false..")
                revised = True
                domains[xi][i] = -2
                removedCounter += 1
                # print("changed domain:", xi, ", value:,", i + 1, "to", domains[xi][i])
    return revised, removedCounter


def CONSTRAIN(constraints=[]):
    row = 0
    column = 0
    r = 0
    c = 0
    for k in range(81):
        for i in range(9):
            for j in range(9):
                if r == i:  # αν είναι στην ίδια γραμμή να είναι διαφορετικοί αριθμοί
                    constraints[row][(9 * i) + j] = 1
                if c == j:  # αν είναι στην ίδια στηλη να είναι διαφορετικοί αριθμοί
                    constraints[row][(9 * i) + j] = 1

                startRow = r - r % 3
                startCol = c - c % 3
                # δείχνουν στο πανω αριστερα στοιχείο του block
                for t in range(3):
                    for y in range(3):
                        constraints[row][(9 * (startRow + t)) + (startCol + y)] = 1

        if k % 9 == 0:  # αν το κ φτασει σε 9,18...κλπ τοτε αυξανουμε μια γραμμή γιατι στο πινακα sudoko θα πρεπει να πάμε στην επόμενη γραμμή
            if k != 0:
                r = r + 1
                # column=0
        c = c + 1
        if c % 9 == 0:  # αν το c ειναι 9 τοτε μηδενιζουμε για να πάμε ξανα απο την αρχή για τις στηλες
            c = 0
        row = row + 1  # αυξανουμε το row για να αποθηκευουμε σωστά στον πινακα C [ROW] αν εχει περιοσρισμο με κάποια απο τις επομενες στήλες
        column = column + 1


def neigh(row, constraints=[]):
    """
    Βρίσκει τους γείτωνες της μεταβλητής
    :param row: κάποια μεταβλητή του sudoku (γραμμη απο πίνακα domains)
    :return: neighbours(array): πίνακας με τους γείτωνες του row, (γραμμη απο πίνακα domains)
    """
    neighbours = []
    for i in range(len(constraints[row])):
        if constraints[row][i] in [1, 2, 3]:
            neighbours.append(i)
    return neighbours


def AC3(sudoku=[], domains=[], constraints=[], removedCounter=0):
    """
    Υλοποιήση του αλγορίθμου AC3
    :param sudoku: array[9][9], πίνακας του sudoku
    :param domains: array[81][9], πίνακας των domains
    :param constraints: array[81][81], πίνακας των constraint
    :param Q: queue, προαιρετικό, άμα θελουμε να τρέξει ο AC3 σε καποια συγκεκριμένη ουρά
    :param removedCounter: Πλήθος διαγραφών τιμών
    :return: False, αν κάποιο domain μήνει άδειο, πλήθος διαγραφών
    """
    # Φτίαχνουμε μια ουρά μέ ολα τα κελιά του Sudoku
    Q = []
    if not Q:
        # Για την περίπτωση που θέλουμε ο AC3 να τρέχει σε μια προκαθορισμένη ουρά
        for row in range(9):
            for col in range(9):
                Q.append(node((row, col), sudoku))


    while (len(Q) > 0):
        # Σε κάθε επανάληψη αφαιρούμε μια μεταβλητή
        tmpNode_i = Q.pop(0)
        i = tmpNode_i.domainsRow  # μας νοιάζει η "θέση" της στην domains
        neighbours = neigh(i, constraints)  # εξετάζουμε τους γείτωνες του i
        for j in neighbours:
            # print("i=", i, "j=", j)
            if i == j:  # για να μην εξετάσουμε τον εαυτό του
                continue
            updated, removedCounter = REVISE(i, j, removedCounter, domains, constraints)  # αν έχει κάνει αλλαγή επιστρέφει true
            count = 9
            for ch in range(9):  # Ελέγχουμε αν κάτι μείνει κενό
                if domains[i][ch] == -2:
                    count = count - 1
                    if count == 0:
                        return False, removedCounter
            if updated:
                Q.append(tmpNode_i)  # Αν έχει αφαιρεθεί κάτι απο το domain που εξετάσαμε,
                # το ξαναβάζουμε στην ουρά

    # print("breaking, len(Q):", len(Q), "i =", i)
    print("Variables with only 1 value available:", countSingleValue(domains))
    # printDomains(domains)
    return True, removedCounter


def AC3_singleton(sudoku=[], domains=[], constraints=[], Q=[], removedCounter=0):
    """
    Υλοποιήση του αλγορίθμου AC3, τρέχει στην προκαθορισμένη ουρά
    :param sudoku: array[9][9], πίνακας του sudoku
    :param domains: array[81][9], πίνακας των domains
    :param constraints: array[81][81], πίνακας των constraint
    :param Q: queue, προαιρετικό, άμα θελουμε να τρέξει ο AC3 σε καποια συγκεκριμένη ουρά
    :return: False, αν κάποιο domain μήνει άδειο
    """
    # Φτίαχνουμε μια ουρά μέ ολα τα κελιά του Sudoku

    while (len(Q) > 0):
        # Σε κάθε επανάληψη αφαιρούμε μια μεταβλητή
        tmpNode_i = Q.pop(0)
        # i = tmpNode_i.domainsRow  # μας νοιάζει η "θέση" της στην domains
        neighbours = neigh(i, constraints)  # εξετάζουμε τους γείτωνες του i
        for j in neighbours:
            # print("i=", i, "j=", j)
            if i == j:  # για να μην εξετάσουμε τον εαυτό του
                continue

            updated, removedCounter = REVISE(i, j, removedCounter, domains, constraints)  # αν έχει κάνει αλλαγή επιστρέφει true
            count = 9
            for ch in range(9):  # Ελέγχουμε αν κάτι μείνει κενό
                if domains[i][ch] == -2:
                    count = count - 1
                    if count == 0:
                        print("Found empty domain", i, domains[i])
                        return False, removedCounter
            if updated:
                Q.append(tmpNode_i)  # Αν έχει αφαιρεθεί κάτι απο το domain που εξετάσαμε,
                # το ξαναβάζουμε στην ουρά
    return True, removedCounter


def RPC1(sudoku=[], domains=[], constraints=[], removedCounter=0):
    # Φτίαχνουμε μια ουρά μέ ολα τα κελιά του Sudoku
    Q = []
    for row in range(9):
        for col in range(9):
            Q.append(node((row, col), sudoku))

    while (len(Q) > 0):
        # Σε κάθε επανάληψη αφαιρούμε μια μεταβλητή
        tmpNode_i = Q.pop(0)
        i = tmpNode_i.domainsRow  # μας νοιάζει η "θέση" της στην domains
        neighbours = neigh(i, constraints)  # εξετάζουμε τους γείτωνες του i
        for j in neighbours:
            # print("i=", i, "j=", j)
            if i == j:  # για να μην εξετάσουμε τον εαυτό του
                continue

            updated, removedCounter = REVISE_RPC(i, j, removedCounter, domains, constraints)  # αν έχει κάνει αλλαγή επιστρέφει true
            count = 9
            for ch in range(9):  # Ελέγχουμε αν κάτι μείνει κενό
                if domains[i][ch] == -2:
                    count = count - 1
                    # print("domainsss", domains[k])
                    if count == 0:
                        print("Found empty domain", i, domains[i])
                        return False, removedCounter
            if updated:
                Q.append(tmpNode_i)  # Αν έχει αφαιρεθεί κάτι απο το domain που εξετάσαμε,
                # το ξαναβάζουμε στην ουρά
    print("Variables with only 1 value available:", countSingleValue(domains))
    # printDomains(domains)
    return True, removedCounter


def REVISE_RPC(xi, xj, removedCounter, domains=[], constraints=[]):
    """
    Ελέγχει για τις τιμές του xi, αν υπάρχουν συνεπής στην xj
    :param xi: γραμμη του domains για την μεταβλητή 1
    :param xj: γραμμη του domains για την μεταβλητή 2
    :return: False αν δεν γίνει κάποια αλλαγή
    """
    # print("checking: xi=", xi, ",xj=", xj)
    revised = False
    for i in domains[xi]:
        if i > 0:
            return revised, removedCounter

    for i in range(len(domains[xi])):
        if domains[xi][i] != -2:
            found = SUPPORT_RPC(xi, i, xj, domains, constraints)
            # print("found....", found)
            if not found:
                # print("false..")
                revised = True
                domains[xi][i] = -2
                removedCounter += 1
                # print("changed domain:", xi, ", value:,", i + 1, "to", domains[xi][i])
    return revised, removedCounter


def SUPPORT_RPC(xi, a, xj, domains=[], constraints=[]):
    """
    Ελέγχει αν για την τιμή a της xi υπάρχουν συνεπής στην xj
    :param xi: Μεταβλητή 1 (1-81)
    :param a: τιμή της μεταβλητής 1
    :param xj: Μεταβλητή 2
    :return: True αν υπάρχει κάποια διαφορετική τιμή
    """
    for j in range(len(domains[xj])):
        if domains[xj][j] == -2:
            continue

        if CHECK(xi, a, xj, j, constraints):
            for m in range(len(domains[xj])):
                if m > j:
                    if domains[xj][m] == -2:
                        continue
                    # print("callin check(", xi, a, xj, m, ")")
                    if CHECK(xi, a, xj, m, constraints):
                        # print("heloooooooooooooooooooo")
                        return True
            # print("calling PC(", xi, a, xj, j, ")")
            if PC(xi, a, xj, j, constraints):
                return True  # ειναι TRUE και RPC1
            else:
                return False  # Δεν είναι RPC1
    return False


def PC(xi, a, xj, b, constraints=[]):
    # περνω τους γείτωνες του xi κ xj
    neighbours_xi = neigh(xi, constraints)  # γειτωνες του xi
    neighbours_xj = neigh(xj, constraints)  # γειτωνες του xj
    sameNeighbours = set(neighbours_xi) & set(neighbours_xj)  # κοινη γείτωνες

    for xk in sameNeighbours:
        pc_support = False
        for c in range(len(domains[xk])):
            if CHECK(xi, a, xk, c, constraints) and CHECK(xj, b, xk, c, constraints):
                pc_support = True
                break
        if not pc_support:
            return False
    return True


def NSACQ(sudoku=[], domains=[], constraints=[], removedCounter=0):
    _, removedCounter = AC3(sudoku, domains, constraints, removedCounter)
    for row in domains:  # na ginei sinartisi
        if (all(elem == -2 for elem in row)):
            print("Found empty domain, domain wipeout")
            return False, removedCounter

    Q = []
    for row in range(9):
        for col in range(9):
            Q.append(node((row, col), sudoku))

    while (len(Q) > 0):
        tmpNode_i = Q.pop(0)
        if tmpNode_i.value != 0:  # Αγνούμε τα κελιά που έχουν προκαθορισμένη τιμή
            continue
        xi = tmpNode_i.domainsRow  # μας νοιάζει η "γραμμή" στον πίνακα domains
        changed = False
        for a in range(len(domains[xi])):  # Λουπα που διατρέχει για όλες τις τιμές του xi
            if domains[xi][a] == -2:  # Επίσης αγνωούμε τις τιμές της μεταβλητής οι οποίες έχουν βγει
                continue
            # print("changing value", a + 1, "from variable", xi)
            # print("domains[xi] before change", domains[xi])
            # επιλέγουμε μια τιμή και βγάζουμε τις υπόλοιπες απο το domain της μεταβλητής xi
            tmpDomains = domains[xi].copy()  # για να επαναφέρουμε το domain αργότερα
            domains[xi] = [-2 for x in domains[xi]]
            domains[xi][a] = -1
            # print("domains[xi] after change", domains[xi])
            ac3_Q = neigh(xi, constraints)  # φτιάχνουμε μια ουρά με τους γείτωνες του xi
            # print("Running ac3 for", xi, "'s neigbours:", ac3_Q)
            _, removedCounter = AC3_singleton(sudoku, domains, constraints, ac3_Q.copy(), removedCounter)  # τρεχουμε ac3 μονο για τους γείτωνες του xi

            # ελέγχουμε αν ο AC3 άδιασε καποιο domain απο εκείνους τους γείτωνες
            for row in ac3_Q:
                if (all(elem == -2 for elem in domains[row])):
                    changed = True
                    tmpDomains[a] = -2  # Αν εν τέλει οδηγειθουμε σε domain wipeout
                    # αλλάζουμε το tmpDomains, μιας και στο τέλος έχουμε domains[xi]=tmpDomains
                    removedCounter += 1  # Μετράμε την αλλαγή που μόλις κάναμε

            domains[xi] = tmpDomains  # επαναφέρουμε το domain
            # print("domains[xi] after reverting", domains[xi])

        # ελέγχουμε για αν άδειασε καποιο domain    (...γιατι και εδω ? )
        for row in domains:  # na ginei sinartisi
            if (all(elem == -2 for elem in row)):
                return False, removedCounter
        if changed:  # άμα έγινε καποιο wipeout σε καποια μεταβλητή προσθέτουμε τους γείτωνες του xi για ελεγχο πάλι
            Q.extend(ac3_Q)
    print("Variables with only 1 value available:", countSingleValue(domains))
    # printDomains(domains)
    return True, removedCounter


def printDomains(domains):
    print("domains array")
    for i in range(len(domains)):
        print(i, domains[i])


def countSingleValue(domains):
    variableCounter = 0
    for i in range(len(domains)):
        counter = 0
        for j in range(len(domains[i])):
            if domains[i][j] == -1:
                counter += 1
        if counter == 1:
            variableCounter += 1

    return variableCounter


if (__name__ == "__main__"):

    # Αρχικοποίηση των πινάκων
    sudoku = [[-1, -1, -1, -1, -1, -1, -1, -1, -1] for i in range(9)]  # 9x9
    domains = [[-1, -1, -1, -1, -1, -1, -1, -1, -1] for i in range(81)]  # 81x9
    constraints = [[0 for i in range(81)] for j in range(81)]  # 81x81

    initArrays(sudoku, domains, "sudoku3.txt")

    # prints Sudoku
    print("sudoku array")
    for i in range(len(sudoku)):
        print(i + 1, sudoku[i])
    print()

    printDomains(domains)

    # print("constrain")
    CONSTRAIN(constraints)

    # for i in range(81):
    #     print(i, C[i])

    print("\nStarting AC3")
    start_time = time.time()
    _, ac3_counter = AC3(sudoku, copy.deepcopy(domains), constraints)
    end_time = time.time()
    print("AC3 Removed Values:", ac3_counter)
    # print("%.2f" % a)
    print("AC3 Execution Time: %.5f sec" % (end_time - start_time))

    print("\nStarting RPC-1")
    start_time = time.time()
    _, rpc_counter = RPC1(sudoku, copy.deepcopy(domains), constraints)
    end_time = time.time()
    print("RPC-1 Removed Values:", rpc_counter)
    print("RPC-1 Execution Time: %.5f sec" % (end_time - start_time))

    print("\nStarting NSACQ")
    start_time = time.time()
    _, nsacq_counter = NSACQ(sudoku, copy.deepcopy(domains), constraints)
    end_time = time.time()
    print("NSACQ Removed Values:", nsacq_counter)
    print("NSACQ Execution Time: %.5f sec" % (end_time - start_time))
    

    # TODO:
    #   1. Grater than, αλλαγη CONSTRAIN και init_arrays
    #   2. Να καθαρίσει λίγο ο κώδικας και να συμμαζευτεί
