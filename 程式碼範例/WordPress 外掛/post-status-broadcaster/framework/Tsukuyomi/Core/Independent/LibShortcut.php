<?php

namespace PostStatusBroadcaster\Tsukuyomi\Core\Independent;

use \GuzzleHttp\Client;
use \ReCaptcha\ReCaptcha;
use \Vectorface\Whip\Whip;

class LibShortcut
{
	function __construct()
	{ }

	function recaptcha($secret = null)
	{
		return $this->ReCaptcha = new ReCaptcha($secret, new \ReCaptcha\RequestMethod\CurlPost());
	}

	function guzzle(...$Arguments)
	{
		return new Client(...$Arguments);
	}

	function getIp()
	{
		$whip = new Whip();
		$clientAddress = $whip->getValidIpAddress();
		return $clientAddress;
	}
}
