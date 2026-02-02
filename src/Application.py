import CLI
import VerkadaPlugin

def init():
    args = CLI.setup_cli()
    VerkadaPlugin.init(args.verkada_api_key)
