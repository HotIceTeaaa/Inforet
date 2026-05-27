class PorterStemmer:
    def __init__(self):
        pass

    def stem(self, tokens):
        res = []

        for token in tokens:
            psw = PorterStemmerWord(token)

            # step 1a
            if(psw.endsWithWord("sses")):
                psw.changeS1ToS2("sses", "ss")
            elif(psw.endsWithWord("ies")):
                psw.changeS1ToS2("ies", "i")
            elif(psw.endsWithWord("s") and psw.getMeasure(1) > 0):      # m > 0 rule baru, kalo ngak nanti is jadi i
                psw.changeS1ToS2("s", "")

            # step 1b
            rightTableNeeded = False
            # left table
            if(psw.endsWithWord("eed") and psw.getMeasure(3) > 0):
                psw.changeS1ToS2("eed", "ee")
            elif(psw.endsWithWord("ed") and psw.containsVokal(2)):
                psw.changeS1ToS2("ed", "")
                rightTableNeeded = True
            elif(psw.endsWithWord("ing") and psw.containsVokal(3)):
                psw.changeS1ToS2("ing", "")
                rightTableNeeded = True

            # right table
            if rightTableNeeded:
                if(psw.endsWithWord("at")):
                    psw.changeS1ToS2("at", "ate")
                elif(psw.endsWithWord("bl")):
                    psw.changeS1ToS2("bl", "ble")
                elif(psw.endsWithWord("iz")):
                    psw.changeS1ToS2("iz", "ize")
                elif(psw.endsInDouble() and not (psw.endsWithLetter("l", 0) or psw.endsWithLetter("s", 0) or psw.endsWithLetter("z", 0))):
                    psw.toSingleLetter()
                elif(psw.getMeasure(0) == 1 and psw.isStarO(0)):
                    psw.addLetter("e")

            # step 1c
            if(psw.containsVokal(0) and psw.endsWithLetter("y", 0)):
                psw.changeS1ToS2("y", "i")

            # step 2
            if psw.endsWithWord("ational") and psw.getMeasure(7) > 0:
                psw.changeS1ToS2("ational", "ate")
            elif psw.endsWithWord("tional") and psw.getMeasure(6) > 0:
                psw.changeS1ToS2("tional", "tion")
            elif psw.endsWithWord("enci") and psw.getMeasure(4) > 0:
                psw.changeS1ToS2("enci", "ence")
            elif psw.endsWithWord("anci") and psw.getMeasure(4) > 0:
                psw.changeS1ToS2("anci", "ance")
            elif psw.endsWithWord("izer") and psw.getMeasure(4) > 0:
                psw.changeS1ToS2("izer", "ize")
            elif psw.endsWithWord("abli") and psw.getMeasure(4) > 0:
                psw.changeS1ToS2("abli", "able")
            elif psw.endsWithWord("alli") and psw.getMeasure(4) > 0:
                psw.changeS1ToS2("alli", "al")
            elif psw.endsWithWord("entli") and psw.getMeasure(5) > 0:
                psw.changeS1ToS2("entli", "ent")
            elif psw.endsWithWord("eli") and psw.getMeasure(3) > 0:
                psw.changeS1ToS2("eli", "e")
            elif psw.endsWithWord("ousli") and psw.getMeasure(5) > 0:
                psw.changeS1ToS2("ousli", "ous")
            elif psw.endsWithWord("ization") and psw.getMeasure(7) > 0:
                psw.changeS1ToS2("ization", "ize")
            elif psw.endsWithWord("ation") and psw.getMeasure(5) > 0:
                psw.changeS1ToS2("ation", "ate")
            elif psw.endsWithWord("ator") and psw.getMeasure(4) > 0:
                psw.changeS1ToS2("ator", "ate")
            elif psw.endsWithWord("alism") and psw.getMeasure(5) > 0:
                psw.changeS1ToS2("alism", "al")
            elif psw.endsWithWord("iveness") and psw.getMeasure(7) > 0:
                psw.changeS1ToS2("iveness", "ive")
            elif psw.endsWithWord("fulness") and psw.getMeasure(7) > 0:
                psw.changeS1ToS2("fulness", "ful")
            elif psw.endsWithWord("ousness") and psw.getMeasure(7) > 0:
                psw.changeS1ToS2("ousness", "ous")
            elif psw.endsWithWord("aliti") and psw.getMeasure(5) > 0:
                psw.changeS1ToS2("aliti", "al")
            elif psw.endsWithWord("iviti") and psw.getMeasure(5) > 0:
                psw.changeS1ToS2("iviti", "ive")
            elif psw.endsWithWord("biliti") and psw.getMeasure(6) > 0:
                psw.changeS1ToS2("biliti", "ble")

            # step 3
            if psw.endsWithWord("icate") and psw.getMeasure(5) > 0:
                psw.changeS1ToS2("icate", "ic")
            elif psw.endsWithWord("ative") and psw.getMeasure(5) > 0:
                psw.changeS1ToS2("ative", "")   
            elif psw.endsWithWord("alize") and psw.getMeasure(5) > 0:
                psw.changeS1ToS2("alize", "al")
            elif psw.endsWithWord("iciti") and psw.getMeasure(5) > 0:
                psw.changeS1ToS2("iciti", "ic")
            elif psw.endsWithWord("ical") and psw.getMeasure(4) > 0:
                psw.changeS1ToS2("ical", "ic")
            elif psw.endsWithWord("ousness") and psw.getMeasure(7) > 0:
                psw.changeS1ToS2("ousness", "ous")
            elif psw.endsWithWord("ful") and psw.getMeasure(3) > 0:
                psw.changeS1ToS2("ful", "")
            elif psw.endsWithWord("ness") and psw.getMeasure(4) > 0:
                psw.changeS1ToS2("ness", "")

            # step 4
            if psw.endsWithWord("al") and psw.getMeasure(2) > 1:
                psw.changeS1ToS2("al", "")
            elif psw.endsWithWord("ance") and psw.getMeasure(4) > 1:
                psw.changeS1ToS2("ance", "")
            elif psw.endsWithWord("ence") and psw.getMeasure(4) > 1:
                psw.changeS1ToS2("ence", "")
            elif psw.endsWithWord("er") and psw.getMeasure(2) > 1:
                psw.changeS1ToS2("er", "")
            elif psw.endsWithWord("ic") and psw.getMeasure(2) > 1:
                psw.changeS1ToS2("ic", "")
            elif psw.endsWithWord("able") and psw.getMeasure(4) > 1:
                psw.changeS1ToS2("able", "")
            elif psw.endsWithWord("ible") and psw.getMeasure(4) > 1:
                psw.changeS1ToS2("ible", "")
            elif psw.endsWithWord("ant") and psw.getMeasure(3) > 1:
                psw.changeS1ToS2("ant", "")
            elif psw.endsWithWord("ement") and psw.getMeasure(5) > 1:
                psw.changeS1ToS2("ement", "")
            elif psw.endsWithWord("ment") and psw.getMeasure(4) > 1:
                psw.changeS1ToS2("ment", "")
            elif psw.endsWithWord("ent") and psw.getMeasure(3) > 1:
                psw.changeS1ToS2("ent", "")
            elif psw.endsWithWord("ion") and psw.getMeasure(3) > 1 and (psw.endsWithLetter("s", 3) or psw.endsWithLetter("t", 3)):
                psw.changeS1ToS2("ion", "")
            elif psw.endsWithWord("ou") and psw.getMeasure(2) > 1:
                psw.changeS1ToS2("ou", "")
            elif psw.endsWithWord("ism") and psw.getMeasure(3) > 1:
                psw.changeS1ToS2("ism", "")
            elif psw.endsWithWord("ate") and psw.getMeasure(3) > 1:
                psw.changeS1ToS2("ate", "")
            elif psw.endsWithWord("iti") and psw.getMeasure(3) > 1:
                psw.changeS1ToS2("iti", "")
            elif psw.endsWithWord("ous") and psw.getMeasure(3) > 1:
                psw.changeS1ToS2("ous", "")
            elif psw.endsWithWord("ive") and psw.getMeasure(3) > 1:
                psw.changeS1ToS2("ive", "")
            elif psw.endsWithWord("ize") and psw.getMeasure(3) > 1:
                psw.changeS1ToS2("ize", "")

            # step 5a
            if psw.endsWithWord("e") and psw.getMeasure(1) > 1:
                psw.changeS1ToS2("e", "")
            elif psw.endsWithWord("e") and psw.getMeasure(1) == 1 and not psw.isStarO(1):
                psw.changeS1ToS2("e", "")

            # step 5b
            if psw.getMeasure(0) > 1 and psw.endsInDouble() and psw.endsWithLetter("l", 0):
                psw.toSingleLetter()

            res.append(psw.word)

        return res
    

