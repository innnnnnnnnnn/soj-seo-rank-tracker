import requests
from datetime import datetime
import time
import schedule

def check_google_ranking_api():
    # 使用您提供的 API Key 和 CSE ID
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
    log_entry = f"Date: {current_date}, Keyword: 清潔公司, Position of soj.com.tw: {position if position > 0 else 'Not found in top 30 results'}\n"
    
    with open("ranking_log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry)
    print(f"搜尋完成 - {log_entry}")

# 設定每天定時執行
schedule.every().day.at("08:00").do(check_google_ranking_api)

if __name__ == "__main__":
    print("程式已啟動，將每天自動檢查排名...")
    check_google_ranking_api()  # 立即測試
