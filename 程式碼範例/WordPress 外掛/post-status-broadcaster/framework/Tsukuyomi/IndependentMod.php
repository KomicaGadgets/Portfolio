<?php

namespace PostStatusBroadcaster\Tsukuyomi;

use PostStatusBroadcaster\Tsukuyomi\Core\Independent\{
	BladeMgr,
	CarbonProxy,
	Debugger,
	Encrypter,
	EnvMgr,
	LibShortcut,
	OptionsMgr,
	PathMgr,
	Str,
	TransientMgr,
	WP
};

class IndependentMod
{
	function __construct()
	{
		$this->PathMgr = new PathMgr;
		$this->Debugger = new Debugger($this->PathMgr);
		$this->CbnProxy = new CarbonProxy;
		$this->Encrypter = new Encrypter;
		$this->EnvMgr = new EnvMgr;
		$this->LibShortcut = new LibShortcut;
		$this->OptionsMgr = new OptionsMgr($this->EnvMgr);
		$this->Str = new Str;
		$this->TransientMgr = new TransientMgr;
		$this->WP = new WP;

		$this->Blade = null;
	}

	function Blade(...$Argument)
	{
		if ($this->Blade === null)
			$this->Blade = new BladeMgr(...$Argument);

		return $this->Blade;
	}
}
