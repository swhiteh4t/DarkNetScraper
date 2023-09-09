#!/usr/bin/env python3
from DarkNetScraper import main

if __name__ == '__main__':
    try:
        args = main.get_arguments()
        dark_scraper = main.DarkNetScraper(args)
        dark_scraper.run()
        dark_scraper.stop()
    except KeyboardInterrupt:
        print("Interrupt received! Exiting cleanly...")
