# Yggdrasil
##### Concept
Yggdrasil is a package meant to facilitate the distribution of scripts into production through the definition of apps.
Each app is defined as:
- Name: Name of the application, as will be called from command lined
- Project directory: Location of the project containing the base code for the app
- Entry point: .bat or .py file that will be run when calling the app from cmd
- Virtual environment: environment to activate for running the app

Once set up, yggdrasil allows the user to run his personal projects from command line, giving a quick way to access all his/her project or to share them.


##### Getting started
Before using the tool to create apps, yggdrasil needs an initial set up.
First, install the package:
```commandline
pip install git+https://www.github.com/mx-personal/yggdrasil.git
```
*(The package is not currently available on pipy)*

Then, create the base folder structure to install yggdrasil into:
```python
import yggdrasil as ygg
ygg.plant_seed()
```
If a path is set up as environment variable (*YGGDRASIL_ROOT*), the folders structure will be created there.
If not, it will be created under the user's *Documents* folder.
To make each app easily callable from the command line, it's also recommended to add the 
*Yggdrasil\Scripts* full path to the *Path* environment variable.

That's it, you're ready to create your first application!

##### Create an application
The configuration of an application is done through the *settings.txt* file (under *settings* folder).
In there, please define the configuration of your app:
- name: Name that will be called from the command line
- py_version: Version of python that will be used to run create the virtual environment
(the version needs to be previously installed and available already)
- venv: Name of the virtual environment (several apps can share a single virtual environment, which will be identified by name).
Each project needs to have a *requirements.txt* file stored at its root.
- directory: Full path to the root directory of the project. The tool doesn't need to be under the *tools* folder to work, however the *tool* folder can be used as
your base 'in production' tools folder if the user wishes (e.g. if installing tool from github)
- entry_point: Entry point that will be launched from the command line. The script needs to be under the project directory, in relative path.
When done, the *settings* file should look like this (on a *spam* application):

| name         | py_version | venv    | directory               | entry_point       |
|--------------|------------|---------|-------------------------|-------------------|
|spam          |3.9         |venv_spam|Path\to\Project\Directory|spam_entry_point.py|

Once this is done, open python:
```python
import yggdrasil as ygg
ygg.create("spam")
```
This will create a virtual environment with dependencies as per *requirements.txt*, and a batch file (under *scripts*)
to simplify running the app from the command line.

And you're done! You should now be able to open a command line and simply write what's below to run your *spam* app:
```commandline
spam
```

##### Others
- If the app creation doesn't seem to work for some reason, you can also pass *debug=True* to the *create* function to see the full log during app creation
- Yggdrasil also presents a *remove* and *update* functions, taking the same arguments as *create*


Any feedback welcome!