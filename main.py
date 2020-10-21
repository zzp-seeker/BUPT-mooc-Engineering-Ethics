from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,json,os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC
from random import choice
import threading,re

# print(os.getcwd())
Num = 1
mainUrl = ""
videoDoing = 0
bookDoing = 0
discussDoing = 0
homeworkDoing = 0
driver = webdriver.Chrome()

def login():
    print("login -> start")
    driver.get("https://grsbupt.yuketang.cn/")

    if not os.path.exists(os.path.join(os.getcwd(), "cookies.txt")):

        time.sleep(60)
        dictCookies = driver.get_cookies()
        jsonCookies = json.dumps(dictCookies)
        with open('cookies.txt', 'w') as f:
            f.write(jsonCookies)
        print('cookies保存成功！')

    with open('cookies.txt', 'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())
    print("登录cookies：", listCookies)

    for cookie in listCookies:  # 遍历添加cookie
        driver.add_cookie(cookie)
    driver.get("https://grsbupt.yuketang.cn/")

    print("login -> success")

def enterMainUrl():
    try:
        e = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//button/*[contains(string(), '学习空间')]")))
        e.click()

        e = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//div[@class='top']/*[contains(string(), '工程伦理')]")))
        e.click()

        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "/*[contains(string(), '第十三章习题')]")))

    finally:
        time.sleep(1)
        global mainUrl
        mainUrl = driver.current_url

def returnMainUrl():
    driver.get(mainUrl)
    try:
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "/*[contains(string(), '第十三章习题')]")))
    except:
        print("return error")
    finally:
        time.sleep(3)


def video():
    print("video learning -> start")

    zero = "//div[@class='leaf-detail']/div/i[contains(@class,'icon--shipin')]/../..//div[contains(@class,'progress-wrap')]/*[contains(string(), '未开始')]"
    little = "//div[@class='leaf-detail']/div/i[contains(@class,'icon--shipin')]/../..//div[contains(@class,'progress-wrap')]/div/span[contains(string(), '%')]"

    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, zero + "|" + little)))
        time.sleep(1)
    except:
        pass
    es = driver.find_elements_by_xpath(zero + "|" + little)
    l = len(es)
    print("待学习视频数量:",len(es))

    for i in range(l):
        global videoDoing # 修改全局变量
        print("正在播放的视频序号：",i)
        try:
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, zero + "|" + little)))
        except:
            pass
        t = driver.find_elements_by_xpath(zero + "|" + little)
        if(videoDoing >= len(t)) : break
        t[videoDoing].click()
        videoDoing += 1

        try:


            spbtn = WebDriverWait(driver, 100).until(EC.presence_of_element_located(
                (By.XPATH, '//div[@id="video-box"]//xt-speedvalue')))

            ts = '''var cb = document.evaluate("//div[@id='video-box']//xt-speedvalue", document).iterateNext();
                        cb.addEventListener("mouseover", function( event ) {
                            console.log("zzp");
                            setTimeout(function() {
                    document.getElementsByClassName("xt_video_player_common_list")[0].firstChild.click();
                    }, 500);})'''

            time.sleep(10)

            driver.execute_script(ts)

            time.sleep(2)

            AC(driver).move_to_element(spbtn).move_by_offset(-1,-1).move_by_offset(1,1).\
                move_by_offset(-1,1).move_by_offset(1,-1).perform()
        except:
            print("speed error")

        try:
            WebDriverWait(driver, 10000).until(
                EC.presence_of_element_located((By.XPATH, "//xt-currenttime[@style='width: 100%;']")))
        except:
            print("video error")

        videoDoing -= 1
        returnMainUrl()

    print("video learning -> end")

