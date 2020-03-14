#!/usr/bin/python3
import numpy as np

officeFloor = []
developersList = []
managersList = []
width_height = []

class Employee(object):
    company = "defaultCompany"
    bonus = 0
    skills = []
    indx = -1
    indy = -1

    def __init__(self, company, bonus, skills):
        self.company = company
        self.bonus = bonus
        self.skills = skills[:]


def readEmployees(employeesNumber, employeesList, fileObject):
    for i in range(employeesNumber):
        line = fileObject.readline()
        splitString = line.split(" ", 3)
        company = splitString[0]
        bonus = (splitString[1].split("\n"))[0]
        skillsString = ""
        if len(splitString) > 2:
            skillsString = (splitString[3].split("\n"))[0]
        employee = Employee(company, int(bonus), skillsString.split(" "))
        employeesList.append(employee)


def readOfficeFloor(fileObject, height):
    for i in range(height):
        line = fileObject.readline()
        parsed = (line.split('\n'))[0]
        row = []
        for char in parsed:
            row.append(char)
        officeFloor.append(row)


def parseInput(fileName):
    fileObject = open(fileName, "r", encoding="UTF-8")

    # Read width and height
    line = fileObject.readline()
    splitString = line.split(sep=" ")
    width = int(splitString[0])
    height = int(splitString[1])

    width_height.append(width)
    width_height.append(height)

    readOfficeFloor(fileObject, height)
    
    # read all developersList
    developersNumber = int(fileObject.readline())
    readEmployees(developersNumber, developersList, fileObject)
    
    # read all project managers
    NUM_PROJECT_MANAGERS = int(fileObject.readline())
    readEmployees(NUM_PROJECT_MANAGERS, managersList, fileObject)

    fileObject.close()

    employeesMatrix = []

    for i in range(height):
        row = []
        for j in range(width):
            row.append(Employee("", 0, []))
        employeesMatrix.append(row)

    return employeesMatrix



def debugInputParse():
    print(officeFloor)
    for developer in developersList:
        print(developer.company, sep=" ")
        print(developer.bonus, sep=" ")
        print(developer.skills)

    for projectManager in managersList:
        print(projectManager.company, sep=" ")
        print(projectManager.bonus, sep=" ")


def printFormattedList(list, outputFile):
    for employee in list:
        if employee.indx > -1 and employee.indy > -1:
            outputString = "{} {}\n".format(employee.indx, employee.indy)
            outputFile.write(outputString)
        else:
            outputFile.write("X\n")


def printOutput(fileName):
    outputFileName = (fileName.split("."))[0]
    outputFileName += "_output.txt"

    outputFile = open(outputFileName, "w", encoding="UTF-8")

    printFormattedList(developersList, outputFile)
    printFormattedList(managersList, outputFile)

    outputFile.close()
 

def workPotential(skills1, skills2) :
    countInCommon = 0
    countNotCommon = 0
    skillIntersect = []
    for skill in skills1 :
        if skill in skills2:
            countInCommon += countInCommon
            skillIntersect.append(skill)
    skillUnion = []
    skillUnion = skills1 + skills2
    for skill in skillUnion :
        if skill not in skillIntersect:
            countNotCommon += countNotCommon

    return countNotCommon * countInCommon

def bonusPotential( employee1, employee2):
    if employee1.company == employee2.company:
        return employee1.bonus * employee2.bonus
    else:
        return 0

def potentialInMatrix(employee, matrix, indx, indy, W, H) :
    totalPotential = 0
    if indy > 0:    
        totalPotential += bonusPotential(employee, matrix[indy - 1][indx]) + workPotential(employee.skills, matrix[indy - 1][indx].skills)
    if indy < (H - 1): 
        totalPotential += bonusPotential(employee, matrix[indy + 1][indx]) + workPotential(employee.skills, matrix[indy + 1][indx].skills)
    if indx > 0:   
        totalPotential += bonusPotential(employee, matrix[indy][indx - 1]) + workPotential(employee.skills, matrix[indy][indx - 1].skills)
    if indx < (W - 1):   
        totalPotential += bonusPotential(employee, matrix[indy][indx + 1]) + workPotential(employee.skills, matrix[indy][indx + 1].skills)

    return totalPotential


