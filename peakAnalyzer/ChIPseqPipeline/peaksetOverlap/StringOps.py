# 
#********************************************************************** 
#   Copyright (c) 2003-2004 Danny Brewer 
#   d29583@groovegarden.com 
# 
#   This library is free software; you can redistribute it and/or 
#   modify it under the terms of the GNU Lesser General Public 
#   License as published by the Free Software Foundation; either 
#   version 2.1 of the License, or (at your option) any later version. 
# 
#   This library is distributed in the hope that it will be useful, 
#   but WITHOUT ANY WARRANTY; without even the implied warranty of 
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU 
#   Lesser General Public License for more details. 
# 
#   You should have received a copy of the GNU Lesser General Public 
#   License along with this library; if not, write to the Free Software 
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA 
# 
#   See:  http://www.gnu.org/licenses/lgpl.html 
# 
#********************************************************************** 
#   If you make changes, please append to the change log below. 
# 
#   Change Log 
#   Danny Brewer         Revised 2004-07-13 
# 
#********************************************************************** 



def constUpperCaseLetters(): 
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
def constLowerCaseLetters(): 
    return "abcdefghijklmnopqrstuvwxyz" 
def constDigits(): 
    return "0123456789" 

def constLetters(): 
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" 
def constLettersAndDigits(): 
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789" 


def IsDigit( cChars ): 
    """Return True if every char in cChars is a digit.""" 
    return AllCharsInSet( cChars, constDigits() ) 

def IsAlpha( cChars ): 
    """Return True if every char in cChars is a letter.""" 
    return AllCharsInSet( cChars, constLetters() ) 

def IsAlphaNumeric( cChars ): 
    """Return True if every char in cChars is a letter or digit.""" 
    return AllCharsInSet( cChars, constLettersAndDigits() ) 

def IsUCaseAlpha( cChars ): 
    """Return True if every char in cChars is an upper case letter.""" 
    return AllCharsInSet( cChars, constUpperCaseLetters() ) 

def IsLCaseAlpha( cChars ): 
    """Return True if every char in cChars is a lower case letter.""" 
    return AllCharsInSet( cChars, constLowerCaseLetters() ) 


def AllCharsInSet( cChars, cSet ): 
    """Return true if EVERY char in cChars is in the set cSet. 
    The string cSet is considered to be a SET of characters. 
    The function returns true if EVERY character of cChars is in the SET cSet.""" 
    for c in cChars: 
        if c not in cSet: 
            return False 
    return True 

def AllCharsNotInSet( cChars, cSet ): 
    """Return true if EVERY char in cChars are NOT in the set cSet. 
    The string cSet is considered to be a SET of characters. 
    The function returns true if EVERY character of cChars is NOT in the SET cSet.""" 
    for c in cChars: 
        if c in cSet: 
            return False 
    return True 


def AnyCharsInSet( cChars, cSet ): 
    """Return true if ANY chars of cChars are in the set cSet.""" 
    bNoneInSet = AllCharsNotInSet( cChars, cSet ) 
    return not bNoneInSet 

def AnyCharsNotInSet( cChars, cSet ): 
    """Return true if ANY char of cChars is NOT in the set cSet.""" 
    bAllInSet = AllCharsInSet( cChars, cSet ) 
    return not bAllInSet 



def BuildStringRange( nFirstChar, nLastChar ): 
    """Build up a string of chars from nFirstChar to nLastChar. 
    Both nFirstChar and nLastChar are the ASCII character numbers. 
    Examples: 
       To Build a string of all printable characters... 
          x = BuildStringRange( 32, 127 ) 
       To build string of all uppercase characters... 
          x = BuildStringRange( ord("A"), ord("Z") ) 
    """ 
    # Convert strings to int if necessary. 
    if type( nFirstChar ) is str: nFirstChar = ord( nFirstChar ) 
    if type( nLastChar ) is str: nLastChar = ord( nLastChar ) 
    # Swap if order is wrong. 
    if nLastChar < nFirstChar: 
        nFirstChar, nLastChar = nLastChar, nFirstChar 
    # Build string range. 
    s = "" 
    for i in range( nFirstChar, nLastChar+1 ): 
        s += chr( i ) 
    return s 



def toLower( cString ): 
    cUCase = constUpperCaseLetters() 
    cLCase = constLowerCaseLetters() 
    cResult = "" 
    for c in cString: 
        nPos = cUCase.find( c ) 
        if nPos >= 0: 
            c = cLCase[ nPos ] 
        cResult += c 
    return cResult 

