# -*- coding: utf-8 -*-
import sys,os
import time
import json
import requests
import urllib2
from urllib import quote_plus
from urllib2 import urlopen
from urllib2 import Request
from urllib2 import URLError
from urllib import urlencode
from record import record
class DemoError(Exception):
    pass
#fetch token of asr
def fetch_token_asr():
    TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
    SCOPE = 'audio_tts_post'  # 有此scope表示有tts能力，没有请在网页里勾选

    #print("fetch token begin")
    params = {'grant_type': 'client_credentials',
              'client_id': "vQj80DGj0CGzBo86fOlnDIb8",
              'client_secret': "NvHV8cZeaI1974DFG4mRPO91gV2z5AGW"}
    post_data = urlencode(params)

    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()

    #print(result_str)
    result = json.loads(result_str)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not SCOPE in result['scope'].split(' '):
            raise DemoError('scope is not correct')
        #print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

#fetch token of unit
def fetch_token_unit():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=ruhiE2tlLCKbVKOEvtloGWhi&client_secret=vliHfSxjyRFDeC8BDwZQg5bOfju2n5CE'
    response = requests.get(host)
    # if response:
    #     print(response.json())
    access_token = response.json()["access_token"]
    return access_token

def baidu_unit(text_words):
    print("you say:")
    print(text_words.decode('UTF-8'))
    access_token = fetch_token_unit()
    url = 'https://unit.su.baidubce.com/rpc/2.0/unit/service/chat?access_token=' + access_token

    post_data = "{\"log_id\":\"UNITTEST_10000\",\
                \"version\":\"2.0\", \
                \"service_id\":\"S53337\",\
                \"skill_ids\":[\"1100085\"],\
                \"session_id\":\"\",\
                \"request\":{\"query\":\""+text_words+"\",\"user_id\":\"Justin1234990\"},\
                \"dialog_state\":{\"contexts\":{\"SYS_REMEMBERED_SKILLS\":[\"1100085\"]}}}"

    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=post_data, headers=headers)
    if response:
        #print (response.json())
        try:
            resp = response.json()['result']['response_list'][0]['action_list'][0]['say']
            print('robot said:')
            print(resp)
        except:
            print(response.json())
    return resp

def tts(words):
    token = fetch_token_asr()
    tex = quote_plus(words)  # 此处TEXT需要两次urlencode
    #print(tex)
    # 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
    # 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美 
    PER = 4
    # 语速，取值0-15，默认为5中语速
    SPD = 5
    # 音调，取值0-15，默认为5中语调
    PIT = 5
    # 音量，取值0-9，默认为5中音量
    VOL = 5
    # 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
    AUE = 6
    FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
    FORMAT = FORMATS[AUE]
    CUID = "123456PYTHON"
    TTS_URL = 'http://tsn.baidu.com/text2audio'
    params = {'tok': token, 'tex': tex, 'per': PER, 'spd': SPD, 'pit': PIT, 'vol': VOL, 'aue': AUE, 'cuid': CUID,
              'lan': 'zh', 'ctp': 1}
    data = urlencode(params)
    #print('test on Web Browser' + TTS_URL + '?' + data)

    req = Request(TTS_URL, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        headers = dict((name.lower(), value) for name, value in f.headers.items())
        has_error = ('content-type' not in headers.keys() or headers['content-type'].find('audio/') < 0)
    except  URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()
        has_error = True

    save_file = "error.txt" if has_error else 'result.' + FORMAT
    with open(save_file, 'wb') as of:
        of.write(result_str)

    if has_error:
        print("tts api  error:" + result_str)
    print("result saved as :" + save_file)

def asr(sound):
    DEV_PID = 80001
    ASR_URL = 'http://vop.baidu.com/pro_api'
    SCOPE = 'brain_enhanced_asr'  # 有此scope表示有asr能力，没有请在网页里开通极速版
    CUID = '123456PYTHON';
    # 采样率
    RATE = 16000;  # 固定值
    # PCM格式
    FORMAT = 'pcm'
    token = fetch_token_asr()
    #解析
    length = len(sound)
    if length == 0:
        raise DemoError('sound length read 0 bytes')

    params = {'cuid': CUID, 'token': token, 'dev_pid': DEV_PID}
    #测试自训练平台需要打开以下信息
    #params = {'cuid': CUID, 'token': token, 'dev_pid': DEV_PID, 'lm_id' : LM_ID}
    params_query = urlencode(params);

    headers = {
        'Content-Type': 'audio/' + FORMAT + '; rate=' + str(RATE),
        'Content-Length': length
    }

    url = ASR_URL + "?" + params_query
    #print("url is", url);
    #print("header is", headers)
    # print post_data
    req = Request(ASR_URL + "?" + params_query, sound, headers)
    timer = time.time
    try:
        begin = timer()
        f = urlopen(req)
        result_str = f.read()
        print("Request time cost %f" % (timer() - begin))
    except  URLError as err:
        print(err.reason)
        exit()
    print(result_str)
    return result_str[result_str.find("[")+2 : result_str.find(']')-1]

if __name__ == '__main__':
    #开启录音
    recorder = record()
    for data,idx in recorder:
        sound = b''.join(data)
        #语音转文字
        words = asr(sound)
        # #获取机器人的答复内容
        robot_say = baidu_unit(words)
        # #将机器人说的话，转换为语音
        tts(robot_say.encode('utf8'))
        #播放
        os.system('aplay -r 16000 -c 2 result.wav')


