This is a guide on how to use the project
# Step 1: Install tkinter for python3

## Windows

Tkinter is included with Python on Windows, so you don't need to install it separately.

## macOS

Tkinter is pre-installed on macOS, so you don't need to install it separately.

## Linux

To install **tkinter** on Linux, open a terminal and use the package manager specific to your distribution:
(NOTE: We've only tested on Windows and Ubuntu.)
### Debian/Ubuntu
```shell
sudo apt-get install python3-tk
```
### Fedora
```shell
sudo dnf install python3-tkinter
```
### Arch Linux
```shell
sudo pacman -S tk
```
Please consult your distribution's documentation if you're using a different Linux distribution.

# Step 2: Installing required packages for python3

To install the packages specified in the requirements.txt file, you can use **pip**, the package installer for Python.

Open a terminal and navigate to the directory where the requirements.txt file is located.
Windows/macOS/Linux.
(You may need to enter a **virtual environment** if the operating system throws an error)

Run the following command:
```shell
pip install -r requirements.txt
```
This command will read the requirements.txt file and install all the packages listed in it. Make sure you have a working internet connection for this step.

Once the installation is complete, you will have all the required packages installed and can proceed with using your application.

# Step 3: Run the MainGame.py naively
```shell
python MainGame.py 1000 250
```
The arguments $(1000, 250)$ passed to MainGame is $(frame\_interval, step\_cut)$ respectively.

$frame\_interval$ means the AI player will perform a step every $frame\_interval$ milliseconds, which is implemented by tkinter and pass 1000 here helps observe AI's action and understand the logic.

$step\_cut$ means the AI player will perform $planA$ before $step\_cut$ steps, and then change to $planB$ as the game is coming to an end soon.
Here our step_limit is set to 250, so set it to 250 we can observe AI's taking $planA$.

# Step 4: Modify the planss of Agent and Target
