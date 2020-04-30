import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# Enter the path of the driver
# browser = webdriver.Chrome()
browser = webdriver.Chrome(executable_path=r"C:\Users\Admin\PycharmProjects\vinay\chromedriver.exe")

# Tell Selenium to get the URL you're interested in.

data = pd.read_csv("apps data.csv", index_col=False)
main_info = []
for d in range(len(data)):
    app_name = data.iloc[d][0]
    url = data.iloc[d][1]

    # url = "https://play.google.com/store/apps/details?id=com.facebook.katana&showAllReviews=true"
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
                print(y, 55)
                try:
                    end = browser.find_element_by_css_selector(
                        '#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > div > div.W4P4ne > div:nth-child(2) > div.PFAhAf > div')
                except:
                    print("regular")
                    flag = 2
                    pass

                if flag == 2:

                    pass
                else:

                    end = browser.find_element_by_css_selector(
                        '#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > div > div.W4P4ne > div:nth-child(2) > div.PFAhAf > div').click()
                if y > 744000:  # this value is calculate by trial and error, print the value and
                    # and checkapproximately at what value of y, the scroll reaches the bottom of page and change it
                    break
            except:
                pass

        time.sleep(5)  # wait dom ready
        page = browser.page_source
        soup_expatistan = BeautifulSoup(page, "html.parser")
        expand_pages = soup_expatistan.findAll("div", class_="d15Mdf")

        # app_name = soup_expatistan.find("h1", class_="AHFaub").find("span").text
        number_of_ratings = soup_expatistan.find("div", class_="dNLKff").find("span", class_="AYi5wd").find_next()[
            'aria-label']
        number_of_ratings = number_of_ratings.split(' ', 1)[0]
        overall_rating = soup_expatistan.find("div", class_="dNLKff").find("div", class_="pf5lIe").find_next()['aria-label']
        splitted = overall_rating.split()
        overall_rating = splitted[1]
        category = soup_expatistan.find("div", class_="qQKdcc").find("a", itemprop="genre").text
        cost = soup_expatistan.find("span", class_="oocvOe").find_next()['aria-label'];
        if cost == "Install":
            cost = 0
        else:
            cost = cost.split(' ', 1)[0]
        main_info.append((app_name,number_of_ratings, overall_rating, category, cost))

        records = []
        for expand_page in expand_pages:
            try:
                author_name = str(expand_page.find("span", class_="X43Kjb").text)
                review_date = expand_page.find("span", class_="p2TkOb").text
                reviewer_ratings = expand_page.find("div", class_="pf5lIe").find_next()['aria-label'];
                reviewer_ratings = reviewer_ratings.split('(')[0]
                reviewer_ratings = ''.join(x for x in reviewer_ratings if x.isdigit())
                review_body = str(expand_page.find("div", class_="UD7Dzf").text)
                records.append((author_name, review_date, reviewer_ratings, review_body))
                # print(records)
            except:
                pass

        df = pd.DataFrame(records, columns=['author_name', 'review_date', 'reviewer_ratings', 'review_body'])

        df.to_csv(r"C:\Users\Admin\PycharmProjects\vinay\reviews_" + str(app_name) + ".csv", sep=",",
                  index_label="index")
    except:
        pass


df = pd.DataFrame(main_info, columns=["app_name","number_of_ratings", "overall_rating", "category", "cost"])

df.to_csv(r"C:\Users\Admin\PycharmProjects\vinay\main_info.csv", sep=",",index_label="index")
