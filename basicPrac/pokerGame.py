from random import shuffle
from random import randint
from random import randrange
from collections import defaultdict
from itertools import combinations
from itertools import product
# two kinds of input should be handled
# straight(ranks): returns True if the hand is a straight.
# flush(hand):     returns True if the hand is a flush.
# kind(n, ranks):  returns the first rank that the hand has
#                  exactly n of. For A hand with 4 sevens 
#                  this function would return 7.
#				   return None if there is no n-of-a-kind in the hand.
# two_pair(ranks): if there is a two pair, this function 
#                  returns their corresponding ranks as a 
#                  tuple. For example, a hand with 2 twos
#                  and 2 fours would cause this function
#                  to return (4, 2).
#				   return two ranks as tuple:(highest,lowest);otherwise return None.
# card_ranks(hand) returns an ORDERED list of the ranks 
#                  in a hand (where the order goes from
#                  highest to lowest rank). 
# A set object is an unordered collection of distinct hashable objects. 
# Common uses include membership testing, removing duplicates from a sequence,
# and computing mathematical operations such as intersection, 
# union, difference, and symmetric difference.

hands = ['JS','JD','2S','2C','7H']
mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC']
hand_names = ['Straight Flush','4 Kind','Full House','Flush','Straight','3 Kind','2 Pair','Pair','High Card']
# hands = [(11,'S'),(11,'D'),(2,'S'),(2,'L'),(7,'H')]
# special_rank ={"T":10,"J":11,"Q":12,"K":13,"A":14}
# rank_list=['2','3','4','5','6','7','8','9']


# def straight(ranks):
	# return len(set(ranks))==5 and (max(ranks)-min(ranks)==4)
def straight(ranks):
	try:
		if len(set(ranks))==5:
			temp=''
			for rank in ranks:temp=temp+'-'+str(rank)
			return '-14-13-12-11-10-9-8-7-6-5-4-3-2-1'.index(temp)>=0
		else:return False
	except ValueError:
		# print "not a straight"
		return False

def flush(hand):
	suits=[s for r,s in hand]
	return len(set(suits))==1
# def flush(hand):
	# if hand is not None and len(hand)==5:
		# prev_suit=hand[0][1]
		# for i in range(1,len(hand)):
			# if prev_suit!=hand[i][1]:
				# return False
			# else:
				# prev_suit=hand[i][1]
		# return True
	# else:
		# return False

def kind(n,ranks):
	for r in ranks:
		if ranks.count(r)==n:return r
	return None
# def kind(n,ranks):
	# rank_result = [rank for rank in ranks if ranks.count(rank)==n]
	# if len(rank_result)==0:return None
	# else:return rank_result[0]

def two_pairs(ranks):
	rank_result = set([rank for rank in ranks if ranks.count(rank)==2])
	if len(rank_result)!=2:return None
	else:return tuple([rank_result.pop(),rank_result.pop()])
# def two_pairs(ranks):
	# pair = kind(2,ranks)
	# ranks.sort(cmp=None,key=None,reverse=False) 
	# lowpair =kind(2,ranks)
	# if pair and lowpair!=pair:return (pair,lowpair)
	# else:return None

# def card_ranks(hand):
	# ranks=[]
	# rank=0
	# for onecard in hand:
		# if str(onecard[0]).isalpha() and onecard[0].upper() in special_rank.keys():
			# rank=special_rank[onecard[0]]
		# else:
			# if str(onecard[0]).isdigit() and str(onecard[0]) in rank_list:
				# rank=int(onecard[0])
		# ranks.append(rank)
		# rank=0
	# ranks.sort(cmp=None,key=None,reverse=True)
	# return ranks
def card_ranks(hand):
	try:
		ranks = ['--23456789TJQKA'.index(r) for r,s in hand]
		ranks.sort(cmp=None,key=None,reverse=True)
		# if ranks==[14,5,4,3,2]:ranks=[5,4,3,2,1]
	except ValueError:
		print "error in looking up ranks"
		return None
	return [5,4,3,2,1] if (ranks==[14,5,4,3,2]) else ranks

