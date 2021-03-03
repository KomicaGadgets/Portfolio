<?php

namespace PostStatusBroadcaster\Tsukuyomi\Core\Independent;

use \eftec\bladeone\BladeOne;

class BladeMgr
{
	function __construct($View = null, $Cache = null)
	{
		$this->blade = new BladeOne(
			$View,
			$Cache,
			(defined('WP_DEBUG') && WP_DEBUG === true) ? BladeOne::MODE_DEBUG : BladeOne::MODE_AUTO
		);
	}

	function run(...$Arguments)
	{
		return $this->blade->run(...$Arguments);
	}
}
