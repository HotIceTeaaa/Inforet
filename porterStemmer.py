class PorterStemmer:
    def __init__(self):
        pass

    def stem(self, tokens):
        # urutan dibuat biar yg S1 paling panjang duluan
        res = []

        for token in tokens:
            psw = PorterStemmerWord(token)

            # step 1a
            if(psw.endsWithWord("sses")):
                psw.changeS1ToS2("sses", "ss")
            elif(psw.endsWithWord("ies")):
                psw.changeS1ToS2("ies", "i")
            elif(psw.endsWithWord("s")):
                psw.changeS1ToS2("s", "")

            # step 1b
            isLeftTableApplied = False
            # left table
            if(psw.endsWithWord("eed") and psw.getMeasure() > 0):
                psw.changeS1ToS2("eed", "ee")
            elif(psw.endsWithWord("ed") and psw.containsVokal()):
                psw.changeS1ToS2("ed", "")
                isLeftTableApplied = True
            elif(psw.endsWithWord("ing") and psw.containsVokal()):
                psw.changeS1ToS2("ing", "")
                isLeftTableApplied = True

            # right table
            if isLeftTableApplied:
                if(psw.endsWithWord("at")):
                    psw.changeS1ToS2("at", "ate")
                elif(psw.endsWithWord("bl")):
                    psw.changeS1ToS2("bl", "ble")
                elif(psw.endsWithWord("iz")):
                    psw.changeS1ToS2("iz", "ize")
                elif(psw.endsInDouble() and not (psw.endsWithLetter("l") or psw.endsWithLetter("s") or psw.endsWithLetter("z"))):
                    psw.toSingleLetter()
                elif(psw.getMeasure() == 1 and psw.isStarO()):
                    psw.addLetter("e")

            # step 1c
            if(psw.containsVokal() and psw.endsWithLetter("y")):
                psw.changeS1ToS2("y", "i")

            # step 2
            if psw.endsWithWord("ational") and psw.getMeasure() > 0:
                psw.changeS1ToS2("ational", "ate")
            elif psw.endsWithWord("tional") and psw.getMeasure() > 0:
                psw.changeS1ToS2("tional", "tion")
            elif psw.endsWithWord("enci") and psw.getMeasure() > 0:
                psw.changeS1ToS2("enci", "ence")
            elif psw.endsWithWord("anci") and psw.getMeasure() > 0:
                psw.changeS1ToS2("anci", "ance")
            elif psw.endsWithWord("izer") and psw.getMeasure() > 0:
                psw.changeS1ToS2("izer", "ize")
            elif psw.endsWithWord("abli") and psw.getMeasure() > 0:
                psw.changeS1ToS2("abli", "able")
            elif psw.endsWithWord("alli") and psw.getMeasure() > 0:
                psw.changeS1ToS2("alli", "al")
            elif psw.endsWithWord("entli") and psw.getMeasure() > 0:
                psw.changeS1ToS2("entli", "ent")
            elif psw.endsWithWord("eli") and psw.getMeasure() > 0:
                psw.changeS1ToS2("eli", "e")
            elif psw.endsWithWord("ousli") and psw.getMeasure() > 0:
                psw.changeS1ToS2("ousli", "ous")
            elif psw.endsWithWord("ization") and psw.getMeasure() > 0:
                psw.changeS1ToS2("ization", "ize")
            elif psw.endsWithWord("ation") and psw.getMeasure() > 0:
                psw.changeS1ToS2("ation", "ate")
            elif psw.endsWithWord("ator") and psw.getMeasure() > 0:
                psw.changeS1ToS2("ator", "ate")
            elif psw.endsWithWord("alism") and psw.getMeasure() > 0:
                psw.changeS1ToS2("alism", "al")
            elif psw.endsWithWord("iveness") and psw.getMeasure() > 0:
                psw.changeS1ToS2("iveness", "ive")
            elif psw.endsWithWord("fulness") and psw.getMeasure() > 0:
                psw.changeS1ToS2("fulness", "ful")
            elif psw.endsWithWord("ousness") and psw.getMeasure() > 0:
                psw.changeS1ToS2("ousness", "ous")
            elif psw.endsWithWord("aliti") and psw.getMeasure() > 0:
                psw.changeS1ToS2("aliti", "al")
            elif psw.endsWithWord("iviti") and psw.getMeasure() > 0:
                psw.changeS1ToS2("iviti", "ive")
            elif psw.endsWithWord("biliti") and psw.getMeasure() > 0:
                psw.changeS1ToS2("biliti", "ble")

            # step 3
            if psw.endsWithWord("icate") and psw.getMeasure() > 0:
                psw.changeS1ToS2("icate", "ic")
            elif psw.endsWithWord("ative") and psw.getMeasure() > 0:
                psw.changeS1ToS2("ative", "")   
            elif psw.endsWithWord("alize") and psw.getMeasure() > 0:
                psw.changeS1ToS2("alize", "al")
            elif psw.endsWithWord("iciti") and psw.getMeasure() > 0:
                psw.changeS1ToS2("iciti", "ic")
            elif psw.endsWithWord("ical") and psw.getMeasure() > 0:
                psw.changeS1ToS2("ical", "ic")
            elif psw.endsWithWord("ousness") and psw.getMeasure() > 0:
                psw.changeS1ToS2("ousness", "ous")
            elif psw.endsWithWord("ful") and psw.getMeasure() > 0:
                psw.changeS1ToS2("ful", "")
            elif psw.endsWithWord("ness") and psw.getMeasure() > 0:
                psw.changeS1ToS2("ness", "")

            # step 4
            if psw.endsWithWord("al") and psw.getMeasure() > 1:
                psw.changeS1ToS2("al", "")
            elif psw.endsWithWord("ance") and psw.getMeasure() > 1:
                psw.changeS1ToS2("ance", "")
            elif psw.endsWithWord("ence") and psw.getMeasure() > 1:
                psw.changeS1ToS2("ence", "")
            elif psw.endsWithWord("er") and psw.getMeasure() > 1:
                psw.changeS1ToS2("er", "")
            elif psw.endsWithWord("ic") and psw.getMeasure() > 1:
                psw.changeS1ToS2("ic", "")
            elif psw.endsWithWord("able") and psw.getMeasure() > 1:
                psw.changeS1ToS2("able", "")
            elif psw.endsWithWord("ible") and psw.getMeasure() > 1:
                psw.changeS1ToS2("ible", "")
            elif psw.endsWithWord("ant") and psw.getMeasure() > 1:
                psw.changeS1ToS2("ant", "")
            elif psw.endsWithWord("ement") and psw.getMeasure() > 1:
                psw.changeS1ToS2("ement", "")
            elif psw.endsWithWord("ment") and psw.getMeasure() > 1:
                psw.changeS1ToS2("ment", "")
            elif psw.endsWithWord("ent") and psw.getMeasure() > 1:
                psw.changeS1ToS2("ent", "")
            elif psw.endsWithWord("ion") and psw.getMeasure() > 1 and (psw.endsWithLetter("s") or psw.endsWithLetter("t")):
                psw.changeS1ToS2("ion", "")
            elif psw.endsWithWord("ou") and psw.getMeasure() > 1:
                psw.changeS1ToS2("ou", "")
            elif psw.endsWithWord("ism") and psw.getMeasure() > 1:
                psw.changeS1ToS2("ism", "")
            elif psw.endsWithWord("ate") and psw.getMeasure() > 1:
                psw.changeS1ToS2("ate", "")
            elif psw.endsWithWord("iti") and psw.getMeasure() > 1:
                psw.changeS1ToS2("iti", "")
            elif psw.endsWithWord("ous") and psw.getMeasure() > 1:
                psw.changeS1ToS2("ous", "")
            elif psw.endsWithWord("ive") and psw.getMeasure() > 1:
                psw.changeS1ToS2("ive", "")
            elif psw.endsWithWord("ize") and psw.getMeasure() > 1:
                psw.changeS1ToS2("ize", "")

            # step 5a
            if psw.endsWithWord("e") and psw.getMeasure() > 1:
                psw.changeS1ToS2("e", "")
            elif psw.endsWithWord("e") and psw.getMeasure() == 1 and not psw.isStarO():
                psw.changeS1ToS2("e", "")

            # step 5b
            if psw.getMeasure() > 1 and psw.endsInDouble() and psw.endsWithLetter("l"):
                psw.toSingleLetter()

            res.append(psw.word)

        return res
    

