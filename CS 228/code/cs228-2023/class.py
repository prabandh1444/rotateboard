#!/usr/bin/python3

from z3 import * # load z3 library









# declare a Boolean variable
p1 = Bool ( "p1" )
p2 = Bool ( "p2" ) 








# construct a formula
phi = Or ( p1 , p2 )
phi = Or (phi,phi)







# printing the formula
# print ( phi )        








# allocate solver
s = Solver ()








# add formula to the solver
s.add ( phi )
# print(s)







# check satisfiability
r = s.check()







# if r == sat :
#     print( " sat " )
# else:
#     print( " unsat " )

    






# if r == sat:
#     # read  assignment/model
#     m = s.model()
#     # print model
#     print(m)
# else:
#     print("unsat")



































# # packaging solving and model printing

def solve ( phi ):
    s = Solver ()
    s.add ( phi )
    r = s.check() # runs CDCL
    if r == sat :
        m = s.model() #pick model 
        print( m )
    else:
        print(r)
        # print( "unsat" )


p1_p2 = And(p1,p2)

solve( p1_p2 )




# accessing sub - formulas
print ( p1_p2.arg(0) )
print ( p1_p2.arg(1) )


# accessing the symbol at the head
ab_decl = p1_p2.decl()
name = ab_decl.name()
if name == "and" :
    print ( "Found an And" )
if name == "or" :
    print ( "Found an Or" )





