import streamlit as st
import requests
import base64
from PIL import Image

# --- 設定頁面配置 (必須是第一行指令) ---
st.set_page_config(
    page_title="AI 飲食熱量管家",
    page_icon="🍱",
    layout="wide" # 使用寬版面，讓左右兩欄更清楚
)

# --- 標題區 ---
st.title("🍱 AI 飲食熱量管家")
st.markdown("透過 **文字描述** 或 **拍照辨識**，輕鬆紀錄你的每日熱量攝取。")
st.divider() # 分隔線

# --- 定義 n8n 的 Webhook URL (之後我們會填入這裡) ---
# 目前先留空，等 n8n 架好後再回來填
N8N_WEBHOOK_URL = "https://n8n-production-092db.up.railway.app/webhook-test/calorie-ai" 

# --- 版面分割：左邊 (文字輸入) vs 右邊 (圖片辨識) ---
col1, col2 = st.columns([1, 1], gap="large")

# ==========================================
# 左欄：日常便當/菜色輸入 (NLP)
# ==========================================
with col1:
    st.subheader("🍚 日常餐點紀錄")
    st.info("輸入你吃的食物，AI 幫你估算熱量。")

    with st.form("meal_form"):
        food_text = st.text_input(
            "今天吃了什麼？", 
            placeholder="例如：一碗白飯、一份燙青菜、一塊炸排骨"
        )
        
        # 讓使用者選擇大概的份量或克數
        weight_gram = st.number_input(
            "總重量大約幾克？(若不確定可不填)", 
            min_value=0, 
            max_value=2000, 
            step=10,
            value=0
        )
        
        submitted_text = st.form_submit_button("計算並加入今日熱量")

        if submitted_text:
            if not food_text:
                st.warning("請先輸入食物名稱喔！")
            else:
                # --- 這裡之後會呼叫 n8n ---
                st.write("🔄 正在傳送給 AI 估算中...")
                
                # (模擬) 假設 n8n 回傳成功的樣子
                # 之後我們會把這段換成真實的 API 請求
                import time
                time.sleep(1) # 假裝運算 1 秒
                
                # 模擬結果
                mock_calories = 650 
                st.success(f"✅ 已紀錄：{food_text}")
                st.metric(label="估算熱量", value=f"{mock_calories} kcal")

# ==========================================
# 右欄：零食/營養標示辨識 (Vision)
# ==========================================
with col2:
    st.subheader("🍪 零食熱量掃描")
    st.info("拍下包裝背面的營養標示表，AI 幫你換算佔比。")

    uploaded_file = st.file_uploader("上傳照片", type=["jpg", "png", "jpeg"])
    
    # 預覽圖片
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="已上傳的圖片", use_container_width=True)

        st.markdown("#### 你打算吃多少？")
        portions = st.slider("選擇份數 (例如：半包是 0.5，整包是 1)", 0.1, 5.0, 1.0, 0.1)
        
        analyze_btn = st.button("分析圖片熱量")

        if analyze_btn:
            # --- 這裡之後會呼叫 n8n ---
            if N8N_WEBHOOK_URL == "":
                st.error("尚未設定 n8n Webhook URL，目前僅為介面展示。")
            else:
                st.write("🔄 AI 正在讀取營養標示...")
            
            # (模擬) 假設 AI 讀出來的結果
            # 之後這段會被真實資料取代
            mock_snack_cal_per_serving = 150 # 假設每份 150 卡
            total_snack_cal = int(mock_snack_cal_per_serving * portions)
            daily_target = 2000 # 成人每日基準
            
            percentage = (total_snack_cal / daily_target)
            if percentage > 1.0: percentage = 1.0 # 避免爆表
            
            st.divider()
            st.markdown(f"### 🔥 熱量分析結果")
            st.write(f"這 **{portions} 份** 的熱量約為： **{total_snack_cal} kcal**")
            
            st.write(f"佔成人每日建議攝取量 ({daily_target} kcal) 的：")
            st.progress(percentage, text=f"{percentage*100:.1f}%")
            
            if percentage > 0.2:
                st.warning("⚠️ 注意：這份零食熱量偏高，建議分次食用！")
            else:
                st.success("👍 沒問題：這在適量範圍內。")

# --- 底部 ---
st.markdown("---")
st.caption("Powered by Streamlit & n8n Workflow")