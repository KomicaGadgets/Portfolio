<?php

namespace PostStatusBroadcaster\Tsukuyomi\Core\Independent;

class TransientMgr
{
	function __construct()
	{
		$this->ValidSaveType = ['raw', 'serialize', 'json'];
	}

	function Save($Name, $Val, $Expiration = 86400, $Type = 'raw')
	{
		$Type = in_array($Type, $this->ValidSaveType) ? $Type : $this->ValidSaveType[0];

		switch ($Type) {
			case 'serialize':
				$Val = serialize($Val);
				break;
			case 'json':
				$Val = json_encode($Val);
				break;
		}

		$SavedObj = [
			'type'	=>	$Type,
			'value'	=>	$Val
		];

		return set_transient($Name, $SavedObj, $Expiration);
	}

	function Get($Name)
	{
		$Data = get_transient($Name);
		$IsExist = ($Data !== false);

		$Output = [
			'is_exist'	=> $IsExist,
			'type'	=>	$IsExist ? $Data['type'] : null,
			'value'	=>	$IsExist ? $Data['value'] : null
		];

		return (object) $Output;
	}
}
