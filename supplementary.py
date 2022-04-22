
def visualizeConstraints(constrains=[]):
    constrainFile = open("constrain.txt", "w")
    constrainFile.write("   ")
    for i in range(81):
        text = str(i) + " "
        if i < 10:
            text = "0"+str(i) + " "
        constrainFile.write(text)
    constrainFile.write("\n")
    counter = 0
    for i in constrains:
        text = str(counter)
        if counter < 10:
            text = "0"+str(counter)
        constrainFile.write(text)

        for j in i:
            text = " " + str(j) + " "
            constrainFile.write(text)
        constrainFile.write('\n')
        counter+=1
    constrainFile.close()