<?php

namespace Tests\DataProviders;

use Tests\TestCase;

class DataProviderBlueprint extends TestCase
{
	function PackDataMethods($MethodNameList = [], $IsAppendDatasetName = false)
	{
		$Output = [];

		foreach ($MethodNameList as $Name) {
			$ParamSerial = $this->$Name();

			if ($IsAppendDatasetName)
				array_unshift($ParamSerial, $Name);

			$Output[] = $ParamSerial;
		}

		return $Output;
	}
}
