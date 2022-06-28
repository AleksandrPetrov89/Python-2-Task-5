from functions import functions


if __name__ == '__main__':
    contacts_list = functions.reading_phonebook("phonebook_raw.csv")
    functions.fixing_phonebook(contacts_list)
    functions.print_phonebook(contacts_list)
    functions.write_phonebook("phonebook.csv", contacts_list)
