import streamlit as st
import imaplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# 配置IMAP服务
imap_server = 'smtp.163.com'  # 你的IMAP服务器地址
username = st.secrets["my_email"]["email"]  # 你的邮箱账号
password =  st.secrets["my_email"]["password"]  # 你的邮箱密码

# 登录邮箱
def login_to_email():
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)
    return mail

# 读取邮箱中的邮件
def read_emails(label, keyword):
    mail = login_to_email()
    mail.select(label)
    _, msg_numbers = mail.search(None, 'ALL')
    email_list = []

    for num in msg_numbers[0].split():
        _, msg_data = mail.fetch(num, '(RFC822)')
        raw_email = msg_data[0][1].decode('utf-8')
        # 在这里你可以解析邮件内容，例如获取发件人、主题、内容等信息
        # 解析的方法取决于邮件的格式（纯文本或HTML）和你的需求
        email_list.append(parse_email(raw_email))

    mail.logout()
    return email_list

# 解析邮件内容
def parse_email(raw_email):
    # 在这里你可以编写解析邮件的代码，根据邮件格式提取发件人、主题、内容等信息
    # 示例：假设邮件格式为普通文本，发件人和主题在邮件的第一行，内容在之后的行
    lines = raw_email.split('\n')
    sender = lines[0]
    subject = lines[1]
    body = '\n'.join(lines[2:])
    return {'sender': sender, 'subject': subject, 'body': body}

def send_email(email, password)

    # 构建邮件主体
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email  # 收件人邮箱
    msg['Subject'] = 'hello_' + localtime
    
    # 邮件正文
    text = MIMEText('你好')
    msg.attach(text)
    
    # # 添加附件
    # with open(file_name, 'rb') as f:
    #     attachment = MIMEApplication(f.read())
    #     attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
    #     msg.attach(attachment)
    
    # 发送邮件
    try:
        smtp = smtplib.SMTP('smtp.163.com')
        smtp.login(email, password)
        smtp.sendmail(email, email, msg.as_string())
        smtp.quit()
        print('邮件发送成功')
    except smtplib.SMTPException as e:
        print('邮件发送失败，错误信息：', e)



# Streamlit应用界面
st.title('邮箱邮件发送应用')
if st.button('发送邮件'):
    send_email(email, password)
    
# label = st.selectbox('选择邮件标签', ['INBOX', 'Sent', 'Spam', 'Custom Label'])
# keyword = st.text_input('搜索关键字')
# if st.button('读取邮件'):
#     emails = read_emails(label, keyword)
#     for email in emails:
#         st.write(f'发件人：{email["sender"]}')
#         st.write(f'主题：{email["subject"]}')
#         st.write(f'内容：{email["body"]}')


