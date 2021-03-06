import email
import re
import numpy

class Parser(object):
    #stripHeaders helper conjoining multiple substitutions into one regex
    @staticmethod
    def multiRegexSubstitute(regexArray, text, substitute = ""):
        rules = "|".join(regexArray)
        pattern = re.compile(rules)
        return pattern.sub(substitute, text)

    #Parse the standard email structure into a plaintext (strip headers, footers and section separators)
    @staticmethod
    def stripHeaders(mail):
        text = ""
        for msg in email.message_from_string(mail).walk():
            try:
                text += msg.get_payload() + " "
            except:
                text += mail
        if "delivered-to" in text:
            text = text[re.search("\n\n", text).start()+1:]

        #REGEX punctuation mark removal
        text = Parser.multiRegexSubstitute(["\.", "\?", ";", ",", "\"", "'", "=", "#", "[0-9]", "\*", "!", "%"], text) # non-expanding substitutions
        text = Parser.multiRegexSubstitute(["-", "\(", "\)", "\n", "\t", "&nbsp", "_", "&", "$", "@", ":", "\[", "\]"], text, " ") # expanding substitutions

        text = re.sub("<[^<>]*>", " ", text) #remove HTML/XML tags
        text = re.sub(" +" ," ", text) #finisher whitespace removal

        return text

    #Return an array of integer from a given email.
    def parseEmail(self, email):
        return None
    
    def __init__(self, dictionary):
        self.dictionary = dictionary

class ParserDictionary(Parser):
    dictionary = None

    #Translate a given email according into a word vector according to the preset dictionary
    def parseEmail(self, mail):
        parsedData = [0] * len(self.dictionary)
        plaintext = Parser.stripHeaders(mail).split(" ")
        for x in plaintext:
            if x in self.dictionary:
                parsedData[self.dictionary.index(x)] += 1
        return parsedData
    
class PCAParser(Parser):
    p = None
    def __init__(self, dictionary, data, dims):
        self.dictionary = dictionary
        data = numpy.matrix(data,dtype='double')
        u,s,v = numpy.linalg.svd(data)
        self.p = v[:dims]
        
    def returnNewData(self,data):
        return data*self.p.T
    
    
    def parseEmail(self, mail):
        parsedData = [0] * len(self.dictionary)
        plaintext = Parser.stripHeaders(mail).split(" ")
        for x in plaintext:
            if x in self.dictionary:
                parsedData[self.dictionary.index(x)] += 1
        parsedData = numpy.dot(self.p,parsedData)
        parsedData = parsedData.tolist()[0]
        return parsedData
        
    
