<?php

namespace PostStatusBroadcaster\Core;

class AuthenticateSetting
{
	use \PostStatusBroadcaster\Proxies\SingletonBaseProxy;

	function __construct()
	{ }

	function MakeSecretKey($Length = 32)
	{
		return psb_tsukuyomi()->str()->random($Length);
	}

	function Ajax_MakeSecretKey()
	{
		wp_send_json($this->MakeSecretKey());
	}
}
