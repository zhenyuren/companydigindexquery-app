import pandas as pd
import streamlit as st
import random

def main():
    st.title('上市公司数字化转型指数查询')
    
    # 读取Excel文件
    df = pd.read_excel("专精特新小巨人企业数字化转型指数结果.xls")
    
    # 确保股票代码列是字符串类型
    if '股票代码' in df.columns:
        df['股票代码'] = df['股票代码'].astype(str)
    
    # 确保数据中包含需要的列
    required_columns = ['股票代码', '企业名称', '数字化转型指数']
    if not all(column in df.columns for column in required_columns):
        st.error(f'数据中缺少必要的列: {required_columns}')
        return

    # 初始化会话状态
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []
    if 'input_code' not in st.session_state:
        st.session_state.input_code = ''

    # 定义按钮点击回调函数
    def select_code(code):
        st.session_state.input_code = code
        # 直接在回调中执行查询
        result = df[df['股票代码'] == code]
        if not result.empty:
            st.session_state.current_result = result[required_columns]
            if code not in st.session_state.query_history:
                st.session_state.query_history.append(code)
        else:
            st.session_state.current_result = None

    # 股票代码输入框
    input_code = st.text_input('请输入股票代码', value=st.session_state.input_code, key='stock_input')
    # 更新会话状态
    if input_code != st.session_state.input_code:
        st.session_state.input_code = input_code
        st.session_state.current_result = None  # 输入变化时清除当前结果

    # 随机推荐股票代码
    if not df.empty and '股票代码' in df.columns:
        all_stock_codes = df['股票代码'].unique().tolist()
        num_to_recommend = min(10, len(all_stock_codes))
        recommended_codes = random.sample(all_stock_codes, num_to_recommend) if len(all_stock_codes) > 0 else []
        
        if recommended_codes:
            st.write("随机推荐股票代码:")
            cols = st.columns(5)
            for idx, code in enumerate(recommended_codes):
                col_idx = idx % 5
                with cols[col_idx]:
                    # 使用回调函数处理按钮点击
                    st.button(code, key=f"recommend_{code}", on_click=select_code, args=(code,))

    # 显示当前结果（如果有）
    if 'current_result' in st.session_state and st.session_state.current_result is not None:
        st.write("查询结果:")
        st.write(st.session_state.current_result)
    elif 'current_result' in st.session_state and st.session_state.current_result is None:
        st.warning('未找到该股票代码对应的记录')

    # 手动查询按钮
    if st.button('查询') and st.session_state.input_code:
        select_code(st.session_state.input_code)  # 复用回调函数

    # 历史查询记录
    if st.session_state.query_history:
        selected_code = st.selectbox('选择历史查询过的股票代码', st.session_state.query_history)
        if st.button('查询历史记录'):
            select_code(selected_code)  # 复用回调函数

if __name__ == '__main__':
    main()