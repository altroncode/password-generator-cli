import argparse


def boolean_type(value: str):
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def create_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(
        prog='password-generator',
        description='Generate passwords and save them to storages',
        epilog="Possible values for --is-digits, --is_note, --is_punctuation, etc.: "
               "true, false, True, False, 1, 0, t, f, T, F, y, n, Y, N"
    )


def configure_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('--length', '-l', type=int, dest='length', nargs='?',
                        help="set the length of the password (default: None)")
    parser.add_argument('--platform', '-p', type=str, dest='platform', nargs='?',
                        help="specify the platform (default: None)")
    parser.add_argument('--emails', '-e', type=str, dest='emails', nargs='*',
                        help="specify one or more email addresses (default: None)")
    parser.add_argument('--login', '-lg', type=str, dest='login', nargs='?',
                        help="set the login (default: None)")
    parser.add_argument('--storages', '-s', type=str, dest='storages', nargs='*',
                        help="specify one or more storages(default: None)")
    parser.add_argument('--password', '-ps', type=str, dest='password', nargs='?',
                        help="set the password (default: None)")
    parser.add_argument('--is_note', '-n', action='store_true', dest='is_note', help="store a note (default: False)")
    parser.add_argument('--is_digits', '-d', type=boolean_type, dest='is_digits',
                        help="use digits in the password (default: None)")
    parser.add_argument('--is_capital_letters', '-cl', type=boolean_type, dest='is_capital_letters',
                        help="use capital letters in the password (default: None)")
    parser.add_argument('--is_small_letters', '-sl', type=boolean_type, dest='is_small_letters',
                        help="use small letters in the password (default: None)")
    parser.add_argument('--is_punctuation', '-pt', type=boolean_type, dest='is_punctuation',
                        help="use punctuation in the password (default: None")


def get_arguments(argument_parser: argparse.ArgumentParser, args: list[str]) -> argparse.Namespace:
    return argument_parser.parse_args(args=args)
