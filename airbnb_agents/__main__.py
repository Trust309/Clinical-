"""Entry point for running the Airbnb Business Agents system."""

import sys


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        from .app import run
        run()
    else:
        from .demo import run_demo
        run_demo()


if __name__ == "__main__":
    main()