def group(items):
	"Return a list of [(count,x),...],highest count first.then highest x first."
	groups = [(items.count(x),x) for x in set(items)]
	groups.sort(cmp=None,key=None,reverse=True)
	return groups

# def hand_rank(hand):
    # ranks = card_ranks(hand)
    # if straight(ranks) and flush(hand):            # straight flush
        # return (8, max(ranks))
    # elif kind(4, ranks):                           # 4 of a kind
        # return (7, kind(4, ranks), kind(1, ranks))
    # elif kind(3, ranks) and kind(2, ranks):        # full house
        # return (6,kind(3, ranks),kind(2, ranks))
    # elif flush(hand):                              # flush
        # return (5,max(ranks),hand)
    # elif straight(ranks):                          # straight
        # return (4,max(ranks))
    # elif kind(3, ranks):                           # 3 of a kind
        # return (3,kind(3, ranks))
    # elif two_pairs(ranks):                          # 2 pair
        # return (2,max(kind(2, ranks),kind(2, ranks)))
    # elif kind(2, ranks):                           # kind 1 pair
        # return (1,kind(2, ranks),ranks)
    # else:                                          # nothing high card
        # return (0,ranks)
count_rankings ={(5,):10,(4,1):7,(3,2):6,(3,1,1):3,(2,2,1):2,(2,1,1,1):1,(1,1,1,1,1):0}
def hand_rank(hand):
	groups = group(['--23456789TJQKA'.index(r) for r,s in hand])
	counts,ranks=zip(*groups)
	if ranks==(14,5,4,3,2):ranks=(5,4,3,2,1)
	straight = len(ranks)==5 and max(ranks)-min(ranks)==4
	flush = len(set([s for r,s in hand]))==1
	# return (9 if (5,)==counts else
			# 8 if straight and flush else
			# 7 if (4,1)==counts else
			# 6 if (3,2)==counts else
			# 5 if flush else
			# 4 if straight else
			# 3 if (3,1,1)==counts else
			# 2 if (2,2,1)==counts else
			# 1 if (2,1,1,1)==counts else
			# 0),ranks
	return max(count_rankings[counts],4*straight+5*flush),ranks

# def allmax(iterable,key=None):
	# "Return a list of all items equal to the max if the iterable."
	# max_val = max([key(item) for item in iterable])
	# reuslt=[]
	# for item in iterable:
		# if key(item)==max_val:reuslt.append(item)
	# return reuslt
def allmax(iterable,key=None):
	result,maxval=[],None
	key = key or (lambda x:x)
	for x in iterable:
		xval = key(x)
		if not result or xval>maxval:
			result,maxval=[x],xval
		elif xval==maxval:
			result.append(x)
	return result


def poker(hands):
	"Return a list of wining hands: poker([hand,...]) => [hand,...]"
	# return max(hands,key=hand_rank)
	# hands_dict={}
	# for hand in hands:
		# hands_dict[hand_rank(hand)]=hand
	# if len(hands_dict)==1:return "ties!!!"
	# else:return hands_dict[max(hands_dict.keys())]
	return allmax(hands,key=hand_rank)


# def deal(numhands, n=5, deck=mydeck):
	# "Shuffle the deck and deal out numhands n-card hands."
	# random.shuffle(deck)
	# return [deck[n*i:n*(i+1)] for i in range(numhands)]
def deal(numhands, n=5, deck=mydeck):
	total_hands=[]
	deckcopy = deck[:]
	shuffle(deckcopy)
	for i in range(numhands):
		index = randint(0,len(deckcopy)-1)
		one_hand=[deckcopy.pop(index)]
		for j in range(1,n):
			index = randint(0,len(deckcopy)-1)
			one_hand.append(deckcopy.pop(index))
		total_hands.append(one_hand)
	return total_hands
def hand_percentages(n=700*1000):
	"Sample n random hands and print a table of perentages for each type of hand."
	counts=[0]*9
	for i in range(n/10):
		for hand in deal(10):
			ranking = hand_rank(hand)[0]
			counts[ranking]+=1
	for i in reversed(range(9)):
		print "%14s: %6.3f %%" % (hand_names[i],100.*counts[i]/n)


