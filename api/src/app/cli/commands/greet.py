def register(subparsers):
    parser = subparsers.add_parser("greet", help="Привітання")
    parser.add_argument("--name", required=True)
    parser.add_argument("--shout", action="store_true")

    def handle(args):
        msg = f"Hello, {args.name}!"
        if args.shout:
            msg = msg.upper()
        print(msg)

    parser.set_defaults(func=handle)
