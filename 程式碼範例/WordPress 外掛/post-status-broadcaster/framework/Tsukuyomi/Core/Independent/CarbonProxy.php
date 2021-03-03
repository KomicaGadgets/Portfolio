<?php

namespace PostStatusBroadcaster\Tsukuyomi\Core\Independent;

use \Carbon\Carbon;

class CarbonProxy
{
	function __construct()
	{ }

	function carbon(...$Arguments)
	{
		return new Carbon(...$Arguments);
	}

	function now()
	{
		$Now = new Carbon();

		if (!is_null(get_option('timezone_string', null)))
			$Now = $Now->setTimezone('Asia/Taipei');

		return $Now;
	}
}