def kunth_shuffle(deck):
	N = len(deck)
	for i in range(N-1):
		swap(deck,i,randrange(i,N))
def swap(deck,i,j):
	# print 'swap',i,j
	deck[i],deck[j]=deck[j],deck[i]
def bad_shuffle(deck):
	N = len(deck)
	swapped =[False]*N
	while not all(swapped):
		i,j = randrange(N),randrange(N)
		swapped[i],swapped[j] = True,True
		swap(deck,i,j)
def shuffle2(deck):
	N =len(deck)
	swapped=[False]*N
	while not all(swapped):
		i,j=randrange(N),randrange(N)
		swapped[i]=True
		swap(deck,i,j)
def shuffle3(deck):
	N = len(deck)
	for i in range(N):
		swap(deck,i,randrange(N))
def test_shuffler(shuffler=kunth_shuffle,deck='abcd',n=10000):
	counts = defaultdict(int)
	for _ in range(n):
		input = list(deck)
		shuffler(input)
		counts[''.join(input)]+=1
	e = n*1./factorial(len(deck))
	ok = all((0.9<=counts[item]/e<=1.1) for item in counts)
	name = shuffler.__name__
	print '%s(%s) %s' % (name,deck,('ok' if ok else'*** BAD ***'))
	print '		'
	for item,count in sorted(counts.items()):
		print "%s:%4.1f" % (item,count*100./n),
	print
def test_shufflers(shufflers=[kunth_shuffle,bad_shuffle],decks=['abc','ab'],n=10000):
	for deck in decks:
		print
		for f in shufflers:
			test_shuffler(f,deck,n)
def factorial(n):
	if n<=1:return 1
	else:return n*factorial(n-1)


def best_hand_7(hand):
	"From a 7-card hand,return the best 5 card hand."
	# return max(combinations(hand, 5),key=hand_rank)
	# result=allmax(combinations(hand, 5),key=hand_rank)
	total_combinations = combinations(hand, 5)
	has_more=True
	result,maxval=[],None
	# count=0
	while has_more:
		try:
			one_possible=list(total_combinations.next())
			xval=hand_rank(one_possible)
			if not result or xval>maxval:
				result,maxval=[one_possible],xval
			elif xval==maxval:
				result.append(one_possible)
			# count+=1
		except StopIteration:
			has_more=False
	# print count,'combinations'
	return tuple(result[0])
black_jokers=[r+s for r in '23456789TJQKA' for s in 'SC']
red_jokers=[r+s for r in '23456789TJQKA' for s in 'DH']
def replacements(card):
	#Return a list of the possible replacesments for a card there will be more than 1 only for wild card.
	if card=='?B': return black_jokers
	elif card=='?R': return red_jokers
	else: return [card]
def best_wild_hand(hand):
	"Try all values for jokers in all 5-card selections."
	# copy_hand = ' '.join(hand)
	# b_in='?B' in copy_hand
	# r_in='?R' in copy_hand
	# if b_in or r_in:
		# hand_replacements=[]
		# if b_in:
			# hand_replacements=[copy_hand.replace('?B',i) for i in black_jokers if i not in copy_hand]
			# if r_in:
				# one_replacesments=[]
				# for one in hand_replacements:
					# one_replacesment=[one.replace('?R',j) for j in red_jokers if j not in one]
					# one_replacesments=one_replacesments+one_replacesment
				# hand_replacements=one_replacesments
		# else:
			# hand_replacements=[copy_hand.replace('?R',i) for i in red_jokers if i not in copy_hand]
		# all_result=[]
		# for one_hand in hand_replacements:
			# one_result=best_hand_7(one_hand.split())
			# all_result.append(one_result)
		# result=allmax(all_result,key=hand_rank)
		# return result if len(result)>1 else result[0] if len(result)==1 else None
	# else:
		# return best_hand_7(hand)]
	hands = set(best_hand_7(h) for h in product(*map(replacements,hand)))
	return max(hands,key=hand_rank)



