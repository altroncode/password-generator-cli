import argparse


parser = argparse.ArgumentParser(prog='password_generator', description='Generate password')
parser.add_argument('--length', '-l', type=int, dest='length', default=32, nargs='?')
parser.add_argument('--platform', '-p', type=str, dest='platform', default='-', nargs='?')
parser.add_argument('--email', '-e', type=str, dest='email')
parser.add_argument('--username', '-u', type=str, dest='username', default='-', nargs='?')
parser.add_argument('--send', type=str, dest='send', default='telegram', nargs='?')
parser.add_argument('--password', '-ps', type=str, dest='password', nargs='?')
parser.add_argument('--note', '-n', action='store_true', dest='note')
parser.add_argument('--digits_in_password', '-d', type=bool, dest='digits_in_password')
parser.add_argument('--capital_letters_in_password', '-cl', type=bool, dest='capital_letters_in_password')
parser.add_argument('--small_letters_in_password', '-sl', type=bool, dest='small_letters_in_password')
parser.add_argument('--punctuation_in_password', '-pt', type=bool, dest='punctuation_in_password')


def get_arguments(argument_parser: argparse.ArgumentParser, args: list[str]):
    return argument_parser.parse_args(args=args)
