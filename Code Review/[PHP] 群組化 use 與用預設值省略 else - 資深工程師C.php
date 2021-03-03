<?php

namespace App\Helpers;

use App\TPM\LicenseClient;
use App\TPM\LicenseString;
use App\TPM\PBEmpty;
use Carbon\Carbon;

class License
{

	//...

	private static function gRPC()
	{
		if (self::mode() == self::Active) {
			return new LicenseClient(config('acts.license_grpc'), ['credentials' => \Grpc\ChannelCredentials::createInsecure()]);
		} else {
			return NULL;
		}
	}

	//...

}
