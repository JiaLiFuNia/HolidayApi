import base64
import json
import os
import time

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)


def base64_api(uname, pwd, b64, typeid):
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(requests.post(url="http://api.ttshitu.com/predict", json=data).text)
    print(result)
    if result['code'] == "0":
        return result["data"]["result"]
    else:
        return False


def verify_code(url, cookies):
    uname = os.environ.get("TT_ACCOUNT")
    pwd = os.environ.get("TT_PWD")

    print(uname, pwd)
    print(cookies)
    try:
        img_res = requests.get(url=url, cookies=cookies, verify=False).content
        base64_data = base64.b64encode(img_res)
        b64 = base64_data.decode()
        verifycode = base64_api(uname=uname, pwd=pwd, b64=b64, typeid=3)
        return verifycode
    except Exception:
        return False


@app.route("/verificationCode", methods=['get'])
def secondClass():
    if request.form.get("time") is not None:
        time_stamp = request.form.get("time")
    else:
        time_stamp = str(int(time.time() * 1000))
    cookies = {'sid': ""}
    if request.cookies.get("sid") is not None:
        cookies['sid'] = request.cookies.get("sid")
    img_url = "http://dekt.htu.edu.cn/img/resources-code.jpg?" + time_stamp
    verify_res = verify_code(img_url, cookies)
    if verify_res:
        result = verify_res
    else:
        result = "abcd"
    return jsonify({
        'code': 200,
        'result': result,
    })


@app.route("/verifyCode", methods=['post'])
def main():
    img_url = request.form.get("url")
    type = request.form.get("type")
    if type == "dekt":
        verify_res = verify_code(img_url, request.cookies, request.headers)
        if verify_res:
            code = 200
            result = verify_res
        else:
            code = 400
            result = "验证码识别失败"
    else:
        code = 401
        result = "type参数错误"
    return jsonify({
        'code': code,
        'result': result,
    })


if __name__ == '__main__':
    app.run(debug=True)
    app.json.ensure_ascii = False
