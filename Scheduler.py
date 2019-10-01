#Schedule script for generating Timetables from specific input
#Idea for improvement: format and save files as .csv


import os, shutil

class myMenu():
    """
    \brief myMenu class that stores menu handling functions
    """
    def printMenuMain(self):
        """
        \breif Function that prints main menu
        \note   Exit - exit program; Create Schedule - Open Create Menu;
        Run Combinations - Finds all possible Timetables for current problem;
        Add Classes - fast adding classes based on number
        """
        print("0. Exit")
        print("1. Create Schedule")
        print("2. Run Combinations")
        print("3. Add Classes")

    def printMenuCreate(self):
        """
        \breif Function that prints Create Menu
        \note Exit - exit program; Add Subject - Add subject and all its classes;
        Create Subject File - Create file that stores raw Subjects
        """
        print("0. Exit")
        print("1. Add Subject")
        print("2. Create Subject File")
        print("3. Open Subjects File")

    def getInput(self, num_of_commands):
        """
        \brief Functions that handles input of commands for menus
        \param num_of_commands Number to mod input commands
        \return Return input number from 0-num_of_commands - 1
        """
        correctInput = True
        while(correctInput):
            try:
                correctInput = False
                cmd = int(input(">> "))
                cmd = cmd % num_of_commands
            except Exception as e:
                print(e)
                correctInput = True
        return cmd

    def menu(self):
        """
        \brief Function that handles all menus
        \return Return value specified by menu by tree
        """
        self.printMenuMain()
        cmd = self.getInput(4)

        if(cmd == 0):
            return 0
        elif(cmd == 1):
            self.printMenuCreate()
            cmd = self.getInput(4)

            if(cmd == 0):
                return 10
            elif(cmd == 1):
                return 11
            elif(cmd == 2):
                return 12
            elif(cmd == 3):
                return 13
        elif(cmd == 2):
            return 21
        elif(cmd == 3):
            return 3


class subject():
    """
    \brief subject Data Structure that contains basic Subject information
    \attr time, description, day, name
    """
    def __init__(self):
        self.time = []
        self.description = ""
        self.day = ""
        self.name = ""

    def setDescription(self, desc):
        self.description = desc

    def addTime(self, time):
        self.time.append(time)

    def getDescription(self):
        return self.description

    def getTime(self):
        return self.time

