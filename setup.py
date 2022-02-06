import os
import os.path
import subprocess

def split_str_into_words(str):
    return str.split()

def run_cmd(command):
    try:
        subprocess.run(split_str_into_words(command))
    except:
        print(f'[{colored_string("could not run command", "red")}]')

def run_under_venv(command):
    python_bin = 'venv\Scripts\\'
    subprocess.run(split_str_into_words(python_bin + command))

def colored_string(string, color):
    colors = {"red": "\u001b[31m",
              "green": "\u001b[32m",
              "yellow": "\u001b[33m",
              "blue": "\u001b[34m",
              "purple": "\u001b[35m",
              "cyan": "\u001b[36m",
              "reset": "\u001b[0m"
              }
    if color in colors:
        return f'{colors[color]}{string}{colors["reset"]}'
    else:
        return string

def create_venv():
    try:
        import virtualenv
    except:
        print(colored_string("WARNING: virtualenv is not installed", "yellow"))
        x = None
        while (x != 'y' and x != 'n' and x != 'Y' and x != 'N'):
            x = input(colored_string("Do you want to install it?(y/n) ", "cyan"))

        if x == 'y' or x == 'Y':
            run_cmd("pip install virtualenv")
        else:
            return

    try:
        run_cmd("virtualenv venv")
    except:
        print(colored_string("error occurred when creating the virtual environment", "red"))

    print(f'[{colored_string("virtual environment created successfully", "green")}]')

def install_req():
    if os.path.isfile("requirements.txt"):
        try:
            run_under_venv("pip install -r requirements.txt")
        except:
            print(f'[{colored_string("failed to install the modules from requirements.txt", "red")}')
    else:
        print(f'[{colored_string("requirements.txt does not exist", "red")}]')


if __name__ == '__main__':
    create_venv()
    install_req()