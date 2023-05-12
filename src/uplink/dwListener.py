
import time

def checkTheFile():
    # open the file called dwoutputmonitor
    # check the last 10 lines of the file
    # if the last 10 lines contain the word "cutdown" then print "slay big time"

    # open the file
    file = open("dwoutputmonitor", "r")

    # read the file
    fileContent = file.read()

    # close the file
    file.close()

    # split the file content into a list of lines
    splitFileContent = fileContent.split("\n")

    # get the last 10 lines of the file
    lastTenLines = splitFileContent[-10:]

    # join the last 10 lines into a string
    lastTenLinesString = "\n".join(lastTenLines)

    # check the last 30 lines of the file
    if "cutdown" in lastTenLinesString:
        print("slay big time")


while True:
    checkTheFile()
    time.sleep(5)