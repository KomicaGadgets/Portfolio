<?php

namespace App\Http\Controllers\PaymentSystem;

use GuzzleHttp\Client;
use Carbon\Carbon;

use UnionAuth\Facades\Member;

use App\Http\Controllers\PaymentSystem\{
	PaymentAbstract,
	IPN\SmilePay
};

class SmilePay_ATM extends PaymentAbstract
{
	protected $Info, $PaymentInfo, $Label;

	const API = 'https://ssl.smse.com.tw/api/SPPayment.asp';

	function __construct()
	{
		$this->Info = [
			'display_name' => '虛擬銀行帳號即時銷帳（ATM、Web ATM、臨櫃匯款）',
			'display_note' => null,
			'description' => '消費者可使用 Web ATM／櫃員機／臨櫃匯款 進行付款，金額不正確將無法付款，匯款後不論銀行下班或休假期間都是約 2-10 分鐘入帳。',
			'recommend' => true,
			'online_payment' => false,
			'have_tutorial' => false
		];

		$this->Label = [
			'Amount' => '總金額',
			'PayEndDate' => '付款截止日期',
			'AtmBankNo' => '銀行代號',
			'AtmNo' => '匯款帳號'
		];

		$WebhookURL = env('TEST_MODE', false)
			? str_replace(url('/'), env('DEV_PROXY_URL'), route('payment_notify.smilepay'))
			: route('payment_notify.smilepay');

		$this->PaymentInfo = [
			'Dcvc' => env('SMILEPAY_DEALERCODE'),
			'Rvg2c' => env('SMILEPAY_RVG2C'),
			'Verify_key' => env('SMILEPAY_VERIFY_KEY'),
			'Pay_zg' => 2,
			'Roturl_status' => (new SmilePay)->IPNResponse(),
			'Roturl' => $WebhookURL,

			'Invoice_name' => null,
			'Invoice_num' => null,
			'Deadline_date' => null,
			'Deadline_time' => null,

			'Pur_name' => null,
			'Email' => null,
			'Remark' => null,

			'Od_sob' => null,
			'Data_id' => 0,
			'Amount' => 0,
		];
	}

	function AdjustPaymentDeadline($TimeStr)
	{
		return (new Carbon($TimeStr))->addDays(6);
	}

	function OrderToPaymentInfo($FullData)
	{
		return [
			'Pur_name' => Member::Profile('name'),
			'Email' => $FullData->user->email,
			'Remark' => empty($FullData->order->note) ? '' : decrypt($FullData->order->note),
			'Od_sob' => ($FullData->order_item->count() > 1)
				? '多項商品'
				: $FullData->order_item->first()->product_name,
			'Data_id' => $FullData->order->id,
			'Amount' => $FullData->total,
		];
	}

	function FormatPaymentResponse($Resp)
	{
		return ((int) $Resp['Status'] > 0)
			? [
				'Status' => (int) $Resp['Status'],
				'Dcvc' => $Resp['Dcvc'],
				'SmilePayNO' => $Resp['SmilePayNO'],
				'Data_id' => (int) $Resp['Data_id'],
				'Amount' => (int) $Resp['Amount'],
				'PayEndDate' => $Resp['PayEndDate'],
				'AtmBankNo' => $Resp['AtmBankNo'],
				'AtmNo' => $Resp['AtmNo']
			]
			: [
				'Status' => (int) $Resp['Status'],
				'Dcvc' => $Resp['Dcvc'],
				'SmilePayNO' => '-1',
				'Data_id' => (int) $Resp['Data_id'],
				'Amount' => (int) $Resp['Amount'],
				'PayEndDate' => now()->addDays(30)->toDateTimeString(),
				'AtmBankNo' => '沒有取得匯款銀行代碼',
				'AtmNo' => '沒有取得匯款帳號'
			];
	}

	function RequestPayment($FullPaymentInfo)
	{
		$RealPaymentInfo = $this->OrderToPaymentInfo($FullPaymentInfo);
		$PaymentData = array_replace($this->PaymentInfo, $RealPaymentInfo);

		//Simulate Error
		// $PaymentData['Dcvc'] .= '9';

		$client = new Client();

		try {
			$response = $client->request('POST', self::API, [
				'form_params' => $PaymentData
			])->getBody()->getContents();
		} catch (\Throwable $th) {
			report($th);
			logger('$PaymentData', $PaymentData);

			return null;
		}

		$ParsedXML = (array) simplexml_load_string($response);

		if ((int) $ParsedXML['Status'] < 0) {
			logger('$RawResponse = ' . $response);
			logger('$ParsedXML', $ParsedXML);
			logger('$PaymentData', $PaymentData);
		}

		$FormattedResponse = $this->FormatPaymentResponse($ParsedXML);
		$FormattedResponse['PaidDate'] = 0;

		return $FormattedResponse;
	}
}
