<?php

use Facades\App\Http\Controllers\{
	JSRenderMgr,
	ShoppingCart,
};

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
 */

 /*
	電商網站管理後台路由設定
	prefix 代表該函數裡所有路由的前綴，例如將 prefix 設為 admin，那麼函數裡的所有路由都要加上 admin 才能進入。
	例如：example.com/admin/refund/、example.com/admin/payment_method_sort。
	以 admin 為前綴的路由都會經過 auth 和 can:browse_admin 這兩個 middleware，檢查是否已登入以及是否為網站管理員。
*/
Route::group(['prefix' => 'admin', 'middleware' => ['auth', 'can:browse_admin']], function () {
	Route::get('refund', function () {
		return view('admin.OrderStatusWizard');
	});

	Route::get('payment_method_sort', 'Admin\PaymentMethodSort@View');

	Route::post('modify_order_status', 'OrderMgr@ModifyGlobalStatus')->name('AdminModifyOrderStatus');
	Route::post('decrypt_payment_info', 'OrderMgr@AjaxDecryptPaymentInfo')->name('AjaxDecryptPaymentInfo');

	Route::group(['prefix' => 'ajax', 'middleware' => ['AjaxCheck']], function () {
		Route::post('load_dl_files', 'ProductMgr@AjaxGetDLFilesForSelect2');
		Route::post('find_item_by_serial', 'Admin\OrderStatusWizard@AjaxFindItemBySerial');
		Route::post('set_item_status', 'Admin\OrderStatusWizard@AjaxSetItemStatus');
		Route::post('save_payment_method_sort', 'Admin\PaymentMethodSort@AjaxSaveSort')->name('AjaxSavePaymentMethodSort');
	});
});

$MainApp = App::make('App\Http\Controllers\Main');

/*
	一般路由設定
	此處所設定之路由皆可直接進入，無須加任何前綴。
*/
Route::group(['middleware' => ['web']], function () use ($MainApp) {
	Route::any('payment/notify/smilepay', 'PaymentSystem\IPN\SmilePay@Main')
		->middleware('signed')
		->name('payment_notify.smilepay');
	Route::get('payment/paypal/express_checkout/{order_id}', 'PaymentSystem\Paypal@ProcessExpressCheckout')
		->where('order_id', '[0-9]+')
		->name('payment.paypal.process_express_checkout');

	Route::group(['middleware' => ['caffeinated']], function () use ($MainApp) {
		Route::get('csrf/drip', 'Main@RenderNull')->name('drip');

		Route::get('/', function () use ($MainApp) {
			return $MainApp->callAction('RenderView', ['vars' => [
				'ViewName' => 'Main'
			]]);
		})->name('home');

		Route::get('login', function () {
			return redirect()->away(\UnionAuth\UnionAuth::GetUALoginRoute());
		})->name('login');

		Route::get('shopping_cart', function () use ($MainApp) {
			return $MainApp->callAction('RenderView', ['vars' => [
				'ViewName' => 'ShoppingCart'
			]]);
		})->name('cart');

		Route::get('checkout', function () use ($MainApp) {
			return $MainApp->callAction('RenderView', ['vars' => [
				'ViewName' => 'Checkout'
			]]);
		})->name('checkout');

		Route::get('products/{slug}', function ($slug) use ($MainApp) {
			return $MainApp->callAction('RenderView', ['vars' => [
				'ViewName' => 'ProductInfo',
				'slug' => $slug
			]]);
		})->name('products');

		...
		
		/*
			Throttle middleware 用來限制指定路由的呼叫次數上限。
			5,30 代表只能呼叫 5 次，30 分鐘後重置此限制。
		*/
		Route::group(['middleware' => ['throttle:5,30']], function () {
			Route::get('download_trial/{file_name}', 'TrialDownloadMgr@DownloadTrial')
				->name('dl_trial');
		});

		...
		
	});
});

...
