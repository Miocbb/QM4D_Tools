#!/usr/bin/python
import source.sub_func_support as sf_support
import source.sub_func_main as sf_main

def main():
    # get the parser arguments
    args = sf_main.Parser()
    # check position args validity
    sf_support.check_position_args(args)
    # init args
    sf_support.init_args_f_name(args)
    sf_support.init_args_slurm_val(args)
    sf_support.init_optional_args(args)
    # get total system elec_num
    elec_num = sf_support.count_elec_num(args)
    # auto set some args
    sf_support.auto_set_mem(args, elec_num) # auto_set arg[mem]
    sf_support.auto_set_mult(args, elec_num) # auto_set arg[mult]
    # Check if all the args are valid
    sf_support.check_optional_arg(args)
    # Start writing the input file
    args._func(args)




if __name__ == "__main__":
    main()
