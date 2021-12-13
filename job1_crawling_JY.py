from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')

driver = webdriver.Chrome('./chromedriver', options=options)

# # 네이버 책 리뷰  자기계발 i 12345
# # https://book.naver.com/category/index.naver?cate_code=1700{}0.format(i)
# https://book.naver.com/category/index.naver?cate_code=1700{}0&list_type=list&tab=recommend.format(i)
# i=12345
# https://book.naver.com/category/index.naver?cate_code=170010&tab=recommend&list_type=list&sort_type=salecount&page={}.format(i)
#
#
# //*[@id="book_title_0"]/a[1]
# //*[@id="book_title_1"]/a[1]

# # https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page=1
# # https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page=2   37까지
# # 영화 제목 xpath
# # //*[@id="old_content"]/ul/li[1]/a
# # //*[@id="old_content"]/ul/li[2]/a
# # //*[@id="old_content"]/ul/li[20]/a
# # //*[@id="movieEndTabMenu"]/li[6]/a/em  리뷰버튼,
# # //*[@id="reviewTab"]/div/div/div[2]/span/em 리뷰 건수
# # //*[@id="pagerTagAnchor1"]   리뷰 페이지 버튼
# # //*[@id="pagerTagAnchor10"]/em   리뷰 다음 페이지 버튼
# # //*[@id="reviewTab"]/div/div/ul/li[1]/a/strong 리뷰 제목
# # //*[@id="SE-ec9bce5c-9be3-47a9-9957-b075426d88fb"] 리뷰 한 줄
# # //*[@id="content"]/div[1]/div[4]/div[1]/div[4]        # class:user_tx_area

review_button_xpath = '//*[@id="container"]/div[5]/ul/li[3]/strong/a'
review_number_xpath = '//*[@id="reviewList"]/li[1]/dl/dt/a'



try:
    for i in range(1, 6):
        url = 'https://book.naver.com/category/index.naver?cate_code=170010&tab=recommend&list_type=list&sort_type=salecount&page={}'.format(i)
        titles = []
        reviews = []
        for j in range(1, 21):
            print(j+((i-1)*20), '번째 책 크롤링 중')
            try:
                driver.get(url)
                print('debug0')
                book_title_xpath = '//*[@id="book_title_{}"]/a[1]'.format(j)
                print('debug1')
                title = driver.find_element_by_xpath(book_title_xpath).text
                print(title)
                driver.find_element_by_xpath(book_title_xpath).click()
                print('debug3')
                driver.find_element_by_xpath('//*[@id="container"]/div[5]/ul/li[3]/a').click()
                time.sleep(1)
                review_url = driver.find_element_by_xpath('//*[@id="reviewList"]/li[1]/dl/dt/a').get_attribute('href')
                driver.get(review_url)
                time.sleep(1)
                driver.switch_to.frame('mainFrame')
                review = driver.find_element_by_xpath('//*[@id="post-view222588927949"]/div/div[3]').text
                print(review)
                driver.close()
                print(review_page_url)
                driver.get(review_page_url)
                print('debug5')
                review_range = driver.find_element_by_xpath(review_number_xpath).text.replace(',', '')
                print('debug6')
                review_range = review_range
                print('debug7')
                review_range = int(review_range)
                print('debug8')
                review_range = review_range // 10 + 2

                if review_range > 6: review_range = 6
                for k in range(1, review_range):
                    driver.get(review_page_url + '&page={}'.format(k))
                    #time.sleep(0.3)
                    for l in range(1, 11):
                        review_title_xpath = '//*[@id="reviewList"]/li[{}]/dl/dt/a'.format(l)
                        try:
                            driver.find_element_by_xpath(review_title_xpath).click()
                            #time.sleep(0.3)
                            review = driver.find_element_by_xpath('//*[@id="post-view222587986143"]/div/div[3]').text
                            # print('===================== =====================')
                            # print(title)
                            # print(review)
                            titles.append(title)
                            reviews.append(review)
                            driver.back()
                        except:
                            # print(l, '번째 review가 없다.')
                            break

            except:
                print('error')
        df_review_20 = pd.DataFrame({'title':titles, 'reviews':reviews})
        df_review_20.to_csv('./crawling_data/book_reviews_{}.csv'.format(1111, i))

except:
    print('totally error')
finally:
    driver.close()
# df_review = pd.DataFrame({'title':titles, 'reviews':reviews})
# df_review.to_csv('./crawling_data/reviews_{}.csv'.format(2020))