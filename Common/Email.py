import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from Common.readConfig import readconfigs


class Send_Email:
    def __init__(self):
        readconf = readconfigs()
        self.smtpserver = readconf.get_emailconf('smtpserver')
        self.port = readconf.get_emailconf("port")
        self.username = readconf.get_emailconf('username')
        self.password = readconf.get_emailconf('password')
        self.sender = readconf.get_emailconf('sender')
        self.receivers = eval(readconf.get_emailconf('receivers'))
        self.mail_cclist=eval(readconf.get_emailconf('mail_cclist'))
        self.subject = readconf.get_emailconf('subject')
        file = readconf.get_emailconf('sendfile')
        self.sendfile = open(file, 'r', encoding="utf-8").read()


    def attach_setup(self):
        att = MIMEText(self.sendfile, 'html', 'utf-8')
        att['Content-Type'] = 'application/octet-stream'
        att['Content-Disposition'] = 'attachment;filename="Web_api_Report_result.html"'
        msg = MIMEText(self.sendfile, _subtype='html', _charset='utf-8')
        msg['Subject'] = self.subject
        msg['Cc'] = ','.join(self.mail_cclist)
        self.receivers.extend((self.mail_cclist))
        # msg['Content-Type'] = 'application/octet-stream'
        # 以附件的形式发送邮件
        # msg['Content-Disposition'] = 'attachment;filename="Web_api_Report_result.html"'

        # 添加邮件正文
        # msgRoot=MIMEMultipart('related')
        # 对于multipart类型，下面有三种子类型：mixed、alternative、related
        # multipart/mixed可以包含附件。
        # multipart/related可以包含内嵌资源。
        # multipart/alternative 纯文本与超文本共存
        msgRoot = MIMEMultipart("alternative")
        msgRoot.attach(msg)
        return msg.as_string()

    def send_email(self):
        try:
            smtp = smtplib.SMTP()
            print(self.smtpserver,self.port)
            smtp.connect(self.smtpserver, port=self.port)
            smtp.ehlo()
            # smtp.starttls()
            print(self.username, self.password)
            smtp.login(user=self.username, password=self.password)
            smtp.sendmail(from_addr=self.sender, to_addrs=self.receivers, msg=self.attach_setup())
            smtp.quit()
        except smtplib.SMTPException:
            print("邮件发送失败！！")
        else:
            print("邮件发送成功！！")


if __name__ == '__main__':
    se = Send_Email()
    se.send_email()
