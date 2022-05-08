import yggdrasil as ygg
import argparse


def foobar():
    map_functions = {
        "create": ygg.create,
        "remove": ygg.remove,
        "show": ygg.show,
    }

    parser = argparse.ArgumentParser(prog="yggdrasil")
    subparsers = parser.add_subparsers(dest="cmd")
    parser_create = subparsers.add_parser("create", help="Create an application")
    parser_create.add_argument("-d", "--debug", action="store_true", help="Show debug log during execution")
    parser_create.add_argument("-f", "--force-regen", action="store_true", dest="force_regen", help="Forces regeneration of the app if already exists")
    parser_create.add_argument("-a", "--apps", nargs='*', default='*', help="(Optional) list of apps to create")

    parser_show = subparsers.add_parser("show", help="Show list of existing applications")
    parser_show.add_argument("-a", "--apps", default='*', nargs='*')
    # args = parser.parse_args(['create', '-d', '-a', 'tool_git'])
    args = parser.parse_args(['show'])

    ygg.run(**vars(args))

if __name__ == "__main__":
    foobar()