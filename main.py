import streamlit as st

# 使用st.secrets读取敏感信息
email_password = st.secrets["my_email"]["password"]
api_key = st.secrets["api_keys"]["my_api_key"]

# 在应用中使用读取的信息
st.write(f"邮箱密码：{email_password}")
st.write(f"API密钥：{api_key}")
