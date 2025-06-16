###[PyZeroTrustUI]###
## Zerofish0        #
## version : 1.0    #
#####################
# Importations
import sys
import colorama

# Main class
class PyZeroTrustUI :
    def __init__(self,replacers_dict : dict = dict()):
        # Defining constants
        self.RUNNING_TASK = colorama.Fore.YELLOW
        self.PROMPT = colorama.Fore.CYAN
        self.OWN = colorama.Fore.BLUE
        self.PEER = colorama.Fore.MAGENTA
        self.ERROR = colorama.Fore.RED + colorama.Style.BRIGHT
        self.SUCCESS = colorama.Fore.GREEN + colorama.Style.BRIGHT
        self.reset = colorama.Style.RESET_ALL

        self.replacers_dict = replacers_dict

    def ui_input(self, prompt : str = str(), default = "") :
        data = str(input(self.PROMPT + prompt + self.reset))
        if data == "":
            data = default
        for rep in self.replacers_dict.keys():
            data = data.replace(rep,self.replacers_dict[rep])
        return data

    def running(self, prompt : str) :
        print(self.RUNNING_TASK + prompt + self.reset)

    def ownMessage(self, message : str) :
        print(self.OWN + message + self.reset)

    def peerMessage(self, message : str, peer_name : str, instance_name : str) :
        # Efface la ligne d'input actuelle
        sys.stdout.write("\r" + " " * 80 + "\r")
        print(self.PEER + f"{peer_name} : {message}")
        # Réaffiche le prompt d'input
        sys.stdout.write(self.OWN + f"{instance_name} (you): " + self.reset)
        sys.stdout.flush()

    def error(self, message : str) :
        print(self.ERROR + message + self.reset)

    def success(self, message : str) :
        print(self.SUCCESS + message + self.reset)

    def classic(self, text : str) :
        print(text + self.reset)
