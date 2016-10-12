# -*- coding:utf-8 -*-
from python_ner import ner


# all possible categories ['film','music','book','entertainer','politician','location','company','country','food']

# initializing 
# By default, we load all categories of our entities, if you want part of them(such as all kind of people: [entertainer, politician] )
# using NER = ner(['entertainer','politician'])
NER = ner()


# note the sentence should be 'utf-8' encoded
sentence = "义勇军进行曲后这一辈人还能看得到温家宝的童话吗?01,小学上300课跟同学看《无间道》被没收。水手服姐啦，中国北京海淀区，去吃烤鸡翅吧, 马云\n"



# one can simply call function findAllEntity to find all entities in a sentence
result = NER.findAllEntity(sentence)



print result
# the result is organised as
# {
#  u'烤鸡翅': {'category': ['food'], 'pos': [[59, 61]]},
#  u'中国': {'category': ['country'], 'pos': [[49, 50]]}, 
#  u'温家宝': {'category': ['politician'], 'pos': [[12, 14]]},
#  u'北京': {'category': ['location'], 'pos': [[51, 52]]}, 
#  u'无间道': {'category': ['film'], 'pos': [[35, 37]]}, 
#  u'海淀区': {'category': ['location'], 'pos': [[53, 55]]},
#  u'义勇军进行曲': {'category': ['music'], 'pos': [[0, 5]]}
# }

for v in result.values():
	print v['category'][0]


# list all items
for k,v in result.iteritems():
	print k, v['category'], v['pos']
