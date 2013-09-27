import dis
#----------------
# User Instructions
#
# The function, matchset, takes a pattern and a text as input
# and returns a set of remainders. For example, if matchset 
# were called with the pattern star(lit(a)) and the text 
# 'aaab', matchset would return a set with elements 
# {'aaab', 'aab', 'ab', 'b'}, since a* can consume one, two
# or all three of the a's in the text.
#
# Your job is to complete this function by filling in the 
# 'dot' and 'oneof' operators to return the correct set of 
# remainders.
#
# dot:   matches any character.
# oneof: matches any of the characters in the string it is 
#        called with. oneof('abc') will match a or b or c.
# any(iterable) Return True if any element of the iterable is true. If the iterable is empty, return False

def matchset(pattern, text):
    "Match pattern at start of text; return a set of remainders of text."
    op, x, y = components(pattern)
    if 'lit' == op:
        return set([text[len(x):]]) if text.startswith(x) else null
    elif 'seq' == op:
        return set(t2 for t1 in matchset(x, text) for t2 in matchset(y, t1))
    elif 'alt' == op:
        return matchset(x, text) | matchset(y, text)
    elif 'dot' == op:
        return set([text[1:]]) if text else null
    elif 'oneof' == op:
        return set([text[1:]]) if any(text.startswith(c) for c in x) else null
    elif 'eol' == op:
        return set(['']) if text == '' else null
    elif 'star' == op:
        return (set([text]) |
                set(t2 for t1 in matchset(x, text)
                    for t2 in matchset(pattern, t1) if t1 != text))
    else:
        raise ValueError('unknown pattern: %s' % pattern)

null = frozenset()

def components(pattern):
    "Return the op, x, and y arguments; x and y are None if missing."
    x = pattern[1] if len(pattern) > 1 else None
    y = pattern[2] if len(pattern) > 2 else None
    return pattern[0], x, y
   
def test():
    assert matchset(('lit', 'abc'), 'abcdef')            == set(['def'])
    assert matchset(('seq', ('lit', 'hi '),
                     ('lit', 'there ')), 
                   'hi there nice to meet you')          == set(['nice to meet you'])
    assert matchset(('alt', ('lit', 'dog'), 
                    ('lit', 'cat')), 'dog and cat')      == set([' and cat'])
    assert matchset(('dot',), 'am i missing something?') == set(['m i missing something?'])
    assert matchset(('oneof', 'a'), 'aabc123')           == set(['abc123'])
    assert matchset(('eol',),'')                         == set([''])
    assert matchset(('eol',),'not end of line')          == frozenset([])
    assert matchset(('star', ('lit', 'hey')), 'heyhey!') == set(['!', 'heyhey!', 'hey!'])
    
    return 'tests pass'

print test()


#---------------
# User Instructions
#
# Fill out the API by completing the entries for alt, 
# star, plus, and eol.


def lit(string):  return ('lit', string)
def seq(x, y):    return ('seq', x, y)
def alt(x, y):    return ('alt',x,y)
def star(x):      return ('star',x)
def plus(x):      return seq(x,star(x))
def opt(x):       return alt(lit(''), x) #opt(x) means that x is optional
def oneof(chars): return ('oneof', tuple(chars))
dot = ('dot',)
eol = ('eol',)

def test_api():
    assert lit('abc')         == ('lit', 'abc')
    assert seq(('lit', 'a'), 
               ('lit', 'b'))  == ('seq', ('lit', 'a'), ('lit', 'b'))
    assert alt(('lit', 'a'), 
               ('lit', 'b'))  == ('alt', ('lit', 'a'), ('lit', 'b'))
    assert star(('lit', 'a')) == ('star', ('lit', 'a'))
    assert plus(('lit', 'c')) == ('seq', ('lit', 'c'), 
                                  ('star', ('lit', 'c')))
    assert opt(('lit', 'x'))  == ('alt', ('lit', ''), ('lit', 'x'))
    assert oneof('abc')       == ('oneof', ('a', 'b', 'c'))
    return 'api tests pass'

