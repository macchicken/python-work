import this
"""
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
"""

pyg = 'ay'
original = raw_input('Enter a word:')
#check is valid word and contain alphabetical character 
if len(original) > 0 and original.isalpha():
    word = original.lower()
    first = word[0]
    if first=="a" or first =="e" or first=="i" or first=="o" or first=="u":
        print "vowel translation"
        new_word = original+pyg
        print new_word
    else:
        print "consonant translation"
        new_word = original[1:len(original)]+original[0]+pyg
        print new_word
else:
    print 'empty or contain non-alphabetical character'