import streamlit as st
import requests
import base64
import pandas as pd # 用來做一點資料處理
from PIL import Image

# --- 1. 設定頁面 ---
st.set_page_config(page_title="AI 熱量計算機", page_icon="🍱", layout="wide")

# --- 2. 初始化 Session State (這是記住清單的關鍵) ---
if 'food_log' not in st.session_state:
    st.session_state.food_log = [] # 建立一個空的食物清單

# --- 3. 設定 n8n 網址 (請填入你 Railway 的那串) ---
# 例如: https://n8n-production-xxxx.up.railway.app/webhook-test/calorie-ai
N8N_WEBHOOK_URL = "https://n8n-production-092db.up.railway.app/webhook-test/calorie-ai"

st.title("🍱 AI 熱量計算機")
st.caption("作業 5-2 Demo：Streamlit + n8n + Gemini Flash")

# --- 版面配置：上層輸入區 ---
col1, col2 = st.columns(2)

# ==========================================
# 左欄：文字輸入 (便當/正餐)
# ==========================================
with col1:
    st.subheader("🍚 新增餐點 (文字)")
    with st.form("text_form", clear_on_submit=True): # clear_on_submit 讓輸入框送出後自動清空
        food_input = st.text_input("吃了什麼？", placeholder="例如：一根雞腿")
        weight = st.number_input("重量(克)", value=100, step=10)
        submit_text = st.form_submit_button("計算並加入")
        
        if submit_text and food_input:
            with st.spinner("AI 正在估算中..."):
                try:
                    payload = {"type": "text", "content": food_input, "weight": weight}
                    response = requests.post(N8N_WEBHOOK_URL, json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        # 取得真正的熱量 (若 AI 沒回傳，預設 0)
                        real_calories = data.get('calories', 0)
                        advice = data.get('advice', '')

                        # 將資料加入暫存清單
                        new_item = {
                            "name": f"{food_input} ({weight}g)",
                            "calories": real_calories,
                            "note": advice,
                            "type": "text"
                        }
                        st.session_state.food_log.append(new_item)
                        st.success(f"已加入：{food_input} ({real_calories} kcal)")
                    else:
                        st.error("連線失敗，請檢查 n8n 是否有按 Execute")
                except Exception as e:
                    st.error(f"發生錯誤：{e}")

# ==========================================
# 右欄：圖片辨識 (零食)
# ==========================================
with col2:
    st.subheader("📸 新增零食 (拍照)")
    uploaded_file = st.file_uploader("上傳營養標示", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        # 顯示縮圖
        st.image(uploaded_file, width=200)
        if st.button("分析圖片並加入"):
            with st.spinner("AI 正在看圖..."):
                try:
                    bytes_data = uploaded_file.getvalue()
                    base64_str = base64.b64encode(bytes_data).decode('utf-8')
                    
                    payload = {"type": "image", "image_data": base64_str}
                    response = requests.post(N8N_WEBHOOK_URL, json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        snack_cal = data.get('snack_calories', 0)
                        
                        # 將資料加入暫存清單
                        new_item = {
                            "name": "圖片掃描零食",
                            "calories": snack_cal,
                            "note": "AI 影像辨識",
                            "type": "image"
                        }
                        st.session_state.food_log.append(new_item)
                        st.success(f"已加入零食：{snack_cal} kcal")
                    else:
                        st.error("連線失敗")
                except Exception as e:
                    st.error(f"錯誤：{e}")

# ==========================================
# 下方：今日飲食清單 (表格 + 刪除功能)
# ==========================================
st.divider()
st.subheader("📋 今日飲食紀錄表")

# 計算總熱量
total_cals = sum(item['calories'] for item in st.session_state.food_log)

# 顯示總熱量進度條
target_cal = 2000
col_sum, col_bar = st.columns([1, 3])
with col_sum:
    st.metric("今日總熱量", f"{total_cals} kcal", delta=f"剩餘 {target_cal - total_cals} kcal")
with col_bar:
    st.write("每日額度使用率")
    progress = min(total_cals / target_cal, 1.0)
    st.progress(progress)
    if progress >= 1.0:
        st.error("⚠️ 熱量超標啦！")

# 顯示清單表格 (手動繪製，為了放刪除按鈕)
if len(st.session_state.food_log) > 0:
    st.markdown("---")
    # 表頭
    h1, h2, h3, h4 = st.columns([3, 2, 3, 1])
    h1.markdown("**食物名稱**")
    h2.markdown("**熱量 (kcal)**")
    h3.markdown("**備註**")
    h4.markdown("**操作**")

    # 迴圈印出每一列
    # 使用 enumerate 取得索引 i，這樣我們才知道要刪除哪一個
    for i, item in enumerate(st.session_state.food_log):
        with st.container():
            c1, c2, c3, c4 = st.columns([3, 2, 3, 1])
            c1.write(item['name'])
            c2.write(f"{item['calories']}")
            c3.caption(item['note'])
            
            # 刪除按鈕
            # key 必須唯一，所以用 f"del_{i}"
            if c4.button("🗑️", key=f"del_{i}"):
                st.session_state.food_log.pop(i) # 從清單移除
                st.rerun() # 強制重新整理頁面，讓表格更新
else:
    st.info("目前還沒有紀錄，快去上面輸入食物吧！")