# - - - - - - - - - - - - - - - - - - - -#
# 실행 전 꼭 github의 README.md를 참고해주시기 바랍니다.
# - - - - - - - - - - - - - - - - - - - -#

import requests
from bs4 import BeautifulSoup as bs
homeURL = "http://www.ssodam.com/"
loginURL = 'http://www.ssodam.com/auth'
myContentURL = 'http://www.ssodam.com/me/contents/'

SSODAM_ID= 'jin2bbo'
SSODAM_PW= 'iLoveU'

waiting_for_delete = []

with requests.Session() as s:
    res = s.get(homeURL)
    cookies = res.headers['Set-Cookie']

    headers = {
        'Host': 'www.ssodam.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Origin': 'http://www.ssodam.com',
        'Referer': 'http://www.ssodam.com/',
        'Content-Length': '41',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': cookies,
        'X-CSRFToken': cookies.split("=")[1].split(";")[0]
    }
    data = {'id': SSODAM_ID, 'password': SSODAM_PW, 'auto': 'false'}

    tmp = s.post(loginURL, headers=headers, data=data)
    newCookie = tmp.headers['Set-Cookie'].split("=")[1].split(";")[0]
    newSession = tmp.headers['Set-Cookie'].split("sessionid=")[1].split(";")[0]

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Host': 'www.ssodam.com',
        'Cookie': 'pop=1; password=1; csrftoken=%s; sessionid=%s' % (newCookie, newSession),
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }

    for i in range(1, 99):
        print("[INFO] now in page", i)
        res = s.get(myContentURL+str(i), headers=headers)
        divs = bs(res.text, 'lxml').select("table > tbody > tr")
        # - - - - - - - - - - - - - - - - - - - -#
        # 위 divs는 여러개의 tr태그로 이루어진 하나의 array이며,
        # 각 tr은 6개의 td를 child로 가지고 있습니다.
        # 순서대로 id / 제목 / 글쓴이 / 추천수 / 날짜(mm/dd) / 조회수
        # 저는 추천수를 기준으로 걸러냈지만 응용하신다면 다른 조건을 걸 수도 있습니다.
        # - - - - - - - - - - - - - - - - - - - -#
        for j in divs:
            boom_up = bs(str(j), 'lxml').select('td:nth-of-type(4)')[0].get_text()
            if(int(boom_up) < 10):
                waiting_for_delete.append(bs(str(j), 'lxml').select('td:nth-of-type(1)')[0].get_text())
        if(res.status_code != 200):
            print("[INFO] searching finished")
            break

    # - - - - - - - - - - - - - - - - - - - -#
    # 이 아래부터 실제로 삭제가 진행됩니다. 
    # 정상적으로 삭제(status_code == 200)되지않는 글들은 
    # 아마도 '질문' 태그가 달려있을 것입니다. 이 글들은 못지웁니다.
    # blocking 방식(=한 번에 하나씩)이기 때문에 양이 많다면 시간이 좀 걸릴 수 있습니다.
    # 아래 print문으로 갯수를 확인해주세요. 넉넉히 1초에 하나라고 생각하고 대략 걸릴 시간을 짐작해보시길 바랍니다.
    # - - - - - - - - - - - - - - - - - - - -#
    print("total", len(waiting_for_delete))

    deletedCnt = 0
    notDeletedCnt = 0
    for i in waiting_for_delete :
        print("now delete id", i)
        res = s.get(homeURL + "delete/"+str(i))
        if (res.status_code != 200):
            print("id", i, "is not deleted. perhaps it would be tagged with '질문'")
            notDeletedCnt+=1
        else:
            deletedCnt += 1

    print("done.", deletedCnt, "deleted, ", notDeletedCnt, "not deleted.")

