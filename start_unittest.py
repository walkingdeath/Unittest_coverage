#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import unittest
from importlib import reload
import time
from scripts import  HTMLTestReportEN



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../src")))
reload(sys)


quick_lane = ''
def build_suite(lists):
    suite = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(lists, pattern='test_*.py', top_level_dir=None)
    for test_suite in discover:
        suite.addTests(test_suite)
    return suite
    # for test_suite in discover:
    #     for test_case in test_suite:
    #         suite.addTest(test_case)
    #     return suite

def emergency_vehicle_lane(signal):
        if signal == 'emergency':
            sys.exit(0)
        elif signal == 'unittest':
            current_time = time.strftime("%Y-%m-%d-%H-%M")

            # report_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), u"../unittest/scripts"))
            report_file = current_time + "-Test_Result.html"
            report_stream = open(report_file, "wb")
            all_cases = build_suite(".")
            runner = HTMLTestReportEN.HTMLTestRunner(stream=report_stream, title=u"自动化测试报告", description=u"用例执行情况如下：")
            rc = runner.run(all_cases)
            report_stream.close()
            # all_cases = build_suite(".")
            # runner = unittest.TextTestRunner()
            # rc = runner.run(all_cases)
            if len(rc.failures) > 0 or len(rc.errors) > 0:
                sys.exit(1)

def send_email(report_file):
    sender = "XXXXXX@qq.com"
    receiver = "XXXXXX@qq.com"
    smtpserver = "smtp.qq.com"
    #发送邮箱的账号密码,此处使用的是qq邮箱和第三方登录的授权码
    username = "XXXXXX@qq.com"
    password = "gfomcomojtuudijc"

    #定义邮件正文
    file = open(report_file,"rb")
    mail_body = file.read()
    file.close()

    msg = MIMEText(mail_body, _subtype="html", _charset="utf-8")
    msg["Subject"] = u"自动化测试报告"

    smtp = smtplib.SMTP_SSL("smtp.qq.com")
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print("Email has send out !")

if __name__ == "__main__":
    try:
        quick_lane = sys.argv[1]
        emergency_vehicle_lane(quick_lane)
    except  IndexError:
        print("please input parameter like 'python start_unittest.py xxx'")
