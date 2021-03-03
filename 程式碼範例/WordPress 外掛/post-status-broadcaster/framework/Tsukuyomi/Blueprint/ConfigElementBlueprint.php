<?php

namespace PostStatusBroadcaster\Tsukuyomi\Blueprint;

use PostStatusBroadcaster\Tsukuyomi\Core\Proxies\APFProxy;

class ConfigElementBlueprint extends APFProxy
{
	function __construct(...$Arguments)
	{
		parent::__construct(...$Arguments);
	}

	function PrefixFieldID($FieldID)
	{
		return $this->IDPrefix . '_' . $FieldID;
	}

	function addSettingFields()
	{
		foreach (func_get_args() as $aField) {
			if (isset($aField['field_id']))
				$aField['field_id'] = $this->PrefixFieldID($aField['field_id']);

			$this->addSettingField($aField);
		}
	}
}
