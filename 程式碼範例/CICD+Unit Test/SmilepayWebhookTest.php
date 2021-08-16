<?php

namespace Tests\Unit;

use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;

use Illuminate\Http\Request;

use Facades\UnionAuth\TrustedConnection;
use App\Http\Controllers\PaymentService\Smilepay\Webhook;

class SmilepayWebhookTest extends \Tests\BaseTestBlueprint
{
	function setUp(): void
	{
		parent::setUp();
	}

	/**
	 * @dataProvider Tests\DataProviders\SmilepayWebhookDataProvider::MemberCenterAddUsrDataProvider()
	 */
	public function testMemberCenterAddUsr($DatasetName, $UsrEmail = '')
	{
		if ($DatasetName != 'GlobalEmail_Existed')
			$this->InitDBForTest('member');

		$Webhook = new Webhook();
		$Webhook->UsrEmail = $UsrEmail;

		$Output = $Webhook->MemberCenterAddUsr();

		if ($Output->type == 'added') {
			$OutputContent = $Output->content->UserRegData;

			$this->assertSame($OutputContent->email, filter_var($OutputContent->email, FILTER_VALIDATE_EMAIL));
			$this->assertSame('test', $OutputContent->name);
			$this->assertNotNull($OutputContent->email_verified_at);
		} else {
			$this->assertSame('exist', $Output->type);
			$this->assertIsArray($Output->content);
			$this->assertCount(0, $Output->content);
		}
	}

	/**
	 * @dataProvider Tests\DataProviders\SmilepayWebhookDataProvider::SubscribeToSegmentDataProvider()
	 */
	public function testSubscribeToSegment($DatasetName, $UsrEmail, $Remark)
	{
		$Webhook = new Webhook();
		$Webhook->UsrEmail = $UsrEmail;

		$Output = $Webhook->SubscribeToSegment(new Request([
			'Remark'	=>	$Remark
		]));

		$this->assertIsArray($Output);
	}
}
