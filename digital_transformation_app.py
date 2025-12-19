import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 设置页面配置
st.set_page_config(
    page_title="企业数字化转型指数分析",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""<style>
    /* 整体主题 */
    :root {
        --primary-color: #3498db;
        --secondary-color: #2ecc71;
        --accent-color: #e74c3c;
        --background-color: #f8f9fa;
        --text-color: #333333;
        --card-bg: #ffffff;
        --border-radius: 10px;
        --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* 页面背景 */
    body {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    /* 卡片样式 */
    .card {
        background-color: var(--card-bg);
        border-radius: var(--border-radius);
        padding: 20px;
        box-shadow: var(--shadow);
        margin-bottom: 20px;
    }
    
    /* 标题样式 */
    h1, h2, h3, h4 {
        color: var(--primary-color);
        margin-bottom: 20px;
    }
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background-color: var(--card-bg);
        padding-top: 20px;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 5px;
        border: none;
        padding: 8px 16px;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: #2980b9;
        color: white;
    }
    
    /* 数据表格样式 */
    .dataframe {
        border-radius: var(--border-radius);
        overflow: hidden;
    }
</style>""", unsafe_allow_html=True)

# 页面标题
st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>企业数字化转型指数分析</h1>", unsafe_allow_html=True)

# 加载数据
@st.cache_data
def load_data():
    try:
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Excel文件路径
        excel_file_path = os.path.join(current_dir, "两版合并后的年报数据_完整版.xlsx")
        
        # 检查文件是否存在
        if not os.path.exists(excel_file_path):
            st.error(f"数据文件不存在：{excel_file_path}")
            return None
        
        # 读取Excel文件
        df = pd.read_excel(excel_file_path)
        
        # 清理列名（去除空格并修复特定列名）
        df.columns = df.columns.str.strip()
        
        # 修复特定列名中的空格
        if '应 用维度' in df.columns:
            df = df.rename(columns={'应 用维度': '应用维度'})
        if '技术 维度' in df.columns:
            df = df.rename(columns={'技术 维度': '技术维度'})
        
        # 将股票代码转换为6位数字符串格式
        if '股票代码' in df.columns:
            df['股票代码'] = df['股票代码'].apply(lambda x: f"{int(x):06d}" if pd.notna(x) else x)
        
        return df
    except Exception as e:
        st.error(f"数据加载失败：{e}")
        st.exception(e)  # 显示详细错误信息
        return None

# 主函数
def main():
    # 加载数据
    data = load_data()
    
    if data is None:
        st.stop()
    
    # 定义关键字段
    stock_code_col = "股票代码"
    company_name_col = "企业名称"
    year_col = "年份"
    digital_index_col = "数字化转型指数"
    
    # 检查必要字段是否存在
    required_columns = [stock_code_col, company_name_col, year_col, digital_index_col]
    missing_columns = [col for col in required_columns if col not in data.columns]
    
    if missing_columns:
        st.error(f"数据中缺少必要字段：{missing_columns}")
        st.stop()
    
    # 创建股票-企业映射，确保每个股票代码对应唯一的企业名称
    # 对于每个股票代码，使用出现次数最多的企业名称
    stock_company_df = data.groupby(stock_code_col)[company_name_col].agg(lambda x: x.mode()[0]).reset_index()
    stock_company_map = stock_company_df.set_index(stock_code_col)[company_name_col].to_dict()
    
    # 用户查询界面 - 侧边栏
    st.sidebar.markdown("<div class='card'>", unsafe_allow_html=True)
    st.sidebar.header("🔍 查询条件")
    
    # 股票代码选择
    st.sidebar.markdown("<h4 style='margin-bottom: 10px;'>企业选择</h4>", unsafe_allow_html=True)
    
    # 创建股票代码-企业名称的选项列表
    stock_options = sorted(stock_company_map.keys())
    selected_stock = st.sidebar.selectbox(
        "选择股票",
        options=stock_options,
        format_func=lambda x: f"{x} - {stock_company_map[x]}",
        help="直接选择要查看的股票"
    )
    
    # 获取企业名称
    company_name = stock_company_map[selected_stock]
    
    # 年份选择
    st.sidebar.markdown("<h4 style='margin-bottom: 10px;'>年份选择</h4>", unsafe_allow_html=True)
    
    # 获取所有可用的年份，不管选择哪个企业或股票代码
    all_years = sorted(data[year_col].unique())
    
    # 默认选择所有年份
    selected_years = st.sidebar.multiselect(
        "选择年份（用于重点标注）",
        options=all_years,
        default=all_years,
        help="选择要在图表上重点标注的年份"
    )
    
    # 获取该股票的所有年份数据，不进行年份过滤
    # 使用股票代码来过滤数据，确保只显示该股票代码的所有数据
    filtered_data = data[
        (data[stock_code_col] == selected_stock)
    ].sort_values(year_col)
    
    # 显示查询结果
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header(f"📊 {company_name} ({selected_stock}) - 数字化转型指数分析")
    
    # 如果没有数据
    if filtered_data.empty:
        st.warning("⚠️ 在所选条件下没有找到数据。")
    else:
        # 数据概览
        st.markdown("<h3 style='margin-bottom: 20px;'>📋 数据概览</h3>", unsafe_allow_html=True)
        
        # 创建两列布局
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("<div style='background-color: #f0f9ff; padding: 15px; border-radius: 8px; text-align: center;'>", unsafe_allow_html=True)
            st.metric("企业名称", company_name)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div style='background-color: #e0f2fe; padding: 15px; border-radius: 8px; text-align: center;'>", unsafe_allow_html=True)
            st.metric("股票代码", selected_stock)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("<div style='background-color: #dbeafe; padding: 15px; border-radius: 8px; text-align: center;'>", unsafe_allow_html=True)
            if selected_years:
                year_range = f"{min(selected_years)} - {max(selected_years)}"
            else:
                year_range = "未选择年份"
            st.metric("年份范围", year_range)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col4:
            st.markdown("<div style='background-color: #eff6ff; padding: 15px; border-radius: 8px; text-align: center;'>", unsafe_allow_html=True)
            st.metric("数据点数量", len(filtered_data))
            st.markdown("</div>", unsafe_allow_html=True)
        
        # 数字化转型指数卡片
        st.markdown("<h3 style='margin-bottom: 20px; margin-top: 30px;'>📈 数字化转型指数</h3>", unsafe_allow_html=True)
        
        # 计算统计指标
        latest_index = filtered_data.sort_values(year_col, ascending=False).iloc[0][digital_index_col]
        max_index = filtered_data[digital_index_col].max()
        min_index = filtered_data[digital_index_col].min()
        avg_index = filtered_data[digital_index_col].mean()
        trend = "上升" if latest_index > avg_index else "下降"
        
        # 创建三列布局
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("<div style='background-color: #fef3c7; padding: 15px; border-radius: 8px; text-align: center;'>", unsafe_allow_html=True)
            st.metric("最新指数", f"{latest_index:.2f}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div style='background-color: #fde68a; padding: 15px; border-radius: 8px; text-align: center;'>", unsafe_allow_html=True)
            st.metric("最高指数", f"{max_index:.2f}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("<div style='background-color: #fcd34d; padding: 15px; border-radius: 8px; text-align: center;'>", unsafe_allow_html=True)
            st.metric("最低指数", f"{min_index:.2f}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col4:
            st.markdown("<div style='background-color: #fbbf24; padding: 15px; border-radius: 8px; text-align: center;'>", unsafe_allow_html=True)
            st.metric("平均指数", f"{avg_index:.2f}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # 历史指数折线图
        st.markdown("<h3 style='margin-bottom: 20px; margin-top: 30px;'>📊 历史指数折线图</h3>", unsafe_allow_html=True)
        
        # 确定要显示的指标列 - 只保留数字化转型指数
        y_columns = [digital_index_col]
        
        # 显示折线图
        fig = px.line(
            filtered_data,
            x=year_col,
            y=y_columns,
            title=f"{company_name} 数字化转型指数趋势",
            labels={year_col: "年份", "value": "指数值"},
            markers=True
        )
        
        # 对用户选择的年份进行重点标注
        for y_col in y_columns:
            # 为每个指标列添加重点标注
            highlight_data = filtered_data[filtered_data[year_col].isin(selected_years)]
            fig.add_scatter(
                x=highlight_data[year_col],
                y=highlight_data[y_col],
                mode='markers',
                marker=dict(
                    symbol='star',  # 使用星星标记
                    size=12,  # 增大标记尺寸
                    color='red'  # 使用红色标记
                ),
                name=f"{y_col} (重点标注)",
                showlegend=False  # 不在图例中显示
            )
        
        # 美化图表
        fig.update_layout(
            xaxis_title="年份",
            yaxis_title="指数值",
            hovermode="x unified",
            template="plotly_white",
            legend_title="指标",
            height=500
        )
        
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            dtick=1,
            range=[1999, 2023]  # 手动设置x轴范围，确保显示所有年份
        )
        
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 添加星星标记说明，与指标说明样式一致
        st.markdown("<p><strong>说明：</strong> 图表中红色星星标记表示您在侧边栏中选择的需要重点关注的年份。</p>", unsafe_allow_html=True)
        
        # 数字化转型指数详细统计
        st.markdown("<h3 style='margin-bottom: 20px; margin-top: 30px;'>📋 数字化转型指数详细统计</h3>", unsafe_allow_html=True)
        
        # 准备详细统计表格
        stats_table = filtered_data[['年份', '数字化转型指数']].copy()
        
        # 如果有应用维度和技术维度，也添加到表格中
        if '应用维度' in filtered_data.columns:
            stats_table['应用维度'] = filtered_data['应用维度']
        if '技术维度' in filtered_data.columns:
            stats_table['技术维度'] = filtered_data['技术维度']
        
        # 重置索引
        stats_table = stats_table.sort_values('年份').reset_index(drop=True)
        
        # 显示表格
        st.dataframe(stats_table.style.format({
            '数字化转型指数': '{:.2f}',
            '应用维度': '{:.2f}',
            '技术维度': '{:.2f}'
        }), use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# 运行应用
if __name__ == "__main__":
    main()