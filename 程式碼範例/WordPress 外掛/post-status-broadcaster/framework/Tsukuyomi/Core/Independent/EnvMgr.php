<?php

namespace PostStatusBroadcaster\Tsukuyomi\Core\Independent;

class EnvMgr
{
	function __construct()
	{
		$this->ENV = null;

		$this->LoadEnv();
	}

	function LoadEnv()
	{
		$OnionPath = __DIR__;

		for ($i = 0; $i < 4; $i++) {
			$OnionPath = dirname($OnionPath);
		}

		$EnvArr = \Dotenv\Dotenv::createArrayBacked($OnionPath)->load();

		$this->ENV = $EnvArr;
	}

	function get($EnvName, $Default = null)
	{
		return isset($this->ENV[$EnvName])
			? $this->ENV[$EnvName]
			: $Default;
	}
}
