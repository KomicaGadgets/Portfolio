<?php

namespace App\Helpers;

use App\TPM\{
	LicenseClient,
	LicenseString,
	PBEmpty
};
use Carbon\Carbon;

class License
{

	//...

	private static function gRPC()
	{
		$Output = null;

		if (self::mode() == self::Active)
			$Output = new LicenseClient(config('acts.license_grpc'), ['credentials' => \Grpc\ChannelCredentials::createInsecure()]);

		return $Output;
	}

	//...

}
