# -*- coding: utf-8 -*-
"""This module implements the WordSub class, modelled after a recipe
in "Python Cookbook" (Recipe 3.14, "Replacing Multiple Patterns in a
Single Pass" by Xavier Defrang).

Usage:
Use this class like a dictionary to add before/after pairs:
    > subber = TextSub()
    > subber["before"] = "after"
    > subber["begin"] = "end"
Use the sub() method to perform the substitution:
    > print subber.sub("before we begin")
    after we end
All matching is intelligently case-insensitive:
    > print subber.sub("Before we BEGIN")
    After we END
The 'before' words must be complete words -- no prefixes.
The following example illustrates this point:
    > subber["he"] = "she"
    > print subber.sub("he says he'd like to help her")
    she says she'd like to help her
Note that "he" and "he'd" were replaced, but "help" and "her" were
not.
"""
from DefaultSubs import defaultNormal 

# 'dict' objects weren't available to subclass from until version 2.2.
# Get around this by importing UserDict.UserDict if the built-in dict
# object isn't available.
try: dict
except: from UserDict import UserDict as dict

import re
import string




class WordSub(dict):
    """All-in-one multiple-string-substitution class."""

    def wordToRegex(self, word):
        """Convert a word to a regex object which matches the word."""
        if word != "" and word[0].isalpha() and word[-1].isalpha():
            if unicode(word[0]) >= u'\u4e00' and unicode(word[0]) <=u'\u9fa5' :
                # return "\s(%s)\s|\s(%s)$" %(word,word)
                return "\s(%s)\s|\s(%s)$|^(%s)" %(word,word,word)
            else :
                return "\\b%s\\b" % re.escape(word)
        else:
            return r"\b%s\b" % re.escape(word)
    
    def update_regex(self):
        """Build re object based on the keys of the current
        dictionary.

        """
        self.regex = re.compile("|".join(map(self.wordToRegex, self.keys())))
        self.regexIsDirty = False

    def __init__(self, defaults = {}):
        """Initialize the object, and populate it with the entries in
        the defaults dictionary.

        """
        self.regex = None
        self.regexIsDirty = True
        for k,v in defaults.items():
            self[k] = v

    def __call__(self, match):
        """Handler invoked for each regex match."""
        # print "match:"+match.group(0).strip()
        if match.group(0).strip()[0] >= u'\u4e00' and match.group(0).strip()[0] <=u'\u9fa5':
            return " "+self[match.group(0).strip()]
        return self[match.group(0).strip()]

    def __setitem__(self, i, y):
        self.regexIsDirty = True
        # for each entry the user adds, we actually add three entrys:
     
        super(WordSub,self).__setitem__(string.lower(i),string.lower(y)) # key = value
        super(WordSub,self).__setitem__(string.capwords(i), string.capwords(y)) # Key = Value
        super(WordSub,self).__setitem__(string.upper(i), string.upper(y)) # K
        # super(type(self),self).__setitem__(string.lower(i),string.lower(y)) # key = value
        # super(type(self),self).__setitem__(string.capwords(i), string.capwords(y)) # Key = Value
        # super(type(self),self).__setitem__(string.upper(i), string.upper(y)) # KEY = VALUE

    def sub(self, text):
        """Translate text, returns the modified text."""
        if self.regexIsDirty:
            self.update_regex()
        return self.regex.sub(self, text)



class InputPreprocess(object):
    pass


# self-test
if __name__ == "__main__":
    subber = ChineseWordSub(defaultNormal)
    print subber
    # test case insensitivity
    import LangSupport
    inStr =  u"北京有啥好玩儿的"
    outStr = u"北京有什么好玩的"
    # instr = u' '.join(LangSupport.splitChinese(inStr))
    print (inStr)
    print ("Test #1 : '%s'" % subber.sub(inStr))
    
    # print (re.sub("\s生快\s|\s生快$","生日快乐","祝 你 生快"))
