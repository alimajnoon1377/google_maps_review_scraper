import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

def scrape_google_maps_reviews(url):
    """
    Scrapes reviews from a Google Maps page and returns a list of dictionaries containing the
    reviewer name, number of previous reviews, rating, review text, and date of the review.
    """
    # send a GET request to the URL
    response = requests.get(url)

    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # find all the reviews on the page
    reviews = soup.find_all('div', {'class': 'section-review'})

    # initialize a list to store the extracted information
    review_list = []

    # loop through each review and extract the relevant information
    for review in reviews:
        reviewer_name = review.find('div', {'class': 'section-review-title'}).find('span').text
        num_reviews = review.find('div', {'class': 'section-review-title'}).find('span', {'class': 'section-review-num-ratings'}).text.strip('()')
        rating = review.find('span', {'class': 'section-review-stars'})['aria-label']
        review_text = review.find('span', {'class': 'section-review-text'}).text
        review_date = review.find('span', {'class': 'section-review-publish-date'}).text
        review_date = re.findall('\d+ \w+ ago', review_date)[0] # extract the date in the format "2 months ago"
        review_date = datetime.now() - timedelta(days=int(review_date.split()[0]), weeks=0, months=0, years=0)
        review_date = review_date.strftime("%Y-%m-%d")

        # append the extracted information to the list
        review_list.append({
            'reviewer_name': reviewer_name,
            'num_reviews': num_reviews,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        })

    return review_list