def book():
    print("book -> start")
    unreadBook = "//div[@class='leaf-detail']/div/i[contains(@class,'icon--tuwen')]/../..//div[contains(@class,'progress-wrap')]/*[contains(string(), '未读')]"
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, unreadBook)))
        time.sleep(1)
    except:
        pass
    es = driver.find_elements_by_xpath(unreadBook)
    l = len(es)
    print("待阅读书页面数量:", len(es))

    for i in range(l):
        global bookDoing
        print("正在阅读书目序号：", i)
        try:
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, unreadBook)))
        except:
            pass
        t = driver.find_elements_by_xpath(unreadBook)
        if (bookDoing >= len(t)): break
        t[bookDoing].click()
        bookDoing += 1
        try:
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'progress-wrap')]/*[contains(string(), '已读')]")))
            time.sleep(5)
        except:
            print("book error")

        bookDoing -= 1
        returnMainUrl()


    print("book -> end")

def discuss():
    print("discuss -> start")
    undiscussed = "//div[@class='leaf-detail']/div/i[contains(@class,'icon--taolun1')]/../..//div[contains(@class,'progress-wrap')]/*[contains(string(), '未发言')]"
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, undiscussed)))
        time.sleep(1)
    except:
        pass
    es = driver.find_elements_by_xpath(undiscussed)
    l = len(es)
    print("待讨论页面数量:", len(es))

    for i in range(l):
        global discussDoing
        print("正在讨论序号：", i)
        try:
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, undiscussed)))
        except:
            pass
        t = driver.find_elements_by_xpath(undiscussed)
        if (discussDoing >= len(t)): break
        t[discussDoing].click()
        discussDoing += 1

        try:
            textarea = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, "//textarea[contains(@class, 'el-textarea__inner')]")))
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'cont_detail')]")))
            time.sleep(0.5)
            s = choice(driver.find_elements_by_xpath("//div[contains(@class,'cont_detail')]")).get_attribute('innerText')
            print("输入内容：",s)
            textarea.send_keys(s)
            time.sleep(0.5)
            driver.find_element_by_xpath("//button[contains(@class,'submitComment')]").click()
            time.sleep(1.5)
        except:
            print("discuss error")

        discussDoing -= 1
        returnMainUrl()

    print("discuss -> end")


def homework():
    print("homework -> start")
    ansAll = ""
    numDict={"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9,"十":1}
    radioDict={"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7}

    if os.path.exists(os.path.join(os.getcwd(), "answer.txt")):
        with open('answer.txt', 'r', encoding='utf8') as f:
            ansAll = f.read()
    ansList = ansAll.split("~ZPEND~")

    homeworkSpan = "//div[@class='leaf-detail']/div/i[contains(@class,'icon--zuoye')]/../..//div[contains(@class,'progress-wrap')]/*[not(contains(string(), '已完成'))]/../../../div/span"
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, homeworkSpan)))
        time.sleep(1)
    except:
        pass
    es = driver.find_elements_by_xpath(homeworkSpan)
    l = len(es)

    for i in range(l):
        global homeworkDoing
        try:
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, homeworkSpan)))
        except:
            pass
        t = driver.find_elements_by_xpath(homeworkSpan)

        if (homeworkDoing >= len(t)): break
        title = t[homeworkDoing].get_attribute('innerText')
        t[homeworkDoing].click()


        print("开始做：",title)
        numStr = re.sub('[第章作业习题]', '', title).strip()
        st = ""
        for j in range(len(numStr)):
            st += str(numDict[numStr[j]])
        index = int(st)-1
        if(numStr=='十'): index = 9

        anss = ansList[index].split("-")
        print(anss)
        if not int(anss[0].split("#")[-1]) == len(anss) - 1:
            print(i, ":error", int(anss[0].split("#")[-1]), " ", len(anss))

        homeworkDoing += 1
        for j in range(len(anss) - 1):

            try:
                WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//div[@class='aside-body']/div/ul/li["+str(j+1)+"]")))
            except:
                pass
            jNode = driver.find_element_by_xpath("//div[@class='aside-body']/div/ul/li["+str(j+1)+"]")
            jNode.click()

            WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='item-type' and contains(string(),'"+str(j+1)+"')]")))

            time.sleep(0.05)

            if "A" in anss[j+1] or "B" in anss[j+1] or "C" in anss[j+1] or "D" in anss[j+1] or "E" in anss[j+1]:
                for k in anss[j+1]:
                    toSelect = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//ul[contains(@class,'list-unstyled')]/li["+str(radioDict[k])+"]//label")))
                    toSelect.click()

            elif "0" in anss[j+1] or "1" in anss[j+1]:
                toSelect = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.XPATH, "//ul[contains(@class,'list-unstyled-radio')]/li["+str(2-int(anss[j+1]))+"]/label//span[@class='radioInput']")))
                toSelect.click()

            elif "#" in anss[j+1]: # 以zp#开头 不同空之间以#分隔
                blankList = anss[j+1].split('#')
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input")))
                toInput = driver.find_elements_by_xpath("//input")
                for k in range(len(blankList)-1):
                    toInput[k].send_keys(blankList[k+1])

            else:
                driver.switch_to.frame("ueditor_0") # 切换frame
                toInput = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//body[@class='view']/p")))
                toInput.send_keys(anss[j + 1])
                driver.switch_to.default_content()

            time.sleep(0.05)
            middleButton = "//div[contains(@class,'el-col-8') and position()=2]//button[contains(@class,'el-button')]/span"
            toSubmit = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, middleButton)))
            loop = 0
            while loop < 20:
                if not '已' in driver.find_element_by_xpath(middleButton).get_attribute('innerText'):
                    toSubmit.click()
                    try:
                        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                            (By.XPATH, "//button[contains(@class,'el-button')]/span[contains(string(),'已')]")))
                    except:
                        pass
                else: break
                loop += 1
            time.sleep(0.1)

        homeworkDoing-=1
        returnMainUrl()

    print("homework -> end")

def f():
    login()
    enterMainUrl()

    homework()
    book()
    discuss()
    video()



def main():
    for i in range(Num):
        t = threading.Thread(target=f)
        time.sleep(1)
        t.start()

if __name__ == '__main__':
    main()

# driver.close()