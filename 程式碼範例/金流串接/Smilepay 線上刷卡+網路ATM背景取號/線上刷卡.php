<?php

namespace App\Http\Controllers;

use Validator;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\URL;

use PayPal;
use Artesaos\SEOTools\Facades\{
	SEOTools,
	SEOMeta
};

use App\Models\{
	Invoice,
	Product,
};

use Facades\App\Http\Controllers\{
	PaymentService\Paypal\SubscriptionWizard,
	GA4EventSender
};

class Checkout extends Controller
{
	function __construct()
	{
		$this->SmilepayAPI = env('TEST_MODE', false)
			? 'https://ssl.smse.com.tw/ezpos_test/mtmk_utf.asp'
			: 'https://ssl.smse.com.tw/ezpos/mtmk_utf.asp';
		$this->RecurringTextMap = [
			'monthly'	=>	'月',
			'yearly'	=>	'年'
		];
		$this->CurrentURL = url()->full();
		$this->SourceRouteData = [
			'product_slug'	=>	null,
			'recurring_type'	=>	null
		];

		$this->UsrData = collect([
			'product_name'	=>	null,
			'plan_name'	=>	null,
			'amount'	=>	null,
			'recurring_type'	=>	null,
			'email'	=>	null,
			'payment_method'	=>	null,
		]);

		$this->PlanModel = null;
	}

	function RecurringCodeToText($RecurringType)
	{
		return $this->RecurringTextMap[$RecurringType] ?? null;
	}

	function MakePaymentURL($UsrData = null)
	{
		if (is_null($UsrData))
			$UsrData = $this->UsrData;

		$PaymentURL = null;

		$FullProductName = $UsrData->get('product_name');

		if (!is_null($UsrData->get('recurring_type'))) {
			$RecurringText = $this->RecurringCodeToText($UsrData->get('recurring_type'));
			$FullProductName = sprintf(
				'%s - %s（%s繳）',
				$UsrData->get('product_name'),
				$UsrData->get('plan_name'),
				$RecurringText
			);
		}

		switch ($UsrData->get('payment_method')) {
			case 'creditcard':
			case 'transfer':
				$Pay_zg = ($UsrData->get('payment_method') == 'creditcard') ? 1 : 2;
				$Roturl = route('smilepay_webhook');

				if (env('TEST_MODE', false))
					$Roturl = str_replace(url('/'), env('DEV_PROXY_URL'), $Roturl);

				if (!$UsrData->has('invoice_id')) {
					$Data_id = is_null($UsrData->get('recurring_type'))
						? 'S' . $UsrData->get('product_id')	// Single
						: 'N' . $this->PlanModel->id;	// New
				} else
					$Data_id = 'R' . $UsrData->get('invoice_id');	// Recurring

				$PaymentParam = [
					'Rvg2c'	=>	1,
					'Dcvc'	=>	2963,
					'Pay_zg'	=>	$Pay_zg,
					'Od_sob'	=>	$FullProductName,
					'Data_id'	=>	$Data_id,
					'Amount'	=>	$UsrData->get('amount'),
					'Email'	=>	$UsrData->get('email'),
					'Remark'	=>	(int)$UsrData->get('receive_blog_post', false),
					'Roturl_status'	=>	'OK',
					'Roturl'	=>	$Roturl
				];
				$PaymentURL = sprintf('%s?%s', $this->SmilepayAPI, http_build_query($PaymentParam));

				break;

			case 'paypal':
				$response = SubscriptionWizard::MakeSubscriptionLink(
					$UsrData->get('email'),
					$this->PlanModel
				);

				if (is_null($response)) {
					logger('$ResponseLink', $response);
					logger('$PlanModel', $this->PlanModel);
				}

				$PaymentURL = $response;
				break;
		}

		return $PaymentURL;
	}
};
