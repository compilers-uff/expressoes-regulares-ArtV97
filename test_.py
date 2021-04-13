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

def test_10():
    #(a+b)*abba(a+b)*
    assert er.match(".(.(*(+(a,b)), .(a,.(b,.(b,a)))), *(+(a,b)))", "abbaba") == True

def test_11():
    #(a+b)*abba(a+b)*
    assert er.match(".(.(*(+(a,b)), .(a,.(b,.(b,a)))), *(+(a,b)))", "ababa") == False

def test_12():
    #0(0+1)*1
    assert er.match(".(.(0,*(+(0,1))),1)", "0001010") == False

def test_13():
    #0(0+1)*1
    assert er.match(".(.(0,*(+(0,1))),1)", "00010101") == True

def test_14():
    # 1*(01*01*)*
    # palavras com numero par de zeros
    assert er.match(".(*(1), *(.(.(0,*(1)), .(0,*(1)))))", "1100") == True

def test_15():
    # 1*(01*01*)*
    # palavras com numero par de zeros
    assert er.match(".(*(1), *(.(.(0,*(1)), .(0,*(1)))))", "110010") == False

#def test_12():    
    #assert er.match("", "") == True
