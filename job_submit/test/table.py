#!/usr/bin/python

a= """
H He
Li Be B  C  N  O  F  Ne
Na Mg Al Si P  S  Cl Ar
K  Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr
Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe
Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl
Pb Bi Po At Rn

Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh
Fi Mc Lv Ts Og
"""

count = 0 
for i in a.split():
    count +=1
    print  "'%-2s':%-3d," %(i, count),
    if count%4==0:
        print '\n'
