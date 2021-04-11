import pytest
import er

def test_0():
    assert er.match("a", "a") == True

def test_1():
    assert er.match("+(a, b)", "a") == True

def test_2():
    assert er.match(".(a, b)", "a") == False

def test_3():
    assert er.match(".(a, b)", "ab") == True
    
def test_4():    
    assert er.match("*(+(a, b))", "a") == True
    
def test_5():    
    assert er.match("*(+(a, b))", "aaa") == True
    
def test_6():    
    assert er.match("*(+(a, b))", "ab") == True
    
def test_7():    
    assert er.match("*(+(a, b))", "aba") == True
    
def test_8():    
    assert er.match("*(+(a, b))", "abababa") == True
