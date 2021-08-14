<?php
/*
	電商網站查詢指定商品之特價資訊，等價於下列 SQL 查詢語法：
	select * from `special_price` where `pid` = ? and `enabled` = ? and date(`start_date`) <= ? and (date(`end_date`) > ? or `end_date` is null)

	參數說明：
	pid = 商品 ID
	enabled = 該商品是否有開啟特價
	start_date = 特價開始日期
	end_date = 特價結束日期
*/
SpecialPrice::where('pid', $pid)
->where('enabled', 1)
->WhereDate('start_date', '<=', $Now)
->where(function ($query) use ($Now) {
	$query->WhereDate('end_date', '>', $Now)
		->orWhereNull('end_date');
})
->first();


/*
	電商網站查詢開放購買之產品資訊，等價於下列 SQL 查詢語法：
	select * from `products` where `enabled` = ? and `available_date` is null or date(`available_date`) >= ? order by `updated_at` desc limit 7

	參數說明：
	enabled = 該商品是否有開放購買
	available_date = 該商品的開放購買日期（用於預購活動）
	updated_at = 產品資訊最後更新日期
*/
Products::with('info')
	->where('enabled', 1)
	->whereNull('available_date')
	->orWhereDate('available_date', '>=', now())
	->latest('updated_at')
	->limit(7)


/*
	會員網站查詢特定會員 2 個月內之帳號活動記錄，等價於下列 SQL 查詢語法：
	select * from `user_activities` where `user_activities`.`user_id` = ? and `user_activities`.`user_id` is not null and date(`created_at`) >= ? order by `id` desc

	參數說明：
	user_id = 指定會員之 ID
	created_at = 帳號活動記錄的建立日期
	id = 帳號活動記錄的 id
*/
$User->activity()
	->whereDate('created_at', '>=', now()->subMonths(2))
	->orderBy('id', 'DESC')
	->get()