def toUpper( cString ): 
    cUCase = constUpperCaseLetters() 
    cLCase = constLowerCaseLetters() 
    cResult = "" 
    for c in cString: 
        nPos = cLCase.find( c ) 
        if nPos >= 0: 
            c = cUCase[ nPos ] 
        cResult += c 
    return cResult 



def ProperName( cName, cWordChars=constLettersAndDigits() ): 
    """Return a string with property capitalization. 
    For example, "joHN smITH" becomes "John Smith". 
    You may optionally specify cWordChars, which characters are to be 
     considered as part of a word. 
    If you do not specify cWordChars, then it defaults to 
     1. uppercase letters 
     2. lowercase letters 
     3. digits 
    """ 
    bInWord = False 
    cResult = "" 
    for c in cName: 
        if bInWord: 
            if AllCharsInSet( c, cWordChars ): 
                c = toLower( c ) 
            else: 
                bInWord = False 
        else: 
            if AllCharsInSet( c, cWordChars ): 
                c = toUpper( c ) 
                bInWord = True 
            else: 
                c = toLower( c ) 
        cResult += c 
    return cResult 



def PadR( cString, nLen, cPad=" " ): 
    """If cString is longer than nLen, then truncate SUFFIX characters to 
    make the length exactly nLen. 
    If cString is shorter than nLen, then pad it on the RIGHT with cPad to 
    make the length exactly nLen. 
    If cPad is not specified, then it is a space. 
    """ 
    while len( cString ) < nLen: 
        cString += cPad 
    cString = cString[0:nLen] 
    return cString 

def PadL( cString, nLen, cPad=" " ): 
    """If cString is longer than nLen, then truncate PREFIX characters to 
    make the length exactly nLen. 
    If cString is shorter than nLen, then pad it on the LEFT with cPad to 
    make the length exactly nLen. 
    If cPad is not specified, then it is a space. 
    """ 
    while len( cString ) < nLen: 
        cString = cPad + cString 

    cString = cString[len(cString)-nLen:] 
    return cString 



def IsPrefix( cPrefixString, cString ): 
    """Return true if cPrefixString matches the beginning of cString. 
    The following would return True... 
       IsPrefix( "Jo", "John" ) 
       IsPrefix( "Jo", "Joseph" ) 
       IsPrefix( "Jo", "Jolly" ) 
    """ 
    return cString[0:len(cPrefixString)] == cPrefixString 
    
def IsSuffix( cSuffixString, cString ): 
    """Return true if cSuffixString matches the ending of cString. 
    The following would return True... 
       IsSuffix( "ing", "Walking" ) 
       IsSuffix( "ing", "Running" ) 
       IsSuffix( "ing", "Programming" ) 
    """ 
    return cString[len(cString)-len(cSuffixString):] == cSuffixString 


def IsPrefixNC( cPrefixString, cString ): 
    """Return true if cPrefixString matches the beginning of cString, but ignoring case. 
    """ 
    return toUpper( cString[0:len(cPrefixString)] ) == toUpper( cPrefixString ) 
    
def IsSuffixNC( cSuffixString, cString ): 
    """Return true if cSuffixString matches the ending of cString, but ignoring case. 
    """ 
    return toUpper( cString[len(cString)-len(cSuffixString):] ) == toUpper( cSuffixString ) 



def CommonPrefixString2( cStr1, cStr2 ): 
    """Return the common prefix, if any, of both strings.""" 
    nLen = min( len( cStr1 ), len( cStr2 ) ) 
    cPrefix = "" 
    for i in range( nLen ): 
        c1 = cStr1[i] 
        c2 = cStr2[i] 
        if c1 == c2: 
            cPrefix += c1 
        else: 
            break 
    return cPrefix 

def CommonPrefixString( *cStrs ): 
    """Return the common prefix, if any, of the strings.""" 
    return reduce( CommonPrefixString2, cStrs ) 


def CommonSuffixString2( cStr1, cStr2 ): 
    """Return the common suffix, if any, of both strings.""" 
    nLen = min( len( cStr1 ), len( cStr2 ) ) 
    cSuffix = "" 
    for i in range( -1, -nLen-1, -1 ): 
        c1 = cStr1[i] 
        c2 = cStr2[i] 
        if c1 == c2: 
            cSuffix = c1 + cSuffix 
        else: 
            break 
    return cSuffix 

def CommonSuffixString( cStrs ): 
    """Return the common suffix, if any, of the strings.""" 
    return reduce( CommonSuffixString2, cStrs ) 




