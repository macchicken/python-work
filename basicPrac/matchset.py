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
def new_oneof(chars): return lambda text: set([text[1:]]) if (text and text[0] in chars) else null
def new_opt(x):       return new_alt(new_lit(''), x) #opt(x) means that x is optional
new_dot = lambda text: set([text[1:]]) if text else null
new_eol = lambda text: set(['']) if text == '' else null
null = frozenset([])

def new_compiler_match(pattern, text):
	"Match pattern against start of text; return longest match found or None."
	remainders=pattern(text)
	if remainders:
		shortest = min(remainders, key=len)
		return text[:len(text)-len(shortest)]

def new_compile_search(pattern, text):
    for i in range(len(text) or 1):
        m = new_compiler_match(pattern, text[i:])
        if m is not None: return m

def test_compiler_match():
	assert new_compiler_match(new_star(new_lit('a')), 'aaaaabbbaa') == 'aaaaa'
	assert new_compiler_match(new_lit('hello'), 'hello how are you?') == 'hello'
	assert new_compiler_match(new_lit('x'), 'hello how are you?') == None
	assert new_compiler_match(new_oneof('xyz'), 'x**2 + y**2 = r**2') == 'x'
	assert new_compiler_match(new_oneof('xyz'), '   x is here!') == None
	assert new_compiler_match(new_star(new_lit('a')), 'aaabcd') == 'aaa'
	assert new_compiler_match(new_lit('abc'), 'abc') == 'abc'
	assert new_compiler_match(new_alt(new_lit('b'), new_lit('c')), 'ab') == None
	assert new_compiler_match(new_alt(new_lit('b'), new_lit('a')), 'ab') == 'a'
	assert new_compile_search(new_lit(''), '') == ''
	assert new_compile_search(new_alt(new_lit('b'), new_lit('c')), 'ab') == 'b'
	assert new_compile_search(new_star(new_alt(new_lit('a'), new_lit('b'))), 'ab') == 'ab'
	assert new_compile_search(new_alt(new_lit('b'), new_lit('c')), 'ad') == None
	assert new_lit('abc')('abcdef') == set(['def'])
	assert (new_seq(new_lit('hi '), new_lit('there '))('hi there nice to meet you')== set(['nice to meet you']))
	assert new_alt(new_lit('dog'), new_lit('cat'))('dog and cat') == set([' and cat'])
	assert new_dot('am i missing something?') == set(['m i missing something?'])
	assert new_dot('') == frozenset([])
	assert new_oneof('a')('aabc123') == set(['abc123'])
	assert new_oneof('abc')('babc123') == set(['abc123'])
	assert new_oneof('abc')('dabc123') == frozenset([])
	assert new_eol('') == set([''])
	assert new_eol('not end of line') == frozenset([])
	assert new_star(new_lit('hey'))('heyhey!') == set(['!', 'heyhey!', 'hey!'])
	assert new_plus(new_lit('hey'))('heyhey!') == set(['!', 'hey!'])
	assert new_opt(new_lit('hey'))('heyhey!') == set(['hey!', 'heyhey!'])
	return 'compiler_match tests pass'

print test_compiler_match()

pat=new_lit('a')
print pat('a string')
pat2=new_plus(pat)
print pat2('aaaaab')
#Disassemble the bytesource object bytesource can denote either a module,a class,a method,a function,or a code object
# dis.dis(pat)
g=new_alt(new_lit('a'),new_lit('b'))
print g('abc')
pat3=new_star(pat)
print pat3('aaa')


# --------------
# User Instructions
#
# Complete the code for the compiler by completing the constructor
# for the patterns alt(x, y) and oneof(chars). 

