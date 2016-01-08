
def test_for_case_sent_by_TA():
    KB = [ "G(x,y) => F(y,x)", "F(S,SS) => G(x,y)", "G(SS,S)"]
    query = "F(B,A)"
    return len(list(bc_ask(KB, query))) > 0

def test_for_sample_input():
    KB = [ "A(x) => H(x)", "D(x,y) => ~H(y)", "B(x,y) ^ C(x,y) => A(x)",\
                "D(x,y) ^ Q(y) => C(x,y)", "F(x) => G(x)", "G(x) => H(x)",\
                "H(x) => F(x)", "R(x) => H(x)", "B(John,Alice)", "B(John,Bob)",\
                "D(John,Alice)", "Q(Bob)", "D(John,Bob)", "R(Tom)"]

    queries = [ "F(Bob)", "H(John)", "~H(Alice)", "~H(Jon)", "G(Bob)", "G(Tom)"]

    for query in queries:
        yield len(list(bc_ask(KB, query))) > 0
        visited_facts = list()

def test_for_whatsapp_test_case():
    global visited_facts
    KB = [ "Male(x) ^ Parent(m,z) ^ Sibling(x,m) => Uncle(x,z)",\
            "Father(x,y) => Parent(x,y)",\
            "Mother(x,y) => Parent(x,y)",\
            "Parent(x,p) ^ Parent(x,w) ^ Parent(a,b) ^ Parent(c,d) => Sibling(p,w)",\
            "Male(John)",\
            "Father(Shawn,John)",\
            "Father(Suresh,Ramesh)",\
            "Mother(Kill,Bill)",\
            "Mother(Neelu,Sarah)",\
            "Father(Shawn,Neelu)"]

    queries = ["Uncle(John,Sarah)", "Sibling(John,Sarah)", "Sibling(John,Neelu)"]

    for query in queries:
        #yield { query: len(list(bc_ask(KB, query)))}
        yield len(list(bc_ask(KB, query))) > 0
        visited_facts = list()

    #print len(list(bc_ask(KB, "Sibling(John,Neelu)")))
    #print len(list(bc_ask(KB, "Uncle(John,Sarah)")))
    #print len(list(bc_ask(KB, "Sibling(John,Sarah)")))

def test_by_aniket_1():
    global visited_facts
    KB = [ "A(x,y) ^ B(x,Bill) => C(John,y)", "B(x,y) => A(Jon,y)",\
            "B(John,Bill)", "B(Tam,Bob)" ]
    queries = ["C(John,Bob)"]

    for query in queries:
        #yield { query: len(list(bc_ask(KB, query)))}
        yield len(list(bc_ask(KB, query))) > 0
        visited_facts = list()

def test_by_aniket_2():
    global visited_facts
    KB = [ "A(x,y) ^ B(x,Bill) => C(John,y)", "B(x,y) => A(John,y)",\
            "B(John,Bill)", "B(Tam,Bob)" ]
    queries = ["C(John,Bob)"]

    for query in queries:
        #yield { query: len(list(bc_ask(KB, query)))}
        yield len(list(bc_ask(KB, query))) > 0
        visited_facts = list()

def test_by_aniket_3():
    global visited_facts
    KB = [ "A(x,y) ^ B(x,Bill) => C(John,y)", "B(x,y) => A(Dad,y)",\
            "B(Bob,Bob)", "B(Dad)" ]
    queries = ["C(John,Bob)"]

    for query in queries:
        #yield { query: len(list(bc_ask(KB, query)))}
        yield len(list(bc_ask(KB, query))) > 0
        visited_facts = list()

def test_vasu_1():
    global visited_facts
    KB = [ "F(x,y,z) ^ R(z) => G(z)", "A(x,y,z) => F(x,y,x)",\
            "A(Add,Sub,Add)", "R(Add)"]
    queries = ["G(Add)"]

    for query in queries:
        #yield { query: len(list(bc_ask(KB, query)))}
        yield len(list(bc_ask(KB, query))) > 0
        visited_facts = list()

def test_vasu_2():
    global visited_facts
    KB = [ "F(y,y,x) ^ R(z) => G(z)", "A(x,y,z) => F(x,y,y)",\
            "A(Random1,Sub,Random2)", "R(Add)"]
    queries = ["G(Add)"]

    for query in queries:
        #yield { query: len(list(bc_ask(KB, query)))}
        yield len(list(bc_ask(KB, query))) > 0
        visited_facts = list()

def test_vasu_3():
    global visited_facts
    KB = [ "F(z,y,x) ^ R(z) => G(z)",\
            "A(x,y,z) => F(x,y,x)",\
            "A(Add,Sub,Random2)",\
            "R(Add)"]

    queries = ["G(Add)"]

    for query in queries:
        #yield { query: len(list(bc_ask(KB, query)))}
        yield len(list(bc_ask(KB, query))) > 0
        visited_facts = list()

def test_vasu_4():
    global visited_facts
    KB = [ "F(x,y,z) ^ R(z) => G(z)",\
            "A(x,y,z) => F(x,y,x)",\
            "A(Add,Sub,Add)",\
            "R(Multiply)"]
    queries = ["G(Multiply)"]

    for query in queries:
        #yield { query: len(list(bc_ask(KB, query)))}
        yield len(list(bc_ask(KB, query))) > 0
        visited_facts = list()


def test_vasu_5():
    global visited_facts
    KB = [ "A(x,AA,y,CC,w) ^ B(John) ^ D(x,w) => C(CC)",\
            "E(XX) => A(a,b,c,CC,a)",\
            "E(XX)",\
            "B(John)",\
            "D(XX,XX)"]
    queries = ["C(CC)"]

    for query in queries:
        #yield { query: len(list(bc_ask(KB, query)))}
        yield len(list(bc_ask(KB, query))) > 0
        visited_facts = list()

def test_rohit_1():
    global visited_facts
    KB = [ "A(x,y) ^ B(z,w) => C(x,w)",\
            "C(y,x) => A(x,y)",\
            "C(x,y) => B(y,x)",\
            "A(EE,CS)",\
            "B(MS,PHD)"]

    queries = ["C(PHD,PHD)",\
               "C(MS,MS)",\
               "C(EE,EE)",\
               "C(CS,CS)"]

    for query in queries:
        #yield { query: len(list(bc_ask(KB, query)))}
        yield len(list(bc_ask(KB, query))) > 0
        visited_facts = list()


#assert (test_for_case_sent_by_TA() == True)
#assert (list(test_for_sample_input()) == [False, True, True, False, False, True])
#assert (list(test_for_whatsapp_test_case()) == [True, False, True])
#assert (list(test_for_whatsapp_test_case()) == [True, False, True])
#assert (list(test_by_aniket_1()) ==  [False]) 
#assert (list(test_by_aniket_2()) == [True])
#assert (list(test_by_aniket_3()) == [False])
#assert (list(test_vasu_1()) == [True] )
#assert (list(test_vasu_2()) == [False])
#assert (list(test_vasu_3()) == [True])
#assert (list(test_vasu_4()) == [False])
#assert (list(test_vasu_5()) == [False])
#print list(test_rohit_1())
