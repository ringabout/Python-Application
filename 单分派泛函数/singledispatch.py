# -*- coding: utf-8 -*-
# Created by Python高效编程
from functools import singledispatch
from numbers import Integral
from collections.abc import MutableSequence


@singledispatch
def pprint(obj):
    print(f'({obj.__class__.__name__}) {obj}')

  
    
@pprint.register
def _(obj:Integral):
    print(f'({obj.__class__.__name__}) {obj}')

   
    
@pprint.register(float)
def _(obj):
    print(f'({obj.__class__.__name__}) {obj:.2f}')
 
    
@pprint.register(tuple)
@pprint.register(set)
@pprint.register(MutableSequence)
def _(obj):
    print(f'{"-"*7}{obj.__class__.__name__}{"-"*8}')
    print(f'index   type      value')
    for index, value in enumerate(obj):
        print(f'{index:^6}->{type(value).__name__:<8}: {value}')


@pprint.register(dict)
def _(obj):
    print(f'{"-"*7}{obj.__class__.__name__}{"-"*8}')
    print('     key            value')
    for k, v in sorted(obj.items()):
        print(f'({type(k).__name__}){k:<6} -> ({type(v).__name__}){v:<6}')
    

@singledispatch
def fprint(obj):
    return NotImplemented


#@fprint.register(str)
#def _(obj):
#    print('我是一个字符串')
#    print(obj)
    
@fprint.register
def _(obj: str):
    print('我是一个字符串')
    print(obj)
    

@fprint.register(int)
def _(obj):
    print('我是一个整型')
    print(obj)    
    
    
    
    
    
    
    
    
    
    
    

