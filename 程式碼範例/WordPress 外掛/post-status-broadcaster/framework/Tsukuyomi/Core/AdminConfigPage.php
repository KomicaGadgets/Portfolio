<?php

namespace PostStatusBroadcaster\Tsukuyomi\Core;

use PostStatusBroadcaster\Tsukuyomi\Core\Independent\{
	PathMgr,
	Str
};

class AdminConfigPage
{
	function __construct(Str $Str, PathMgr $PathMgr)
	{
		$this->Str = $Str;
		$this->PathMgr = $PathMgr;

		$this->AdminPageDir = '';
		$this->Pages = [];
	}

	function SetPrefix($DirPath = '')
	{
		if (!empty($DirPath))
			$this->AdminPageDir = $this->Str->finish($DirPath, '/');

		return $this;
	}

	function AddPages($Page = [])
	{
		if (is_string($Page))
			$Page = [$Page];

		$this->Pages = array_unique(array_merge($this->Pages, $Page));

		return $this;
	}

	function LoadPages()
	{
		$PathPrefix = $this->PathMgr->plugin_root() . $this->AdminPageDir;
		$TopClass = explode('\\', __CLASS__, 2)[0];

		foreach ($this->Pages as $ClassName) {
			require_once $PathPrefix . $ClassName . '.php';
			$NewClassName = sprintf('%s\%s%s', $TopClass, str_replace('/', '\\', $this->AdminPageDir), $ClassName);
			new $NewClassName;
		}
	}
}
