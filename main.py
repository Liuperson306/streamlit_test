import streamlit as st

# 使用st.secrets读取敏感信息
email = st.secrets["my_email"]["email"]
email_password = st.secrets["my_email"]["password"]

# 在应用中使用读取的信息
st.write(f"API密钥：{email}")
st.write(f"邮箱密码：{email_password}")