print test_api()


#---------------
# User Instructions
#
# Complete the search and match functions. Match should
# match a pattern only at the start of the text. Search
# should match anywhere in the text.


def search(pattern, text):
    "Match pattern anywhere in text; return longest earliest match or None."
    for i in range(len(text)):
        m = match(pattern, text[i:])
        if m is not None:#in this problem empty string count as true result
            return m
        
def match(pattern, text):
    "Match pattern against start of text; return longest match found or None."
    remainders = matchset(pattern, text)
    if remainders:
        shortest = min(remainders, key=len)
        return text[:len(text)-len(shortest)]
    
def components(pattern):
    "Return the op, x, and y arguments; x and y are None if missing."
    x = pattern[1] if len(pattern) > 1 else None
    y = pattern[2] if len(pattern) > 2 else None
    return pattern[0], x, y

def matchset(pattern, text):
    "Match pattern at start of text; return a set of remainders of text."
    op, x, y = components(pattern)
    if 'lit' == op:
        return set([text[len(x):]]) if text.startswith(x) else null
    elif 'seq' == op:
        return set(t2 for t1 in matchset(x, text) for t2 in matchset(y, t1))
    elif 'alt' == op:
        return matchset(x, text) | matchset(y, text)
    elif 'dot' == op:
        return set([text[1:]]) if text else null
    elif 'oneof' == op:
        return set([text[1:]]) if text.startswith(x) else null
    elif 'eol' == op:
        return set(['']) if text == '' else null
    elif 'star' == op:
        return (set([text]) |
                set(t2 for t1 in matchset(x, text)
                    for t2 in matchset(pattern, t1) if t1 != text))
    else:
        raise ValueError('unknown pattern: %s' % pattern)

def test_matchset():
    assert match(('star', ('lit', 'a')),'aaabcd') == 'aaa'
    assert match(('alt', ('lit', 'b'), ('lit', 'c')), 'ab') == None
    assert match(('alt', ('lit', 'b'), ('lit', 'a')), 'ab') == 'a'
    assert search(('alt', ('lit', 'b'), ('lit', 'c')), 'ab') == 'b'
    return 'match tests pass'

print test_matchset()


# --------------
# User Instructions
#
# Fill out the function match(pattern, text), so that 
# remainders is properly assigned. 


def new_lit(string): return lambda text: set([text[len(string):]]) if text.startswith(string) else null
def new_seq(x, y): return lambda text: set().union(*map(y, x(text)))
def new_star(x): return lambda text: (set([text])|set(t2 for t1 in x(text) if t1 != text for t2 in new_star(x)(t1)))
def new_plus(x): return lambda text: new_seq(x, new_star(x))(text)
def new_alt(x,y): return lambda text: set(x(text))|set(y(text))
def new_oneof(chars): return lambda text: set([t[1:]]) if (text and text[0] in chars) else null
new_dot = lambda t: set([t[1:]]) if t else null
new_eol = lambda t: set(['']) if t == '' else null

pat=new_lit('a')
print pat('a string')
pat2=new_plus(pat)
print pat2('aaaaab')
#Disassemble the bytesource object bytesource can denote either a module,a class,a method,a function,or a code object
# dis.dis(pat)
g=new_alt(new_lit('a'),new_lit('b'))
print g('abc')

def new_compiler_match(pattern, text):
	"Match pattern against start of text; return longest match found or None."
	remainders=pattern(text)
	if remainders:
		shortest = min(remainders, key=len)
		return text[:len(text)-len(shortest)]

def test_compiler_match():
    assert new_compiler_match(star(lit('a')), 'aaaaabbbaa') == 'aaaaa'
    assert new_compiler_match(lit('hello'), 'hello how are you?') == 'hello'
    assert new_compiler_match(lit('x'), 'hello how are you?') == None
    assert new_compiler_match(oneof('xyz'), 'x**2 + y**2 = r**2') == 'x'
    assert new_compiler_match(oneof('xyz'), '   x is here!') == None
    return 'compiler_match tests pass'

print test_compiler_match()