class Schedule(myMenu):
    """
    \brief Schedule Class that handles Timetables and Subjects
    \attr subjectsTime - Dictionary that maps subject to list of classes
    \attr generatedAnswers - All Timetables (list of subjects)
    \attr listClasses - list of all different subjects
    """
    def __init__(self):
        self.subjectsTime = {}
        self.generatedAnswers = []
        self.start()

    def start(self):
        """
        \brief Handles menu and methods
        """
        while(1):
            cmd = self.menu()

            if(cmd == 0):
                exit()
            elif(cmd == 10):
                continue
            elif(cmd == 11):
                self.addSubject()
            elif(cmd == 12):
                self.createFile()
            elif(cmd == 13):
                self.openFile()
            elif(cmd == 3):
                self.addClasses()
            elif(cmd == 21):
                self.generateWrap()

    def addSubject(self):
        """
        \brief Method that adds Subject with all its classes
        \note Input method DAY-XX-XX
        """
        name = input("Name ")
        self.subjectsTime.setdefault(name, [])

        val = input("Time\n DAY-XX-XX, 0 to exit\n >> ")
        while(val != '0'):
            tempSubj = subject()
            tempSubj.name = name
            try:
                day, start, end = val.split("-")
                start = int(start)
                end = int(end)
            except Exception as e:
                print(e)

            tempSubj.day = day

            for i in range(start, end):
                tempSubj.addTime(i)

            val = input("Description ")
            tempSubj.setDescription(val)

            self.subjectsTime[name].append(tempSubj)
            val = input("Time\n XX-XX, 0 to exit\n >> ")

    def createFile(self):
        """
        \brief Creates file from subjectsTime that contains Raw Subjects
        """
        file = open("Subjects.txt", "w")

        for key in self.subjectsTime:
            file.write(key + "::")
            for subj in self.subjectsTime[key]:
                file.write(subj.day + "-" + str(subj.time[0]) + "-" + str(subj.time[-1] + 1) + "##" + subj.description + '//')
            file.write('\n')
        file.close()

    def openFile(self):
        """
        \brief Read subjects from file that contains Raw Subjects
        """
        file = open("Subjects.txt", "r")
        self.subjectsTime.clear()
        for line in file:
            name, rest = line.split("::")
            rest = rest[:-3]
            self.subjectsTime.setdefault(name, [])
            subjList = rest.split("//")
            #subjList.pop()
            for subj in subjList:
                tempSubj = subject()
                tempSubj.name = name
                time, desc = subj.split("##")
                day, start, end = time.split("-")
                start = int(start)
                end = int(end)
                tempSubj.setDescription(desc)
                tempSubj.day = day
                for i in range(start, end):
                    tempSubj.addTime(i)
                self.subjectsTime[name].append(tempSubj)
        file.close()

    def addClasses(self):
        """
        \brief Inesrts classes into Data Structure
        \note Input format NAME..DAY-XX-XX..DESC
        """
        num = int(input("Number of classes "))
        for i in range(num):
            line = input("Add Class \n NAME..DAY-XX-XX..DESC")

            name, time, desc = line.split("..")
            day, start, end = time.split("-")

            start = int(start)
            end = int(end)

            tempSubj = subject()
            tempSubj.day = day
            tempSubj.description = desc
            tempSubj.name = name
            for i in range(start, end):
                tempSubj.addTime(i)

            self.subjectsTime.setdefault(name, []).append(tempSubj)

    def allClasses(self):
        """
        \brief Creates list of all different subjects listClasses
        """
        self.listClasses = []
        for key in self.subjectsTime:
            self.listClasses.append(key)

    def generateWrap(self):
        """
        \brief Wrapper function for genereta(). Also prints the generated answers in txt files
        """
        self.allClasses()
        #dayDict = {"MON":[], "TUE":[], "WED":[], "THU":[], "FRI":[]}
        dayFlag = {"MON":[], "TUE":[], "WED":[], "THU":[], "FRI":[]}
        self.listClasses.sort()
        self.generate(dayFlag, 0, [])

        self.printScheduleWrap()


    def generate(self, dayFlag, ind, genAnswer):
        """
        \brief Function that racursively generates all permutations of Subjects and adds it to generatedAswers
        \param dayFlag - dctionary that flags busy hours
        \param ind Index of Subjects from listClasses
        \param genAnswer previous Classes that are in current Timetable
        """
        if(ind >= len(self.listClasses)):
            self.generatedAnswers.append(genAnswer)
            return

        for subj in self.subjectsTime[self.listClasses[ind]]:
            if(not subj.time[0] in dayFlag[subj.day] and not subj.time[-1] in dayFlag[subj.day]):
                temp = dayFlag.copy()
                l = temp[subj.day].copy()
                l += subj.time
                temp[subj.day] = l
                self.generate(temp, ind+1, genAnswer + [subj])
        return

    def printScheduleWrap(self):
        """
        \brief Wrapper function for printing Timetables
        """
        for i, ans in enumerate(self.generatedAnswers):
            self.printSchedule(ans, i)

    def printSchedule(self, combination, num):
        """
        \brief Prints single combination of classes in Timetables/Timetable.txt
        \param combination Combination of classes that are in timetable
        \param num Ordinaty number of combination
        """
        dayDict = {"MON":[], "TUE":[], "WED":[], "THU":[], "FRI":[]}
        for subj in combination:
            # if(subj.name == "ASP2P" and subj.description.find("MILO") != -1):
            #     return
            # if(subj.name == "ASP2V" and subj.description.find("MISIC") == -1):
            #     return

            dayDict[subj.day].append(subj.name + " " + subj.day + " " + str(subj.time[0]) + "-" + str(subj.time[-1] + 1) + " " + subj.description + '\n')

##        if(len(dayDict["MON"]) != 0):
##            return

        try:
            os.stat("Timetables/")
        except:
            os.mkdir("Timetables/")

        file = open("Timetables/Timetable" + str(num) + ".txt", "w")

        for day in dayDict:
            file.write(day + ':\n')
            for sub in dayDict[day]:
                file.write(sub)
            file.write("---------\n")

        file.close()




def main():
    sch = Schedule()

    pass

if __name__ == "__main__":
    main()