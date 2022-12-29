from find_projects import find_all_projects
from scrape import scrape_page, get_links
from datetime import datetime
from interact_with_database import connect_to_db, write_to_db


def lambda_handler(event, context):
    # Finds all the projects and stores them in a file
    find_all_projects()

    # Get the connection
    conn = connect_to_db()

    # Scrape the project and write into the database
    dt = int(datetime.now().timestamp())
    links = [link.strip("\n") for link in get_links()]
    for link in links:
        project = scrape_page(link, dt).return_obj()
        print(link)
        write_to_db(conn, project)
