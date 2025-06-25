import pandas as pd
import streamlit as st

def main():
    st.title('上市公司数字化转型指数查询')
    
    # 定义文件路径（使用相对路径，假设CSV文件与app1.py在同一目录）
    csv_file = "含公司股票代码名称等.csv"
    
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

    # 初始化查询历史（使用session_state持久化）
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []

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
    if st.session_state.query_history:
        st.subheader("历史查询记录")
        selected_code = st.selectbox(
            "选择历史查询过的股票代码",
            st.session_state.query_history,
            format_func=lambda x: f"{x} - {df[df['股票代码']==x]['企业名称'].values[0] if not df[df['股票代码']==x]['企业名称'].empty else x}"
        )
        if st.button('查询历史记录'):
            result = df[df['股票代码'] == selected_code]
            if not result.empty:
                st.dataframe(result[required_columns])
            else:
                st.warning(f"未找到股票代码为 {selected_code} 的记录")

    # 数据说明（可选）
    st.markdown("---")
    st.caption(f"数据更新时间：{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')} | 数据来源：{csv_file}")

if __name__ == '__main__':
    main()