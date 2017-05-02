import csv
import os
import os.path
import time
import random


def display_menu():
    """Main menu of program (what user sees), returns foolproofed user input"""
    os.system("clear")
    print("Welcome to the music collector. Choose your action: \n")
    print(" 1) Add new album to collection")
    print(" 2) Find all albums by an artist")
    print(" 3) Find all albums by the year")
    print(" 4) Find a musician by an album")
    print(" 5) Find albums by the letter(s)")
    print(" 6) Find all albums by genre")
    print(" 7) Calculate the age of all albums")
    print(" 8) Choose a random album by genre")
    print(" 9) Show the total amount of albums by an artist")
    print("10) Find the longest album")
    print(" 0) Exit")
    user_choice = check_input_choice()
    return user_choice


def check_input_choice():
    """Checks menu input for foolproofing"""
    while True:
        option = input("\nSelect an option: ")
        if option not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            print("Pick a number 1 - 10, or 0 to exit ")
            continue
        else:
            return option


def read_from_file():
    """Reads whole database from file and returns it as a list of tuples"""
    albums = []
    with open('music.csv', newline='') as csvfile:
        content = csv.reader(csvfile, delimiter='|')
        for line in content:
            if len(line) == 5:  # To prevent blank lane at the end of file from wrecking havoc
                albums.append(
                    ((line[0].strip().title(), line[1].strip().title()),
                     (int(line[2]), line[3].strip().lower(), line[4].strip())))
    return albums


def add_new():
    """Adds new album to the collection"""
    print("Here you can add a new album to collection.")
    print("You can type 'exit' any time to go back to menu\n")

    artist = input("Enter artist name:\n")
    if artist == "exit":
        return

    album = input("Enter album name:\n")
    if album == "exit":
        return

    while True:
        year = input("Enter year of release:\n")
        if year == "exit":
            return
        try:
            year = int(year)
            break
        except ValueError:
            print("Enter year in YYYY format:\n")
            continue

    genre = input("Enter music genre:\n")
    if genre == "exit":
        return

    while True:
        # Will check if length is entered in correct format nn:nn, n is number
        length = input("Enter length of the album:\n")
        if length == "exit":
            return
        if length[-3] == ":" and (length[:-3]+length[-2:]).isdigit():
            break
        else:
            print("Next time enter length as MM:SS\n")

    with open('music.csv', 'a', newline='') as csvfile:
        content = csv.writer(csvfile, delimiter='|')
        content.writerow([artist.title(), album.title(), year, genre.lower(), length])
    print("Database updating. Thank you!")
    time.sleep(2)


def find_album_by_artist(all_albums):
    """Takes in list of albums, searches for specific artist, prints matching"""
    while True:
        zero_match = 0
        artist = input("Enter name of an artist you're looking for (or 'exit'): \n")
        if artist == "exit":
            return
        print("")
        for data in all_albums:
            if data[0][0] == artist.title():
                zero_match += 1
                print(str(zero_match) + ") " + str(data[0][1]))
                print("   Year: " + str(data[1][0]) + ", Genre: " + str(data[1][1]) + ", Length: " + str(data[1][2]))
        if zero_match == 0:
            print("Sorry. Couldn't find this artist on our list. Try again.")
        print("")


def find_album_by_year(all_albums):
    """Takes in list of albums, searches for specific year, prints matching"""
    while True:
        zero_match = 0
        year = input("Enter the year you're looking for (or 'exit'): \n")
        if year == "exit":
            return
        print("")
        try:
            year = int(year)
        except ValueError:
            print("Next time please enter a valid year\n")
            continue
        for data in all_albums:
            if data[1][0] == year:
                zero_match += 1
                print(str(zero_match) + ") " + str(data[0][1]))
                print("   Artist: " + str(data[0][0]) + ", Genre: " + str(data[1][1]) + ", Length: " + str(data[1][2]))
        if zero_match == 0:
            print("Sorry. No album in database was released that year. Try again.")
        print("")


def find_artist_by_album(all_albums):
    """Takes in list of albums, searches for specific album, prints matching artist"""
    while True:
        zero_match = 0
        album = input("Enter name of an album you're looking for (or 'exit'): \n")
        if album == "exit":
            return
        print("")
        for data in all_albums:
            if data[0][1] == album.title():
                zero_match += 1
                print(str(zero_match) + ") " + str(data[0][0]))
                print("   Year: " + str(data[1][0]) + ", Genre: " + str(data[1][1]) + ", Length: " + str(data[1][2]))
        if zero_match == 0:
            print("Sorry. Couldn't find this album on our list. Try again.")
        print("")


def find_album_by_letter(all_albums):
    """Takes in list of albums, searches for letters in albums, prints matching"""
    while True:
        zero_match = 0
        letters = input("Enter any sequence of characters to search for the album\n \
                         \rTIP: blank input will list whole database, 'exit' will do the obvious\n")
        if letters == "exit":
            return
        print("")
        for data in all_albums:
            if letters.lower() in data[0][1].lower():
                zero_match += 1
                print(str(zero_match) + ") " + str(data[0][1]) + "  by  " + str(data[0][0]))
                print("   Year: " + str(data[1][0]) + ", Genre: " + str(data[1][1]) + ", Length: " + str(data[1][2]))
        if zero_match == 0:
            print("Sorry. Couldn't find any album containing those characters. Try again.")
        print("")


