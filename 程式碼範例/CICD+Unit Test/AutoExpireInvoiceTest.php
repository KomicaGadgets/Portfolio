<?php

namespace Tests\Unit;

use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;

use Illuminate\Http\Request;

use Facades\Tests\DataProviders\AutoExpireInvoiceDataProvider as AEO;

use App\Models\Invoice;

use Facades\App\Http\Controllers\InvoiceMgr;

class AutoExpireInvoiceTest extends \Tests\BaseTestBlueprint
{
	function setUp(): void
	{
		parent::setUp();
	}

	function ConditionalAddInvoice()
	{
		if ($this->IsStrInDSName('AddFreshInvoice')) {
			AEO::AddFreshInvoiceReal();
		}

		if ($this->IsStrInDSName('AddExpiredInvoice')) {
			AEO::AddExpiredInvoiceReal();
		}
	}

	/**
	 * @dataProvider Tests\DataProviders\AutoExpireInvoiceDataProvider::AutoExpireDataProvider()
	 */
	public function testAutoExpire($DatasetName)
	{
		$this->SaveDatasetName($DatasetName);

		if ($this->IsStrInDSName('AddFreshInvoice'))
			$this->InitDBForTest('aimistworkstation');

		$this->ConditionalAddInvoice();

		$UnpaidInvoiceQuery = Invoice::where('status', 0)
			->whereDate('due_date', '<=', now());

		if ($this->IsStrInDSName('AddFreshInvoice')) {
			$this->assertFalse($UnpaidInvoiceQuery->exists());
		}

		if ($this->IsStrInDSName('AddExpiredInvoice')) {
			$this->assertTrue($UnpaidInvoiceQuery->exists());
		}
	}
}
