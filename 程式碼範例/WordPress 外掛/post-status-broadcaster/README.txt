WP 文章廣播精靈

WP 文章廣播精靈是一個 WordPress 外掛，它可以偵測文章狀態的變化並傳送 POST 請求給其它網站。

例如說，假設我希望我的某一個網站能在網站有新文章時透過 Webhook 收到通知，那麼我就可以在這個外掛裡設定「舊文章狀態」、「新文章狀態」以及「目標網址」。

這樣當文章從「舊文章狀態」變成「新文章狀態」時，它就會傳送一個 POST 或 GET 請求至目標網址。

這個外掛原本是為了要用來整合我的 E-mail 行銷系統所開發的，我使用 Mautic 這個開源的 E-mail 行銷系統，這個外掛的主要目的是為了要讓 Mautic 知道我的部落格發表了新文章並自動抓取文章資料、轉換成 E-mail 並寄給我的讀者們看。

原先有想到讓 Mautic 定期去掃描網站 RSS 看是否有新文章，但這麼做會消耗不少資源，所以改成 WordPress 端主動通知的方式。

每當 WordPress 發佈新文章時，系統會觸發相關 event 並啟動掛載於 transition_post_status 這個 hook 的 PostTransitionListener 函數。

然後 PostTransitionListener 會去判斷該文章狀態變化是否有符合使用者所設定的條件，若有，則傳送連線請求給目標網址，藉此通知 Mautic 前來抓取新文章資料並製作成 E-mail 寄出。
