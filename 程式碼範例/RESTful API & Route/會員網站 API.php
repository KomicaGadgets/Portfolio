<?php

use Illuminate\Http\Request;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

/*
	可讓其他子站存取會員資料的會員網站 API。
	使用 API 時會經過 tcsigned 這個 middleware，檢查傳入資料的 HMAC 簽名確認 API 請求是由合法金鑰持有者所發出來的，避免他人偽造連線請求。
	以 example.com 為例，POST 傳入 example.com/api/ua_get_profile 可取得指定 E-mail 的會員資料。
	POST 傳入 example.com/api/ma_register_user 則可遠端註冊新會員。
*/

Route::group([
	'prefix'	=> 'api',
	'middleware'	=>	['tcsigned']
], function () {
	Route::post('ua_get_profile', 'App\Http\Controllers\MemberAccessor@Profile');
	Route::post('ma_register_user', 'App\Http\Controllers\MemberAccessor@RemoteAddUsr');
});
