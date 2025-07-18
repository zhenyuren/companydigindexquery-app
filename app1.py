import pandas as pd
import streamlit as st
import random

def main():
    st.title('上市公司数字化转型指数查询')
    
<<<<<<< HEAD
    # 读取CSV文件
    df = pd.read_csv("C:/Users/Administrator/Desktop/test/含公司股票代码名称等.csv")
=======
    # 定义文件路径（使用相对路径，假设CSV文件与app1.py在同一目录）
    csv_file = "含公司股票代码名称等.csv"
>>>>>>> 4fb2b95cdc60af485d390a0619824fdfaf9886ba
    
    try:
        # 使用相对路径读取CSV文件
        df = pd.read_csv(csv_file)
        
        # 确保股票代码列是字符串类型（避免数值转换导致的前导零丢失）
        if '股票代码' in df.columns:
            df['股票代码'] = df['股票代码'].astype(str)
        
        # 检查必要列是否存在
        required_columns = ['股票代码', '企业名称', '数字化转型指数']
        if not all(column in df.columns for column in required_columns):
            st.error(f"数据中缺少必要的列: {required_columns}")
            return
            
    except FileNotFoundError:
        st.error(f"未找到文件：{csv_file}。请确保文件与app1.py在同一目录，或修改代码中的文件路径。")
        return
    except Exception as e:
        st.error(f"读取文件时发生错误：{str(e)}")
        return

<<<<<<< HEAD
    # 初始化会话状态
=======
    # 初始化查询历史（使用session_state持久化）
>>>>>>> 4fb2b95cdc60af485d390a0619824fdfaf9886ba
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []
    if 'input_code' not in st.session_state:
        st.session_state.input_code = ''

<<<<<<< HEAD
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
=======
    # 手动输入股票代码的输入框
    col1, col2 = st.columns([3, 1])
    with col1:
        input_code = st.text_input('请输入股票代码', placeholder="例如：600000")
    with col2:
        query_button = st.button('查询', use_container_width=True)

    # 执行查询逻辑
    if query_button:
        if not input_code:
            st.warning("请输入股票代码")
        else:
            result = df[df['股票代码'] == input_code]
            if not result.empty:
                st.success(f"查询到股票代码：{input_code} 的信息")
                st.dataframe(result[required_columns])
                # 添加到历史记录（去重）
                if input_code not in st.session_state.query_history:
                    st.session_state.query_history.append(input_code)
            else:
                st.warning(f"未找到股票代码为 {input_code} 的记录")

    # 历史查询功能（优化布局）
>>>>>>> 4fb2b95cdc60af485d390a0619824fdfaf9886ba
    if st.session_state.query_history:
        st.subheader("历史查询记录")
        selected_code = st.selectbox(
            "选择历史查询过的股票代码",
            st.session_state.query_history,
            format_func=lambda x: f"{x} - {df[df['股票代码']==x]['企业名称'].values[0] if not df[df['股票代码']==x]['企业名称'].empty else x}"
        )
        if st.button('查询历史记录'):
<<<<<<< HEAD
            select_code(selected_code)  # 复用回调函数
=======
            result = df[df['股票代码'] == selected_code]
            if not result.empty:
                st.dataframe(result[required_columns])
            else:
                st.warning(f"未找到股票代码为 {selected_code} 的记录")

    # 数据说明（可选）
    st.markdown("---")
    st.caption(f"数据更新时间：{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')} | 数据来源：{csv_file}")
>>>>>>> 4fb2b95cdc60af485d390a0619824fdfaf9886ba

if __name__ == '__main__':
    main()