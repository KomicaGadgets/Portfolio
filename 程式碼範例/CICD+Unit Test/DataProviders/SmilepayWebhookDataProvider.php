<?php

namespace Tests\DataProviders;

use Tests\TestCase;
use Illuminate\Http\Request;

class SmilepayWebhookDataProvider extends DataProviderBlueprint
{
	function __construct()
	{
		$this->GlobalEmail = 'test2@example.com';
	}

	function GlobalEmail()
	{
		$this->setUp();

		return [
			$this->GlobalEmail
		];
	}

	function GlobalEmail_Existed()
	{
		$this->setUp();

		return [
			$this->GlobalEmail
		];
	}

	function SubscribeToSegment_11()
	{
		$this->setUp();

		return [
			$this->GlobalEmail, '11'
		];
	}

	function Entry_OneTimeProduct_CreditCard()
	{
		$this->setUp();

		return [
			[
				"Classif"	=>	"A",
				"Od_sob"	=>	"產品A - 單一版 - 測試",
				"Data_id"	=>	"S2",
				"Process_date"	=>	"2021/4/16",
				"Process_time"	=>	"下午 10:07:36",
				"Response_id"	=>	"1",
				"Auth_code"	=>	"0000",
				"LastPan"	=>	"1234",
				"Moneytype"	=>	"TW",
				"Purchamt"	=>	"2000",
				"Amount"	=>	"2000",
				"Errdesc"	=>	null,
				"Pur_name"	=>	null,
				"Tel_number"	=>	null,
				"Mobile_number"	=>	null,
				"Address"	=>	null,
				"Email"	=>	"test@example.com",
				"Invoice_num"	=>	null,
				"Smseid"	=>	"4_16_1_0009090",
				"Mid_smilepay"	=>	"315",
				"Remark"	=>	null,
				"Payment_no"	=>	null,
				"Foreign"	=>	null,
				"Veirify_number"	=>	null,
				"Fee"	=>	"58",
				"Ship_Fee"	=>	"0"
			]
		];
	}

	function Entry_OneTimeProduct_Bank()
	{
		$this->setUp();

		return [
			[
				"Classif"	=>	"B",
				"Od_sob"	=>	"產品B - 單一版 - 測試",
				"Data_id"	=>	"S2",
				"Process_date"	=>	"2021/4/17",
				"Process_time"	=>	"上午 10:48:06",
				"Response_id"	=>	"0",
				"Auth_code"	=>	null,
				"LastPan"	=>	null,
				"Moneytype"	=>	"TW",
				"Purchamt"	=>	"2000",
				"Amount"	=>	"2000",
				"Errdesc"	=>	null,
				"Pur_name"	=>	null,
				"Tel_number"	=>	null,
				"Mobile_number"	=>	null,
				"Address"	=>	null,
				"Email"	=>	"test@example.com",
				"Invoice_num"	=>	null,
				"Smseid"	=>	"4_17_1_0009093",
				"Mid_smilepay"	=>	"324",
				"Remark"	=>	null,
				"Payment_no"	=>	"30285390009093,",
				"Foreign"	=>	null,
				"Veirify_number"	=>	null,
				"Fee"	=>	"8",
				"Ship_Fee"	=>	"0"
			]
		];
	}

	function Entry_RecurringProduct_Month_CreditCard()
	{
		$this->setUp();

		return [
			[
				"Classif"	=>	"A",
				"Od_sob"	=>	"產品A - 標準版（月繳）",
				"Data_id"	=>	"N1",
				"Process_date"	=>	"2021/4/17",
				"Process_time"	=>	"上午 01:47:07",
				"Response_id"	=>	"1",
				"Auth_code"	=>	"0000",
				"LastPan"	=>	"1234",
				"Moneytype"	=>	"TW",
				"Purchamt"	=>	"600",
				"Amount"	=>	"600",
				"Errdesc"	=>	null,
				"Pur_name"	=>	null,
				"Tel_number"	=>	null,
				"Mobile_number"	=>	null,
				"Address"	=>	null,
				"Email"	=>	"test@example.com",
				"Invoice_num"	=>	null,
				"Smseid"	=>	"4_17_1_0009091",
				"Mid_smilepay"	=>	"318",
				"Remark"	=>	null,
				"Payment_no"	=>	null,
				"Foreign"	=>	null,
				"Veirify_number"	=>	null,
				"Fee"	=>	"17",
				"Ship_Fee"	=>	"0"
			]
		];
	}