#TEST-----------------------------------------------------------------------
def test():
	try:
		"Test cases for the functions in poker program."
		sf = "6C 7C 8C 9C TC".split()# straight flsuh
		fk = "9D 9H 9S 9C 7D".split()# four of a kind
		fh = "TD TC TH 7C 7D".split()# full house
		tp = "5S 5D 9H 9C 6S".split()# two pair
		s1 = "AS 2S 3S 4S 5C".split()# A-5 straight
		s2 = "2C 3C 4C 5S 6S".split()# 2-6 straight
		ah = "AS 2S 3S 4S 6C".split()# A high
		sh = "2S 3S 4S 6C 7D".split()# 7 high
		assert poker([s1,s2,ah,sh]) == [s2]
		assert poker([sf,fk,fh]) == [sf]
		assert poker([fk,fh]) == [fk]
		assert poker([fh,fh]) == [fh,fh]
		assert poker([sf]) == [sf]
		assert poker([sf for x in range(1,101)]) == [sf]*100
		assert card_ranks(hands) == [11, 11, 7, 2, 2]
		assert card_ranks(sf) == [10, 9, 8, 7, 6]
		assert card_ranks(fk) == [9, 9, 9, 9, 7]
		assert card_ranks(fh) == [10, 10, 10, 7, 7]
		assert hand_rank(sf) == (8,10)
		assert hand_rank(fk) == (7,9,7)
		assert hand_rank(fh) == (6,10,7)
		assert straight([9,8,7,6,5]) == True
		assert straight([9,8,8,6,5]) == False
		assert flush(sf) == True
		assert flush(fk) == False
		assert flush(fh) == False
		fkranks = card_ranks(fk)
		tpranks = card_ranks(tp)
		assert kind(4,fkranks) ==9
		assert kind(3,fkranks) ==None
		assert kind(2,fkranks) ==None
		assert kind(1,fkranks) ==7
		assert two_pairs(fkranks) ==None
		assert two_pairs(tpranks) ==(9,5)
		assert allmax([sh,s2],key=hand_rank) == [s2]
	except AssertionError:
		return "tests fail"
	return "tests pass"
def testfkfh():
	try:
		"Test cases for the functions in poker program."
		fk = "9D 9H 9S 9C 7D".split()
		fh = "TD TC TH 7C 7D".split()
		assert poker([fk,fh]) == fk
	except AssertionError:
		return "tests fail"
	return "tests pass"
def testfhtwo():
	try:
		"Test cases for the functions in poker program."
		fh = "TD TC TH 7C 7D".split()
		assert poker([fh,fh]) == fh
	except AssertionError:
		return "tests fail"
	return "tests pass"
def test_best_hand_7():
    assert (sorted(best_hand_7("6C 7C 8C 9C TC 5C JS".split()))
			== ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand_7("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand_7("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    return 'test_best_hand passes'
def test_best_wild_hand():
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    return 'test_best_wild_hand passes'
#TEST-----------------------------------------------------------------------


if __name__ == '__main__':
	# print test()
	# print poker(deal(4))
	# hand_percentages()
	# test_shufflers(shufflers=[shuffle2,shuffle3])
	# print best_hand_7(s1)
	# print test_best_hand_7()
	# print test_best_wild_hand()
	# print best_hand_7("6C 7C 8C 9C TC 5C JS".split())
	# s1="6C 7C 8C 9C TC 5C JS".split()
	# s2="6C 7C 8C 9C TC 5C ?B".split()
	# print map(replacements,s2)
	# print list(product(*[['6C'], ['7C'], ['8C'], ['9C'], ['TC'], ['5C'], 
	# ['2S', '2C', '3S', '3C', '4S','4C', '5S', '5C', '6S', '6C', '7S', 
	# '7C', '8S', '8C', '9S', '9C', 'TS', 'TC', 'JS', 'JC', 'QS', 'QC', 'KS', 'KC', 'AS', 'AC']]))
	pass