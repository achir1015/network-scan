# network-scan  https://achir1015.github.io/network-scan/
用 Python + Scapy 發送 ARP 廣播來掃描，這才能取得真實的 IP 和 MAC 位址。
<img width="1252" height="590" alt="image" src="https://github.com/user-attachments/assets/2c758957-642a-4315-968a-c2b01bbbe08c" />
第一步：安裝 Python
去官網下載：https://www.python.org/downloads/
安裝時注意勾選這個選項（非常重要）：
☑ Add Python to PATH
第二步：安裝完後關閉 PowerShell 重新開啟，再執行：
pip install scapy flask flask-cors
第三步：同時安裝 Npcap（Windows 上 Scapy 需要它）
下載：https://npcap.com/#download

確認 Python 是否安裝成功的方法：
python --version
看到 Python 3.x.x 就代表安裝成功了。
<img width="1446" height="695" alt="image" src="https://github.com/user-attachments/assets/0ba09382-d70f-46e0-8b22-aee40f9a0fea" />
問題 1：Windows 的「App 執行別名」攔截了 python 指令
先關掉它：

開始 → 設定 → 應用程式 → 進階應用程式設定 → 應用程式執行別名
找到 python.exe 和 python3.exe，全部關閉


問題 2：Python 裝在 \bin 路徑，但 python.exe 其實不在那裡
正常 Python 安裝路徑是 Programs\Python\Python3xx\，你的路徑看起來不標準。
建議重新安裝 Python：

去 https://www.python.org/downloads/ 下載最新版
安裝時選 Customize installation
確認勾選：

   ☑ Add Python to PATH
   ☑ Install for all users

安裝完成後重新開啟 PowerShell
執行：

   python --version
看到版本號就成功了，再執行：
   python -m pip install scapy flask flask-cors

Windows 不需要 sudo，直接這樣做：
第一步：先確認 scan_server.py 放在哪裡
例如你放在「下載」資料夾，就執行：
cd C:\Users\achir\Downloads
如果放在桌面：
cd C:\Users\achir\Desktop
第二步：確認檔案在這裡
dir scan_server.py
看到檔案名稱就對了。
第三步：以系統管理員身分執行（Scapy 需要）
用系統管理員身分重新開啟 PowerShell，然後：
cd 你的檔案路徑
python scan_server.py

開啟系統管理員 PowerShell 方法：在開始功能表搜尋 PowerShell，對它按右鍵 → 以系統管理員身分執行
使用步驟提醒：

系統管理員 PowerShell → cd 到 scan_server.py 所在資料夾 → python scan_server.py
開啟新的 network_scan.html（舊的要關掉重開）
預設範圍已設為 192.168.6.1-254，按「掃描」即可
這次的改動：
後端（scan_server.py）加了 socket.gethostbyaddr(ip)，ARP 掃到裝置後立刻做反向 DNS 查詢，把主機名稱一起回傳給前端。
前端（network_scan.html）名稱欄的邏輯：
情況顯示查到名稱（例如 lpmos、iPad）粗體正常顯示查不到（例如 IP 攝影機、IoT 裝置）灰色斜體「未知」
IP 欄位則是獨立乾淨的 IP，不再重複顯示。
注意： scan_server.py 有更新，記得兩個檔案都重新下載，然後重啟後端再掃描。
<img width="627" height="674" alt="image" src="https://github.com/user-attachments/assets/f54b61c4-b85e-44ca-b083-76e8e3e6c83f" />
<img width="804" height="743" alt="image" src="https://github.com/user-attachments/assets/dd8d7ed3-bd8d-4012-b3d1-d62aacc22eba" />
<img width="685" height="640" alt="image" src="https://github.com/user-attachments/assets/d908a684-7474-41b6-9426-7cd74f3e2f32" />






