import VerkadaPlugin
import Utils

def main():
    verkada_events = VerkadaPlugin.get_data()

    # print the first entry in our response
    # keeping this in for now as a sanity check
    Utils.pretty_print_json(verkada_events['events'][0])

if __name__ == '__main__':
    main()
