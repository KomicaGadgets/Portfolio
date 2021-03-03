<?php

namespace PostStatusBroadcaster\Tsukuyomi\Core\Independent;

use PostStatusBroadcaster\Tsukuyomi\Core\{
	Independent\EnvMgr,
	Proxies\APFProxy as APF
};

class OptionsMgr
{
	function __construct(EnvMgr $EnvMgr)
	{
		$this->EnvMgr = $EnvMgr;
		$this->DefaultAPFOptionKey = $this->EnvMgr->get('PLUGIN_APF_PREFIX') . '\admin\ConfigPages\\';
	}

	function GetAPFOption($PageClassName = '', $FieldKey = null, $Default = null, $TypeCast = null)
	{
		if ($FieldKey !== null) {
			$FieldID = is_array($FieldKey)
				? [$FieldKey[0], $this->EnvMgr->get('PLUGIN_VAR_PREFIX') . '_' . $FieldKey[1]]
				: $this->EnvMgr->get('PLUGIN_VAR_PREFIX') . '_' . $FieldKey;
		} else
			$FieldID = $FieldKey;

		$APFOptionKey = $this->IsOptionExist($this->DefaultAPFOptionKey . $PageClassName)
			? $this->DefaultAPFOptionKey . $PageClassName
			: $this->EnvMgr->get('PLUGIN_APF_PREFIX') . '_' . $PageClassName;

		$Option = APF::getOption(
			$APFOptionKey,
			$FieldID,
			$Default
		);

		if (!is_null($TypeCast))
			settype($Option, $TypeCast);

		return $Option;
	}

	function IsOptionExist($OptName)
	{
		$IsValFalse = get_option($OptName);
		$IsValTrue = get_option($OptName, true);

		return ($IsValFalse === false && $IsValTrue === true) ? false : true;
	}

	function LoadOrCreateOption($OptName, $NewValue, $autoload = 'yes')
	{
		if (!$this->IsOptionExist($OptName))
			update_option($OptName, $NewValue, $autoload);

		return get_option($OptName);
	}
}
