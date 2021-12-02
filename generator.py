from code.util.utils import generate_benchmarks
import argparse


#Call example
#python generator.py -v 5 6 7 8 9 10 11 12 13 14 15 16 --densities 2 3 4 5 -k 3 -e 10 --seed 1

parser = argparse.ArgumentParser(description='SAT generator')
parser.add_argument('-v','--variables', nargs='+', help='A list with the number of variables in the SAT problems', required=True)
parser.add_argument('-k','--ksat', nargs='+', help='A list with the number of variables per clause in the SAT problems', required=True)
parser.add_argument('-d','--densities', nargs='+', help='A list with the densities in the SAT problems', required=True)
parser.add_argument('-e','--examples', help='The number of SAT problems per case', required=True)
parser.add_argument('-s','--seed', help='Seed for the random generator', required=False)
parser.add_argument('-p','--path', help='Path for the benchmark folder', required=False)
args = vars(parser.parse_args())

num_variables = [int(v) for v in args['variables']]
k_sat = [int(k) for k in args['ksat']]
densities = [int(d) for d in args['densities']]

    
if 'path' in args.keys():
    if 'examples' in args.keys():
        if 'seed' in args.keys():
            generate_benchmarks(num_variables=num_variables, k_sat=k_sat, densities=densities, path=args['path'], examples=int(args['examples']), seed=int(args['seed']))
        else:
            generate_benchmarks(num_variables=num_variables, k_sat=k_sat, densities=densities, path=args['path'], examples=int(args['examples']))
else:
    if 'examples' in args.keys():
        if 'seed' in args.keys():
            generate_benchmarks(num_variables=num_variables, k_sat=k_sat, densities=densities, examples=int(args['examples']), seed=int(args['seed']))
        else:
            generate_benchmarks(num_variables=num_variables, k_sat=k_sat, densities=densities, examples=int(args['examples']))