def find_album_by_genre(all_albums):
    """Takes in list of albums, searches for specific genre, prints matching"""
    while True:
        zero_match = 0
        genre = input("Enter the genre you're looking for (or 'exit'): \n")
        if genre == "exit":
            return
        print("")
        for data in all_albums:
            if data[1][1] == genre.lower():
                zero_match += 1
                print(str(zero_match) + ") " + str(data[0][1]) + "  by  " + str(data[0][0]))
                print("   Year: " + str(data[1][0]) + ", Length: " + str(data[1][2]))
        if zero_match == 0:
            print("Sorry. No album in database from that genre. Try again.")
        print("")


def calculate_age(all_albums):
    """Takes in list of albums, calculates their age in years, prints out total and average"""
    current_year = int(time.strftime("%Y"))
    print("There is a total of", len(all_albums), "albums in the database\n")
    show_more = input("Type anything to calculate their average age (or 'exit' to leave):\n")
    if show_more == "exit":
        return
    avg_age = 0
    for data in all_albums:
        avg_age += current_year - data[1][0]
    avg_age /= len(all_albums)
    print("\nIts year {} now, meaning average age of the albums is {:.5} years\n".format(current_year, avg_age))
    show_all = input("Type anything to list all the albums by their age (or 'exit' to leave):\n")
    if show_all == "exit":
        return
    print("")
    sorting_index = 1
    for data in all_albums:
        print(str(sorting_index) + ") " + str(data[0][1]) + "  by  " + str(data[0][0]))
        print("  ", current_year - data[1][0], "years old")
        sorting_index += 1
    input("\nType anything to return to main menu\n")


def pick_random_by_genre(all_albums):
    """Takes in list of albums, searches for specific genre, prints random match"""
    while True:
        genre = input("Enter the genre you're looking for (or 'exit') to leave \n \
                      \rTIP: this will include all the sub-genres, meaning that typing 'metal'\n \
                      \r     will search through heavy metal, death metal, trash metal, etc.\n")
        if genre == "exit":
            return
        print("")
        random_genre_list = []
        for data in all_albums:
            if genre.lower() in data[1][1]:
                random_genre_list.append(data)
        if len(random_genre_list) == 0:
            print("Sorry. No album in database from that genre. Try again.")
        else:
            random_pick = random_genre_list[random.randint(0, len(random_genre_list)-1)]
            print("Here is the random album from that genre:\n")
            print(random_pick[0][1] + "  by  " + random_pick[0][0])
            print("Year:", random_pick[1][0], "\b, Genre: " + random_pick[1][1] + ", Length: " + random_pick[1][2])
        print("")


def find_total_albums_by_artist(all_albums):
    """Takes in list of albums, searches for specific artist, prints all matching albums"""
    while True:
        zero_match = 0
        artist = input("Enter name of an artist you're looking for (or 'exit'): \n")
        if artist == "exit":
            return
        print("")
        for data in all_albums:
            if data[0][0] == artist.title():
                zero_match += 1
        if zero_match == 0:
            print("Sorry. Couldn't find this artist on our list. Try again.")
        else:
            print("There is a total of {} album by {} in our database".format(zero_match, artist.title()))
        print("")


def find_longest_album(all_albums):
    """Takes in list of albums, prints the longest album"""
    print("Here you can find out what is the longest album in our database")
    user_choice = input("Type 'exit' to return to main menu or anything else to continue\n")
    if user_choice == "exit":
        return
    current_longest = 0
    for data in all_albums:
        length_in_seconds = 0
        # This is to make sure inputs like 1:24:31 are understood same as 84:31, and 2:51:36 same as 171:36
        try:
            if data[1][2][-6] == ":":
                length_in_seconds = 3600*int(data[1][2][:-6]) + 60*int(data[1][2][-5:-3]) + int(data[1][2][-2:])
            elif data[1][2][-6].isdigit():
                length_in_seconds = 60*int(data[1][2][:-3]) + int(data[1][2][-2:])
        except IndexError:
            length_in_seconds = 60*int(data[1][2][:-3]) + int(data[1][2][-2:])
        if length_in_seconds > current_longest:
            current_longest = length_in_seconds
            longest = data
    print("The longest album in database is:\n")
    print(longest[0][1], " by ", longest[0][0])
    print("Year:", longest[1][0], "\b, Genre: " + longest[1][1] + ", Length: " + longest[1][2])
    input("\nPress enter to return to main menu\n")


def main():
    try:
        all_albums = read_from_file()
    except FileNotFoundError:
        print("\nMissing CSV file. Please download it from the repository.\n")
        exit()

    while True:
        user_choice = display_menu()
        os.system("clear")
        if user_choice == "1":
            add_new()
            all_albums = read_from_file()
        elif user_choice == "2":
            find_album_by_artist(all_albums)
        elif user_choice == "3":
            find_album_by_year(all_albums)
        elif user_choice == "4":
            find_artist_by_album(all_albums)
        elif user_choice == "5":
            find_album_by_letter(all_albums)
        elif user_choice == "6":
            find_album_by_genre(all_albums)
        elif user_choice == "7":
            calculate_age(all_albums)
        elif user_choice == "8":
            pick_random_by_genre(all_albums)
        elif user_choice == "9":
            find_total_albums_by_artist(all_albums)
        elif user_choice == "10":
            find_longest_album(all_albums)
        else:
            exit()


if __name__ == '__main__':
    main()
