import time
import copy


class node():
    # Βοηθητική κλάση για την ουρά, δεν είναι απαραίτητη
    def __init__(self, sudokuCordinate=(-1, -1), sudoku=[]):
        self.sudokuCordinate = sudokuCordinate
        self.domainsRow = self.sudokuCordinate[0] * 9 + self.sudokuCordinate[1]
        self.value = sudoku[self.sudokuCordinate[0]][self.sudokuCordinate[1]]

    def print(self):
        print(self.sudokuCordinate, self.domainsRow, self.value)


def initArrays(sudoku=[], domains=[], constraints=[], filename=""):
    """
    Διαβάζει απο αρχείο και αποθυκεύει στους πίνακες:
    :param sudoku: array[9][9], αναπαράσταση του sudoku,
    :param domains: array[81][9], domain για κάθε κελί του sudoku
    :param constraints: array[81][81], πίνακας των constraint, για τους greater than περιορισμούς
    :param filename: string, όνομα του αρχείου απο το οποίο θα διαβάσει
    :return:
    """
    with open(filename, "r") as f:
        lines = f.readlines()

    count = 0
    for line in lines:
        if (count < 9):  # οι πρότες 9 γραμμές είναι το sudoku
            sudoku[count] = line.split(" ")  # Διαβάζει γραμμη γραμμη το αρχείο, την σπαει στα κενα
            sudoku[count][-1] = sudoku[count][-1].replace('\n', '')  # Αφαιρεί το \n απο το τελευταίο στοιχείο
            sudoku[count] = [int(x) for x in sudoku[count]]  # Μετατρέπει ολα τα στοιχεία της γραμμης σε int

        else:  # οι υπόλοιπες (αν υπάρχουν) είναι για το greater than
            # επεξεργασία της γραμμής έτσι ώστε οι αριθμοι να είνια int και τα <,> να είναι str
            gt_line = line.split(' ')
            gt_line[-1] = gt_line[-1].replace('\n', '')
            gt_line[0] = int(gt_line[0])
            gt_line[-1] = int(gt_line[-1])

            # gt_line[0] το ένα κελί, gt_line[1] είναι το άλλο, gt_line[0] ειναι τα < ή >
            if (gt_line[1] == '>'):
                constraints[gt_line[0]][gt_line[-1]] = 2  # Βάζουμε τον "ορθό" περιορισμό για την μία μεταβλητή
                constraints[gt_line[-1]][gt_line[0]] = 3  # Και τον "ανάστροφο" για την άλλη
            elif (gt_line[1] == '<'):
                constraints[gt_line[0]][gt_line[-1]] = 3
                constraints[gt_line[-1]][gt_line[0]] = 2
        count += 1  # μετρητής γραμμής αρχείου

    # Αφαιρεί όλες τις άλλες τιμές απο τις μεταβλητές με προκαθορισμένη τιμή (ΔΕΝ ΤΙΣ ΜΕΤΡΆΜΕ)
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                pass
            else:
                # (9*i)+j αντιστοιχεί την δυσδιάστατη θέση του sudoku στην μονοδιάστατη γραμμή του domains
                domains[(9 * i) + j] = [-2 for x in domains[(9 * i) + j]]  # κάθε -1 στην γραμμή του domains το κάνει -2
                domains[(9 * i) + j][sudoku[i][j] - 1] = sudoku[i][j]
    return constraints


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
        if CHECK(xi, a, xj, j, constraints):
            support = True
            return support
    return support


def REVISE(xi, xj, removedCounter, domains=[], constraints=[]):
    """
    Ελέγχει για τις τιμές του xi, αν υπάρχουν συνεπής στην xj
    :param xi: γραμμη του domains για την μεταβλητή 1
    :param xj: γραμμη του domains για την μεταβλητή 2
    :param removedCounter: Πλήθος διαγραφών τιμών
    :param domains: array[81][9], πίνακας των domains
    :param constraints: array[81][81], πίνακας των constraint
    :return: False αν δεν γίνει κάποια αλλαγή
    """
    revised = False
    for i in domains[xi]:
        if i > 0:
            return revised, removedCounter

    for i in range(len(domains[xi])):
        if domains[xi][i] != -2:
            found = SUPPORTED(xi, i, xj, domains, constraints)
            if not found:
                revised = True
                domains[xi][i] = -2
                removedCounter += 1
    return revised, removedCounter


