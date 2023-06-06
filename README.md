This is a guide on how to use the project
# Step 1: Install tkinter for python3
Tkinter is the standard Python interface for creating graphical user interfaces (GUIs). It provides a way to create windows, dialogs, buttons, textboxes, and other GUI elements in a platform-independent manner. 

Tkinter may be not included with Python installations on some platforms, here are some instructions for
installing it manually.

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

# Step 2: Install required packages for python3

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

# Step 3: Run the *MainGame.py* naively

## Introduction
Our *Agent* is colored in red so we sometimes call it *red*, *Hero Target* too.  
And *Target*, colored in blue, also called *blue*, *Enemy Target* similarly. 
```shell
python MainGame.py 1000 251
```
The arguments `(1000, 251)` passed to MainGame is `(frame_interval, step_cut)` respectively.

`frame_interval` means the  player will perform a step every `frame_interval` milliseconds, which is implemented by tkinter and pass 1000 here helps observe their actions and understand the logic.  
<sub>
When passing `0` to `frame_interval`, the game will disable GUI to speed up progress, you can make use of this feature when collecting data and evaluate algorithms. See $Step5$ for more information.</sub>

`step_cut` means the  player will perform $planA$ before `step_cut` steps, and then change to $planB$ as the game is coming to an end soon.
Here our step_limit is set to 250, so set it to 251 we can observe them taking $planA$.

# Step 4: Modify the plans of Agent and Target then watch them fighting
For better view and clear logic, we implement Agent and Target seperately.  
Go to *Agent.py* and check **make_action(self, end, home,game_coord, target_bullets)**，and   
**make_action_less_time_left(self, end, home,game_coord, target_bullets)** to understand the logic more clearly.  
Agent will perform **make_action()** at first period, aka when `0` ≤ `step_count` ≤ `step_cut`,  
and then perform **make_action_less_time_left()** at second period when `step_cut` ≤ `step_count` ≤ `step_limit`.

Similarly, you can change Target's plan in *Target.py*.
Then follow $Step3$ to run the *MainGame.py* and you can watch them fighting.
# Step 5: Use CollectScores to collect data and evaluate different algorithms
As you know in $Step3$, when collecting scores we disable the GUI to avoid some issues and speed up the process.
Go to *CollectScores.py* and check our single thread test collector with GUI and multi thread collector without GUI. 
The arguments passed to them is `(num_runs,num_cut)`, increase `num_runs` to run more times on a certain `num_cut` so that you can get a smaller stdev. `num_cut` is used to spilt the game period, when will the agents change its plan. Please pass a `num_cut` which is smaller than `step_limit` to make it meaningful.

In `__main__()`, you can call `single_thread_with_gui(20,20)` to visually check each game process or call `multi_plot()` to collect data and draw graphs using matplotlib. Note that this may take a long time.
# Some more options if you like
Our framework is well designed and most of the parameters are supported for modification and customization.
For example you can change the game grid size and cell size in `MainGame::__main__()`, change the wall probablility in `MainGame::__init__()`, you can write more actions and return it in `Agent::make_action()` to test your own way, set any cell to *6* to make it the home of agent. Do consider bugs if you change the game state. For any other details, just check our source code and take your modification as you like.

# TODO
We initially implemented the bullet killing logic but due to time we have to simplify it. Now it's disabled just visually but actually work in backgroud and won't kill the agents. If you are interested just uncomment related parts and enable the canvas drawing for bulles.