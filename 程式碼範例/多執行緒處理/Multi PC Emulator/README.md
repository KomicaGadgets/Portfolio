# 多執行緒 MultiProcess Python 程式展示

該程式是擷取自我過去曾做過的一個案子，它的功能主要是模擬多 PC 在同一設備下共同執行時會給設備造成何種負擔並檢測設備的穩定度。

我在該案子裡負責處理底層核心程式，包括程式的多執行緒併發與管理。

這個程式在啟動後，會自動去執行 PC1、PC2 一直到 PC8 資料夾裡的 .py 檔案，而每一個 PCn 資料夾裡的 Python 程式分別會跑哪些程式則可透過 ParallelActions.txt 來定義，每一行一個要執行的程式路徑。

雖然後來發現這個程式還有很多可以改善的地方，例如有一些共通的程式碼可以透過繼承 Class 的方式來重複利用...等，但由於開發途中有修改需求多次，為了趕上結案時間所以就沒多花時間去改善它。