def CONSTRAIN(constraints=[]):
    """
    Γεμίζει τον πίνακα Constrains ανάλογα με τον περιορισμούς των μεταβλητών
    :param constraints: array[81][81], πίνακας των constraint
    :return: None
    """
    row = 0
    column = 0
    r = 0
    c = 0
    for k in range(81):
        for i in range(9):
            for j in range(9):
                # Μιάς και γράφουμε και στην initArrays() αγνωούμε τις μεταβλητές που έχουν ήδη κάποιο constrain
                if constraints[row][(9 * i) + j] != 0:
                    continue
                # αν είναι στην ίδια γραμμή να είναι διαφορετικοί αριθμοί
                if r == i:
                    constraints[row][(9 * i) + j] = 1
                # αν είναι στην ίδια στηλη να είναι διαφορετικοί αριθμοί
                if c == j:
                    constraints[row][(9 * i) + j] = 1

                # Αν είναι στο ίδιο κουτι να είναι διαφορετικοί αριθμοί
                startRow = r - r % 3  # δείχνουν στο πανω αριστερα στοιχείο του block
                startCol = c - c % 3
                for t in range(3):
                    for y in range(3):
                        # οπότε σε αυτές τις 9 επανναήψεις προσθέτουμε απο την πάνω αριστερά γωνία
                        if constraints[row][(9 * (startRow + t)) + (startCol + y)] == 0:
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
    :param constraints: array[81][81], πίνακας των constraint
    :return: neighbours(array): πίνακας με τους γείτωνες του row, (γραμμη απο πίνακα domains)
    """
    neighbours = []
    for i in range(len(constraints[row])):
        if constraints[row][i] in [1, 2, 3]:  # επιστρέφει τους γείτωνες βλέποντας τις τιμές στον πίνακα constrains
            neighbours.append(i)
    return neighbours


def AC3(sudoku=[], domains=[], constraints=[], removedCounter=0):
    """
    Υλοποιήση του αλγορίθμου AC3
    :param sudoku: array[9][9], πίνακας του sudoku
    :param domains: array[81][9], πίνακας των domains
    :param constraints: array[81][81], πίνακας των constraint
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
        tmpNode_i = Q.pop(0)  # Η ουρά περιέχει nodes
        i = tmpNode_i.domainsRow  # μας νοιάζει η "θέση" της στην domains
        neighbours = neigh(i, constraints)  # εξετάζουμε τους γείτωνες του i
        for j in neighbours:
            if i == j:  # για να μην εξετάσουμε τον εαυτό του
                continue
            updated, removedCounter = REVISE(i, j, removedCounter, domains,
                                             constraints)  # αν έχει κάνει αλλαγή επιστρέφει true
            count = 9
            for ch in range(9):  # Ελέγχουμε αν κάτι μείνει κενό
                if domains[i][ch] == -2:
                    count = count - 1
                    if count == 0:
                        return False, removedCounter
            if updated:
                Q.append(tmpNode_i)  # Αν έχει αφαιρεθεί κάτι απο το domain που εξετάσαμε,
                # το ξαναβάζουμε στην ουρά

    print("Variables with only 1 value available:", countSingleValue(domains))
    return True, removedCounter


def AC3_singleton(sudoku=[], domains=[], constraints=[], Q=[], removedCounter=0):
    """
    Υλοποιήση του αλγορίθμου AC3, τρέχει σε προκαθορισμένη ουρά
    :param sudoku: array[9][9], πίνακας του sudoku
    :param domains: array[81][9], πίνακας των domains
    :param constraints: array[81][81], πίνακας των constraint
    :param Q: queue, Η ουρά στην οποία θέλουμε να τρέξει (γραμμές του πίνακα domains)
    :param removedCounter: Μετρητής για τις αφαιρέσεις τιμών (τον μεταφέρει στην revise)
    :return: False, αν κάποιο domain μήνει άδειο
    """

    while (len(Q) > 0):
        # Σε κάθε επανάληψη αφαιρούμε μια μεταβλητή
        i = Q.pop(0)  # Η ουρά περιέχει γραμμές domains
        neighbours = neigh(i, constraints)  # εξετάζουμε τους γείτωνες του i
        # print("variable:", i, "checking neighbours:", neighbours)
        for j in neighbours:
            if i == j:  # για να μην εξετάσουμε τον εαυτό του
                continue

            updated, removedCounter = REVISE(i, j, removedCounter, domains,
                                             constraints)  # αν έχει κάνει αλλαγή επιστρέφει true
            count = 9
            for ch in range(9):  # Ελέγχουμε αν κάτι μείνει κενό
                if domains[i][ch] == -2:
                    count = count - 1
                    if count == 0:
                        # print("Found empty domain", i, domains[i])
                        return False, removedCounter
            if updated:
                Q.append(i)  # Αν έχει αφαιρεθεί κάτι απο το domain που εξετάσαμε,
                # το ξαναβάζουμε στην ουρά
    return True, removedCounter


