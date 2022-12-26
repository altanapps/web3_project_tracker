import scrape

class Project:
    def __init__(self, time_stamp, url, stars):
        # Amend and change as you add more data
        self.time_stamp = time_stamp
        self.url = url
        self.stars = stars


scrape.scrape_page("https://github.com/ethereum/go-ethereum")
