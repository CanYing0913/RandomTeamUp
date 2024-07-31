from src.GUI import App


def main():
    app = App()
    try:
        app.gui()
    except Exception as e:
        app.logger.error(f"Exception: {e}")
        pass


if __name__ == '__main__':
    main()
