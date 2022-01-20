"""This program will select a random name from a list.
The current list will be built from the full list.
You will be able to modify the current or full list.
You will be able to skip a name for a cycle
Created by Michael Tiday, https://github/mtiday/
"""

import random
import os
import time
from datetime import datetime
import jokes_to_choose_from


# Main function
def main_menu():
    """Displays main menu, user chooses action to take."""
    #  Sort, ignoring case, the current and full list if needed
    sort_if_needed()

    # Main Menu below
    while True:
        clear_screen()
        choice_from_main_menu =\
            input("Enter a number between 1-3\n"
                  "1.  View or Run Current List\n"
                  "2.  View or Modify Full List\n"
                  "3.  I want to see a joke!\n"
                  "4.  Close Program\n\n")

        # View or Run Current List
        if choice_from_main_menu == "1":
            current_list()

        # View or Run Full List
        elif choice_from_main_menu == "2":
            full_list()

        # Tell a joke
        elif choice_from_main_menu == "3":
            clear_screen()
            random_joke()

        # Close program
        elif choice_from_main_menu == "4":
            close_program()
        else:
            print("Try again!")
            time.sleep(3)


# Display and work with the current list
def current_list():
    """View the current list of names. Modify or randomly choose a nam
     from the current list."""

    modify_current_list = []
    list_of_names_to_skip = []

    # Load from scrum_list_current.txt file
    with open("scrum_list_current.txt", "r", encoding="utf-8") as\
            scrum_list_current:
        for name in sorted(scrum_list_current, key=str.casefold):
            modify_current_list.append(name.strip())

    while True:
        name_count = 1
        #  If current list is empty, reload from full list

        modify_current_list.sort(key=str.casefold)  # non-case sort
        clear_screen()

        choice_from_menu =\
            input("1. Pick the next SCRUM master!\n"
                  "2. Remove someone from this picking\n"
                  "3. Remove someone from the current list\n"
                  "4. Add someone to the current list\n"
                  "5. Show Current List\n"
                  "6. Reload from the Full List\n"
                  "7. Main Menu\n"
                  "8. Close Program\n\n")

        # Pick the next SCRUM master
        if choice_from_menu == "1":
            new_scrum_master(modify_current_list, list_of_names_to_skip)

        # Remove someone from this picking
        elif choice_from_menu == "2":
            name_to_skip, modify_current_list =\
                remove_name_from_list(modify_current_list, True)

            # List in case there's more than one name to skip
            list_of_names_to_skip.append(name_to_skip)

        # Remove someone from the current list
        elif choice_from_menu == "3":
            modify_current_list = remove_name_from_list(modify_current_list)
            log_data("name_removed_from_list.log",
                     "Above removed from Current List")
            change_current_list_text_file(modify_current_list)

        # Add someone to the current list
        elif choice_from_menu == "4":
            # write_to_disk = copy.deepcopy(modify_current_list)
            modify_current_list = add_name_to_list(modify_current_list)
            log_data("name_added_to_list.log", "Above added to Current List")
            change_current_list_text_file(modify_current_list)

        # Show Current List
        elif choice_from_menu == "5":
            clear_screen()
            for name in modify_current_list:
                print(f"{name_count}. {name}")
                name_count += 1
            print()
            input('Press any key to continue\n')

        # Reload from the Full List
        elif choice_from_menu == "6":
            reload_from_full_list()
            main_menu()

        # Main menu
        elif choice_from_menu == "7":
            main_menu()

        # Close Program
        elif choice_from_menu == "8":
            close_program()

        else:
            print("Try Again!")
            time.sleep(3)


# Display and work with the full list
def full_list():
    """View or modify the full list of names."""

    while True:
        name_count = 1
        list_of_names = []  # Clear list every loop start

        with open("scrum_list_full.txt", "r", encoding="utf-8") as\
                scrum_list_full:
            for name in scrum_list_full:
                list_of_names.append(name.strip())

        clear_screen()

        choice_from_full_list_menu =\
            input("Enter a number between 1 and 5\n"
                  "1.  View Full List\n"
                  "2.  Remove a Name from Full List\n"
                  "3.  Add a Name to Full List\n"
                  "4.  Main Menu\n"
                  "5.  Close Program\n\n")

        # View Full List
        if choice_from_full_list_menu == "1":
            clear_screen()
            for name in list_of_names:
                print(f"{name_count}. {name.strip()}")
                name_count += 1
            print("\n")
            input('Press any key to continue\n')

        # Remove a name from Full List
        elif choice_from_full_list_menu == "2":
            list_of_names = remove_name_from_list(list_of_names)
            log_data("name_removed_from_list.log",
                     "Above removed from Full List")
            change_full_list_text_file(list_of_names)

        # Add a name to Full List
        elif choice_from_full_list_menu == "3":
            list_of_names = add_name_to_list(list_of_names)
            log_data("name_added_to_list.log", "Above added to Full List")
            change_full_list_text_file(list_of_names)

        # Main Menu
        elif choice_from_full_list_menu == "4":
            main_menu()

        # Close program
        elif choice_from_full_list_menu == "5":
            close_program()
        else:
            print("Try Again!")
            time.sleep(3)


