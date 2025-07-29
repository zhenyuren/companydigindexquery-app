import streamlit as st
import pandas as pd
import qrcode  # 新增二维码库导入
from io import BytesIO  # 新增字节流处理导入

# 设置页面配置
st.set_page_config(
    page_title="上市公司数字化转型指数查询",
    page_icon="📊",
    layout="wide"
)

# 读取数据（使用相对路径）
@st.cache_data  # 缓存数据加载，提高性能
def load_data():
    try:
        # 使用相对路径读取文件，确保文件与app1.py在同一目录下
        excel_file = pd.ExcelFile('含公司股票代码名称等.xlsx')
        df = excel_file.parse('Sheet1')
        # 确保数据类型正确
        df['股票代码'] = df['股票代码'].astype(int)
        return df
    except Exception as e:
        st.error(f"数据加载错误: {e}")
        return pd.DataFrame()

df = load_data()

# 页面标题和说明
st.title("上市公司数字化转型指数查询系统")
st.markdown("通过输入上市公司股票代码，查询其数字化转型指数相关信息")

# 创建搜索区域
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        stock_code = st.text_input(
            "请输入上市公司股票代码:",
            placeholder="例如: 300076",
            key="stock_code_input"
        )
    with col2:
        st.write("")  # 占位
        search_button = st.button("🔍 查询", use_container_width=True)

# 查询逻辑
if search_button or stock_code:
    if not stock_code:
        st.warning("请输入股票代码")
    else:
        try:
            stock_code = int(stock_code)
            result = df[df['股票代码'] == stock_code]
            
            if not result.empty:
                # 提取查询结果
                code = result['股票代码'].values[0]
                name = result['企业名称'].values[0]
                index_value = result['数字化转型指数'].values[0]
                
                # 使用卡片式布局展示结果
                st.success(f"已找到股票代码为 **{code}** 的公司信息")
                
                with st.container():
                    st.markdown("""
                    <style>
                        .info-card {
                            background-color: #f0f2f6;
                            border-radius: 10px;
                            padding: 1rem;
                            margin: 1rem 0;
                            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                        }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="info-card">
                        <h3 style="color: #1E88E5;">{name} ({code})</h3>
                        <p><b>股票代码:</b> {code}</p>
                        <p><b>企业名称:</b> {name}</p>
                        <p><b>数字化转型指数:</b> <span style="color: {'green' if index_value > 50 else 'red'};">{index_value}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                # 显示数据来源和更新时间（示例）
                st.markdown(f"数据来源: 含公司股票代码名称等.xlsx (更新于: {pd.Timestamp.now().strftime('%Y-%m-%d')})")
                
            else:
                st.error(f"未找到股票代码为 **{stock_code}** 的数据")
                
        except ValueError:
            st.error("请输入有效的整数股票代码（如 300076）")
        except Exception as e:
            st.error(f"查询过程中发生错误: {e}")

# 页面底部信息
st.markdown("---")
st.caption("© 2025 上市公司数字化转型研究中心 | 数据仅供参考")

# 新增二维码生成功能
def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

import os

# 添加应用访问二维码
if os.environ.get('STREAMLIT_ENV') == 'development':
    st.markdown("### 📱 移动端访问（开发环境）")
    st.write("扫描下方二维码访问应用：")
    app_url = "https://companydigindexquery-app-eqsmbnfht2xbqupfkqttsv.streamlit.app/"
    qr_image = generate_qr_code(app_url)
    st.image(qr_image, caption=f"应用二维码 (URL: {app_url})")