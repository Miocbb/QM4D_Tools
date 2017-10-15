import argparse
#
#parser_parent = argparse.ArgumentParser(add_help=False)
#parser_parent.add_argument('parent', help='parent parse')
#
#
#parser = argparse.ArgumentParser()
#subparsers = parser.add_subparsers(help='commands')
#
## A list command
#list_parser = subparsers.add_parser('list', parents=[parser_parent])
#list_parser.add_argument('dirname', action='store', help='Directory to list')
#
### A create command
##create_parser = subparsers.add_parser('create', help='Create a directory')
##create_parser.add_argument('dirname', action='store', help='New directory to create')
##create_parser.add_argument('--read-only', default=False, action='store_true',
##                                   help='Set permissions to prevent writing to the directory')
##
### A delete command
##delete_parser = subparsers.add_parser('delete', help='Remove a directory')
##delete_parser.add_argument('dirname', action='store', help='The directory to remove')
##delete_parser.add_argument('--recursive', '-r', default=False, action='store_true',
##                                   help='Remove the contents of the directory too')
##
##subsubparser = list_parser.add_subparsers(help='sub parser of list')
##sub_list_parser1 = subsubparser.add_parser('sub_list1')
##sub_list_parser1.add_argument('sub_list1_arg')
##sub_list_parser2 = subsubparser.add_parser('sub_list2')
##sub_list_parser2.add_argument('sub_list2_arg')
#
#print parser.parse_args()


# sub-command functions
def foo(args):
    print args.x * args.y

def bar(args):
    print '((%s))' % args.z

# create the top-level parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# create the parser for the "foo" command
parser_foo = subparsers.add_parser('foo')
parser_foo.add_argument('-x', type=int, default=1)
parser_foo.add_argument('y', type=float)
parser_foo.set_defaults(func=foo)

# create the parser for the "bar" command
parser_bar = subparsers.add_parser('bar')
parser_bar.add_argument('z')
parser_bar.set_defaults(func=bar)

# parse the args and call whatever function was selected
#args = parser.parse_args('foo 1 -x 2'.split())
args = parser.parse_args()
print args
args.func(args)