def Split( cString, cBreakChars=" " ): 
    """Split the string into a list of strings. 
    The string is broken any time a character from cBreakChars is encountered. 
    If you don't specify cBreakChars, then it is a blank, resulting in splitting 
     the original string whenever a blank occurs.  This results in returning an 
     array of the words of the original string. 
    This is the opposite of the Join() function. 
    """ 
    cResultList = [] 
    while len(cString) > 0: 
        cResultStr = "" 
        for c in cString: 
            if c in cBreakChars: 
                break 
            else: 
                cResultStr += c 
        cString = cString[len(cResultStr)+1:] 
        cResultList += [cResultStr] 
    return cResultList 


def Join( cListOfStrings, cJoinPadding=" " ): 
    """Create one long string from an array of strings. 
    This is the opposite of the Split() function. 
    """ 
    cResultStr = "" 
    if len(cListOfStrings) > 0: 
        cResultStr = cListOfStrings[0] 
        for cString in cListOfStrings[1:]: 
            cResultStr += cJoinPadding + cString 
    return cResultStr 



def RemTrailing( cString, cSetOfCharsToRemove=" " ): 
    """Remove trailing characters from a string. 
    The default is to remove trailing blanks, if you don't specify the cSetOfCharsToRemove. 
    The cSetOfCharsToRemove specifies a SET of characters that you want removed from the suffix of cString. 
    For example, specify " 0" to remove trailing blanks and zeros. 
    For example, specify " "+chr(9) to remove trailing blanks and tabs. 
    This function returns a second value which is the string that was removed. 
    """ 
    nLen = len( cString ) 
    i = nLen-1 
    while (i >= 0) and AllCharsInSet( cString[i], cSetOfCharsToRemove ): 
        i -= 1 
    return cString[0:i+1], cString[i+1:] 

def RemLeading( cString, cSetOfCharsToRemove=" " ): 
    """Remove leading characters from a string. 
    The default is to remove leading blanks, if you don't specify the cSetOfCharsToRemove. 
    The cSetOfCharsToRemove specifies a SET of characters that you want removed from the prefix of cString. 
    For example, specify " 0" to remove leading blanks and zeros. 
    For example, specify " "+chr(9) to remove leading blanks and tabs. 
    This function returns a second value which is the string that was removed. 
    """ 
    nLen = len( cString ) 
    i = 0 
    while (i < nLen) and AllCharsInSet( cString[i], cSetOfCharsToRemove ): 
        i += 1 
    return cString[i:], cString[0:i] 

def RemLeadingAndTrailing( cString, cSetOfCharsToRemove=" " ): 
    """Remove leading and trailing characters from a string. 
    The default is to remove blanks, if you don't specify the cSetOfCharsToRemove. 
    The cSetOfCharsToRemove specifies a SET of characters that you want removed from the ends of cString. 
    For example, specify " 0" to remove blanks and zeros. 
    For example, specify " "+chr(9) to remove blanks and tabs. 
    This function returns three values: the shortened string, the leading stuff that was removed, 
     and the trailing stuff that was removed. 
    """ 
    cString, cTrailing = RemTrailing( cString, cSetOfCharsToRemove ) 
    cString, cLeading = RemLeading( cString, cSetOfCharsToRemove ) 
    return cString, cLeading, cTrailing 




def RemoveCharsInSet( cString, cSetOfUnwantedChars ): 
    """Remove from cString, all characters in the SET of cSetOfUnwantedChars.""" 
    cResult = "" 
    for c in cString: 
        if AllCharsNotInSet( c, cSetOfUnwantedChars ): 
            cResult += c 
    return cResult 

def RemoveCharsNotInSet( cString, cSetOfWantedChars ): 
    """Remove from cString, all characters NOT in the SET of cSetOfWantedChars.""" 
    cResult = "" 
    for c in cString: 
        if AllCharsInSet( c, cSetOfWantedChars ): 
            cResult += c 
    return cResult 

# synonyms 
KeepCharsInSet = RemoveCharsNotInSet 
KeepCharsNotInSet = RemoveCharsInSet 




def CoalesceMultipleBlanks( cString ): 
    """Convert runs of multiple spaces into a single space. 
    Thus "John     Smith" becomes "John Smith". 
    """ 
    return CoalesceMultipleChars( cString, " " ) 

def CoalesceMultipleChars( cString, cSetToCoalesce ): 
    """ Whenever there are runs of multiple chars, of any char in the set cSetToCoalesce, 
    then convert that run of chars into a single char. 
    For example... 
    If cSetToCoalesce was "AB", 
     the string "AAABBBCCCAAABBBCCC"      would become "ABCCCABCCC" 
     the string "AAABBBCCCAAABBBCCCA"     would become "ABCCCABCCCA" 
     the string "AAABBBCCCAAABBBCCCAAA"   would become "ABCCCABCCCA" 
     the string "AAABBBCCCAAABBBCCCAAAB"  would become "ABCCCABCCCAB" 
     the string "AAABBBCCCAAABBBCCCAAABB" would become "ABCCCABCCCAB" 
    """ 
    i = 0 
    # note that the length of cString can change during the loop. 
    while i < len( cString ): 
        c = cString[i] 
        if AllCharsInSet( c, cSetToCoalesce ): 
            cString = cString[0:i+1] + RemLeading( cString[i:], c ) 
        i += 1 
    return cString 




