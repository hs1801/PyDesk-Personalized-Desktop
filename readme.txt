------------------------------------- WELCOME TO PYDESK 2.0 -------------------------------------

INTRODUCTION:

> This is a project designed in Python which provides user a Desktop-like interface

> The app starts with the creation of an ADMIN user of the app.

> There can be multiple users using the app, created at the Login (startup) window of app
	* After user creation, it is mandatory to login any Desk user to save changes
	* Guest user - No Data is saved after logout

> After login, a desk of grid 8x10 is created with some pre-loaded files and apps

> Files can be opened by Double-clicking icon, or via OptionMenu which appears on Right-clicking the file icon.

> Right Side of Desk contains Dock Area having 'Exit', 'Add File', 'Apps', 'MyFiles', 'Settings' buttons respectively

> At Bottom is the Dialog box with 2 side-arrows. These arrows indicate buttons for switching Desks. There can be as many desks as required by the user.
	* New Desk cannot be created before 0th desk or till the current desk is truly empty

> The files on Desk are identified by Desk co-ordinates in the form (desk_no, row_no, col_no)
	* desk_no begins with 0, row_no is from 0 to 7 and col_no from 0 to 9

---------------------------------------------------------------------------------------------------
ADDING A FILE:

> Click on 'Add File' Button in the Dock Area.

> Type-in name and Windows path or Browse for a file using 'Browse' button
	* Filename must be unique from other files on desk and need not to be same as original file (can be an Alias)

> Checking the 'Add File to Desktop' option will create a file reference at Desktop. If not checked, the file gets stored in 'MyFiles' but not on Desktop.
	* Can be later added to Desktop using MyFiles, if required.

> Select DeskFolder option sets the parent desk folder to view in 'MyFiles'. Set to 'Home' or '' by default.

> On saving, if adding to Desktop, the file gets auto-arranged in the grid in the first empty cell moving vertically downward.

---------------------------------------------------------------------------------------------------
MANAGING APPS ON PYDESK:

> On clicking 'Apps' Button in Dock Area, a grid of apps appears.

> Users can add an app by clicking the 'Add App' Button in the grid and filling in App Details.
	* App Location may not take full path of app, if already added to WINDOWS PATH
	* Adding app just creates App reference, to have it work, click on the created app icon to enter APP Setting

> Users can modify any app by clicking the respective app icon.

> On entering the APP Setting, users can manage WINDOWS CMD commands to run the app, modify or delete the app from PyDesk, and manage app extensions.

> APP commands can be run by clicking on the command while FILE commands can ONLY run with action on a file.

> Users can manage extensions supported by APP. Extensions are MANDATORY to be entered in the form of list.

> ADDING A COMMAND: 
	To add a command, type the CMD Command for the action to be performed, with app_name replaced with <app> and file_name replaced with <file>
	For eg: To open a file in notepad CMD Command is: notepad filename.txt
		Therefore text entered in Command block : <app> <file>

> Command options for some of common apps are listed in the text file 'command_line_options.txt'

> Command options can be viewed by right-clicking any command. There user can delete command, or set a command as default (file commands)

---------------------------------------------------------------------------------------------------
CHANGE USER SETTINGS:

> Click on 'Settings' Button in Dock Area.

> Click on any Setting value to modify.

> User can also Reset the Desk or even the Terminate the User 

---------------------------------------------------------------------------------------------------
MY FILES:

> On clicking 'MyFiles' Button in Dock Area, an hierarchical tree of files and folders appears.

> Every file and folder open by Double-clicking on them. By Right-clicking, users can find different options for them

> Users can rename file, delete file, add/remove file from Desk 
	* Folders can also be renamed and deleted

> In the Search box at the bottom, users can search for files by their filenames or properties.
	* Only files can be searched, not folders

---------------------------------------------------------------------------------------------------
# COOL THINGS TO TRY :

> MOVE MODE: To move a file on Desktop to a different location, right click the file and select move. Select the cell where you want the file to be moved. (on any desk no.)
	* In move mode, you cannot perform any File or Dock operations

> CREATING NEW FOLDERS: While adding a file, you can select any of the folders from Drop-Down and add the new folder name separated by '/'. Users can do the same while renaming a folder in 'My Files'
	For eg. if creating new folder at 'Home' or '', folder location must be '/folder_name'
			
> Try Glitching Desk no. by adding files 2 alternate desks, and then making the middle one truly empty by Deleting, Removing, or Moving file.

> MULTI - THEME: Try changing theme background in Settings window.

> Try crashing the code, by deleting the default file command in any app in 'Apps' window

> MULTI - USER: Add more than 10 users to challenge space for user icons in 'Login Area'

> SORT MY FILES: In My Files, click on any column heading to sort files accordingly

> OPEN WITH: In right click menu of any file, select 'Open With' and choose any app. If you want the App to add the extension in supported extensions, click 'YES' on pop-up message-box and see changes.

---------------------------------------------------------------------------------------------------
CREDITS:

Development of Project: Harshit Singhal, Student

Special Thanks: Archana ma’am, Subject Teacher
		Bhagat Singh, Classmate

References:    Basic- Python course (CBSE)
		Advanced (Tkinter, OS modules)- YouTube (learning),
 StackOverflow (queries), 
 GeeksforGeeks and EFFBOT (Tkinter Guide)

------------------------------------ THANKS FOR CHOOSING PYDESK ------------------------------------
