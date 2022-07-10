from functools import total_ordering
from gettext import find
import requests
import pandas as pd
from bs4 import BeautifulSoup
import random

# GLOBAL LIST TO STORE ALL THE REVIEWS
reviewList = []


def extractReviews(reviewsUrl):
    # TO GET DIFFERERENT PROXY SERVER EVERY TIME
    proxy = 9000 + random.randint(0, 9)

    resp = requests.get(reviewsUrl, proxies = {"http": "http://127.0.0.1:"+str(proxy)})

    soup = BeautifulSoup(resp.text, 'html.parser')
    reviews = soup.findAll('div', {'data-hook': "review"})

    for item in reviews:
        with open('output/file.html', 'w') as f:
            f.write(str(item))

        date_list = item.find('span', {'data-hook': 'review-date'}).text.strip().split()[4:]
        review_date = ' '.join(map(str, date_list))

        # This Dictionary will be saved in Excel.
        review = {
            'Product Title': soup.title.text.replace("Amazon.in:Customer reviews: ", "").strip(),
            'Review Title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
            'Rating': item.find('i', {'data-hook': 'review-star-rating'}).text.strip(),
            'Review Body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
            'Reviewed On' : review_date
        }
        reviewList.append(review)


def Totalreviews(reviewsUrl):
    proxy = 9000 + random.randint(0, 9)

    resp = requests.get(reviewsUrl, proxies = {"http": "http://127.0.0.1:"+str(proxy)})

    soup = BeautifulSoup(resp.text, 'html.parser')
    reviews = soup.find('div', {'data-hook': "cr-filter-info-review-rating-count"})
    return int(reviews.text.strip().split(', ')[1].split()[0])


def main():
    # Change this URL for any other site (like Flipkart, Walmart, etc.)
    productUrl = "https://www.amazon.in/HP-3-3250-Laptop-Windows-15s-gr0012AU/dp/B08T6THSMQ/ref=sr_1_10"

    #The Url of the 'reviews' page
    reviewsUrl = productUrl.replace("dp", "product-reviews") + "?PageNumber=" + str(1)
    print(reviewsUrl)

    total_reviews = Totalreviews(reviewsUrl)

    print("Total Reviews = ", total_reviews)
    for i in range(total_reviews):
        print(f"Running for Review : {i+1}")
        try:
            reviewsUrl = productUrl.replace("dp", "product-reviews") + "?PageNumber=" + str(i)
            extractReviews(reviewsUrl)
        except Exception as e:
            print(e)

    df = pd.DataFrame(reviewList)
    df.to_excel('Reviews.xlsx', index=False)


main()
