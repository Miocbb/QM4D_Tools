#!/usr/bin/python
import argparse
import sub_claims
import sub_func_inp as sfi

def main():
    # Cerate top-level parser
    parser = argparse.ArgumentParser(description=
                """Use *.xyz file to wirte the input
                files needed for QM4D calculations""")
    # Create sub-level parser for command {dft, losc, hf}
    subparser = parser.add_subparsers(help= "Calculation method choices")
    
    # Create parser for "dft" command
    parser_dft = subparser.add_parser('dft',
                    help='DFT calculation with standard dfa',
                    parents=[sub_claims.parent_parser])
    parser_dft.add_argument('-dfa', default = 'b3lyp',
                    help='Default=b3lyp')
    parser_dft.add_argument('-g09', action='store_true',
                    help='[calculation package: g09]')
    parser_dft.set_defaults(func=sfi.dft_main, method='dft')

    # Create parser for "losc" command
    parser_losc = subparser.add_parser('losc', parents=[sub_claims.parent_parser],
                    help='DFT calculation with LOSC dfa')
    parser_losc.add_argument('-dfa', default = 'b3lyp',
                    help='Default=b3lyp')
    parser_losc.add_argument('-fitbasis', default = 'aug-cc-pVTZ',
                    help='Default=aug-cc-pVTZ')
    parser_losc.add_argument('-window', default = '-30  10',
                    help='Default="-30 10", [set LOSC calculation wimdow]')
    parser_losc.add_argument('-postSCF', default = '1',
                    help='Default=1 [1:POSTSCF  0:SCF]')
    parser_losc.set_defaults(func=sfi.losc_main, method='losc')

    # Create parser for "hf" command
    parser_hf = subparser.add_parser('hf', help='HF calculation',
                    parents=[sub_claims.parent_parser])
    parser_hf.add_argument('-g09', action='store_true',
                    help='[calculation package: g09]')
    parser_hf.set_defaults(func=sfi.hf_main, method='hf')

    args = parser.parse_args()
    # get total system elec_num
    elec_num = sfi.count_elec_num(args)
    sfi.auto_set_mem(args, elec_num) # auto_set arg[mem]
    sfi.auto_set_mult(args, elec_num) # auto_set arg[mult]
    print args
    # Check if all the args are valid
    sfi.check_arg(args)
    # Start writing the input file
    args.func(args)



if __name__ == "__main__":
    main()
