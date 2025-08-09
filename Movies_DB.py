# This script will 'scrape'

import requests
import json
import csv
from bs4 import BeautifulSoup
import time
import random

BASE_URL = "https://www.the-numbers.com"
SLUG_APPENDAGE = "#tab=summary"


def get_100():
    # URL for the top 100 domestic box-office earners
    url = "https://www.the-numbers.com/box-office-records/domestic/all-movies/cumulative/all-time"
    # This header will help to disguise the request that I send to look like a normal person browing the internet
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://accounts.youtube.com/",
        "Connection": "keep-alive"

    }
    # using a get request, I can get the raw html for the url I gave
    print("sleeping.....")
    time.sleep(random.uniform(5, 10))
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # BeautifulSoup parses the html into a tree that can allow me to cherry-pick the things that I want.
        soup = BeautifulSoup(response.text, "html.parser")

        print(soup.prettify()[:1000])

        movie_data = []

        table = soup.find("table")
        for row in table.find_all("tr")[1:]:  # Skip header row
            #print("4")
            cols = row.find_all("td")
            if len(cols) < 2:
                continue  # Skip incomplete rows

            rank = cols[0].text.strip()
            title_link = cols[2].find("a")
            title = title_link.text.strip()
            relative_url = title_link['href']
            full_url = "https://www.the-numbers.com" + relative_url
            domestic_gross = cols[4].text.strip() if len(cols) >= 5 else None

            movie_data.append({
                "rank": rank,
                "title": title,
                "url": full_url,
                "domestic_gross": domestic_gross
            })
        print(movie_data)
        return movie_data
    else:
        print(response.status_code)


def get_300():
    # URL for the top 100 domestic box-office earners
    url = "https://www.the-numbers.com/box-office-records/domestic/all-movies/cumulative/all-time/201"
    # This header will help to disguise the request that I send to look like a normal person browsing the internet
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://www.the-numbers.com/box-office-records/domestic/all-movies/cumulative/all-time/101",
        "Connection": "keep-alive"

    }
    # using a get request, I can get the raw html for the url I gave
    print("sleeping.....")
    time.sleep(random.uniform(5, 10))
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # BeautifulSoup parses the html into a tree that can allow me to cherry-pick the things that I want.
        soup = BeautifulSoup(response.text, "html.parser")

        print(soup.prettify()[1000:2000])

        movie_data = []

        table = soup.find("table")
        for row in table.find_all("tr")[1:]:  # Skip header row0
            #print("4")
            cols = row.find_all("td")
            if len(cols) < 2:
                continue  # Skip incomplete rows

            rank = cols[0].text.strip()
            title_link = cols[2].find("a")
            title = title_link.text.strip()
            relative_url = title_link['href']
            full_url = "https://www.the-numbers.com" + relative_url
            domestic_gross = cols[4].text.strip() if len(cols) >= 5 else None

            movie_data.append({
                "rank": rank,
                "title": title,
                "url": full_url,
                "domestic_gross": domestic_gross
            })
        print(movie_data)
        return movie_data
    else:
        print(response.status_code)

# def get_movie_data(url, dictionary):
#     # url = f"{BASE_URL}/movie/{slug}"
#     headers = {"User-Agent": "Mozilla/5.0"}
#     time.sleep(random.uniform(5, 10))
#     response = requests.get(url, headers=headers)
#
#     if response.status_code != 200:
#         print(f"Failed to fetch: {url}")
#         return None
#
#     soup = BeautifulSoup(response.text, "html.parser")
#
#     data = {"url": url}
#
#     # Find the financial summary table
#     financial_table = soup.find("table", class_="financials")
#
#     if financial_table:
#         rows = financial_table.find_all("tr")
#         for row in rows:
#             header = row.find("td", class_="clear")
#             value = row.find_all("td")[-1]
#             if header and value:
#                 label = header.text.strip().replace(":", "")
#                 amount = value.text.strip()
#                 data[label] = amount
#
#     return data

# Example usage: scrape Inception (its slug is like "Inception#tab=summary")
# movie_slug = "Inception#tab=summary"
# info = get_movie_data(movie_slug)
# print(info)

