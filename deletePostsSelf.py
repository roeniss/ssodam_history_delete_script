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

# - - - - - - - - - - - - - - - - - - - -#
# 삭제하고 싶은 글들의 일련번호를 아래에 기입해주세요.
# - - - - - - - - - - - - - - - - - - - -#
waiting_for_delete = [283726,332817,124592]

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

