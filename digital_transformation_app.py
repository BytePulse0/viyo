import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np
# 移除对scipy和scikit-learn的依赖，仅使用基础库

# 设置页面配置
st.set_page_config(
    page_title="企业数字化转型指数分析平台",
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
    
    /* 指标卡片样式 */
    .metric-card {
        background-color: var(--card-bg);
        border-radius: var(--border-radius);
        padding: 20px;
        text-align: center;
        box-shadow: var(--shadow);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: var(--primary-color);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
    }
</style>""", unsafe_allow_html=True)

# 页面标题和副标题
st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>企业数字化转型指数分析平台</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #666; margin-bottom: 30px;'>数字化转型趋势分析与可视化系统</h3>", unsafe_allow_html=True)

# 简介卡片
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("""
        **欢迎使用数字化转型指数分析平台！**
        
        本平台提供全面的企业数字化转型指数分析功能，帮助您深入了解企业数字化发展趋势。
        
        - 📊 **数据可视化**：支持多种图表类型展示数字化转型指数趋势
        - 🔍 **智能查询**：快速搜索和筛选企业数据
        - 📈 **趋势分析**：查看历年数字化转型发展趋势
        - 📋 **数据下载**：支持多种格式的数据导出
        - 📊 **多维度分析**：从应用维度、技术维度等多个角度分析数据
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# 加载数据
@st.cache_data

def load_data():
    try:
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Excel文件路径 - 正确的文件名（不含空格）
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
        
        # 数据加载成功信息
        with st.container():
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.success(f"✅ 数据加载成功！")
            
            # 数据概览卡片
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-value'>{df.shape[0]}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-label'>总记录数</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            with col2:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-value'>{df.shape[1]}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-label'>数据字段</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            with col3:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-value'>{df['股票代码'].nunique()}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-label'>企业数量</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # 显示数据前5行预览
            st.markdown("<h3 style='margin-top: 30px;'>数据预览</h3>", unsafe_allow_html=True)
            st.dataframe(df.head(), use_container_width=True)
            
            # 显示数据列信息
            st.markdown("<h3 style='margin-top: 30px;'>数据字段说明</h3>", unsafe_allow_html=True)
            st.markdown(f"**可用字段：** {', '.join(df.columns.tolist())}")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
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
    
    # 获取唯一的股票代码和年份
    unique_stocks = sorted(data[stock_code_col].unique())
    unique_years = sorted(data[year_col].unique())
    
    # 用户查询界面
    st.sidebar.markdown("<div class='card'>", unsafe_allow_html=True)
    st.sidebar.header("🔍 查询条件")
    
    # 股票代码搜索和选择
    st.sidebar.markdown("<h4 style='margin-bottom: 10px;'>企业选择</h4>", unsafe_allow_html=True)
    stock_search = st.sidebar.text_input(
        "搜索企业（股票代码或名称）",
        value="",
        placeholder="输入股票代码或企业名称进行搜索...",
        help="支持按股票代码或企业名称进行搜索"
    )
    
    # 根据搜索词过滤股票代码
    filtered_stocks = unique_stocks
    if stock_search:
        # 创建股票代码和企业名称的映射
        stock_company_map = data.set_index('股票代码')['企业名称'].to_dict()
        filtered_stocks = [
            stock for stock in unique_stocks 
            if stock_search.lower() in str(stock).lower() or 
               stock_search.lower() in str(stock_company_map.get(stock, '')).lower()
        ]
        
        if not filtered_stocks:
            st.sidebar.info(f"未找到匹配 '{stock_search}' 的企业，请尝试其他搜索词。")
            filtered_stocks = unique_stocks
    
    # 股票代码选择
    selected_stock = st.sidebar.selectbox(
        "选择股票代码",
        options=filtered_stocks,
        format_func=lambda x: f"{x} - {data[data['股票代码'] == x]['企业名称'].iloc[0]}"
    )
    
    # 年份范围选择
    st.sidebar.markdown("<h4 style='margin-bottom: 10px; margin-top: 20px;'>时间范围</h4>", unsafe_allow_html=True)
    selected_years = st.sidebar.slider(
        "选择年份范围",
        min_value=int(min(unique_years)),
        max_value=int(max(unique_years)),
        value=(int(min(unique_years)), int(max(unique_years))),
        step=1
    )
    
    # 数据维度选择
    available_dimensions = [col for col in data.columns if col in ['应用维度', '技术维度', '数字化转型指数']]
    if available_dimensions:
        st.sidebar.markdown("<h4 style='margin-bottom: 10px; margin-top: 20px;'>数据维度</h4>", unsafe_allow_html=True)
        selected_dimensions = st.sidebar.multiselect(
            "选择要分析的数据维度",
            options=available_dimensions,
            default=available_dimensions,
            help="选择要查看的数据维度"
        )
    else:
        selected_dimensions = ['数字化转型指数']
    
    # 添加高级筛选选项
    st.sidebar.markdown("<h4 style='margin-bottom: 10px; margin-top: 20px;'>高级筛选</h4>", unsafe_allow_html=True)
    with st.sidebar.expander("⚙️ 高级筛选选项", expanded=False):
        # 添加数字化转型指数范围筛选
        min_index, max_index = st.sidebar.slider(
            "数字化转型指数范围",
            min_value=float(data['数字化转型指数'].min()),
            max_value=float(data['数字化转型指数'].max()),
            value=(float(data['数字化转型指数'].min()), float(data['数字化转型指数'].max())),
            step=0.1,
            help="筛选数字化转型指数在指定范围内的数据"
        )
        
        # 添加应用维度范围筛选
        if '应用维度' in data.columns:
            min_app, max_app = st.sidebar.slider(
                "应用维度范围",
                min_value=float(data['应用维度'].min()),
                max_value=float(data['应用维度'].max()),
                value=(float(data['应用维度'].min()), float(data['应用维度'].max())),
                step=0.1,
                help="筛选应用维度指数在指定范围内的数据"
            )
        
        # 添加技术维度范围筛选
        if '技术维度' in data.columns:
            min_tech, max_tech = st.sidebar.slider(
                "技术维度范围",
                min_value=float(data['技术维度'].min()),
                max_value=float(data['技术维度'].max()),
                value=(float(data['技术维度'].min()), float(data['技术维度'].max())),
                step=0.1,
                help="筛选技术维度指数在指定范围内的数据"
            )
    
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    
    # 过滤数据
    filtered_data = data[
        (data[stock_code_col] == selected_stock) &
        (data[year_col] >= selected_years[0]) &
        (data[year_col] <= selected_years[1]) &
        (data[digital_index_col] >= min_index) & 
        (data[digital_index_col] <= max_index)
    ]
    
    # 应用应用维度筛选
    if '应用维度' in data.columns:
        filtered_data = filtered_data[
            (filtered_data['应用维度'] >= min_app) & 
            (filtered_data['应用维度'] <= max_app)
        ]
    
    # 应用技术维度筛选
    if '技术维度' in data.columns:
        filtered_data = filtered_data[
            (filtered_data['技术维度'] >= min_tech) & 
            (filtered_data['技术维度'] <= max_tech)
        ]
    
    # 按年份排序
    filtered_data = filtered_data.sort_values(year_col)
    
    # 获取企业名称
    company_name = filtered_data[company_name_col].iloc[0] if not filtered_data.empty else "未知企业"
    
    # 显示查询结果
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header(f"📊 查询结果 - {company_name} ({selected_stock})")
    
    # 如果没有数据
    if filtered_data.empty:
        st.warning("⚠️ 在所选条件下没有找到数据。")
    else:
        # 数据概览卡片
        st.markdown("<h4 style='margin-bottom: 15px;'>数据概览</h4>", unsafe_allow_html=True)
        overview_cols = st.columns(4)
        
        # 计算统计指标
        total_records = len(filtered_data)
        avg_index = filtered_data['数字化转型指数'].mean()
        max_index = filtered_data['数字化转型指数'].max()
        min_index = filtered_data['数字化转型指数'].min()
        
        with overview_cols[0]:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{total_records}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-label'>数据条数</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with overview_cols[1]:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{avg_index:.2f}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-label'>平均指数</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with overview_cols[2]:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{max_index:.2f}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-label'>最高指数</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with overview_cols[3]:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{min_index:.2f}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-label'>最低指数</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # 显示详细数据
        st.markdown("<h4 style='margin-top: 30px; margin-bottom: 15px;'>详细数据</h4>", unsafe_allow_html=True)
        st.dataframe(filtered_data, use_container_width=True)
        
        # 统计分析部分
        st.markdown("<h4 style='margin-top: 30px; margin-bottom: 15px;'>📈 数据统计分析</h4>", unsafe_allow_html=True)
        
        # 描述性统计
        st.markdown("<h5 style='margin-bottom: 10px;'>描述性统计</h5>", unsafe_allow_html=True)
        stats_container = st.container()
        with stats_container:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            
            # 计算描述性统计
            desc_stats = filtered_data[['数字化转型指数', '应用维度', '技术维度']].describe().round(2)
            
            # 显示统计表格
            st.dataframe(desc_stats, use_container_width=True)
            
            # 添加统计解释
            st.markdown("""
            **统计指标说明：**
            - `count`: 有效数据条数
            - `mean`: 平均值
            - `std`: 标准差（数据离散程度）
            - `min`: 最小值
            - `25%`: 25%分位数
            - `50%`: 中位数
            - `75%`: 75%分位数
            - `max`: 最大值
            """)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # 趋势分析
        st.markdown("<h5 style='margin-top: 20px; margin-bottom: 10px;'>趋势分析</h5>", unsafe_allow_html=True)
        trend_container = st.container()
        with trend_container:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            
            # 计算趋势
            trend_results = []
            for dimension in ['数字化转型指数', '应用维度', '技术维度']:
                if dimension in filtered_data.columns:
                    # 计算增长率
                    data = filtered_data.sort_values('年份')
                    if len(data) >= 2:
                        start_val = data[dimension].iloc[0]
                        end_val = data[dimension].iloc[-1]
                        growth_rate = ((end_val - start_val) / start_val * 100) if start_val != 0 else 0
                        
                        # 使用numpy实现简单的线性回归
                        years = data['年份'].values
                        values = data[dimension].values
                        
                        # 计算线性回归参数
                        n = len(years)
                        if n < 2:
                            slope = 0
                            intercept = 0
                            r_value = 0
                        else:
                            # 计算均值
                            x_mean = np.mean(years)
                            y_mean = np.mean(values)
                            
                            # 计算斜率和截距
                            numerator = np.sum((years - x_mean) * (values - y_mean))
                            denominator = np.sum((years - x_mean) ** 2)
                            
                            if denominator != 0:
                                slope = numerator / denominator
                                intercept = y_mean - slope * x_mean
                                
                                # 计算相关系数
                                r_value = np.corrcoef(years, values)[0, 1]
                            else:
                                slope = 0
                                intercept = y_mean
                                r_value = 0
                        
                        p_value = np.nan  # 不计算p值
                        std_err = np.nan  # 不计算标准误差
                        
                        trend_results.append({
                            '维度': dimension,
                            '起始值': start_val,
                            '结束值': end_val,
                            '增长率(%)': growth_rate,
                            '趋势斜率': slope,
                            '相关系数(R²)': r_value ** 2,
                            '趋势显著性(p值)': p_value
                        })
            
            if trend_results:
                trend_df = pd.DataFrame(trend_results).round(4)
                st.dataframe(trend_df, use_container_width=True)
                
                # 趋势分析结论
                st.markdown("""
                **趋势分析结论：**
                - 正数增长率表示该维度呈上升趋势
                - 负数增长率表示该维度呈下降趋势
                - R²值越接近1，趋势越明显
                - p值小于0.05表示趋势具有统计学意义
                """)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # 可视化部分
        st.markdown("<h4 style='margin-top: 30px; margin-bottom: 15px;'>📊 数据可视化</h4>", unsafe_allow_html=True)
        
        # 图表选择
        chart_type = st.selectbox(
            "选择图表类型",
            options=["折线图", "条形图", "组合图", "多维度对比图", "雷达图", "箱线图", "散点矩阵图", "热力图"]
        )
        
        # 创建图表容器
        chart_container = st.container()
        with chart_container:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            
            if chart_type == "折线图":
                # 折线图 - 支持多维度
                fig = px.line(
                    filtered_data,
                    x=year_col,
                    y=selected_dimensions,
                    title=f"{company_name} 数字化转型指数趋势",
                    labels={year_col: "年份"},
                    markers=True
                )
                fig.update_layout(
                    xaxis_title="年份",
                    yaxis_title="指数值",
                    hovermode="x unified",
                    template="plotly_white",
                    legend_title="数据维度"
                )
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
                st.plotly_chart(fig, use_container_width=True)
                
            elif chart_type == "条形图":
                # 条形图 - 支持多维度
                fig = px.bar(
                    filtered_data,
                    x=year_col,
                    y=selected_dimensions,
                    title=f"{company_name} 数字化转型指数分布",
                    labels={year_col: "年份"},
                    color_discrete_sequence=px.colors.qualitative.Plotly
                )
                fig.update_layout(
                    xaxis_title="年份",
                    yaxis_title="指数值",
                    template="plotly_white",
                    legend_title="数据维度",
                    barmode='group'
                )
                st.plotly_chart(fig, use_container_width=True)
                
            elif chart_type == "组合图":
                # 组合图 - 折线图+散点图
                fig = px.scatter(
                    filtered_data,
                    x=year_col,
                    y=digital_index_col,
                    title=f"{company_name} 数字化转型指数趋势",
                    labels={year_col: "年份", digital_index_col: "数字化转型指数"},
                    trendline="ols",
                    trendline_color_override="red"
                )
                fig.update_layout(
                    xaxis_title="年份",
                    yaxis_title="数字化转型指数",
                    hovermode="x unified",
                    template="plotly_white"
                )
                st.plotly_chart(fig, use_container_width=True)
                
            elif chart_type == "多维度对比图":
                # 多维度对比图 - 使用子图
                if len(selected_dimensions) > 1:
                    fig = go.Figure()
                    colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
                    
                    for i, dimension in enumerate(selected_dimensions):
                        fig.add_trace(go.Bar(
                            x=filtered_data[year_col],
                            y=filtered_data[dimension],
                            name=dimension,
                            marker_color=colors[i % len(colors)]
                        ))
                    
                    fig.update_layout(
                        title=f"{company_name} 多维度数字化转型指数对比",
                        xaxis_title="年份",
                        yaxis_title="指数值",
                        template="plotly_white",
                        legend_title="数据维度",
                        barmode='group'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("请至少选择两个数据维度来查看多维度对比图。")
                    
            elif chart_type == "雷达图":
                # 雷达图 - 显示各维度的平均水平
                if len(selected_dimensions) > 1:
                    # 计算各维度的平均值
                    avg_values = filtered_data[selected_dimensions].mean()
                    
                    # 创建雷达图数据
                    radar_data = go.Scatterpolar(
                        r=avg_values.values.tolist(),
                        theta=avg_values.index.tolist(),
                        fill='toself',
                        name='平均水平'
                    )
                    
                    fig = go.Figure(data=[radar_data])
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, max(avg_values) * 1.2]
                            )),
                        title=f"{company_name} 数字化转型各维度平均水平",
                        template="plotly_white"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("请至少选择两个数据维度来查看雷达图。")
                    
            elif chart_type == "箱线图":
                # 箱线图 - 显示数据分布
                fig = px.box(
                    filtered_data,
                    y=selected_dimensions,
                    title=f"{company_name} 数字化转型指数分布箱线图",
                    labels={"value": "指数值", "variable": "数据维度"},
                    color_discrete_sequence=px.colors.qualitative.Plotly
                )
                fig.update_layout(
                    yaxis_title="指数值",
                    template="plotly_white",
                    legend_title="数据维度"
                )
                st.plotly_chart(fig, use_container_width=True)
                
            elif chart_type == "散点矩阵图":
                # 散点矩阵图 - 显示变量间关系
                if len(selected_dimensions) >= 2:
                    fig = px.scatter_matrix(
                        filtered_data,
                        dimensions=selected_dimensions,
                        title=f"{company_name} 数字化转型指数散点矩阵图",
                        color_discrete_sequence=['#3498db']
                    )
                    fig.update_layout(
                        template="plotly_white"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("请至少选择两个数据维度来查看散点矩阵图。")
                    
            elif chart_type == "热力图":
                # 热力图 - 显示数据相关性
                if len(selected_dimensions) >= 2:
                    # 计算相关性矩阵
                    corr_matrix = filtered_data[selected_dimensions].corr()
                    
                    # 创建热力图
                    fig = px.imshow(
                        corr_matrix,
                        title=f"{company_name} 数字化转型指数相关性热力图",
                        color_continuous_scale="RdBu_r",
                        text_auto=True,
                        aspect="auto"
                    )
                    fig.update_layout(
                        template="plotly_white"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 相关性解释
                    st.markdown("""
                    **相关性说明：**
                    - 数值范围：-1 到 1
                    - 1：完全正相关
                    - 0：无相关
                    - -1：完全负相关
                    - 颜色越深，相关性越强
                    """)
                else:
                    st.info("请至少选择两个数据维度来查看热力图。")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # 相关性分析部分
        if len(selected_dimensions) >= 2:
            st.markdown("---")
            st.markdown("<h4 style='margin-top: 30px; margin-bottom: 15px;'>🔗 维度间相关性分析</h4>", unsafe_allow_html=True)
            with st.container():
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                
                # 计算维度间相关性
                corr_matrix = filtered_data[selected_dimensions].corr()
                
                # 显示相关性表格
                st.dataframe(corr_matrix.style.format(precision=4).background_gradient(cmap='coolwarm'), use_container_width=True)
                
                # 相关性解释
                st.markdown("""
                **相关性解释：**
                - **强正相关 (0.7-1.0)**：两个维度变化方向完全一致
                - **中度正相关 (0.3-0.7)**：两个维度变化方向基本一致
                - **弱相关 (-0.3-0.3)**：两个维度之间关系不明显
                - **中度负相关 (-0.7-0.3)**：两个维度变化方向基本相反
                - **强负相关 (-1.0-0.7)**：两个维度变化方向完全相反
                """)
                
                st.markdown("</div>", unsafe_allow_html=True)

        # 趋势预测部分
        if len(filtered_data) >= 3:  # 需要至少3个数据点进行预测
            st.markdown("---")
            st.markdown("<h4 style='margin-top: 30px; margin-bottom: 15px;'>📈 趋势预测分析</h4>", unsafe_allow_html=True)
            with st.container():
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                
                # 选择要预测的维度
                predict_dimension = st.selectbox(
                    "选择要预测的维度",
                    options=selected_dimensions,
                    index=0
                )
                
                # 选择预测年份数量
                predict_years = st.slider(
                    "选择预测未来年份数量",
                    min_value=1,
                    max_value=5,
                    value=2,
                    step=1
                )
                
                # 准备数据
                X = filtered_data['年份'].values.reshape(-1, 1)
                y = filtered_data[predict_dimension].values
                
                # 使用numpy实现简单的线性回归
                X_flat = X.flatten()
                
                # 计算均值
                x_mean = np.mean(X_flat)
                y_mean = np.mean(y)
                
                # 计算斜率和截距
                numerator = np.sum((X_flat - x_mean) * (y - y_mean))
                denominator = np.sum((X_flat - x_mean) ** 2)
                
                if denominator != 0:
                    slope = numerator / denominator
                    intercept = y_mean - slope * x_mean
                    
                    # 计算R²值
                    predictions = slope * X_flat + intercept
                    residuals = y - predictions
                    ss_res = np.sum(residuals ** 2)
                    ss_tot = np.sum((y - y_mean) ** 2)
                    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
                else:
                    slope = 0
                    intercept = y_mean
                    r_squared = 0
                
                # 生成预测数据
                last_year = int(filtered_data['年份'].max())
                future_years = np.arange(last_year + 1, last_year + predict_years + 1)
                future_predictions = slope * future_years + intercept
                
                # 合并历史数据和预测数据
                historical_data = pd.DataFrame({
                    '年份': X.flatten(),
                    '类型': '历史数据',
                    predict_dimension: y
                })
                
                prediction_data = pd.DataFrame({
                    '年份': future_years.flatten(),
                    '类型': '预测数据',
                    predict_dimension: future_predictions
                })
                
                all_data = pd.concat([historical_data, prediction_data], ignore_index=True)
                
                # 创建预测图表
                fig = px.line(
                    all_data,
                    x='年份',
                    y=predict_dimension,
                    color='类型',
                    title=f"{company_name} {predict_dimension} 趋势预测",
                    color_discrete_map={'历史数据': '#3498db', '预测数据': '#e74c3c'},
                    markers=True
                )
                
                fig.update_layout(
                    xaxis_title="年份",
                    yaxis_title=predict_dimension,
                    template="plotly_white",
                    legend_title="数据类型"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 显示预测结果
                st.subheader("预测结果")
                prediction_table = pd.DataFrame({
                    '预测年份': future_years.flatten(),
                    f'预测{predict_dimension}': [round(val, 4) for val in future_predictions]
                })
                
                st.dataframe(prediction_table, use_container_width=True)
                
                # 模型性能指标
                st.subheader("模型性能")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("R² 系数", f"{r_squared:.4f}")
                with col2:
                    st.metric("斜率", f"{slope:.4f}")
                
                # 预测解释
                st.markdown("""
                **预测说明：**
                - 模型使用简单线性回归，基于历史数据预测未来趋势
                - R² 系数：衡量模型拟合度，越接近1拟合效果越好
                - 预测结果仅供参考，实际趋势可能受多种因素影响
                - 预测年限不宜过长，建议在2-3年内较为可靠
                """)
                
                st.markdown("</div>", unsafe_allow_html=True)

        # 数据下载功能
        st.markdown("<h4 style='margin-top: 30px; margin-bottom: 15px;'>数据下载</h4>", unsafe_allow_html=True)
        
        # 下载选项
        download_format = st.selectbox(
            "选择下载格式",
            options=["CSV", "Excel", "JSON"]
        )
        
        # 准备下载数据
        if download_format == "CSV":
            csv_data = filtered_data.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 下载当前查询结果 (CSV)",
                data=csv_data,
                file_name=f"{selected_stock}_{company_name}_数字化转型指数.csv",
                mime="text/csv"
            )
        elif download_format == "Excel":
            # 使用BytesIO保存Excel文件
            import io
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                filtered_data.to_excel(writer, index=False, sheet_name='数字化转型指数')
            buffer.seek(0)
            st.download_button(
                label="📥 下载当前查询结果 (Excel)",
                data=buffer,
                file_name=f"{selected_stock}_{company_name}_数字化转型指数.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        elif download_format == "JSON":
            json_data = filtered_data.to_json(orient='records', force_ascii=False)
            st.download_button(
                label="📥 下载当前查询结果 (JSON)",
                data=json_data,
                file_name=f"{selected_stock}_{company_name}_数字化转型指数.json",
                mime="application/json"
            )
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 多股票比较功能
    st.markdown("---")
    st.markdown("<h3 style='margin-bottom: 20px;'>📊 多股票对比分析</h3>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # 选择多个股票
        selected_stocks = st.multiselect(
            "选择要比较的企业（最多5家）",
            options=unique_stocks,
            max_selections=5,
            help="最多可选择5家企业进行对比分析"
        )
        
        if selected_stocks:
            # 定义维度列
            dimension_columns = ['数字化转型指数', '应用维度', '技术维度']
            
            # 选择对比维度
            comparison_dimension = st.selectbox(
                "选择对比维度",
                options=dimension_columns,
                index=0
            )
            
            # 选择年份范围
            comp_start_year, comp_end_year = st.slider(
                "选择对比年份范围",
                min_value=int(min(unique_years)),
                max_value=int(max(unique_years)),
                value=(int(min(unique_years)), int(max(unique_years))),
                step=1
            )
            
            # 创建股票代码和企业名称的映射
            stock_company_map = data.set_index('股票代码')['企业名称'].to_dict()
            
            # 准备对比数据
            comparison_data = []
            for stock_code in selected_stocks:
                company_name = stock_company_map[stock_code]
                company_data = data[(data['股票代码'] == stock_code) & 
                                 (data['年份'] >= comp_start_year) & 
                                 (data['年份'] <= comp_end_year)][['年份', comparison_dimension]]
                company_data = company_data.rename(columns={comparison_dimension: company_name})
                company_data['年份'] = company_data['年份'].astype(int)
                comparison_data.append(company_data)
            
            # 合并数据
            merged_data = comparison_data[0]
            for data_df in comparison_data[1:]:
                merged_data = pd.merge(merged_data, data_df, on='年份', how='outer')
            
            # 创建对比图表
            fig = go.Figure()
            for company_name in merged_data.columns[1:]:
                fig.add_trace(go.Scatter(
                    x=merged_data['年份'],
                    y=merged_data[company_name],
                    mode='lines+markers',
                    name=company_name,
                    connectgaps=True
                ))
            
            fig.update_layout(
                title=f"企业数字化转型 {comparison_dimension} 对比分析",
                xaxis_title="年份",
                yaxis_title=comparison_dimension,
                template="plotly_white",
                legend_title="企业名称"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 显示对比表格
            with st.expander("📋 详细对比数据", expanded=False):
                st.dataframe(merged_data.set_index('年份'), use_container_width=True)
                
            # 下载对比数据
            with st.expander("📥 下载对比数据", expanded=False):
                comp_download_format = st.selectbox(
                    "选择下载格式",
                    options=["CSV", "Excel"],
                    key="download_format_comp"
                )
                
                if comp_download_format == "CSV":
                    csv = merged_data.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="📊 下载对比数据 CSV",
                        data=csv,
                        file_name=f"多企业数字化转型对比_{comparison_dimension}_{comp_start_year}-{comp_end_year}.csv",
                        mime="text/csv"
                    )
                elif comp_download_format == "Excel":
                    import io
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        merged_data.to_excel(writer, index=False, sheet_name='对比数据')
                    output.seek(0)
                    st.download_button(
                        label="📊 下载对比数据 Excel",
                        data=output.getvalue(),
                        file_name=f"多企业数字化转型对比_{comparison_dimension}_{comp_start_year}-{comp_end_year}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        else:
            st.info("请选择至少一家企业进行对比分析。")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# 运行应用
if __name__ == "__main__":
    main()