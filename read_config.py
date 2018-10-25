def readConfig(configName="config.txt"):
    """
    Reads the information from configuration file (config.txt)
    Returns the following information in a list:
    1) The name of the Excel file containing the designated Excel sheet
    2) The name of the Excel sheet to read the data from
    3) The name of the Word document to save the analysis to
    4) A dictionary with the details of each question
       Each entry is arranged as <question no.>: <question type>
    5) A list of strings to leave out from the summary
    6) The number of lines in the summary

    >>> readConfig("Hello.txt")
    Error: Hello.txt not found
    'ERROR'
    
    >>> readConfig("./config_testing/config-wrong(1).txt")
    Error on line 1: Incorrect file type. Your filename should end in '.xlsx'
    'ERROR'
    >>> readConfig("./config_testing/config-wrong(5).txt")
    Error on line 5: Please enter the number of lines you want in your summary
    'ERROR'
    >>> readConfig("./config_testing/config-wrong(7).txt")
    Error on line 7: Incorrect file type. Your filename should end in '.docx'
    'ERROR'
    >>> readConfig("./config_testing/config-wrong(19++).txt")
    Error on line 20: Please enter either 'demographic', 'numerical', 'categorical' or 'free-response'
    'ERROR'
    >>> readConfig("./config_testing/config-right.txt")
    ('responses_testing.xlsx', 'Form responses 1', 'response_analysis.docx', {'1': 'demographic', '2': 'numeric', '3': 'categorical', '4': 'free-response'}, ['nil', 'na', 'none', '-', '–', 'everything', 'nothing', 'your mum'], 5)
    """
    try:
        config = open(configName, "r", encoding="utf-8") #opens the config file. The utf-8 encoding is to ensure that the program will not crash when met with the dashes I used in the file
    except:
        print("Error: {} not found".format(configName))
        return "ERROR" #to tell the main program about the error, so as to not run the rest of the program
    try:
        filename = str(config.readline().replace("\n", "").split(": ")[1]) #obtains the name of the Excel file
                                                                           #the line is split to get only the second part such that the instruction won't be included
    except:
        print("Error on line 1: Please enter the name of a file")
        return "ERROR" 
    else:
        if ".xlsx" not in filename:
            print("Error on line 1: Incorrect file type. Your filename should end in '.xlsx'")
            return "ERROR" 
    try:
        sheetname = str(config.readline().replace("\n", "").split(": ")[1])#obtains the name of the Excel sheet
    except:
        print("Error on line 2: Please enter a string")
        return "ERROR"
    config.readline() #on the config file, this is an empty line
    try:
        leaveOut = str(config.readline().replace("\n", "").split(": ")[1]).split(", ") #obtains the list of words to leave out
    except:
        print("Error on line 4: Please enter a list of strings to exclude from the summary")
        return "ERROR"
    try:
        summLen = int(config.readline().replace("\n", "").split(": ")[1].strip()) #obtains the number of lines to have in the summary
    except:
        print("Error on line 5: Please enter the number of lines you want in your summary")
        return "ERROR"
    config.readline() #on the config file, this is an empty line
    try:
        docsname = str(config.readline().replace("\n", "").split(": ")[1]) #obtains the name of the Word document
    except:
        print("Error on line 7: Please enter the name of a file")
        return "ERROR"
    else:
        if ".docx" not in docsname:
            print("Error on line 7: Incorrect file type. Your filename should end in '.docx'")
            return "ERROR"
    for i in range(11): #on the config file, these 11 lines include instructions about the following section, along with a few empty lines
        config.readline()
    qnTypes = config.readlines() #reads the remaining of the document (the question types, arranged in the form of <question no.>: <question type>
    questions = {} #initialises the output dictionary that will save the information about the questions
    lineCount = 19 #keeps track of the line so as to produce the correct error message
    for line in qnTypes: #iterates through the remaining lines (information about the question types)
        qn = line.lower().replace("\n", "").split(": ") #splits up the question number and question type
        if qn[1] not in ("demographic", "numeric", "categorical", "free-response"):
            print("Error on line {}: Please enter either 'demographic', 'numerical', 'categorical' or 'free-response'".format(lineCount))
            return "ERROR"
        questions[qn[0]] = qn[1] #sets the dictionary such that key = question number and value = question type
        lineCount += 1 #updates the counter
    config.close() #closes config file
    return filename, sheetname, docsname, questions, leaveOut, summLen #returns all the information collected from the config file
