import streamlit as st

def get_session_state():
    # 创建一个名为'session'的全局变量来保存用户交互数据
    if 'session' not in st.session_state:
        st.session_state['session'] = {
            'number_one_count': 0
        }
    return st.session_state['session']

def increment_number_one_count():
    session_state = get_session_state()
    session_state['number_one_count'] += 1

def main():
    session_state = get_session_state()

    st.title('Number Count App')
    st.write(f"Number 1 has been rolled {session_state['number_one_count']} times.")

    roll_button = st.button("Roll a number")
    if roll_button:
        # 在这里模拟得到一个1-10之间的随机数字
        random_number = 1  # 假设得到数字1
        if random_number == 1:
            increment_number_one_count()

if __name__ == '__main__':
    main()
