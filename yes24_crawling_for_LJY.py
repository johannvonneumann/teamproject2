
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

df_titles = pd.DataFrame( columns = ['titles','writers','contents'])
titles = []
writers = []
contents = []

options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KO')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-gpu')
driver = webdriver.Chrome('./chromedriver',
                          options=options)

headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'}
driver.set_window_position(0, 0)
driver.set_window_size(1200, 1400)

driver.get('http://www.yes24.com/main/default.aspx')

elem = driver.find_element_by_xpath(' //*[@id="query"]')
elem.send_keys('소설') #크롤링하고 싶은 도서 검색어 입력
elem.submit()

#-------------크롤링 부분 함수 선언 -------------------------------------
def crawling():
    driver.get(url)
    book_title_xpath = '//*[@id="yesSchList"]/li[{}]/div/div[2]/div[2]/a[1]'.format(j)
    driver.find_element_by_xpath(book_title_xpath).click()
    time.sleep(2)
    title = driver.find_element_by_xpath('//*[@id="yDetailTopWrap"]/div[2]/div[1]/div/h2').text
    writer = driver.find_element_by_xpath('//*[@id="yDetailTopWrap"]/div[2]/div[1]/span[2]/span[1]').text
    content1 = ''
    content1 = driver.find_element_by_xpath('//*[@id="infoset_introduce"]').text
    content2 = ''
    try:
        content2 = driver.find_element_by_xpath('//*[@id="infoset_inBook"]/div[2]/div[1]/div[1]').text
    except:
        print('책속으로가 존재하지 않습니다.')

    content3 = ''
    try:
        content3 = driver.find_element_by_xpath('//*[@id="infoset_yesReivew"]/div[2]/div[2]').text
    except:
        print('예스24 리뷰가 존재하지 않습니다.')

    content4 = ''
    try:
        content4 = driver.find_element_by_xpath('// *[ @ id = "infoset_pubReivew"] / div[2] / div[1]').text

    except:
        print('출판사리뷰가 존재하지 않습니다.')

    content5 = ''
    try:
        content5 = driver.find_element_by_xpath('//*[@id="infoset_nomiCmt"]/div[2]').text
    except:
        print('출판사리뷰가 존재하지 않습니다.')
    content = content1 + ' ' + content2 + ' ' + content3 + ' ' + content4 + ' ' + content5

    titles.append(title)
    writers.append(writer)
    contents.append(content)
    (print('리스트에 추가 성공 12'))
# ______
try:
    for i in range(430,450):  # 400페이지부터 500 페이지까지. 예스24 소설부문은 1~939페이지 까지 있어요.
        url = 'http://www.yes24.com/Product/Search?domain=ALL&query=%EC%86%8C%EC%84%A4&page={}'.format(i)
        print(url)

        titles = []
        writers = []
        contents = []

        for j in range(1, 25):
            try:
                print(j + ((i - 1) * 24), '번째 도서 크롤링 중')
                crawling()
            except:
                pass

        df_yes24_book24 = pd.DataFrame({'titles': titles, 'writers': writers, 'contents': contents})
        df_yes24_book24.to_csv('./book_crawling_data/yes24_LJY_{}.csv'.format(i), index=False)

except:
    print('error')
    df_yes24_book24 = pd.DataFrame({'titles': titles, 'writers': writers, 'contents': contents})
    df_yes24_book24.to_csv('./book_crawling_data/yes24_LJY_errorsave_{}.csv'.format(i), index=False)
    print('에러파일을 저장했어요')
finally:
    driver.close()

