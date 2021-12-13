from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import re




options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")# 'headless'라고 주면 크롤링하는 웹브라우저가 안떠.


options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')


driver = webdriver.Chrome('./chromedriver', options=options)

# 책 제목 xpath: '//*[@id="book_title_0"]/a[1]'
# 마지막 xpath(동페이지): '//*[@id="book_title_19"]/a[1]'
# 네티즌 리뷰 버튼 '//*[@id="container"]/div[5]/ul/li[3]/a' # 2일 때도 있어
# 네티즌 리뷰 글자 '//*[@id="container"]/div[5]/ul/li[3]/a/span'

# 첫 번째 리뷰: '//*[@id="reviewList"]/li[1]/dl/dt/a'
# 두 번째 리뷰: '//*[@id="reviewList"]/li[2]/dl/dt/a'
#  마지막 리뷰: '//*[@id="reviewList"]/li[10]/dl/dt/a'

# 작가1 xpath: //*[@id="category_section"]/ol/li[1]/dl/dd[1]/a[1]
# 작가2 xpath: //*[@id="category_section"]/ol/li[2]/dl/dd[1]/a[1]
# 작가20 xpath: //*[@id="category_section"]/ol/li[20]/dl/dd[1]/a[1]

netizen_review_button_xpath = '//*[@id="container"]/div[5]/ul/li[3]/a'
netizen_review_button_xpath_2 = '//*[@id="container"]/div[5]/ul/li[2]/a'

titles = []
writers = []
reviews = []

# url은 분야 > 추천도서까지 눌러놓은 상태(다른 항목일 경우 url만 바꿔서 돌려주면 됨)

for i in range(1,52):   # 추천도서 페이지(51페이지까지 있음)
    url = 'https://book.naver.com/category/index.naver?cate_code=110&tab=recommend&list_type=list&sort_type=salecount&page={}'.format(i)
    driver.get(url)
    try:
        for j in range(2,20):  # 책 제목 클릭(20개씩 있음)
            movie_title_xpath = '//*[@id="book_title_{}"]/a[1]'.format(j)
            title = driver.find_element_by_xpath(movie_title_xpath).text
            writer = driver.find_element_by_xpath('//*[@id="category_section"]/ol/li[{}]/dl/dd[1]/a[1]'.format(j+1)).text
            print(title)
            print(writer)
            driver.find_element_by_xpath(movie_title_xpath).click()
            time.sleep(1)
            if driver.find_element_by_xpath(netizen_review_button_xpath + '/span').text == '네티즌 리뷰':
                driver.find_element_by_xpath(netizen_review_button_xpath).click()
            elif driver.find_element_by_xpath(netizen_review_button_xpath_2 + '/span').text == '네티즌 리뷰':
                driver.find_element_by_xpath(netizen_review_button_xpath_2).click()
            else:
                print('네티즌 리뷰 버튼이 다른 곳에 있어요({}페이지 {}번 책)'.format(i, j))
                continue
            review_page_url = driver.current_url
            for l in range(1, 6):  # 리뷰는 최대 50개씩만 따오자
                try:
                    driver.get(review_page_url + '&page={}'.format(l))
                    for k in range(1, 11): # 리뷰 클릭하기
                        try:
                            driver.find_element_by_xpath('//*[@id="reviewList"]/li[{}]/dl/dt/a'.format(k)).click()
                            time.sleep(1)
                            driver.switch_to.window(driver.window_handles[1]) # 열린 새로운 창으로 이동
                            current_url = driver.current_url # 이동한 창의 url 가져오기
                            print(current_url)
                            driver.get(current_url)
                            driver.switch_to.frame('mainFrame')
                            try:
                                review = driver.find_element_by_xpath('//*[@id="postViewArea"]').text
                            except:
                                review = driver.find_element_by_class_name('se-main-container').text

                            print(review)
                            driver.switch_to.default_content()
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                        except:
                            print('error, 창이 안열려요')
                            continue
                except:
                     driver.switch_to.default_content()
                     driver.close()
                     driver.switch_to.window(driver.window_handles[0])
                     print('error')
                     continue
            driver.get(url)
    except:
        print('error, i don\'t know the reason' )
        continue
#
# print(titles)
# print(len(titles))
# print(writers)
# print(len(writers))

# driver.get(url)
# driver.switch_to.frame('mainFrame')
# reviews = driver.find_element_by_xpath().text
#
# driver.get('https://blog.naver.com/sallimnea/222179474804')
# driver.switch_to.frame('mainFrame')
# title = driver.find_element_by_xpath('//*[@id="SE-f3a18593-425e-11eb-a467-5984c566b50c"]/div/div').text
# print(title)
# driver.close()


# pretrain된 모델을 가져와서 적용시키자
# 자연어 모델은 그렇게 갖다가 쓰자. 벡터라이징이 이미 된 것을 갖다가 쓰자



# 리뷰 따오면 리뷰랑 작가, 책제목 맞춰서 append 해주자.
# 리뷰 어떻게 따올까..(iframe)
# 비공개글입니다..?
# 삭제되었거나 존재하지 않는 게시글입니다.(살인자들과의 인터뷰)38~39(2페이지)


# # for _ in range(5):
# url = 'https://book.naver.com/category/index.naver?cate_code=110&tab=recommend&list_type=list&sort_type=salecount&page=1'
# driver.get(url)
# # time.sleep(1)
# movie_title_xpath = '//*[@id="book_title_0"]/a[1]'
# title = driver.find_element_by_xpath(movie_title_xpath).text
# driver.find_element_by_xpath(movie_title_xpath).click()
# time.sleep(1.5)
# if driver.find_element_by_xpath(netizen_review_button_xpath + '/span').text == '네티즌 리뷰':
#     driver.find_element_by_xpath(netizen_review_button_xpath).click()
# elif driver.find_element_by_xpath(netizen_review_button_xpath_2 + '/span').text == '네티즌 리뷰':
#     driver.find_element_by_xpath(netizen_review_button_xpath_2).click()
# else: print('네티즌 리뷰 버튼이 다른 곳에 있어요')
# # time.sleep(1)
# # try: # 첫 번째 리뷰 클릭하기
# driver.find_element_by_xpath('//*[@id="reviewList"]/li[1]/dl/dt/a').click()
# time.sleep(5)
#
# driver.switch_to.window(driver.window_handles[1]) # 열린 새로운 창으로 이동
#
# current_url = driver.current_url # 이동한 창의 url 가져오기
# print(current_url)




# res = urlopen(current_url)
# soup = BeautifulSoup(res, 'html.parser')
# temp = soup.findAll("div", {"id":"postViewArea"})
# print(temp)
# for a in temp:
#     print(a.get_text())


# driver.switch_to.default_content()

# html = driver.page_source
# html = re.sub('[^가-힣 ]', '', html)
# print(html)
# print(len(html))


# html = urlopen('')
# bsobject = BeautifulSoup(html, 'html.parser')
#
# for link in bsobject.find_all('p'):
#     print(link.text.strip(), link.get('href'))


# review = driver.find_element_by_xpath('//*[@id="post-view221336615289"]').text
# reviews.append(review)
# titles.append(title)
# print('=========================================')
# print(titles)
# print(reviews)
    # except: print('리뷰가 없어요')