def get_movies():
    with open("movies.json", "r") as f:
        data = json.load(f)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://www.the-numbers.com/box-office-records/domestic/all-movies/cumulative/all-time/",
        "Connection": "keep-alive"
    }

    output_file = "movies_extended.csv"
    fieldnames = [
        "title", "domestic_gross", "url",
        "opening_weekend", "legs", "domestic_share",
        "production_budget", "theater_counts", "infl_adj_domestic_bo"
    ]

    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for movie in movies:
            print(f"Scraping: {movie['title']}")
            time.sleep(random.uniform(4, 8.5))

            try:
                response = requests.get(movie["url"], headers=headers, timeout=10)
                response.raise_for_status()
            except Exception as e:
                print(f"❌ Failed to fetch {movie['title']}: {e}")
                movie["opening_weekend"] = "N/A"
                movie["production_budget"] = "N/A"
                writer.writerow(movie)
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            metrics_heading = soup.find("h2", string="Metrics")
            finance_table = metrics_heading.find_next("table") if metrics_heading else None
            opening = legs = share = budget = theaters = infl_adj = "N/A"

            if finance_table:
                rows = finance_table.find_all("tr")
                row_values = [row.find_all("td")[-1].text.strip() for row in rows if row.find_all("td")]

                # Assign based on known order
                try:
                    opening = row_values[0]
                    legs = row_values[1]
                    share = row_values[2]
                    budget = row_values[3]
                    theaters = row_values[4]
                    infl_adj = row_values[5]
                except IndexError:
                    print(f"⚠️ Incomplete table for {movie['title']}")

            movie.update({
                "opening_weekend": opening,
                "legs": legs,
                "domestic_share": share,
                "production_budget": budget,
                "theater_counts": theaters,
                "infl_adj_domestic_bo": infl_adj
            })

            writer.writerow(movie)


def get_movies_extended():
    # Load the JSON file containing your movies
    with open("movies.json", "r", encoding="utf-8") as f:
        movies = json.load(f)

    # Set a realistic browser-like header
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.6312.86 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.the-numbers.com/box-office-records/domestic/all-movies/cumulative/all-time/",
        "Connection": "keep-alive",
    }

    # Define the output CSV file and the fields to be saved
    output_file = "movies_extended.csv"
    fieldnames = [ "rank",
        "title", "domestic_gross", "url",
        "opening_weekend", "legs", "domestic_share",
        "production_budget", "theater_counts", "infl_adj_domestic_bo"
    ]

    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Loop through each movie in the JSON file
        for movie in movies:
            print(f"Scraping: {movie['title']}")

            # Add a random delay to mimic human behavior
            time.sleep(random.uniform(6, 12.5))

            try:
                response = requests.get(movie["url"], headers=headers, timeout=10)
                response.raise_for_status()
            except Exception as e:
                print(f"❌ Failed to fetch {movie['title']}: {e}")
                movie.update({
                    "opening_weekend": "N/A",
                    "legs": "N/A",
                    "domestic_share": "N/A",
                    "production_budget": "N/A",
                    "theater_counts": "N/A",
                    "infl_adj_domestic_bo": "N/A"
                })
                writer.writerow(movie)
                continue

            # Parse the fetched HTML content
            soup = BeautifulSoup(response.text, "html.parser")

            # Locate the <h2> heading with "Financial Summary"
            summary_heading = soup.find("h2", string="Metrics")
            # Find the next table following that heading
            table = summary_heading.find_next("table") if summary_heading else None
            # skip that table and go to the next one
            table = table.find_next("table") if table else None

            # Set default values in case any data is missing
            opening = legs = share = budget = theaters = infl_adj = "N/A"

            if table:
                #print(table)
                # Get all rows (each row is assumed to have a label and a value)
                rows = table.find_all("tr")
                #print(rows)
                # For each row, extract the text from the last <td> (value)
                row_values = [row.find_all("td")[-1].text.strip()
                              for row in rows]
                print("Row Values:\n", row_values)
                try:
                    opening = row_values[0]  # Opening Weekend
                    legs = row_values[1]  # Legs
                    share = row_values[2]  # Domestic Share
                    budget = row_values[3]  # Production Budget
                    theaters = row_values[4]  # Theater Counts
                    infl_adj = row_values[5]  # Inflation-Adjusted Domestic BO
                except IndexError:
                    print(f"⚠️ Incomplete table for {movie['title']}. Some data may be missing.")
            else:
                print(f"⚠️ Could not locate the Financial Summary table for {movie['title']}.")

            # Update the current movie dictionary with new information
            movie.update({
                "opening_weekend": opening,
                "legs": legs,
                "domestic_share": share,
                "production_budget": budget,
                "theater_counts": theaters,
                "infl_adj_domestic_bo": infl_adj
            })

            # Write the updated movie data to the CSV file
            writer.writerow(movie)
            print(f"✅ Completed: {movie['title']}")



if __name__ == "__main__":
    get_movies_extended()