# Modify Current List text file
def change_current_list_text_file(modify_current_list):
    """Modify scrum_list_current.txt"""
    clear_screen()
    with open("scrum_list_current.txt", "w", encoding="utf-8") as\
            scrum_list_current:
        for name in sorted(modify_current_list, key=str.casefold):
            # If last name in list no \n
            if name == modify_current_list[-1]:
                scrum_list_current.write(name)
            elif not name.endswith("\n"):
                scrum_list_current.write(name + "\n")
            else:  # Not likely to be used
                scrum_list_current.write(name)


# Modify Full List text file
def change_full_list_text_file(list_of_names):
    """Modify file scrum_list_full.txt"""

    with open("scrum_list_full.txt", "w", encoding="utf-8") as \
            scrum_list_full:
        for name in sorted(list_of_names, key=str.casefold):
            # If last name in list no \n
            if name == list_of_names[-1]:
                scrum_list_full.write(name)
            elif not name.endswith("\n"):
                scrum_list_full.write(name + "\n")
            else:  # Not likely to be used
                scrum_list_full.write(name)


# Removes a name from any list
def remove_name_from_list(list_of_names, temp_removal=False):
    """Function will remove a name from a list"""
    clear_screen()
    while True:
        name_count = 1

        for name in list_of_names:
            print(f"{name_count}. {name.strip()}")
            name_count += 1
        name_to_remove = input('\nEnter a number that corresponds to a name.\n'
                               'Or enter "Q" to return to main menu: ')
        if name_to_remove.casefold() == "q":
            main_menu()

        try:
            if temp_removal:
                # The name_to_remove is the int index of name_to_skip
                log_data("people_skipped.log",
                         list_of_names[int(name_to_remove) - 1])
                list_of_names.pop(int(name_to_remove) - 1)
                if len(list_of_names) == 0:  # Reload if list is empty
                    list_of_names = reload_from_full_list()
                return name_to_remove, list_of_names

            if len(list_of_names) > 1:  # Log if list isn't empty
                log_data("name_removed_from_list.log",
                         list_of_names[int(name_to_remove) - 1])

            list_of_names.pop(int(name_to_remove) - 1)

            if len(list_of_names) == 0:  # Reload if list is empty
                list_of_names = reload_from_full_list()
            return sorted(list_of_names, key=str.casefold)

        except ValueError:
            clear_screen()
            print(f"You didn't enter a number between 1 and "
                  f"{len(list_of_names)} or a \"Q\"")

        except IndexError:
            clear_screen()
            print(f"You didn't enter a number between 1 and "
                  f"{len(list_of_names)} or a \"Q\"")


# Adds a name to any list
def add_name_to_list(list_of_names):
    """"Function will add a name to the list"""
    clear_screen()
    name_count = 1
    while True:
        for name in list_of_names:
            print(f"{name_count}. {name.strip()}")
            name_count += 1

        name_to_add = input('\nEnter new name, First and Last.\n'
                            'Are you sure?,\n'
                            'If not enter "Q" to return to main menu: ')

        # if "Q" or spaces are entered, call main_menu()
        if name_to_add.casefold() == "q" or name_to_add.strip() == "":
            main_menu()

        list_of_names.append(name_to_add)
        log_data("name_added_to_list.log", name_to_add)
        return sorted(list_of_names, key=str.casefold)


# sort .txt list if needed
def sort_if_needed():
    """Sort non-case if needed"""

    # Compare full list with non-case sort of full list
    with open("scrum_list_full.txt", "r", encoding="utf-8") as scum_list_full:
        original_list_full = list(scum_list_full)
        sort_full_if_needed = \
            sorted(original_list_full, key=str.casefold)
    if sort_full_if_needed != original_list_full:
        with open("scrum_list_full.txt", "w", encoding="utf-8") as\
                scrum_list_full:
            for name in sort_full_if_needed:
                if not name.endswith("\n"):
                    scrum_list_full.write(name + "\n")
                else:
                    scrum_list_full.write(name)

    # Compare current list with non-case sort of current list
    with open("scrum_list_current.txt", "r", encoding="utf-8") as\
            scrum_list_current:
        original_list_current = list(scrum_list_current)
        sort_current_if_needed = \
            sorted(original_list_current, key=str.casefold)
    if sort_current_if_needed != original_list_current:
        with open("scrum_list_current.txt", "w", encoding="utf-8") as\
                scrum_list_current:
            for name in sort_current_if_needed:
                scrum_list_current.write(name)