	function Entry_RecurringProduct_Month_Bank()
	{
		$this->setUp();

		return [
			[
				"Classif"	=>	"B",
				"Od_sob"	=>	"產品B - 標準版（月繳）",
				"Data_id"	=>	"N1",
				"Process_date"	=>	"2021/4/17",
				"Process_time"	=> "下午 02:09:36",
				"Response_id"	=>	"0",
				"Auth_code"	=>	null,
				"LastPan"	=>	null,
				"Moneytype"	=>	"TW",
				"Purchamt"	=>	"600",
				"Amount"	=>	"600",
				"Errdesc"	=>	null,
				"Pur_name"	=>	null,
				"Tel_number"	=>	null,
				"Mobile_number"	=>	null,
				"Address"	=>	null,
				"Email"	=>	"test@example.com",
				"Invoice_num"	=>	null,
				"Smseid"	=>	"4_17_1_0009095",
				"Mid_smilepay"	=>	"330",
				"Remark"	=>	null,
				"Payment_no"	=>	"30280790009095,",
				"Foreign"	=>	null,
				"Veirify_number"	=>	null,
				"Fee"	=>	"8",
				"Ship_Fee"	=>	"0"
			]
		];
	}

	function Entry_RecurringProduct_Year_CreditCard()
	{
		$this->setUp();

		return [
			[
				"Classif"	=>	"A",
				"Od_sob"	=>	"產品A - 標準版（年繳）",
				"Data_id"	=>	"N2",
				"Process_date"	=>	"2021/4/17",
				"Process_time"	=>	"上午 10:26:38",
				"Response_id"	=>	"1",
				"Auth_code"	=>	"0000",
				"LastPan"	=>	"1234",
				"Moneytype"	=>	"TW",
				"Purchamt"	=>	"6000",
				"Amount"	=>	"6000",
				"Errdesc"	=>	null,
				"Pur_name"	=>	null,
				"Tel_number"	=>	null,
				"Mobile_number"	=>	null,
				"Address"	=>	null,
				"Email"	=>	"test@example.com",
				"Invoice_num"	=>	null,
				"Smseid"	=>	"4_17_1_0009092",
				"Mid_smilepay"	=>	"357",
				"Remark"	=>	null,
				"Payment_no"	=>	null,
				"Foreign"	=>	null,
				"Veirify_number"	=>	null,
				"Fee"	=>	"174",
				"Ship_Fee"	=>	"0"
			]
		];
	}

	function Entry_RecurringProduct_Year_Bank()
	{
		$this->setUp();

		return [
			[
				"Classif"	=>	"B",
				"Od_sob"	=>	"產品B - 標準版（年繳）",
				"Data_id"	=>	"N2",
				"Process_date"	=>	"2021/4/17",
				"Process_time"	=>	"下午 10:56:48",
				"Response_id"	=>	"0",
				"Auth_code"	=>	null,
				"LastPan"	=>	null,
				"Moneytype"	=>	"TW",
				"Purchamt"	=>	"6000",
				"Amount"	=>	"6000",
				"Errdesc"	=>	null,
				"Pur_name"	=>	null,
				"Tel_number"	=>	null,
				"Mobile_number"	=>	null,
				"Address"	=>	null,
				"Email"	=>	"test@example.com",
				"Invoice_num"	=>	null,
				"Smseid"	=>	"4_17_1_0009096",
				"Mid_smilepay"	=>	"369",
				"Remark"	=>	null,
				"Payment_no"	=>	"30282490009096,",
				"Foreign"	=>	null,
				"Veirify_number"	=>	null,
				"Fee"	=>	"8",
				"Ship_Fee"	=>	"0"
			]
		];
	}

	function SubscribeToSegmentDataProvider()
	{
		$MethodNameList = [
			'SubscribeToSegment_11',
		];

		return $this->PackDataMethods($MethodNameList, true);
	}

	function MemberCenterAddUsrDataProvider()
	{
		$MethodNameList = [
			'GlobalEmail',
			'GlobalEmail_Existed'
		];

		return $this->PackDataMethods($MethodNameList, true);
	}

	function EntryDataProvider()
	{
		$MethodNameList = [
			'Entry_OneTimeProduct_CreditCard',
			'Entry_OneTimeProduct_Bank',
			'Entry_RecurringProduct_Month_CreditCard',
			'Entry_RecurringProduct_Month_Bank',
			'Entry_RecurringProduct_Year_CreditCard',
			'Entry_RecurringProduct_Year_Bank'
		];

		return $this->PackDataMethods($MethodNameList, true);
	}
}
