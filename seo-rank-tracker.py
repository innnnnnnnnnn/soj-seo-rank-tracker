import requests
from datetime import datetime

# ✅ 替換為你的 LINE Notify Token
LINE_NOTIFY_TOKEN = "你的_LINE_Notify_Token"

def send_line_notify(message):
    """發送 LINE Notify 訊息"""
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"
    }
    data = {
        "message": message
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print("✅ LINE 訊息發送成功！")
    else:
        print(f"❌ LINE 訊息發送失敗: {response.text}")

def check_google_ranking_api():
    """查詢 Google 搜尋排名"""
    api_key = "AIzaSyCz7WA4Cpy0SnuYqqe0JLDQqY6fGSmb1l4"
    cse_id = "0776f01b6a61c4820"
    query = "清潔公司"
    target_domain = "soj.com.tw"
    position = 0

    # 檢查前 30 個結果 (分 3 次請求，每次 10 個)
    for start in [1, 11, 21]:
        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cse_id}&q={query}&start={start}&gl=tw&hl=zh-TW"
        response = requests.get(url)
        
        if response.status_code != 200:
            error_msg = f"API Error at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {response.text}\n"
            with open("ranking_log.txt", "a", encoding="utf-8") as f:
                f.write(error_msg)
            print(error_msg)
            send_line_notify(f"❌ SEO Rank Tracker API 錯誤：\n{response.text}")  # 發送 LINE 錯誤通知
            return
        
        data = response.json()
        for i, item in enumerate(data.get("items", []), 1):
            if target_domain in item["link"]:
                position = start + i - 1
                break
        if position > 0:
            break

    # 記錄結果
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result_message = f"📊 SEO Rank Tracker\n🔎 關鍵字：清潔公司\n📅 日期：{current_date}\n🌐 排名：{position if position > 0 else '未進入前 30 名'}"
    
    with open("ranking_log.txt", "a", encoding="utf-8") as f:
        f.write(result_message + "\n")

    print(f"搜尋完成 - {result_message}")
    send_line_notify(result_message)  # ✅ 發送 LINE 訊息

if __name__ == "__main__":
    print("程式已啟動，執行一次查詢...")
    check_google_ranking_api()
    print("查詢完成，程式結束。")
