

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib

from net_app.common.string_helper import gen_vcode


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def gen_vcode_msg(vcode, from_addr, to_addr):
    # 构建一个文本的mail对象
    text = '您好，欢迎注册测试网。您的验证码是：{}，有效期为20分钟, 请立即验证。'
    msg = MIMEText(text.format(vcode), 'plain', 'utf-8')
    msg['From'] = _format_addr('测试网<%s>' % from_addr)
    msg['To'] = _format_addr('新用户<%s>' % to_addr)
    msg['Subject'] = Header('测试网注册验证码', 'utf-8').encode()

    return msg

def send_vcode(smtp_server, from_addr, password, to_addr):
    # 构建一个 smtp 对象
    server = smtplib.SMTP(smtp_server, 25)
    # 设置一个调试级别
    server.set_debuglevel(1)
    # 登录
    server.login(from_addr, password)
    # 发送邮件
    vcode = gen_vcode()
    msg = gen_vcode_msg(vcode, from_addr, to_addr)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

    return vcode

if __name__ == '__main__':
    from_addr = 'xt269810408@163.com'
    to_addr = '269810408@qq.com'
    password = 'MNIPUFDOZJRGOUNJ'
    smtp_server = 'smtp.163.com'
    send_vcode(smtp_server, from_addr, password, to_addr)