def RPC1(sudoku=[], domains=[], constraints=[], removedCounter=0):
    """
    Υλοποίηση του αλγόριθμου RPC
    :param sudoku: array[9][9], πίνακας του sudoku
    :param domains: array[81][9], πίνακας των domains
    :param constraints: array[81][81], πίνακας των constraint
    :param removedCounter:  Μετρητής για τις αφαιρέσεις τιμών ( τον μεταφέρει στην revise)
    :return: True/False ανάλογα με το αν άδιασε domain, removedCounter: μετρήτής αφαιρέσεων
    """
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
            if i == j:  # για να μην εξετάσουμε τον εαυτό του
                continue

            updated, removedCounter = REVISE_RPC(i, j, removedCounter, domains,
                                                 constraints)  # αν έχει κάνει αλλαγή επιστρέφει true
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
    print("Variables with only 1 value available:", countSingleValue(domains))
    return True, removedCounter


def REVISE_RPC(xi, xj, removedCounter, domains=[], constraints=[]):
    """
    Ελέγχει για τις τιμές του xi, αν υπάρχουν συνεπής στην xj (εκδοση RPC)
    :param xi: γραμμη του domains για την μεταβλητή 1
    :param xj: γραμμη του domains για την μεταβλητή 2
    :param removedCounter: Μετρητής για τις αφαιρέσεις τιμών
    :param domains: array[81][9], πίνακας των domains
    :param constraints: array[81][81], πίνακας των constraint
    :return: False αν δεν γίνει κάποια αλλαγή, removedCounter: μετρήτής αφαιρέσεων
    """
    revised = False
    for i in domains[xi]:
        if i > 0:
            return revised, removedCounter

    for i in range(len(domains[xi])):
        if domains[xi][i] != -2:
            found = SUPPORT_RPC(xi, i, xj, domains, constraints)
            if not found:
                revised = True
                domains[xi][i] = -2
                removedCounter += 1
    return revised, removedCounter


