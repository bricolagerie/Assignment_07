#------------------------------------------#
# Title: CDInventory.py
# Desc: Assignment 07 - Working with classes and functions.
# Change Log: (Who, When, What)
# BAnson, 2020-Aug-16, Created File for Assignment 06
# BAnson, 2020-Aug-16, moved write to file code to write_file function
#   Added try-except block to create new file if none exists
#   Cleaned up formatting in I/O presentation
#   Added data processing functions add_data and del_id
#   Added IO functions to collect user inputs of new_id, new_title, new_artist
# BAnson, 2020-Aug-18, removed calls to IO class from DataProcessor class in add_data()
#   Consolidated 3 user input IO functions into 1 get_data()
#   Added:
#       Review of entered data and y/n choice to add to table
#       "are you sure?" to exit sequence
# DKlos, 2020-Aug-21, Removed dependence on global variables.
# BAnson, 2020-Aug-25, resaved for Assignment 07
# BAnson, 2020-Aug-26, renamed add_data args to be distinct from program variables; 
#       Updated docstrings.
#       Added error handling to add_data(), read_file(), and get_data()
#       Recreated read_file() and write_file() using pickling
#------------------------------------------#

# TODid: import pickle
import pickle

# -- DATA -------------------------------------------------------------------- #

strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
# TODid: Create new binary file variable for data storage
binFileName = 'CDInventory.dat'  # binary data storage file
objFile = None  # file object



# -- PROCESSING FUNCTIONS ---------------------------------------------------- #

class DataProcessor:
    
    @staticmethod
    def add_data(ID, title, artist, table):
        """Appends Inventory with values assigned to ID, title, and artist
        
        Args:
            ID (string) = user input ID
            title (string) = user input Title
            artist (string) = user input Artist
            table of dicts = user designated table to store inventory
            
        Returns:
            Integer version of ID (intID)
            A dictionary row (dictRow) containing intID, title, artist
            
        """
        # TODid: added error handling for type casting
        # In the context of this script this is redundant because this is already
        #   checked in the get_data() function, but the intention is to make
        #   this function self-contained
        try:
            intID = int(ID)
            dicRow = {'ID': intID, 'Title': title, 'Artist': artist}
            table.append(dicRow)
        except ValueError as e:
            print('That ID is not an integer!')
            print('Build in error info:')
            print(type(e), e, e.__doc__, sep= '\n')

        
    @staticmethod
    def del_id(id_to_delete, table):
        """Deletes CD inventory item based on ID
        
        Args:
            id_to_delete = user input ID
            table of dicts = user designated table from which to delete row
            
        Returns:
            None
            
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == id_to_delete:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')


class FileProcessor:
    """Processing the data to and from text file"""

    # TODid: Create read_file to read from binary file
    @staticmethod
    def read_file(file_name):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from

        Returns:
            table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime
        """
        
        # TODid: Add error handling in case file doesn't exist
        try: 
            with open(file_name, 'rb') as fileObj:
                table = pickle.load(fileObj)
                print('File read complete. Load data to populate table.')
            return table
        except FileNotFoundError as e:
            print('This file does not exist!')
            print('Build in error info:')
            print(type(e), e, e.__doc__, sep= '\n')
            print('\nAdd data and save to create file.')


    # TODid: Create write_file function to write to binary file       
    @staticmethod
    def write_file(table, file_name):
        """Writes data in memory table to a binary file (or creates binary text file if none exists
        
        Args:
            file_name = name of the file to open and write data to (or create)
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
        
        Returns:
            Binary file containing data of current table in memory
        """
        with open(file_name, 'wb') as fileObj:
            pickle.dump(table, fileObj)


# -- PRESENTATION (Input/Output) FUNCTIONS ----------------------------------- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('\nMenu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selectioni

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
            
        """
        print('\n======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by: {})'.format(*row.values()))
        print('======================================')

    # added I/O functions:
    
    @staticmethod
    def get_data():
        """Collects three pieces of data from user: ID, title, and artist
        
        Args:
            None
            
        Returns:
            Tuple containing values corresponding to ID (strID), title (strTitle), and artist (strArtist)
            
        """
         # TODid: Add error handling to make sure entry can be converted to integer       
        while True:
            strID = input('Enter ID: ').strip()
            try:
                intID = int(strID)
                break
            except ValueError as e:
                print('That ID is not an integer!')
                print('Build in error info:')
                print(type(e), e, e.__doc__, sep= '\n')
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        tplUserData = (strID, strTitle, strArtist)
        return tplUserData

        
# -- MAIN PROGRAM ------------------------------------------------------------ #

# 1. When program starts, read in the currently saved Inventory, or create empty file
# TODid: change file name variable to binFileName
try:
    FileProcessor.read_file(binFileName)

except:
    print('\nUse \'a\' to add new data to the table and \'s\' to save and create a new file.')


# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection 
    # 3.1 process exit first
    if strChoice == 'x':
        choice = input('Are you sure you want to exit? [y/n]: ') # prevent exiting accidentally
        if choice.lower() == 'y':
            break
        else:
            continue

    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            lstTbl.clear()
            print('reloading...')
            # TODid: change strFileName to binFileName
            lstTbl = FileProcessor.read_file(binFileName)
            if lstTbl != None:
                IO.show_inventory(lstTbl)
            else:
                lstTbl = []
                IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        # Moved IO code into function
        tplUserData = IO.get_data()
        # Review entry
        print('\nYou entered: ', tplUserData)
        choice = input('Continue to add data to table? [y/n]: ')
        if choice.lower() == 'y':
            strID, strTitle, strArtist = tplUserData
            # 3.3.2 Add item to the table
            # Need to pass lstTbl to the function
            # DataProcessor.add_data(strID, strTitle, strArtist)
            DataProcessor.add_data(strID, strTitle, strArtist, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            print('Data not added to table.')
        continue  # start loop back at top.
    
    # 3.4 process display current inventory
    elif strChoice == 'i':
        if lstTbl:
            IO.show_inventory(lstTbl)
        else:
            print('Inventory is empty. Use \'l\' to load existing inventory or \'a\' to add CD to new inventory.')
        continue  # start loop back at top.
    
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        # 3.5.2 search thru table and delete CD
        # Moved processing code into function
        # Need to pass in id to delete and table to delete from.
        # DataProcessor.del_id()
        DataProcessor.del_id(intIDDel, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            # TODid: Change strFileName to binFileName
            FileProcessor.write_file(lstTbl, binFileName) # function call replaces previous code
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')






