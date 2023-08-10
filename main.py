import streamlit as st
import imaplib
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import email
from email.header import decode_header
import numpy as np
import random


username = st.secrets["my_email"]["email"]  # 邮箱账号
password =  st.secrets["my_email"]["password"]  # 邮箱密码

def send_email(email, password, array):
    # 构建邮件主体
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email  # 收件人邮箱
    msg['Subject'] = 'Number of submissions'
    
    # 邮件正文
    string = ''.join([str(element) for element in array])
    text = MIMEText(string)
    msg.attach(text)
     
    # 发送邮件
    try:
        smtp = smtplib.SMTP('smtp.126.com')
        smtp.login(email, password)
        smtp.sendmail(email, email, msg.as_string())
        smtp.quit()
        print('邮件发送成功')
    except smtplib.SMTPException as e:
        print('邮件发送失败，错误信息：', e)

def read_email(username, password):
    try:
        # 连接IMAP服务器
        mail = imaplib.IMAP4_SSL('imap.126.com')
        mail.login(username, password)
        mail.select('inbox')  # 选择收件箱
        # 搜索标题为"题目提交次数"的邮件
        _, msg_nums = mail.search(None, '(SUBJECT "Number of submissions")')

        if msg_nums[0]:
            latest_email_id = msg_nums[0].split()[-1]
            _, msg_data = mail.fetch(latest_email_id, '(RFC822)')
            raw_email = msg_data[0][1].decode('utf-8')

            # 解析邮件内容
            email_message = email.message_from_string(raw_email)
            subject, encoding = decode_header(email_message['subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding)

            sender = email.utils.parseaddr(email_message['from'])[1]
            body = ""
            # 提取邮件正文
            if email_message.is_multipart():
                for part in email_message.walk():
                    content_type = part.get_content_type()
                    if "text/plain" in content_type:
                        body = part.get_payload(decode=True).decode()
                        break
        # 将字符串中的每个数字字符转换为整数，并存入数组
        array = [int(char) for char in body]
        mail.logout()
        return array
    except Exception as e:
        st.error(f'出现错误：{e}')

def instrunction():
    st.subheader("Instructions: ")
    text1 = 'Please watch the short videos (duration 4~7s) of two animated talking heads. \
            You need to choose the talking head (the left or the right) that moves more naturally in terms of the full face and the lips. '
    text2 = '**Reminder 1**: Please **turn on the sound on your computer** while you are watching the videos. '
    text3 = '**Reminder 2**: Some of the videos (one or two) are qualification testing videos.\
             **Your task might get rejected if you make the choices randomly**.'
    st.write(text1)
    st.write(text2)
    st.write(text3)

def QA(data_face, data_lip, num):
    # 定义问题和选项
    question_1 = "Comparing the two full faces (Left and Right), which one looks more realistic?"
    options_1 = ["The Left one looks more realistic", "The Right one looks more realistic"]
    question_2 = "Comparing the lips of two faces, which one is more in sync with audio?"
    options_2 = ["The Left one is more in sync with audio", "The Right one is more in sync with audio"]

    # 显示问题并获取用户的答案
    answer_1 = st.radio(label=question_1, options=options_1, key=fr"button{num}.1")
    answer_2 = st.radio(label=question_2, options=options_2, key=fr"button{num}.2")

    # 以1/0数据保存
    ans1 = get_ans(answer_1)
    ans2 = get_ans(answer_2)

    # 保存结果到列表
    data_face[num - 1] = ans1
    data_lip[num - 1] = ans2

# 将用户的答案转化为1/0
def get_ans(answer_str):
    if "Left" in answer_str:
        return "1"
    elif "Right" in answer_str:
        return "0"
    
# 播放Video文件下的视频
def play_video(file_name,num):
    st.subheader(fr"Video{num}/12")
    # st.subheader(file_name)
    st.video(fr'merge_video2/{file_name}',start_time=0)
    st.write("Please answer the following questions, after you watch the video. ")

def data_collection(sender_email, sender_password, data_face, data_lip):
    # 发送内容
    data1 = ''.join(str(x) for x in data_face)
    data2 = ''.join(str(x) for x in data_lip)
    string = "face:" + data1 + "\n" + "lip:" + data2
    localtime = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
    # 打开文件并指定写模式
    file_name = "data_" + localtime + ".txt"
    file = open(file_name, "w")
    # 将字符串写入文件
    file.write(string)
    # 关闭文件
    file.close()

    # 构建邮件主体
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = sender_email  # 收件人邮箱
    msg['Subject'] = 'data_' + localtime

    # 邮件正文
    text = MIMEText('')
    msg.attach(text)

    # 添加附件
    with open(file_name, 'rb') as f:
        attachment = MIMEApplication(f.read())
        attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
        msg.attach(attachment)

    # 发送邮件
    try:
        smtp = smtplib.SMTP('smtp.126.com')
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, sender_email, msg.as_string())
        smtp.quit()
        print('邮件发送成功')
    except smtplib.SMTPException as e:
        print('邮件发送失败，错误信息：', e)

def page(num):
    st.write(f'这是第{num}页面')
    if not st.session_state.button_clicked:
        if st.button('Submit results'):
            st.write(num)
            st.session_state.button_clicked = True
            array[num]+=1
            send_email(username, password, array)
            st.write(array)
    if st.session_state.button_clicked == True:
        #st.balloons()
        st.success("Successfully submitted the results. Thank you for using it. Now you can exit the system.")


def page(random_num):
    # 注意事项
    instrunction()
    #file = open(r"file_list.txt", "r", encoding='utf-8') # 保证每次读取的文件顺序相同
    #file_list = file.readlines()
    #file.close()
    # max_num = len(file_list)

    if "button_clicked" not in st.session_state:
        st.session_state.button_clicked = False

    if "data_face" and "data_lip" not in st.session_state:
        # 初始化data变量
        data_face = [1 for x in range(0, 12)]
        data_lip = [1 for x in range(0, 12)]
    else:
        # 恢复data变量的状态
        data_face = st.session_state["data_face"]
        data_lip = st.session_state["data_lip"]

    for num in range(12):
        # 显示页面内容
        #play_video(file_list[num-1].rstrip(),num)
        st.write(f'这是第{num+1}题')
        QA(data_face, data_lip, num+1)

    if not st.session_state.button_clicked:
        if st.button("Submit results"):
            st.write(random_num)
            array[random_num]+=1
            send_email(username, password, array)
            st.write(array)
            data_collection(username, password, data_face, data_lip)
            st.session_state.button_clicked = True

    if st.session_state.button_clicked == True:
        st.balloons()
        st.success("Successfully submitted the results. Thank you for using it. Now you can exit the system.")
        st.write(data_face,data_lip)


if __name__ == '__main__':
    # array = [0,0,0,0,0,0,0,0,0,0]
    array = read_email(username, password)
    st.write(array)
    random_num = 0

    # if 'random_num' not in st.session_state:
    #     st.session_state.random_num = random.randint(0, 9)
    # if array[st.session_state.random_num] == 3:
    #     while True:
    #         st.session_state.random_num = random.randint(0, 9)
    #         if array[st.session_state.random_num] < 3 :
    #             break

    # random_num = st.session_state.random_num
    st.write(f'这是第{random_num+1}份试卷')
    page(random_num)


    
