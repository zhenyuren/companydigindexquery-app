import pandas as pd
import streamlit as st

def main():
    st.title('上市公司数字化转型指数查询')
    
    # 直接使用pd.read_csv()读取CSV文件
    df = pd.read_csv("C:/Users/Administrator/Desktop/test/含公司股票代码名称等.csv")
    
    # 确保股票代码列是字符串类型
    if '股票代码' in df.columns:
        df['股票代码'] = df['股票代码'].astype(str)
    
    # 确保数据中包含需要的列
    required_columns = ['股票代码', '企业名称', '数字化转型指数']
    if not all(column in df.columns for column in required_columns):
        st.error(f'数据中缺少必要的列: {required_columns}')
        return

    # 初始化查询历史
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []

    # 提供手动输入股票代码的输入框
    input_code = st.text_input('请输入股票代码')

    if st.button('查询'):
        if input_code:
            result = df[df['股票代码'] == input_code]
            if not result.empty:
                st.write(result[required_columns])
                # 将查询过的股票代码添加到历史记录中
                if input_code not in st.session_state.query_history:
                    st.session_state.query_history.append(input_code)
            else:
                st.warning('未找到该股票代码对应的记录')

    # 使用下拉菜单选择历史查询过的股票代码
    if st.session_state.query_history:
        selected_code = st.selectbox('选择历史查询过的股票代码', st.session_state.query_history)
        if st.button('查询历史记录'):
            result = df[df['股票代码'] == selected_code]
            if not result.empty:
                st.write(result[required_columns])
            else:
                st.warning('未找到该股票代码对应的记录')

if __name__ == '__main__':
    main()