def SUPPORT_RPC(xi, a, xj, domains=[], constraints=[]):
    """
    Ελέγχει αν για την τιμή a της xi υπάρχουν συνεπής στην xj (εκδοση RPC)
    :param xi: Μεταβλητή 1 (1-81)
    :param a: τιμή της μεταβλητής 1
    :param xj: Μεταβλητή 2
    :param domains: array[81][9], πίνακας των domains
    :param constraints: array[81][81], πίνακας των constraint
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
                    if CHECK(xi, a, xj, m, constraints):
                        return True
            if PC(xi, a, xj, j, constraints):
                return True  # ειναι TRUE και RPC1
            else:
                return False  # Δεν είναι RPC1
    return False


def PC(xi, a, xj, b, constraints=[]):
    """
    Υλοποίηση του path consistency
    :param xi: Μεταβλητή 1  (γραμμή στον πίνακα domains)
    :param a: τιμή της μεταβλητής 1
    :param xj: Μεταβλητή 2  (γραμμή στον πίνακα domains)
    :param b: τιμή της μεταβλητής 2
    :param constraints: Πίνακας constrains
    :return: True/False ανάλογα με το αν οι τιμές των xi, xj (και μία τρίτη) είναι path Consistent
    """

    # παίρνω τους γείτωνες του xi κ xj
    neighbours_xi = neigh(xi, constraints)  # γειτωνες του xi
    neighbours_xj = neigh(xj, constraints)  # γειτωνες του xj
    sameNeighbours = set(neighbours_xi) & set(neighbours_xj)  # κοινοί γείτωνες

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
    """
    Υλοποίηση του NSACQ αλγορίθμου.
    :param sudoku: array[9][9], πίνακας του sudoku
    :param domains: array[81][9], πίνακας των domains
    :param constraints: array[81][81], πίνακας των constraint
    :param removedCounter: Πλήθος διαγραφών τιμών
    :return: False, αν κάποιο domain μήνει άδειο, πλήθος διαγραφών
    """
    print("From AC3: ", end="")
    _, removedCounter = AC3(sudoku, domains, constraints, removedCounter)

    for row in domains:  # na ginei sinartisi
        if (all(elem == -2 for elem in row)):
            print("Found empty domain, domain wipeout")
            return False, removedCounter
    startDomains = copy.deepcopy(domains)
    Q = []
    for row in range(9):
        for col in range(9):
            Q.append(node((row, col), sudoku))

    while (len(Q) > 0):
        tmpNode_i = Q.pop(0)
        if type(tmpNode_i) != int:  # Αυτο το κανουμε γιατι στην αρχη η ουρα εχει nodes και αργοτερα ints
            if tmpNode_i.value != 0:  # Αγνούμε τα κελιά που έχουν προκαθορισμένη τιμή
                continue
            xi = tmpNode_i.domainsRow  # μας νοιάζει η "γραμμή" στον πίνακα domains
        else:
            if tmpNode_i != 0:  # Αγνούμε τα κελιά που έχουν προκαθορισμένη τιμή
                continue
            xi = tmpNode_i  # μας νοιάζει η "γραμμή" στον πίνακα domains
        changed = False

        for a in range(len(domains[xi])):  # Λουπα που διατρέχει για όλες τις τιμές του xi
            if domains[xi][a] == -2:  # Επίσης αγνωούμε τις τιμές της μεταβλητής οι οποίες έχουν βγει
                continue
            # επιλέγουμε μια τιμή και βγάζουμε τις υπόλοιπες απο το domain της μεταβλητής xi
            tmpDomains = domains[xi].copy()  # για να επαναφέρουμε το domain αργότερα
            domains[xi] = [-2 for x in domains[xi]]
            domains[xi][a] = -1
            ac3_Q = neigh(xi, constraints)  # φτιάχνουμε μια ουρά με τους γείτωνες του xi
            AC3_singleton(sudoku, domains, constraints, ac3_Q.copy(),
                                              removedCounter)  # τρεχουμε ac3 μονο για τους γείτωνες του xi

            # ελέγχουμε αν ο AC3 άδιασε καποιο domain απο εκείνους τους γείτωνες
            for row in ac3_Q:
                if (all(elem == -2 for elem in domains[row])):
                    changed = True
                    tmpDomains[a] = -2  # Αν εν τέλει οδηγειθουμε σε domain wipeout
                    # αλλάζουμε το tmpDomains, μιας και στο τέλος έχουμε domains[xi]=tmpDomains
                    removedCounter += 1  # Μετράμε την αλλαγή που μόλις κάναμε
            domains = startDomains
            domains[xi] = tmpDomains  # επαναφέρουμε το domain
            # print("after: domains[",xi,"]:", domains[xi])

        # ελέγχουμε αν αδιασε
        if (all(elem == -2 for elem in domains[xi])):
            print("Found empty domain:", xi, domains[xi])
            return False, removedCounter

        if changed:  # άμα έγινε καποιο wipeout σε καποια μεταβλητή προσθέτουμε τους γείτωνες του xi για ελεγχο πάλι
            Q.extend(ac3_Q)

    print("Variables with only 1 value available:", countSingleValue(domains))
    return True, removedCounter

def printDomains(domains):
    """
    Τυπώνει τον πίνακα domains σε ευανάγνωστη μορφή (και τους άλλους βασικά)
    :param domains: array, πίνακας για εκτύπωση
    :return: None
    """
    for i in range(len(domains)):
        print(i, domains[i])


def countSingleValue(domains):
    """
    Βλέπει πόσες μεταβλητές έμειναν με μία τιμή
    :param domains: array[81][9], πίνακας των domains
    :return: variableCounter: int, πλήθος μεταβλητών με μία τιμή
    """
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

    constraints = initArrays(sudoku, domains, constraints, "sudoku1.txt")
    # prints Sudoku

    print("sudoku array")
    printDomains(sudoku)
    print("Domains array")
    printDomains(domains)

    CONSTRAIN(constraints)
    # print("Constraints array")
    # printDomains(constraints)

    print("\nStarting AC3")
    start_time = time.time()
    _, ac3_counter = AC3(sudoku, copy.deepcopy(domains), constraints)
    end_time = time.time()
    print("AC3 Removed Values:", ac3_counter)
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
