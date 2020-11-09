from references import addref, analyse, indices, updaterefs
import sys
import argparse

def main():
  # create parser and subparsers
  parser = argparse.ArgumentParser(description="Manage references.")
  subparsers = parser.add_subparsers(description="command", required=True)

  # addref
  parser_addref = subparsers.add_parser("add-ref",
    help="Add reference through interactive interface.")
  parser_addref.set_defaults(func=addref.addref)

  # analyse
  parser_analyse = subparsers.add_parser("analyse",
    help="Analyse references and referents data.\
      By default, analyses everything (names, titles, episodes).\
      Add -h to see more options.",
    description="Analyse references and referents data.\
      By default, analyses everything.\
      Add -t or --type followed by one of the options to see analysis of only that thing.")
  parser_analyse.add_argument("--type", "-t",
    choices=["names", "titles", "seasons", "episodes", "writers"],
    help="analyse only one type")
  parser_analyse.set_defaults(func=analyse.analyse)

  # indices
  parser_indices = subparsers.add_parser("indices",
    help="Checks references file for mismatches with transcripts (audit), \
      identifies correct indices and shifts indices (fix), and helps with manual indices fixes (find). \
      Add -h to see more options.")
  indices_subparsers = parser_indices.add_subparsers(description="command", required=True)
  # audit
  parser_audit = indices_subparsers.add_parser("audit",
    help="List mismatches between references and transcripts for given episodes. \
      Add -h to see more options.",
    description="List mismatches between references and transcripts for given episodes. \
      If no epCode is given, all episodes will be checked. \
      If --all is not given, only the first result will be shown.")
  parser_audit.add_argument("epCode",
    help="episode code, e.g. s01e01 for season 1 episode 1",
    type=indices.epCodeType,
    nargs="*")
  parser_audit.add_argument("-a", "--all",
    help="show all results",
    action="store_true")
  parser_audit.set_defaults(func=indices.audit)
  # fix
  parser_fix = indices_subparsers.add_parser("fix",
    help="Fix first mismatch found. Interactive interface to confirm indices shifts.\
      Add -h to see more options.",
    description="Fix first mismatch found. Interactive interface to confirm indices shifts.\
      Insert the epCodes for as many episodes as desired. If no epCode is given, all episodes will be checked.\
      Add the --run or -r flag to run automatically through all mismatches.")
  parser_fix.add_argument("epCode",
    help="episode code, e.g. s01e01 for season 1 episode 1",
    type=indices.epCodeType,
    nargs="*")
  parser_fix.add_argument("-r", "--run",
    help="Run automatically through all mismatches.",
    action="store_true")
  parser_fix.set_defaults(func=indices.fix)
  # find
  parser_find = indices_subparsers.add_parser("find",
    help="Get list of indices for all matches of a search string in an episode. \
      Helpful for a manual indices fix.\
      Add -h to see more options.",
    description="Get list of indices for all matches of a search string in an episode. \
      Helpful for a manual indices fix.")
  parser_find.add_argument("epCode",
    help="episode code, e.g. s01e01 for season 1 episode 1",
    type=indices.epCodeType)
  parser_find.add_argument("search",
    help="search string in quotes")
  parser_find.set_defaults(func=indices.find)

  # updaterefs
  parser_referents = subparsers.add_parser("update-refs",
    help="Generate referents file from references file.")
  parser_referents.set_defaults(func=updaterefs.updaterefs)

  # parse arguments and execute functions
  args = parser.parse_args()
  args.func(args)
  
if __name__ == "__main__":
  main()