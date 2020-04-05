# -*- coding: utf-8 -*-
import scrapy
from twisted.python import log as twisted_log
import logging
import os
import glob
from game_crawler.items import GameDetailsItem
import pandas as pd

class GamedetailsSpider(scrapy.Spider):
    name = 'gamedetails'

    custom_settings = {
        'FEED_URI': "../dataset/game_details_raw.csv",
        'FEED_FORMAT' : "csv",
        'DOWNLOAD_DELAY' : 0,
        "AUTOTHROTTLE_ENABLED" : False,
        "CONCURRENT_REQUESTS": 1024,
        "CONCURRENT_REQUESTS_PER_IP": 1024
    }

    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('gamedetails_local_scrape.log', 'w', 'utf-8-sig')])
    observer = twisted_log.PythonLoggingObserver()
    observer.start()

    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    files = [f for f in glob.glob(project_dir + "/dataset_html/*.html", recursive=True)]
    start_urls = ["file:///" + f for f in files]
    # start_urls = start_urls[:10]
    # start_urls = ['file:///D:/Research/itchio-game/dataset_html/_oreo_.stellar-cat-damon.html']

    fname_errors = []
    game_overview = pd.read_csv(os.path.join(project_dir + "/dataset", 'games_raw.csv'))

    def parse(self, response):
        item = GameDetailsItem()

        # D:\Research\itchio-game\dataset_html\_oreo_.stellar-cat-damon.html
        # input(response.url)
        file_name = response.url.replace("file:///", "").replace("%5C", "/").split("/")[4]
        print(file_name)
        fname_comp = file_name.split(".")
        if (len(fname_comp) > 3):
            self.fname_errors.append(file_name)
        else:
            # input(fname_comp)
            author = fname_comp[0]
            game_name = fname_comp[1]

            item['game_url'] = author + ".itch.io/" + game_name
            # self.all_game_urls_based_on_file.append(item['game_url'])
            passtag = response.css(".game_password_page")
            if passtag:
                item['game_status'] = 'A password is required to view this page'
                yield item
                return

            GAME_NAME_SELECTOR = ".game_title ::text"
            item['game_name'] = response.css(GAME_NAME_SELECTOR).extract_first("")

            GAME_DESC_SELECTOR = ".formatted_description *::text"
            description = response.css(GAME_DESC_SELECTOR).extract()
            item['game_desc_len'] = len("".join(description).strip().replace('\n', '').replace('\r', ''))
            item['game_desc'] = " ".join(description).strip().replace('\n', '').replace('\r', '')

            # Extract github location
            # example multiple github links: https://hunterkepley.itch.io/ice

            all_links = response.css("a ::attr(href)").extract()
            githubs = [s for s in all_links 
                        if "github.com/" in s or 
                        "gitlab.com/" in s or 
                        "bitbucket.org/" in s]
            item['game_source_code'] = "||".join(githubs) if len(githubs) > 0 else ""

            # Couting number of screenshots
            item['game_no_screenshots'] = len(response.css(".screenshot") + response.css(".formatted_description img"))

            # Extract game price
            GAME_PRICE_SELECTOR = ".buy_message ::text"
            item["game_price"] = response.css(GAME_PRICE_SELECTOR).extract_first()

            # Extract "More information" section
            GAME_INFO_TABLE_ROW_SELECTOR = ".game_info_panel_widget table tr"
            info_rows = response.css(GAME_INFO_TABLE_ROW_SELECTOR)
            info = {}
            for row in info_rows:
                row_key = row.xpath("td[1]/text()").extract_first()
                if ("update" in row_key.lower()) or ("publish" in row_key.lower()) or ("release" in row_key.lower()):
                    # print(row_key)
                    info[row_key] = row.css("abbr ::attr(title)").extract_first()
                elif ("author" in row_key.lower()) or ("authors" in row_key.lower()):
                    info[row_key] = "||".join(row.xpath("td[2]/a/text()").extract())
                    info["Author's Url"] = "||".join(row.xpath("td[2]/a/@href").extract())
                elif ("mentions" in row_key.lower()):
                    info["Mentions"] = "||".join(row.xpath("td[2]/a/@href").extract())
                elif ("links" in row_key.lower()):
                    info["Links"] = "||".join(row.xpath("td[2]/a/@href").extract())
                elif ("rating" in row_key.lower()):
                    num_rating = row.css(".aggregate_rating .rating_count ::text").extract_first("")
                    info["Num rating"] = int(num_rating.replace("(", "").replace(")", ""))
                    info["Rating"] = float(row.css(".aggregate_rating ::attr(title)").extract_first(""))
                else:
                    info[row_key] = "||".join(row.xpath("td[2]/a/text()").extract())

            item["game_last_update"]     = info.get("Updated", "")
            item["game_publish_date"]    = info.get("Published", "")
            item["game_release_date"]    = info.get("Release date", "")
            item["game_status"]          = info.get("Status", "")
            item["game_platforms"]       = info.get("Platforms", "")
            item["game_genres"]          = info.get("Genre", "")
            item["game_tags"]            = info.get("Tags", "")
            item["game_made_with"]       = info.get("Made with", "")
            item["game_ave_session"]     = info.get("Average session", "")
            item["game_language"]        = info.get("Languages", "")
            item["game_inputs"]          = info.get("Inputs", "")
            item["game_accessibility"]   = info.get("Accessibility", "")
            item["game_license"]         = info.get("License", "")
            item["game_asset_license"]   = info.get("Asset license", "")
            item["game_developers"]      = info.get("Author", info.get("Authors", ""))
            item["game_developers_url"]  = info.get("Author's Url", "")
            item["game_multiplayer"]     = info.get("Multiplayer", "")
            item["game_mentions"]        = info.get("Mentions", "")
            item["game_links"]           = info.get("Links", "")
            item["game_rating"]          = info.get("Rating", "")
            item["game_no_ratings"]      = info.get("Num rating", "")

            # Download section
            # UPLOAD_SELECTOR = ".upload"
            # all_uploads = response.css(UPLOAD_SELECTOR)
            # download_infos = []
            # for upload in all_uploads:
            #     upload_date = upload.css(".upload_date *::attr(title)").extract_first(default = "")
            #     upload_size = upload.css(".file_size ::text").extract_first(default = "")
            #     upload_name = upload.css(".upload_name .name ::text").extract_first()
            #     upload_platform = [plf.replace("Download for ", "") for plf in upload.css(".download_platforms *::attr(title)").extract()]
            #     download_infos.append(upload_name + "||" + upload_size + "||" + upload_date + '||' + "||".join(upload_platform))

            # item['game_size'] = "<>".join(download_infos)

            yield item

