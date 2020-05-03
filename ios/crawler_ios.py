import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

# Enter the path of the driver
# browser = webdriver.Chrome()
browser = webdriver.Chrome(executable_path=r"C:\Users\Parth\Documents\540\android_review_crawler\ios_Xamarin_and_React_apps_reviews\chromedriver.exe")
## change path depending if its native or framework
# path = "./Native_ios_apps_reviews"
path = "C:\\Users\\Parth\\Documents\\540\\android_review_crawler\\ios_Xamarin_and_React_apps_reviews"
# Tell Selenium to get the URL you're interested in.

data = pd.read_csv("apps data.csv", index_col=False)
main_info = []
for d in range(len(data)):
    # app_name = data.iloc[d][0]
    url = data.iloc[d][1]

    # url = "https://play.google.com/store/apps/details?id=com.facebook.katana&showAllReviews=true"
    browser.get(url)
    SCROLL_PAUSE_TIME = 0.5

    time.sleep(5)  # wait dom ready
    page = browser.page_source
    soup_expatistan = BeautifulSoup(page, "html.parser")

    app_name = soup_expatistan.find("h1", class_="product-header__title app-header__title").text.split()[0]
    overall_and_number = soup_expatistan.find("li",
                                              class_="product-header__list__item app-header__list__item--user-rating").find(
        "figcaption", class_="we-rating-count star-rating__count").text
    overall_rating = overall_and_number.split()[0].replace(',', '')
    number_of_ratings = overall_and_number.split()[1]

    for c in number_of_ratings:
        print(c)
        if c.isalpha():
            if c == 'K':
                number_of_ratings = number_of_ratings.replace('K', '')
                number_of_ratings = float(number_of_ratings)*1000

            if c == 'M':
                number_of_ratings = number_of_ratings.replace('M', '')
                number_of_ratings = float(number_of_ratings)*1000000

    category_parent = soup_expatistan.find("h2", class_="section__headline", text="Information").find_parent('div')
    category = category_parent.find_next("a").text.strip()
    cost_parent = category_parent.find("dt", class_="information-list__item__term", text="Price").find_parent('div')
    cost = cost_parent.find_next("dd").text.strip()

    if cost == "Free":
        cost = 0

    main_info.append((app_name, number_of_ratings, overall_rating, category, cost))

    reviews_parent = soup_expatistan.find("h2", class_="section__headline",
                                          text=re.compile('Ratings and Reviews')).find_parent('div')
    if reviews_parent.find_next("a"):
        url = url + "#see-all/reviews"
        browser.get(url)
        SCROLL_PAUSE_TIME = 0.5
        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")
        new_height = 100
        x = 50
        y = 100
        to_break = 0
        all_data = {}
        try:
            while True:
                try:
                    flag = 0
                    time.sleep(SCROLL_PAUSE_TIME)
                    new_height = browser.execute_script("window.scrollTo({0},{1});".format(50 + x, 50 + y))
                    time.sleep(SCROLL_PAUSE_TIME)
                    x = x + 1500
                    y = x + 1500
                    print(y, last_height)
                    if y > 744000:  # this value is calculate by trial and error, print the value and
                        # and checkapproximately at what value of y, the scroll reaches the bottom of page and change it
                        # this gets around 840reviews
                        break
                except:
                    pass

            time.sleep(5)  # wait dom ready
            page = browser.page_source
            soup_expatistan = BeautifulSoup(page, "html.parser")
            expand_pages = soup_expatistan.findAll("div", class_="we-customer-review")

            records = []
            for expand_page in expand_pages:
                try:

                    author_date = expand_page.find("div", class_="we-customer-review__header")
                    author_name = author_date.find("span", class_="we-customer-review__user").text.strip()
                    review_date = author_date.find("time")['aria-label']
                    reviewer_ratings = expand_page.find("figure", class_="we-star-rating")['aria-label'].split()[0];
                    header_review = str(expand_page.find("h3", class_="we-customer-review__title").text.strip())
                    review_body = str(
                        expand_page.find("blockquote", class_="we-customer-review__body").find_next("p").text)
                    review_body = header_review + " " + review_body
                    records.append((author_name, review_date, reviewer_ratings, review_body))

                except:
                    pass
            df2 = pd.DataFrame(records, columns=['author_name', 'review_date', 'reviewer_ratings', 'review_body'])
            review_file_name = "reviews_" + app_name + ".csv"
            output_file = os.path.join(path, review_file_name)
            df2.to_csv(output_file, sep=",", index_label="index")
        except:
            pass

        # records = []
        # for expand_page in expand_pages:
        #     try:
        #         author_name = str(expand_page.find("span", class_="X43Kjb").text)
        #         review_date = expand_page.find("span", class_="p2TkOb").text
        #         reviewer_ratings = expand_page.find("div", class_="pf5lIe").find_next()['aria-label'];
        #         reviewer_ratings = reviewer_ratings.split('(')[0]
        #         reviewer_ratings = ''.join(x for x in reviewer_ratings if x.isdigit())
        #         review_body = str(expand_page.find("div", class_="UD7Dzf").text)
        #         records.append((author_name, review_date, reviewer_ratings, review_body))
        #         # print(records)
        #     except:
        #         pass
        #
        # df = pd.DataFrame(records, columns=['author_name', 'review_date', 'reviewer_ratings', 'review_body'])
        #
        # df.to_csv(r"C:\Users\Admin\PycharmProjects\vinay\reviews_" + str(app_name) + ".csv", sep=",",
        #           index_label="index")
    # except:
    #     pass

main_file_name = "main_info_new.csv"
output_file = os.path.join(path, main_file_name)
df1 = pd.DataFrame(main_info, columns=['app_name', 'number_of_ratings', 'overall_rating', 'category', 'cost'])
df1.to_csv(output_file, sep=",", index_label="index")
