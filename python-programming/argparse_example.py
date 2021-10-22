import argparse

import os
import sys

# Create the parser
my_parser = argparse.ArgumentParser(description='List the content of a folder')

# Add the arguments
my_parser.add_argument('Path',
                       metavar='path', # only used for help messages
                       action='store',
                       type=str,
                       help='the path to list',
                       nargs=1)

# optional argument by adding -l
my_parser.add_argument('-l',
                       '--long',
                       action='store',
                       help='enable the long listing format',
                       nargs=1,
                       default=50,
                       choices=[50,100],
                       type=int,
                       required=False)

# Execute the parse_args() method
args = my_parser.parse_args()

print(args.Path) 
print(args.long)