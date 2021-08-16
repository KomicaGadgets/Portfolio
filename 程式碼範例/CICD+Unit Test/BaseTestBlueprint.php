<?php

namespace Tests;

use Illuminate\Http\Request;
use Illuminate\Support\Collection;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithFaker;
use Tests\TestCase;

class BaseTestBlueprint extends TestCase
{
	function InitDBForTest($DBSlug = 'member')
	{
		$this->vd('正在複製並初始化測試資料庫...');

		$OutputArray = [];

		$Cmd = sprintf(
			'mysqldump -h "mysql" -u root --password=555 "dbprefix_%1$s" | mysql -h "mysql" -u root -p555 "dbprefix_%1$s_test"',
			$DBSlug
		);

		exec($Cmd, $OutputArray);

		return $OutputArray;
	}

	function vd($var)
	{
		var_dump($var);
	}

	function SaveDatasetName($DatasetName = null)
	{
		$this->DatasetName = $DatasetName;
	}

	function IsStrIn($Needle, $Haystack)
	{
		return (strpos($Haystack, $Needle) !== false);
	}

	function IsStrInDSName($Needle)
	{
		if (!isset($this->DatasetName))
			return false;

		return (strpos($this->DatasetName, $Needle) !== false);
	}

	function IsOneStrInDSName(array $NeedleArr)
	{
		foreach ($NeedleArr as $Needle) {
			if ($this->IsStrInDSName($Needle))
				return true;
		}

		return false;
	}

	function assertIsURL($Input)
	{
		$this->assertTrue(
			(filter_var($Input, FILTER_VALIDATE_URL) !== FALSE)
		);
	}

	function assertIsBase64($Input)
	{
		return $this->assertTrue(
			(bool) preg_match('/^[a-zA-Z0-9\/\r\n+]*={0,2}$/', $Input)
		);
	}

	function assertIsHex($Input)
	{
		return $this->assertTrue(
			ctype_xdigit($Input)
		);
	}
}
