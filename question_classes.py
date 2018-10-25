#Import other python libraries
import math #for math.ceil()
import string #for string.punctuation

#Import other libraries from external sources
from matplotlib import pyplot as plt #allows me to create pie charts 
from sumy.summarizers.luhn import LuhnSummarizer #allows me to summarise free response data
                                                 #the rest of the items imported are also for the summarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.utils import get_stop_words

class Qn:
    """
    The overarching class for all the questions
    """
    def __init__(self, questionNo, questionSt, questionResp):
        """
        Initialises the question number, question statement and the responses for that particular question
        
        >>> Qn(1, "Random question", ["Hello", "Hi", "Random", "Incorrect", "Hello"]).qNumber
        1
        >>> Qn(1, "Random question", ["Hello", "Hi", "Random", "Incorrect", "Hello"]).qStatement
        'Random question'
        >>> Qn(1, "Random question", ["Hello", "Hi", "Random", "Incorrect", "Hello"]).responses
        ['Hello', 'Hello', 'Hi', 'Incorrect', 'Random']
        """
        self.qNumber = questionNo #sets the question number
        self.qStatement = questionSt #sets the question statement
        self.responses = sorted(list(questionResp)) #sets the responses, sorted (to make numerical responses more presentable)
    def frequency(self):
        """
        Returns a dictionary containing the number of responses per choice (mostly for numerical and categorical data)
        
        >>> Qn(1, "Random question", ["Hello", "Hi", "Random", "Incorrect", "Hello"]).frequency()
        {'Hello': 2, 'Hi': 1, 'Incorrect': 1, 'Random': 1}
        >>> Qn(2, "Another random question", [1, 2, 1, 2, 2, 4, 2, 3]).frequency()
        {1: 2, 2: 4, 3: 1, 4: 1}
        """
        frequency = { } #initialises the output dictionary
        for choice in self.responses: #iterates through the responses
            if choice not in frequency.keys(): #if the current choice is not previously recorded in the dictionary, create a new entry and set it to 0
                frequency[choice] = 0
            frequency[choice] += 1 #for all cases, add 1 to the total response count for the choice
        return frequency #return the dictionary
    def freqPercent(self):
        """
        Returns a dictionary containing the percentage of responses per choice (as compared to the total number of responses) (mostly for numerical and categorical data)

        >>> Qn(1, "Random question", ["Hello", "Hi", "Random", "Incorrect", "Hello"]).freqPercent()
        {'Hello': 40.0, 'Hi': 20.0, 'Incorrect': 20.0, 'Random': 20.0}
        >>> Qn(2, "Another random question", [1, 2, 1, 2, 2, 4, 2, 3]).freqPercent()
        {1: 25.0, 2: 50.0, 3: 12.5, 4: 12.5}
        """
        frequency = self.frequency() #obtains the dictionary with the number of responses per choice
        lstLen = float(len(self.responses)) #find out the total number of reponses
                                            #it is saved as a float such that the percentage would not be unnecessarily rounded to the nearest integer (making the results inaccurate)
        freqPercent = { } #initialises the output dictionary
        for choice, freq in frequency.items(): #iterates through each choice
            freqPercent[choice] = (freq/lstLen)*100 #converts the absolute number of reponses per choice to a percentage and saves it into the new dictionary
        return freqPercent #returns the dictionary
    def mode(self):
        """
        Returns the most frequent choice (mostly for numerical and categorical data)
        
        >>> Qn(1, "Random question", ["Hello", "Hi", "Random", "Incorrect", "Hello"]).mode()
        ['Hello']
        >>> Qn(2, "Another random question", [1, 2, 1, 2, 2, 4, 2, 3]).mode()
        [2]
        >>> Qn(3, "Yet another random question", [1, 2, 1, 1, 2, 4, 2, 3]).mode()
        [1, 2]
        """
        frequency = self.frequency() #obtains the dictionary with the number of responses
        mode = [ ] #in case that there is more than 1 mode, all modes are saved into this list
        highestFreq = max(frequency.values()) #searches for the number of people who chose the most popular choice
        for choice, freq in frequency.items(): #searches through the frequency dictionary to save all the choices that have the same number of respondents as the most popular choice (basically, search for the most popular choice(s))
                                               #and save it to the list of modes
            if freq == highestFreq:
                mode.append(choice)
        return mode #return the mode(s)
    def plot_pie(self):
        """
        Creates a pie chart that reflects the distribution of responses per choice and saves it according to the question number
        Returns the name of the file containing the pie chart

        >>> Qn(1, "Random question", ["Hello", "Hi", "Random", "Incorrect", "Hello"]).plot_pie()
        'Q1_pie.png'
        Qn(2, "Another random question", [1, 2, 1, 2, 2, 4, 2, 3]).plot_pie()
        'Q2_pie.png'
        """
        pieChart = plt.subplots()[1] #initialise the subplot
        pieChart.set_title("Q{}: {}".format(self.qNumber, self.qStatement)) #set the title of the pie chart (<question number>: <question statement>)
        choices = self.frequency().keys() #obtains the list of choices
        exact = self.frequency().values() #obtains the list of responses per choice
        percent = self.freqPercent().values() #obtains the list of percentage of responses per choice
        def label(pct, exact):
            """
            Arranges the percentage of responses and number of responses for the relevant choice in a way that is suitable for displaying on the pie chart
            """
            currExact = int(math.ceil((pct/100)*sum(exact))) #converts the percentage to the exact value
            return "{}\n({:.1f}%)".format(currExact, pct) #returns the percentage and exact value, formatted to be displayed on the pie chart
        pieChart.pie(percent, autopct=lambda pct: label(pct, exact), startangle=90) #create the pie chart, along with the labels
        pieChart.legend(choices, title="Choices", loc="center left", bbox_to_anchor=(0.85, 0, 0.5, 1)) #creates a legend to the right of the pie chart
        pieChart.axis('equal') #ensure that the pie chart is in a circle
        pieName = "Q{}_pie.png".format(self.qNumber) #names the pie chart according to the question number
        plt.savefig(pieName, bbox_inches='tight', pad_inches=0.5) #saves the pie chart to a PNG file
        return pieName #returns the name of the PNG file where the pie chart is saved in


