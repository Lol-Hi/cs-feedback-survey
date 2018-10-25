#Importing my other python files
import read_config as rc #python file to read config.txt. Functions from this file: readConfig(configName="config.txt")
import excel_functions as ex #python file to read from the required excel sheet. Functions from this file: openExcel(filename, sheetname)
from question_classes import NumericQn, CategoricalQn, FreeResponseQn, DemographicQn #python file containing classes for each question type, with functions to evaluate them
import output_methods #python file to output the analysis to the console and a word document. Functions from this file: console_output(question, exclude=[ ], summLen=5) and docx_output(question, doc, exclude=[ ], summLen=5)

#Importing other libraries
import docx #allows me to write to a Microsoft Word Document

####################
### Main program ###
####################

#reading from the configuration file
configs = rc.readConfig() #read config.txt. Returns a list containing various information (as listed below)
                          #simply returns "ERROR" when an error occurs
if configs != "ERROR": #if configs == "ERROR", do not execute the rest of the program
    #elements of the configuration file
    xlName = configs[0] #first element: the name of the Excel file containing the desired sheet
    sheetName = configs[1] #second element: the name of the Excel sheet to read the data from
    docName = configs[2] #third element: the name of the Word Document to save the analysis from
    questions = configs[3] #fourth element: a dictionary with the details of each question
                           #each question is arranged as <question no.>: <question type>
    leaveOut = configs[4] #fifth element: a list of words (strings) to leave out from the summary
    summLen = configs[5] #sixth element: the number of sentences to be included in the summary

    #opening the files
    responses = ex.openExcel(xlName, sheetName) #reads from the desired excel sheet. Returns a 2D list containing the responses for each question

if configs != "ERROR" and responses != "ERROR": #if configs == "ERROR" or responses == "ERROR", do not execute the rest of the program
    #opening the files (cont'd)
    analysisDoc = docx.Document() #opens the Word Document to output the analysis in. Returns the name of the document
    
    #outputting the title
    print("Analysis of {} (from {})".format(sheetName, xlName)) #printing the title to the console
    docTitle = analysisDoc.add_heading("Analysis of {}\n(from {})".format(sheetName, xlName), 0) #writing the title to the Word Document
    
    #evaluation of the questions and outputting the analysis
    qnCount = 0 #keeps count of the questions (so that the relevant response list can be obtained)

    for qnNo, qnType in questions.items(): #iterates through the dictionary of questions (containing the question number and the type of question)
        qnResponse = responses[qnCount] #gets the relevent response list for the question (containing the question statement and the list of responses)
        qnStatement = qnResponse[0] #retrieving the question statement from the response list (since the question statement for each question is in row A of the excel sheet)
        del qnResponse[0] #delete the question statement from the response list to get a list purely with the responses for the questions
        #setting the required question class
        if qnType == "numeric":
            try:
                currQn = NumericQn(qnNo, qnStatement, qnResponse)
            except TypeError:
                break
        elif qnType == "categorical": 
            currQn = CategoricalQn(qnNo, qnStatement, qnResponse)
        elif qnType == "free-response":
            currQn = FreeResponseQn(qnNo, qnStatement, qnResponse)
        else:
            currQn = DemographicQn(qnNo, qnStatement)
        output_methods.console_output(currQn, exclude=leaveOut, summLen=summLen) #print the analysis of the question to the console
        output_methods.docx_output(currQn, analysisDoc, exclude=leaveOut, summLen=summLen) #write the analysis of the question to the Word Document
        qnCount += 1 #update the question count

    #saving the Word Document
    analysisDoc.save(docName) #saves the word document according to the required name

print("\n------------------\n")
print("Program ending...") #tells the user that the program is ending. Prints regardless if an error has occurred
