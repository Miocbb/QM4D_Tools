#!/usr/bin/env python3
"""
a script used to calculate the distance between two atoms, the bond angle of
three atoms.

usage:
    python3 calcxzy.py xyz_file [-dist num1, num2] [-angle num1, num2, num3]

    1. The xyz_file are the path (absolute or relative path) to the xyz file.
       Each line in the xyz file start with a atom name and followed by three
       number (x, y and z coordinates).

    2. num1, num2, num3 are the line number of each atoms in the xyz file.

    3. the center atom in angle calculation is atom2 (num2).
"""

import math
import sys
import os
import argparse


def make_parser():
    parse = argparse.ArgumentParser()
    parse.add_argument('xyz', help='optimized xyz file from qm4d_geo_opt, in \
                       which each line represents one atom, [atom x y z]')
    parse.add_argument('-dist', help='calc distance of two atoms. [line1, line2]',
                       nargs='+', type=int, dest='dist')
    parse.add_argument('-angle', help='calc angle of formed form atoms  A-B-C. \
                       [line_A, line_B, line_C]', nargs='+',type=int, dest='angle')
    return parse.parse_args()

def get_xyz(args):
    """
    return <type: dict> xyz
    example:
    {int(line_num): [1,2,3]}
    line_num count from 1.
    """
    xyz_dict = {}
    f = open(args.xyz, 'r')
    line_count = 1
    for line in f:
        line_split = line.split()
        try:
            xyz_dict[line_count] = [float(i) for i in line_split[1:]]
            line_count += 1
        except:
            continue
    f.close()
    return xyz_dict

def calc_angle(xyz_dict, three_atoms):
    '''
    input: <type: list [int]> three_atoms
    '''
    atomA = three_atoms[0]
    atomB = three_atoms[1]
    atomC = three_atoms[2]
    dist_a =  calc_dist(xyz_dict, [atomB, atomC])
    dist_b =  calc_dist(xyz_dict, [atomA, atomC])
    dist_c =  calc_dist(xyz_dict, [atomA, atomB])
    cosB = (math.pow(dist_c,2) + math.pow(dist_a,2) -math.pow(dist_b,2))/(2*dist_a*dist_c)
    angle = math.acos(cosB)/math.pi *180
    if angle > 180:
        angle = 360 - angle
    return angle

def calc_dist(xyz_dict, two_atoms):
    '''
    input: <type: list [int]> two_atoms
    '''
    atom1 = xyz_dict[two_atoms[0]]
    atom2 = xyz_dict[two_atoms[1]]
    SUM = 0
    for i in range(3):
        SUM += math.pow(atom1[i]-atom2[i], 2)
    return math.sqrt(SUM)

def main():
    args = make_parser()
    args.xyz = os.path.abspath(args.xyz)
    if not (args.dist != None or args.angle != None):
        print("Terminated: please specify what you want to calc, distance or angle")
        sys.exit()
    xyz_dict = get_xyz(args)
    if args.dist != None:
        if len(args.dist) != 2:
            print('Terminated: 2 atoms are needed for distance calc.')
            sys.exit()
        print('distance: ', calc_dist(xyz_dict, args.dist))
    if args.angle != None:
        if len(args.angle) != 3:
            print('Terminated: 3 atoms are needed for angle calc.')
            sys.exit()
        print('angle: ', calc_angle(xyz_dict, args.angle))


if __name__ == '__main__':
    main()
