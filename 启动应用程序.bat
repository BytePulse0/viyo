@echo off
echo ====================================
echo 企业数字化转型指数查询与可视化应用
echo ====================================
echo.
echo 正在启动应用程序...
echo.

REM 获取当前脚本所在目录
set "SCRIPT_DIR=%~dp0"

REM 切换到脚本所在目录
cd /d "%SCRIPT_DIR%"

REM 启动Streamlit应用
echo 使用默认浏览器打开应用...
start "" "http://localhost:8501"

REM 启动Streamlit应用 - 使用正确的文件名
py -m streamlit run digital_transformation_app.py

echo.
echo 应用程序已启动！
echo 如果浏览器没有自动打开，请手动访问 http://localhost:8501
echo.
echo 按任意键退出...
pause > nul