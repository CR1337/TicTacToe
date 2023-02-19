from ui import TerminalUi


def main():
    try:
        TerminalUi().run()
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()