class PorterStemmerWord:
    def __init__(self, word):
        self.vokalArr = ['a', 'i', 'u', 'e', 'o', 'A', 'I', 'U', 'E', 'O']
        self.consonantArr = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z', 'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Z']
        self.yArr = ['y', 'Y']
        self.word = word

    def calculateNotation(self, offset):
        notation = ""

        for i in range(len(self.word) - offset):
            if self.word[i] in self.vokalArr:
                if len(notation) == 0 or notation.endswith("c"): 
                    notation += "v"
            elif self.word[i] in self.yArr and i != 0 and self.word[i - 1] in self.consonantArr:
                if len(notation) == 0 or notation.endswith("c"): 
                    notation += "v"
            else:
                if len(notation) == 0 or notation.endswith("v"): 
                    notation += "c"

        return notation

    def getMeasure(self, offset):
        notation = self.calculateNotation(offset)

        if notation.startswith("c"):
            notation = notation[1:]
        if notation.endswith("v"):
            notation = notation[:-1]

        return len(notation) // 2
    
    def containsVokal(self, offset):
        notation = self.calculateNotation(offset)
        return notation.__contains__("v")

    def endsInDouble(self):
        wordCopy = self.word.lower()
        if len(wordCopy) < 2:
            return False
        
        return wordCopy[-1] == wordCopy[-2]

    def endsWithLetter(self, letter, offset):
        if offset == 0:
            wordCopy = self.word.lower()
        else:
            wordCopy = self.word[:-offset].lower()

        letterCopy = letter.lower()

        return wordCopy.endswith(letterCopy)
    
    def endsWithWord(self, word):
        selfWordCopy = self.word.lower()
        wordCopy = word.lower()

        return selfWordCopy.endswith(wordCopy)

    # cek *o
    def isStarO(self, offset):
        if offset == 0:
            wordCopy = self.word.lower()
        else:
            wordCopy = self.word[:-offset].lower()

        notation = self.calculateNotation(offset)

        a = not wordCopy.endswith("w")
        b = not wordCopy.endswith("x")
        c = not wordCopy.endswith("y")

        return notation.endswith("cvc") and a and b and c

    def toSingleLetter(self):
        self.word = self.word[:-1]

    def changeS1ToS2(self, S1, S2):
        self.word = self.word[:-len(S1)]
        self.word += S2

    def addLetter(self, letter):
        self.word += letter

"""
line = "Such an analysis can reveal features that are not easily visible from the variations in the individual genes and can lead to a picture of expression that is more biologically transparent and accessible to interpretation"

ps = PorterStemmer()
tokens = line.split(" ")
res = ps.stem(tokens)
print(res)

#Hasilnya: ['Such', 'an', 'analysi', 'can', 'reveal', 'featur', 'that', 'ar', 'not', 'easili', 'visibl', 'from', 'the', 'variat', 'in', 'the', 'individu', 'gene', 'and', 'can', 'lead', 'to', 'a', 'pictur', 'of', 'express', 'that', 'is', 'more', 'biolog', 'transpar', 'and', 'access', 'to', 'interpret']
sama persis kyk di ppt
"""

