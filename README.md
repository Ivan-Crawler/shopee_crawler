爬蟲說明文件
=========

<img src="https://imgur.com/NVCBYfI.png"/>

此專案目的只為了學術技術分享，請勿拿來從事不法行為，違者自行負起法律責任

```
貼心提醒：

刑法第三百五十八條：「 無故輸入他人帳號密碼、破解使用電腦之保護措施或利用電腦系統之漏洞，而入侵他人之電腦或其相關設備者，處三年以下有期徒刑、拘役或科或併科十萬元以下罰金。 」 刑法第三百六十三條：「第三百五十八條至第三百六十條之罪，須告訴乃論。」
```

目錄
=================
* [使用方式](#使用方式)
    * [程式碼執行方式](#程式碼執行方式)
    * [終端機執行方式](#終端機執行方式)
* [檔案說明](#檔案說明)
    * [PTT爬蟲範例.py](#PTT爬蟲範例py)
    * [Ivan_ptt.py](#Ivan_pttpy)
    
    使用方式
=================

程式碼執行方式
-----------
```
Crawler(keyword = '關鍵字名稱', page='想爬幾頁').shopee()
```

範例
```
Crawler(keyword = '手機殼', page=50).shopee()
```

終端機執行方式
-----------
1. 切換到Ivan_shopee.py的檔案路徑下。
```
cd 檔案位置
```
<img src="https://imgur.com/Y9VYwPh.png"/>

2. 啟動Ivan_shopee.py，並按照指示輸入相關資訊。
```
python Ivan_shopee.py
```

3. 開始自動爬蟲，爬蟲完成後，在Ivan_shopee.py的檔案路徑下就會出現「您輸入的關鍵字_商品資料.csv」與「您輸入的關鍵字_留言資料.csv」檔案，過程中的爬蟲，為了避免執行到一半有任何意外導致程式中止，因此每爬完一頁都會存檔。
<img src="https://imgur.com/Puf5JcA.png"/>




檔案說明
=================

PTT爬蟲範例.py
-----------
範例使用方式。講述如何使用Ivan_shopee.py檔案。

Ivan_shopee.py
-----------
shopee爬蟲工具主程式。

Windows/chromedriver.exe
-----------
Windows系統的chrome模擬器，64位元，若無法執行請自行另外做調整[下載](https://chromedriver.chromium.org/downloads)。

Windows/phantomjs.exe
-----------
Windows系統的phantomjs，64位元，若無法執行請自行另外做調整[下載](https://phantomjs.org/download.html)。

Linux/chromedriver
-----------
Linux系統的chrome模擬器，64位元，若無法執行請自行另外做調整[下載](https://chromedriver.chromium.org/downloads)。

Linux/phantomjs
-----------
Linux系統的phantomjs，64位元，若無法執行請自行另外做調整[下載](https://phantomjs.org/download.html)。
