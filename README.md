# KanbanForBerlinHousing

## Links
- https://seatable.github.io/seatable-scripts/python/
- https://www.w3schools.com/sql/default.asp
- https://pypi.org/project/seatable-api/
- https://medium.datadriveninvestor.com/how-to-build-email-marketing-automation-tool-using-seatable-50347b95d344
- https://github.com/seatable/seatable-scripts/tree/master/examples/python


## Setup of your machine
- Open your cmd/Eingabeaufforderung
- Install python (Version >3.5 required)
    - Windows: Run ```winget install -e --id Python.Python.3``` in your cmd
    - Or download it here https://www.python.org/downloads/
    - Run following commands to install all needed python packages
        - ```pip install seatable-api```
        - ```pip install request```
        - ```pip install socketIO-client-nexus```
- Install Git
    - Windows: Run command ```winget install -e --id Git.Git```
    - Or download it here https://git-scm.com/
    - Run command ```git lfs install``` in your cmd
    - Recommendation: Use Sourcetree for working with git. Especially when you are not familiar with git. This is tool with a graphic user interface including diff views and more. https://www.sourcetreeapp.com/. There is no need of dealing cmd commands and is providing a better overview. 
- Install one of these IDE
    - PyCharm ```winget install -e --id JetBrains.PyCharm.Community``` or https://www.jetbrains.com/pycharm/download/#section=windows
    - Visual Code https://code.visualstudio.com/
    - or other

### Working with git
- Links to dive in
    - https://git-scm.com/
    - There many quick tutorials in Youtube
    - This is useful overview to understand basic git commands ![](https://pbs.twimg.com/media/EKw-jzoUYAA-9WS.jpg)
- Steps to work with git on your machine
    - Open your cmd
    - Run ```cd <Path to your Target Dir```
    - Run ```git clone https://github.com/misterrioes/KanbanForBerlinHousing.git```
    - Open sourcetree and navigate to your target dir
    - Press Fetch for updates from remote (Online)
    - Press Pull to get branch updates from remote to your local workspace
    - Stage your changed files and then press commit to save your changes locally. Recommended to do this regularly.
    - Press push if you want to share your changes with other users

### Scripting with Seatable API
#### Getting started with the Script Template
- Open your IDE
- Open the directory of your local repo
- Make a copy of utils/DummyScript.py and move it to a fitting directory in the repo
  - This Dummy Script provides you a working script with a Library/Wrapper. This library makes our scripting easier, less redundant and reduce debugging. 
    It also helps to react easier to changes of table, column and enums definitions. Those have to be hardcoded in every line otherwise. 
    Please, read also the comments of the DebugMode Class to understand the usage. Unfortunately, SeaTable requires different variable declarations and intializations, if you are working in the cloud or locally. The Workaround is the introduced DebugMode to make it easier for coders that are not so deep in Python.
  - Why are all classes and functions in a super large single file? 
     > The seatable cloud doesn't support the import of other files even when they are all imported. 
    
#### Dealing with the API Token
- Go to the Seatable cloud and log in
- Navigate to your base
- Click on the ```</>``` Button next to the plugins button
- Import utils/getAPIToken.py and utils/sendnewrow4debug.py
- Run getApiToken() and copy the token to your clipboard
- Go back to your IDE
- Copy the token into initStaticBase() and initSocketIOBase(). This has to updated every 2-3 of hours. :(
- 
### Scripting From Template to Cloud Usage
- Your task logic shall be added to the run()function (very much at the bottom of file). Placeholder/Example Code can be removed here :) 
> Please try to modify code in this section only. Extensions of the library are welcome, if they are reused multiple times in other scripts.
- Push your changes to the repo when your script is running without bugs.
- Go again to ```</>``` Button and import your script
- Double click on the script and set the correct debug mode depending if your script is triggerd manually (e.g. buttons or similar) or triggered by automatization
- Now you can link it to the intended trigger
    - For Automated Scripts, use the 'Automation Rules' in the menu next to the little bell in the upper right corner. Usage is very straightforward.
    - For Manual Trigger, I recommend to add a Button column and link the button the script. Configuration is also straightforward.
- Test your script in the cloud by operating the needed triggers (update colum, adding new lines by running sendnewrow4debug.py, ect). I recommend to add many print() to your code for debugging because there are no breaking points
- For Loggings, open the script menu (...) in the ```</>``` view and open Script logs. Then select 'details' of the latest script executions

That's it. Feel free to extend this readme and/or the library. :) Cheers!
