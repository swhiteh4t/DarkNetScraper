from DarkNetScraper import main



if __name__ == '__main__':
    try:
        args = main.get_arguments()
        darknet_scraper = main.DarkNetScraper(args)
        darknet_scraper.run()
        darknet_scraper.stop()
    except KeyboardInterrupt:
        print("Interrupt received! Exiting cleanly...")