class NumericQn(Qn):
    """
    The class containing functions specific to numeric questions
    """
    def __init__(self, questionNo, questionSt, questionResp):
        """
        Largely the same as the __init__() function in the Qn() class, but ensures that the responses are intergers.
        
        >>> NumericQn(1, "Random question", ["Hello", "Hi", "Random", "Incorrect", "Hello"])
        Error: Numeric questions should have integer responses
        Traceback (most recent call last):
          ...
        TypeError: __init__() should return None, not 'str'
        >>> NumericQn(2, "Another random question", [1, 2, 1, 2, 2, 4, 2, 3]).qNumber
        2
        >>> NumericQn(2, "Another random question", [1, 2, 1, 2, 2, 4, 2, 3]).qStatement
        'Another random question'
        >>> NumericQn(2, "Another random question", [1, 2, 1, 2, 2, 4, 2, 3]).responses
        [1, 1, 2, 2, 2, 2, 3, 4]
        """
        for r in questionResp:
            try:
                int(r)
            except:
                print("Error: Numeric questions should have integer responses")
                return "ERROR" #communicates with the main program, informing it of an error
                               #I initially wanted to check for the "ERROR" string, but I realised that this produced a TypeError since __init__() functions are not supposed to return anything other than None
                               #hence in the main program, I will check for TypeErrors instead
        Qn.__init__(self, questionNo, questionSt, questionResp)

    def mean(self):
        """
        Returns the average choice out of all the responses
        
        >>> NumericQn(2, "Another random question", [1, 2, 1, 2, 2, 4, 2, 3]).mean()
        2.125
        """
        lstSum = sum(self.responses) #adds up all the responses
        lstLen = len(self.responses) #calculates the number of responses
        mean = lstSum/lstLen #calculates the average response
        return mean #returns the average response
    def median(self):
        """
        Returns the middle choice when all responses are arranges in order
        If there is an even number of reponses, the average of the middle choices is returned

        >>> NumericQn(2, "Another random question", [1, 2, 1, 2, 2, 4, 2, 3]).median()
        2.0
        >>> NumericQn(3, "Yet another random question", [1, 2, 1, 1, 2, 4, 2]).median()
        2
        """
        lstLen = len(self.responses) #calculates the number of respondents
        if lstLen%2 == 0: #if there is an even number of responses, set the median to the average of the 2 middle responses and
            mid1 = self.responses[lstLen//2]
            mid2 = self.responses[(lstLen//2)-1]
            median = (mid1+mid2)/2.0
        else: #if there is an odd number of responses, set the median to the middle response
            median = self.responses[lstLen//2]
        return median #return the median

class CategoricalQn(Qn):
    """
    The class containing functions specific to categorical questions
    As all the functions required for categorical questions are already defined in the Qn() class, this class is empty and inherits all of its methods from the Qn class
    """
    pass

class FreeResponseQn(Qn):
    """
    The class containing functions specific to free response questions
    """
    def summarize(self, sentenceNo=5, leaveOut=[ ]):
        """
        Returns a summary of all the responses, excuding irrelevant responses stated in the leaveOut parameter

        >>> FreeResponseQn(4, "Randome response question", ["I like apples", "I like pears", "Everything", "I love microbit", "Nil", "None", "Python rocks!", "Nil", "Nothing", "I like oranges too", "Python is the best", "-", "Microbit is the best", "I love python", "Javascript is better", "Nil", "Maybe we should use C++", "Nothing", "Apple is the best", "Apples", "Everything", "Python", "Apples are better than pears", "Nothing", "-", "Mircrobit and Python", "Apples and oranges"]).summarize(sentenceNo=3, leaveOut=["everything", "nil", "none", "nothing", "-"])
        ['Apples and oranges.', 'I love microbit.', 'I love python.']
        """
        def stripPunct(response):
            """
            Removes all punctuation from the responses. This allows for easier manipulation of the responses later
            """
            for ch in string.punctuation: #iterates through each punctuation 
                response = response.replace(ch, "") #removes all instances of the current punctuation in the given string
            return response#returns the string, with all the puctuations removed
        
        resp = "" #initialises the string to store all the (relevant) responses
        for r in self.responses: #iterates through the responses
            r = stripPunct(r) #removes all punctuation from the current response
            if r.strip().lower() not in leaveOut: #if the current response is relevant, add a full stop behind and include it in the string of relevant responses
                resp += r + ". "
        parseResp = PlaintextParser.from_string(resp, Tokenizer("english")) #parses the string such that it can be used in the summariser
        s = LuhnSummarizer(Stemmer("english")) #initialises the summariser
        s.stop_words = get_stop_words("english") #updates the stop words used for the summariser
        summarized = s(parseResp.document, sentenceNo) #summarises the text
        summaryLst = [ ] #initialises a list to store each sentence in the summary (for easy output)
        for sentence in summarized: #iterates through each sentence in the summary, converting them to strings before adding them in the new summary list
            summaryLst.append(str(sentence))
        return summaryLst #returns the summary list

class DemographicQn:
    """
    The class containing functions specific to demographic questions
    As we do not need responses to demographic questions, this class does not inherit any functions from the Qn() class
    Instead, it will have its own __init__() function, only initialising its question number and question statement
    """
    def __init__(self, questionNo, questionSt):
        """
        Initialises the question number and question statement
        
        >>> DemographicQn(5, "Random question asking for your name").qNumber
        5
        >>> DemographicQn(5, "Random question asking for your name").qStatement
        'Random question asking for your name'
        """
        self.qNumber = questionNo #sets the question number
        self.qStatement = questionSt #sets the question statement