def interpreter_lit(s): set_s=set([s]);return lambda Ns: set_s if len(s) in Ns else null
def interpreter_alt(x, y):      return lambda Ns: set(x(Ns))|set(y(Ns))
def interpreter_star(x):        return lambda Ns: interpreter_opt(interpreter_plus(x))(Ns)
def interpreter_plus(x):        return lambda Ns: genseq(x, interpreter_star(x), Ns,startx=1) #Tricky
def interpreter_oneof(chars): set_chars=set(chars);return lambda Ns: set_chars if Ns and 1 in Ns else null
def interpreter_seq(x, y):      return lambda Ns: genseq(x, y, Ns)
def interpreter_opt(x):         return interpreter_alt(interpreter_epsilon, x)
interpreter_dot = interpreter_oneof('?')    # You could expand the alphabet to more chars.
interpreter_epsilon = interpreter_lit('')   # The pattern that matches the empty string.
def infinite_genseq(x,y,Ns,startx=0):
	Nss=range(startx,max(Ns)+1)
	return set(m1+m2 for m1 in x(Nss) for m2 in y(Nss) if len(m1+m2) in Ns)
def genseq(x,y,Ns,startx=0):
	# generate all x to produce the length of x from giving possible size startx 
	# and deduct the Ns from x to generate all length of y
	# then do the generation of all y,finally concatenate x and y
	if not Ns:return null
	xmatches=x(set(range(startx,max(Ns)+1)))
	Ns_x=set(len(m) for m in xmatches)
	Ns_y=set(n-m for n in Ns for m in Ns_x if n-m>=0)
	ymatches=y(Ns_y)
	return set(m1+m2 for m1 in xmatches for m2 in ymatches if len(m1+m2) in Ns)
null = frozenset([])

def interpreter_test():
    f = interpreter_lit('hello')
    assert f(set([1, 2, 3, 4, 5])) == set(['hello'])
    assert f(set([1, 2, 3, 4]))    == null 

    g = interpreter_alt(interpreter_lit('hi'), interpreter_lit('bye'))
    assert g(set([1, 2, 3, 4, 5, 6])) == set(['bye', 'hi']) 
    assert g(set([1, 3, 5])) == set(['bye'])

    h = interpreter_oneof('theseletters')
    assert h(set([1, 2, 3])) == set(['t', 'h', 'e', 's', 'l', 'r'])
    assert h(set([2, 3, 4])) == null
    return 'interpreter tests pass'

def test_gen():
    def N(hi):return set(range(hi+1))
    a, b, c = map(interpreter_lit, 'abc')
    assert interpreter_star(interpreter_oneof('ab'))(N(2)) == set(['', 'a', 'aa', 'ab', 'ba', 'bb', 'b'])
    assert (interpreter_seq(interpreter_star(a), interpreter_seq(interpreter_star(b), interpreter_star(c)))(set([4])) ==
            set(['aaaa', 'aaab', 'aaac', 'aabb', 'aabc', 'aacc', 'abbb',
                 'abbc', 'abcc', 'accc', 'bbbb', 'bbbc', 'bbcc', 'bccc', 'cccc']))
    assert (interpreter_seq(interpreter_plus(a), interpreter_seq(interpreter_plus(b), interpreter_plus(c)))(set([5])) ==
            set(['aaabc', 'aabbc', 'aabcc', 'abbbc', 'abbcc', 'abccc']))
    assert (interpreter_seq(interpreter_oneof('bcfhrsm'), interpreter_lit('at'))(N(3)) ==
            set(['bat', 'cat', 'fat', 'hat', 'mat', 'rat', 'sat']))
    assert (interpreter_seq(interpreter_star(interpreter_alt(a, b)), interpreter_opt(c))(set([3])) ==
            set(['aaa', 'aab', 'aac', 'aba', 'abb', 'abc', 'baa',
                 'bab', 'bac', 'bba', 'bbb', 'bbc']))
    assert interpreter_lit('hello')(set([5])) == set(['hello'])
    assert interpreter_lit('hello')(set([4])) == set()
    assert interpreter_lit('hello')(set([6])) == set()
    return 'test_gen passes'

print interpreter_test()
print test_gen()