class PorterStemmerWord:
    def __init__(self, word):
        self.vokalArr = ['a', 'i', 'u', 'e', 'o', 'A', 'I', 'U', 'E', 'O']
        self.consonantArr = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z', 'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Z']
        self.yArr = ['y', 'Y']
        self.word = word
        self.notation = ""

        self.calculateNotation()

    def calculateNotation(self):
        notation = ""

        for i in range(len(self.word)):
            if self.word[i] in self.vokalArr:
                if len(notation) == 0 or notation.endswith("c"): 
                    notation += "v"
            elif self.word[i] in self.yArr and i != 0 and self.word[i - 1] in self.consonantArr:
                if len(notation) == 0 or notation.endswith("c"): 
                    notation += "v"
            else:
                if len(notation) == 0 or notation.endswith("v"): 
                    notation += "c"

        self.notation = notation

    def getMeasure(self):
        notationCopy = self.notation

        if notationCopy.startswith("c"):
            notationCopy = notationCopy[1:]
        if notationCopy.endswith("v"):
            notationCopy = notationCopy[:-1]

        return len(notationCopy) // 2
    
    def containsVokal(self):
        return self.notation.__contains__("v")

    def endsInDouble(self):
        wordCopy = self.word.lower()
        if len(wordCopy) < 2:
            return False
        
        return wordCopy[-1] == wordCopy[-2]

    def endsWithLetter(self, letter):
        wordCopy = self.word.lower()
        letterCopy = letter.lower()

        return wordCopy.endswith(letterCopy)
    
    def endsWithWord(self, word):
        selfWordCopy = self.word.lower()
        wordCopy = word.lower()

        return selfWordCopy.endswith(wordCopy)

    # cek *o
    def isStarO(self):
        wordCopy = self.word.lower()

        a = not wordCopy.endswith("w")
        b = not wordCopy.endswith("x")
        c = not wordCopy.endswith("y")

        return self.notation.endswith("cvc") and a and b and c

    def toSingleLetter(self):
        #g perlu panggil calculateNotation() krn notation pasti tetep sama
        self.word = self.word[:-1]

    def changeS1ToS2(self, S1, S2):
        self.word = self.word[:-len(S1)]
        self.word += S2

        self.calculateNotation()

    def addLetter(self, letter):
        self.word += letter

        self.calculateNotation()


"""
line = "Such an analysis can reveal features that are not easily visible from the variations in the individual genes and can lead to a picture of expression that is more biologically transparent and accessible to interpretation"

ps = PorterStemmer()
tokens = line.split(" ")
res = ps.stem(tokens)
print(res)

Hasilnya: ['Such', 'an', 'analysi', 'can', 'rev', 'featur', 'that', 'ar', 'not', 'easili', 'vis', 'from', 'the', 'vari', 'in', 'the', 'individu', 'gen', 'and', 'can', 'lead', 'to', 'a', 'pictur', 'of', 'expression', 'that', 'i', 'mor', 'biolog', 'transpar', 'and', 'access', 'to', 'interpret']
di ppt teams hasil porter stemmernya salah kyk
"""