def CharTranslate( cString, cFromChars, cToChars ): 
    """Any character of cString that is in cFromChars is replaced by the character 
     from the corresponding position of cToChars. 
    If cToChars is shorter than cFromChars, then characters in cFromChars which 
     have no counterpart in cToChars are removed from the string, shortening it. 
    To remove all dollar signs from a string, you could write... 
     cString = CharTranslate( cString, "$", "" ) 
    To change all semicolons into commas, and all underscored into dashes... 
     cString = CharTranslate( cString, ";_", ",-" ) 
    """ 
    cResult = "" 
    for c in cString: 
        nPos = cFromChars.find( c ) 
        if nPos >= 0: 
            # find counterpart in cToChars 
            if nPos < len( cToChars ): 
                c = cToChars[nPos] 
                cResult += c 
        else: 
            # char not found in cFromChars, so don't translate it. 
            cResult += c 
    return cResult 




def StrSubstitute( cString, cFindStr, cReplaceStr ): 
    """All occurences of cFindStr are replaced by cReplaceStr. 
    cFindStr and cReplaceStr do not need to be the same length. 
    """ 
    nFindLen = len( cFindStr ) 
    cResult = "" 
    if len( cFindStr ) > 0: 
        while True: 
            nPos = cString.find( cFindStr ) 
            if nPos >= 0: 
                cResult += cString[0:nPos] + cReplaceStr 
                cString = cString[nPos+nFindLen:] 
            else: 
                # append rest of original string 
                cResult += cString 
                break 
    return cResult 

def StrSubstituteNC( cString, cFindStr, cReplaceStr ): 
    """Case insensitive version of StrSubstitute.""" 
    nFindLen = len( cFindStr ) 
    cStringUC = toUpper( cString ) 
    cFindStrUC = toUpper( cFindStr ) 
    cResult = "" 
    if len( cFindStrUC ) > 0: 
        while True: 
            nPos = cStringUC.find( cFindStrUC ) 
            if nPos >= 0: 
                cResult += cString[0:nPos] + cReplaceStr 
                cString = cString[nPos+nFindLen:] 
                cStringUC = cStringUC[nPos+nFindLen:] 
            else: 
                # append rest of original string 
                cResult += cString 
                break 
    return cResult 


def TranslateToL33tSp3ak( cEnglish ): 
    """Translate an english phrase into the grammer spoken by script kiddies on Slashdot. 
    TranslateToL33tSp3ak( "Test to see if you are owned by elite hackers." ) 
    would return: 7357 70 533 if J00 ar3 0wn3d 8y 1337 4aX0r5. 
    """ 
    cL33t = cEnglish 
    cL33t = StrSubstituteNC( cL33t, "you", "Joo" ) 
    cL33t = StrSubstituteNC( cL33t, "elite", "leet" ) 
    cL33t = StrSubstituteNC( cL33t, "acker", "aXor" ) 
    cL33t = CharTranslate( cL33t, "oO1lZzEeHhSsGTtB", "0011223344556778" ) 
    return cL33t 



def StrNormalize( cString ): 
    """Convert a name or ID into a form that makes it likely to match a similar name or ID. 
    That way, if two different operators type in variations of " JoHn ,  SmITh ", 
    they are likely to both get the same record from a database. 
    1. Trim leading and trailing blanks. 
    2. Remove punctuation. (prior to coalescing blanks!) 
    3. Coalesce multiple blanks. 
    4. Convert to Proper case. 
    """ 
    cString = RemLeadingAndTrailing( cString ) 
    cString = RemoveCharsInSet( cString, ".,;:-'" ) 
    cString = CoalesceMultipleBlanks( cString ) 
    cString = ProperName( cString ) 
    return cString 


def StrRot13( cString, nRotate=13 ): 
    cResult = "" 
    nLen = len( cString ) 
    for c in cString: 
        if IsUCaseAlpha( c ): 
            n = ord( c ) - ord("A") 
            n = (n + nRotate) % 26 
            c = chr( n + ord("A") ) 
        elif IsLCaseAlpha( c ): 
            n = ord( c ) - ord("a") 
            n = (n + nRotate) % 26 
            c = chr( n + ord("a") ) 
        cResult += c 
    return cResult 
