import pyautogui
import time
import psutil
"""
这是一个模拟键盘鼠标，进行网页的请求
然后，通过导出浏览器历史记录获取url
"""
scroll_distance = 50
click_interval = 50
# 设置页面计数器和最大页面数量
page_count = 0
max_pages = 10
time.sleep(5)  # 确保你放到正确位置
while True:
    # 向下滚动 scroll_distance 像素
    pyautogui.scroll(-scroll_distance)
    # 等待一段时间，防止操作过快
    # time.sleep(0.05)
    # 获取鼠标当前位置
    x, y = pyautogui.position()
    # 点击鼠标左键
    pyautogui.click(x, y)
    # 页面计数器加 1
    page_count += 1
    # 判断是否达到最大页面数量
    if page_count >= max_pages:
        # 关闭所有浏览器窗口
        for proc in psutil.process_iter():
            try:
                if proc.name() == 'msedge.exe':
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        # 重置页面计数器
        page_count = 0
        # 等待一段时间，确保浏览器完全关闭
        time.sleep(1)
    # 等待 click_interval 像素再进行下一次点击
    time.sleep(click_interval / scroll_distance)
