from db_connector import *

my_title = "title"
my_other_title = "title2"
my_list = ["String 1", "string 2", "string 3", "etc."]
my_other_list = ["string 4", "string 5", "string 6"]

my_db = DatabaseConnection()
my_db.insert_data(my_other_title, my_other_list)
my_db.retrieve_data(my_other_title)
my_db.close_connection()
my_db.delete_data()