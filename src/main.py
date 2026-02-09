from dotenv import load_dotenv
import Application

def main():
    load_dotenv(override=False)
    Application.init()

if __name__ == '__main__':
    main()
