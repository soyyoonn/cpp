from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  # By.~을 쓰기위해 import
import time
import csv
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# selenium 사용에 필요한 chromedriver.exe 파일 경로 지정
driver = webdriver.Chrome("./chromedriver.exe")
driver.set_window_position(0, 0)
driver.set_window_size(1500, 1200)

# 크롤링 하고자 하는 URL을 엽니다
driver.get('https://seereal.lh.or.kr/main.do#none')
time.sleep(1)

# 원하는 요소를 클릭하기 위해 XPATH를 찾아 설정해줍니다. - 부동산종합정보
loca = driver.find_element(By.XPATH, '//*[@id="upperMenu_estate"]/a')
loca.click()
time.sleep(1)

# 원하는 요소를 클릭하기 위해 XPATH를 찾아 설정해줍니다. - 공시가격
loca = driver.find_element(By.XPATH, '//*[@id="menu_estate260"]')
loca.click()
time.sleep(1)

# 원하는 요소를 클릭하기 위해 XPATH를 찾아 설정해줍니다. - 개별공시지가
loca = driver.find_element(By.XPATH, '//*[@id="privateprice"]/a')
loca.click()
time.sleep(1)

# 원하는 요소를 클릭하기 위해 XPATH를 찾아 설정해줍니다. - 서울특별시
loca = driver.find_element(By.XPATH, '//*[@id="sidoTable"]/tr[2]/td[1]')
loca.click()
time.sleep(1)

# 원하는 요소를 클릭하기 위해 XPATH를 찾아 설정해줍니다. - 강남구
loca = driver.find_element(By.XPATH, '//*[@id="sggTable"]/tr[2]/td[1]')
loca.click()
time.sleep(1)

result = []

# for i in range(1,6):
#     for j in range(1,4):
# 원하는 요소를 클릭하기 위해 XPATH를 찾아 설정해줍니다. - 동의 이름  원하는 동의 이름의 XPATH를 가져와 바꿔줍니다.

a = '//*[@id="emdTable"]/tr[4]/td[1]'  # 지역 번호 바꿔줘야댐 !!!!!!!!!!!!!!!!!!!!!@!@@#!#@!#@!#!@#!@#!#@#@!@$#@!$#@!$#@!$#@!$#!
area = driver.find_element(By.XPATH, a)
areatext = area.text  # 동의 이름
area.click()  # 텍스트를 클릭합니다
time.sleep(1)  # 정보가 로딩되기까지 기다려야 합니다.

local_address = driver.find_element(By.XPATH, '//*[@id="blockList"]')  # 지번이 들어있는 프레임
local_address_result = []
local_address_real = local_address.find_elements(By.TAG_NAME, 'li')  # li가 태그로 들어가있는것들을 리스트로 만들어준다.
for x in local_address_real:  # 리스트 안의 각각 li 태그마다 for문이 돔
    print(x)  # 각각의 li
    print(x.text, '12341123')  # li의 text 즉 지번
    x.click()  # 지번을 클릭함
    time.sleep(3)  # 지번에 대한 공시지가가 나오기까지 로딩 시간을 줌.

    # 원래는 다음 버튼을 눌러야 하는데 바로 다음버튼을 누르면 오류가 나서 이전버튼을 눌렀음.
    # prev_Button을 CSS SELECTOR 로 가져온 이유는 XPATH로 가져오면 표의 형태로 가져와서 숫자가 페이지마다 다르게 바뀌어서 CSS SELECTOR 형태로 가져옴
    # XPATH : //*[@id="pagingPrivatePriceList"]/ul/li[5]/a or //*[@id="pagingPrivatePriceList"]/ul/li[4]/a  or //*[@id="pagingPrivatePriceList"]/ul/li[6]/a
    # XPATH가 페이지의 수마다 달라지는걸 볼수 있음
    # 그래서 태그값인 CSS SELECTOR를 사용함
    prev_button = driver.find_element(By.CSS_SELECTOR, '#pagingPrivatePriceList > ul > li.prev > a')
    prev_button.click()
    time.sleep(1)
    while True:  # 마지막 페이지까지 이동하기 위해서 While문을 사용함
        try:
            prices = driver.find_element(By.XPATH, '//*[@id="privatepriceTbody"]') # 공시지가들을 가지고오기 위해서

            for pricetextlist in prices.text.split('\n'):  # pricetextlist 는 한 줄이고 prices.text는 표의 모든 텍스트이다.
                temp_list = pricetextlist.split(' ')  # 한줄의 정보를 공백을 가지고 스플릿하여 리스트로 만들어준다.
                temp_list.insert(0, areatext)  # temp_list의 가장 첫번재 인덱스에 어떤 동의 정보인지 넣어준다.
                local_address_result.append(temp_list)  # 지역 정보 결과에 temp_list를 추가함.
                print(local_address_result)
            button = driver.find_element(By.CSS_SELECTOR, '#pagingPrivatePriceList > ul > li.next')
            if "disabled" not in button.get_attribute("class"):
                nextbutton = button.find_element(By.TAG_NAME, 'a')  # li.next태그가 공간이 없는상태여서 a까지 선택해야 클릭이 가능했음.
                nextbutton.click()
                time.sleep(1)
            else:
                break # 멈추고 다음 지번으로 넘어감
        except Exception as e:
            print("에러")
            break
result += local_address_result
print(result)

with open('land_price_result_yeoksam.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    for x in result:
        w.writerow(x)