def fillManagers(managerList, refMatrix, matrix, W, H) :
    bestI = -1
    bestJ = -1
    manListIdx = 0
    bestPotential = 0
    for i in range(H):
        for j in range(W):
            if refMatrix[i][j] == 'M' :
                matrix[i][j] = managerList[manListIdx]
                managerList[manListIdx].indx = j
                managerList[manListIdx].indy = i
                manListIdx = manListIdx + 1
                if manListIdx > 2 :
                    for k in range(i):
                        for t in range(W):
                            if (refMatrix[i][j] == 'M') & (k != i | t < j) :
                                if(potentialInMatrix(matrix[i][j], matrix, j, i, W, H) + potentialInMatrix(matrix[k][t], matrix, t, k, W, H)< potentialInMatrix(matrix[k][t], matrix, j, i, W, H) + potentialInMatrix(matrix[i][j], matrix, t, k, W, H)):
                                    troca(matrix[i][j], matrix[k][t])
    for m in range(manListIdx, len(managerList)) :
        bestI = -1
        bestJ = -1
        bestPotential = 0
        for i in range(H):
            for j in range(W):
                 if refMatrix[i][j] == 'M' :
                    if(potentialInMatrix(matrix[i][j], matrix, j, i, W, H) < potentialInMatrix(managersList[m], matrix, j, i, W, H) ):
                        if(potentialInMatrix(managersList[m], matrix, j, i, W, H) > bestPotential):
                            bestI = i
                            bestJ = j
                            bestPotential = potentialInMatrix(managersList[m], matrix, j, i, W, H)
        if( bestI >= 0):
            troca(matrix[bestI][bestJ], managersList[m])                   


def fillDevelopers(developersList, refMatrix, matrix, WIDTH, H) :
    bestI = -1
    bestJ = -1
    devListIdx = 0
    bestPotential = 0
    for i in range(H):
        for j in range(WIDTH):
            if refMatrix[i][j] == '_' :
                matrix[i][j] = developersList[devListIdx]
                developersList[devListIdx].indx = j
                developersList[devListIdx].indy = i
                devListIdx = devListIdx + 1
                if devListIdx > 1  :
                    for k in range(i):
                        for t in range(WIDTH):
                            if (refMatrix[i][j] == '_') and (k != i | t < j) :
                                if(potentialInMatrix(matrix[i][j], matrix, j, i, WIDTH, H) + potentialInMatrix(matrix[k][t], matrix, t, k, WIDTH, H)< potentialInMatrix(matrix[k][t], matrix, j, i, WIDTH, H) + potentialInMatrix(matrix[i][j], matrix, t, k, WIDTH, H)):
                                    troca(matrix[i][j], matrix[k][t])
    
    for d in range(devListIdx, len(developersList)) :
        bestI = -1
        bestJ = -1
        bestPotential = 0
        for i in range(H):
            for j in range(WIDTH):
                 if refMatrix[i][j] == '_' :
                    if(potentialInMatrix(matrix[i][j], matrix, j, i, WIDTH, H) < potentialInMatrix(developersList[d], matrix, j, i, WIDTH, H) ):
                        if(potentialInMatrix(developersList[d], matrix, j, i, WIDTH, H) > bestPotential):
                            bestI = i
                            bestJ = j
                            bestPotential = potentialInMatrix(developersList[d], matrix, j, i, WIDTH, H)
        if( bestI >= 0):
            troca(matrix[bestI][bestJ], developersList[d])   
                

def troca(employee1, employee2) :
    aux = Employee("", 0, [])
    aux.company = employee1.company
    aux.bonus = employee1.bonus
    aux.skills = employee1.skills[:]
    aux.indx = employee1.indx
    aux.indy = employee1.indy

    employee1.company = employee2.company
    employee1.bonus = employee2.bonus
    employee1.skills = employee2.skills[:]
    employee1.indx = employee2.indx
    employee1.indy = employee2.indy
    
    employee2.company = aux.company
    employee2.bonus = aux.bonus
    employee2.skills = aux.skills[:]
    employee2.indx = aux.indx
    employee2.indy = aux.indy


def main():
    employeesMatrix = parseInput("a_solar.txt")
    fillManagers(managersList, officeFloor, employeesMatrix, width_height[0], width_height[1])
    fillDevelopers(developersList, officeFloor, employeesMatrix, width_height[0], width_height[1])
    printOutput("a_solar.txt")


if __name__ == "__main__":
    main()   