# Mirrors the full list to the current list
def reload_from_full_list():
    """Function will copy the current list from the full list"""
    from_full_to_current = []
    list_to_return = []
    log_data("current_list_reloaded.log",
             "Current List reloaded from Full List")
    # Read from full list
    with open("scrum_list_full.txt", "r", encoding="utf-8") as scrum_list_full:
        for name in sorted(scrum_list_full, key=str.casefold):
            from_full_to_current.append(name)

    # Return to Main Menu if the scrum_list_full.txt file <= 1
    if len(from_full_to_current) <= 1:
        clear_screen()
        input("Please add some names to the full list\n"
              "\n"
              "Press any key to return to the main menu")
        main_menu()

    # Write to current list
    with open("scrum_list_current.txt", "w", encoding="utf-8") as\
            scrum_list_current:
        for name in from_full_to_current:
            scrum_list_current.write(name)

    for name in from_full_to_current:
        list_to_return.append(name.strip())
    return list_to_return


# Displays new SCRUM master, removes from current_list, closes program
def new_scrum_master(list_of_names, list_of_names_to_skip=None):
    """Displays the new scrum master, removes from current_list,
    closes program, or returns to current_list menu"""
    clear_screen()
    name_count = 1
    if len(list_of_names) == 0:
        reload_from_full_list()

    print("Who will be the next SCRUM master?")
    for name in sorted(list_of_names):
        print(f"{name_count}. {name}")
        name_count += 1
    proceed = input('\n"Y"es to proceed: ')

    if proceed.casefold() in ("y", "yes", ):
        clear_screen()
        print("I'll tell you a joke while you wait for me to find "
              "the next SCRUM Master.\n")
        random_joke()  # Tell a random joke

        if len(list_of_names) > 1:
            index = random.randrange(0, len(list_of_names) - 1)
        else:
            index = 0
        chosen_scrum_master = list_of_names[index]
        log_data("scrum_masters.log", chosen_scrum_master)

        countdown = 5
        print("I'll have the name ready in a few seconds:")
        while countdown:
            print(f"Almost there... ({countdown})")
            time.sleep(1)
            countdown -= 1

        print(f"\nCongratulations:\n{chosen_scrum_master}!\n")
        print("You are the next SCRUM MASTER!")
        time.sleep(8)
        list_of_names.pop(index)  # Remove name of SCRUM master

        # If names were skipped this picking
        if list_of_names_to_skip:
            # Add skipped names back to list
            for name in list_of_names_to_skip:
                list_of_names.append(name)
        with open("scrum_list_current.txt", "w", encoding="utf-8") as\
                scrum_list_current:
            for name in sorted(list_of_names):
                scrum_list_current.write(name + "\n")

        close_program()

    # Return list sent if "No" to proceed
    return list_of_names


# Tells a random joke while they are "waiting" on the new SCRUM master
def random_joke():
    """Tell a random joke"""
    jks = jokes_to_choose_from.scrum_chooser_jokes
    index = random.randrange(0, len(jks)-1)

    print("Warning, not everyone likes my jokes, but here goes!\n\n")
    print(jks[index] + "\n\n")
    log_data("jokes_told.log", jks[index])
    time.sleep(2)
    # Pause until user input
    input("Press any key when ready to proceed")
    clear_screen()


def log_data(name_of_log_file, data_to_add):
    """Create or add to log files"""
    complete_name = os.path.join(os.getcwd(), "logs", name_of_log_file)
    complete_entry = str(datetime.now()) + ": " + data_to_add
    with open(complete_name, "a", encoding="utf-8") as log_to_modify:
        log_to_modify.write(complete_entry + "\n")


# Clears the screen
def clear_screen():
    """Function clears the screen for easier reading"""
    os.system("cls" if os.name == "nt" else 'clear')


# Closes the program
def close_program():
    """7-second timer, then program closes."""
    countdown = 7
    while countdown:
        clear_screen()
        print("I hope you enjoyed using this program!")
        print("Contact Michael Tiday with issues or suggestions.\n")
        print(f"Program exits in {countdown} seconds.")
        countdown -= 1
        time.sleep(1)
    raise SystemExit


if __name__ == "__main__":
    main_menu()
