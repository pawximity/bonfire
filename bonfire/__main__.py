"""
bonfire - a controlled fire for resetting your local Docker environment.

Bonfire removes Docker resources (images, containers, networks, and volumes)
from a local development environment. It can run in destructive mode or in
"smolder" mode, which performs a non-destructive dry run.

Usage:
    bonfire ignite --images --containers
    bonfire ignite --all --smolder
"""
import argparse

from bonfire.core import process_args
from bonfire.error import BonfireError


def bonfire():
    return r"""
      (  .      )
   )           (              )
         .  '   .   '  .  '  .
  (    , )       (.   )  (   ',    )
   .' ) ( . )    ,  ( ,     )   ( .
)_ . , ( .   ) ( )   ,. ) ( . )  ( .
"""


def main():
    print(bonfire())
    parser = arg_parser()
    args = parser.parse_args()
    try:
        resource_metrics = args.func(args)
        print("\n[*] The bonfire is over!")
        for resource, count in resource_metrics.items():
            if count > 0:
                print(f"[-] {count} {resource}s burned")
    except BonfireError as e:
        print("[!]", e)
        return 1


def arg_parser():
    parser = argparse.ArgumentParser(
        description=
        "bonfire: a controlled fire for resetting your local docker environment"
    )
    commands_subparser = parser.add_subparsers(title="commands",
                                               dest="command",
                                               required=True)
    ignite_parser = commands_subparser.add_parser("ignite",
                                                  help="start the fire")
    ignite_parser.add_argument(
        "--all",
        action="store_true",
        help="burn everything (images, containers, networks, volumes)")
    ignite_parser.add_argument("--all-images",
                               action="store_true",
                               help="burn all images (not just dangling ones)")
    ignite_parser.add_argument("--images",
                               action="store_true",
                               help="burn dangling images only")
    ignite_parser.add_argument("--containers",
                               action="store_true",
                               help="burn all containers")
    ignite_parser.add_argument(
        "--networks",
        action="store_true",
        help="burn all networks (excluding default: bridge, host, none)")
    ignite_parser.add_argument("--volumes",
                               action="store_true",
                               help="burn all volumes")
    ignite_parser.add_argument("--smolder",
                               action="store_true",
                               help="non destructive dry run")
    ignite_parser.set_defaults(func=process_args)
    return parser


if __name__ == '__main__':
    raise SystemExit(main())