# 🍱 AI 飲食熱量管家 (AI Smart Calorie Tracker)

> **作業 5-2：n8n 自動化流程整合專案**
> 
> 這是一個結合 **Streamlit 前端介面** 與 **n8n 自動化後端** 的智慧熱量計算應用。透過整合 Google 最新 **Gemini 2.5 Flash** 模型，實現多模態（文字與圖片）的熱量估算功能。

## ✨ 專案功能

本專案解決了傳統熱量紀錄繁瑣的問題，提供以下核心功能：

* **🍚 自然語言估算**：輸入「一根炸雞腿」或「滷肉飯加蛋」，AI 自動分析並估算熱量。
* **📸 營養標示辨識**：上傳零食或包裝食品的營養標示圖，AI 自動讀取「每份熱量」，並根據使用者輸入的份數自動計算總和。
* **📊 每日熱量追蹤**：視覺化進度條顯示今日攝取量與剩餘額度。
* **📝 互動式清單**：支援即時查看已紀錄的食物，並提供刪除功能。
* **🤖 智慧建議**：AI 會針對輸入的食物提供簡短的營養建議。

## 🛠️ 技術架構

* **Frontend**: [Streamlit](https://streamlit.io/) (Python)
* **Backend / Automation**: [n8n](https://n8n.io/) (Self-hosted on Railway)
* **AI Model**: Google Gemini 2.5 Flash (via Google AI Studio)
* **Deployment**: Streamlit Cloud + Railway.app

---

## 🚀 部署教學 (Deployment Guide)

請依照以下順序完成專案部署。

### 1. 準備專案檔案
確保你的資料夾中包含以下三個核心檔案：
* `app.py`: Streamlit 主程式碼。
* `requirements.txt`: 專案依賴套件 (內容如下)。
    ```txt
    streamlit
    requests
    pandas
    pillow
    ```
* `workflow.json`: n8n 的自動化流程設定檔。

### 2. 上傳至 GitHub
1.  建立一個新的 GitHub Repository。
2.  將上述檔案 Push 到該 Repository。

### 3. 部署 Streamlit Web
1.  前往 [Streamlit Cloud](https://share.streamlit.io/) 並連結你的 GitHub 帳號。
2.  點擊 **"New app"**。
3.  選擇剛剛上傳的 Repository，Main file path 選擇 `app.py`。
4.  點擊 **Deploy**。
    * *注意：此時網頁可能會報錯，因為尚未設定正確的 n8n Webhook URL，請繼續往下做。*

### 4. 申請 Google AI Studio API Key
1.  前往 [Google AI Studio](https://aistudio.google.com/)。
2.  點擊 **Get API key** -> **Create API key**。
3.  複製這串 API Key，稍後會在 n8n 中使用。

### 5. 在 Railway 部署輕量版 n8n
為了讓 n8n 24小時運作，我們使用 Railway 進行部署：
1.  註冊/登入 [Railway.app](https://railway.app/)。
2.  點擊 **New Project** -> **Empty Project**。
3.  點擊 **+ Add a Service** -> **Docker Image**。
4.  輸入 Image 名稱：`n8nio/n8n:latest` 並按 Enter。
5.  等待部署完成 (綠燈) 後，點擊該服務方塊 -> **Settings**。
6.  找到 **Networking** 區塊，點擊 **Generate Domain**，取得你的 n8n 專屬網址 (例如：`https://n8n-xxx.up.railway.app`)。

### 6. 設定 n8n 流程
1.  打開剛剛產生的 n8n 網址，設定帳號密碼登入。
2.  點擊右上角選單 -> **Import from File**，選擇專案中的 `workflow.json`。
3.  **設定 API Key**：
    * 雙擊 **Gemini (Text)** 與 **Gemini (Vision)** 節點。
    * 將 URL 中的 `YOUR_KEY_HERE` 替換為步驟 4 取得的 Google API Key。
4.  **啟用流程**：
    * 將右上角的開關從 `Inactive` 切換為綠色的 **`Active`**。
5.  **取得 Webhook URL**：
    * 點擊 **Webhook** 節點 -> Webhook URLs -> **Production URL**。
    * 複製該網址 (路徑應包含 `/webhook/` 而非 `/webhook-test/`)。

### 7. 完成串接
1.  回到你的電腦，修改 `app.py` 中的 `N8N_WEBHOOK_URL` 變數，填入步驟 6 複製的網址。
2.  將修改後的 `app.py` 再次 Push 到 GitHub。
3.  回到 Streamlit 網頁重新整理，你的 AI 熱量計算機就完成了！🎉

---

### 📂 專案展示
sample1~3.jpg