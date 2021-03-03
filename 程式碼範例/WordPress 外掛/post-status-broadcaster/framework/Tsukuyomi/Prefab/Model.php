<?php

namespace PostStatusBroadcaster\Tsukuyomi\Prefab;

use PostStatusBroadcaster\Tsukuyomi\Core\Independent\EnvMgr;

class Model
{
	function __construct($TblName, $DefaultFormat = [], $IsPrependPrefix = 1, EnvMgr $EnvMgr = null)
	{
		global $wpdb;

		$this->EnvMgr = $EnvMgr;

		$this->wpdb = $wpdb;
		$this->charset_collate = $this->wpdb->get_charset_collate();

		$this->TblName = $IsPrependPrefix
			? $this->wpdb->prefix . $this->EnvMgr->get('PLUGIN_VAR_PREFIX') . '_' . $TblName
			: $this->wpdb->prefix . $TblName;

		$this->DefaultFormat = $DefaultFormat;

		$this->Data = [];

		if ($this->TblExist())
			$this->InitData();
	}

	private function InitData()
	{
		$ColumnList = $this->column_list();

		if ($ColumnList[0] == 'id')
			array_shift($ColumnList);

		$this->Data = collect(array_fill_keys($ColumnList, null));
	}

	function TblExist()
	{
		return ($this->wpdb->get_var($this->wpdb->prepare("SHOW TABLES LIKE %s", $this->TblName)) === $this->TblName);
	}

	function RowExist($Column = 'id', $Value = null)
	{
		return !is_null($this->wpdb->get_row(
			$this->wpdb->prepare(
				sprintf('SELECT * FROM %s WHERE %s = %%s', $this->TblName, $Column),
				$Value
			)
		));
	}

	function column_list()
	{
		return $this->wpdb->get_col("DESC {$this->TblName}", 0);
	}

	function select($Decorator, $ValMap, $OutputType = OBJECT)
	{
		return $this->wpdb->get_results(
			$this->wpdb->prepare(
				sprintf('SELECT * FROM %s %s', $this->TblName, $Decorator),
				...$ValMap
			),
			$OutputType
		);
	}

	function insert(...$Arguments)
	{
		$this->wpdb->insert($this->TblName, ...$Arguments);
		return $this->wpdb->insert_id;
	}

	function update(...$Arguments)
	{
		return $this->wpdb->update($this->TblName, ...$Arguments);
	}

	function delete(...$Arguments)
	{
		return $this->wpdb->delete($this->TblName, ...$Arguments);
	}

	function query($MainCmd = 'UPDATE', $Decorator = '')
	{
		return $this->wpdb->query(sprintf(
			'%s FROM %s %s',
			$MainCmd,
			$this->TblName,
			$Decorator
		));
	}

	function upsert($data, $where, ...$Arguments)
	{
		$Column = array_key_first($where);
		$Val = $where[$Column];

		// 1 = insert
		// 2 = update
		if ($this->RowExist($Column, $Val)) {
			return [
				'type'	=>	2,
				'val'	=>	$this->update($data, $where, ...$Arguments)
			];
		} else {
			$this->insert($data, ...$Arguments);
			return [
				'type'	=>	1,
				'val'	=>	$this->wpdb->insert_id
			];
		}
	}

	function setData($data)
	{
		foreach ($data as $key => $val) {
			$this->Data->put($key, $val);
		}
	}

	function loadData($indicator)
	{
		$Column = array_key_first($indicator);
		$Val = $indicator[$Column];

		if ($this->RowExist($Column, $Val)) {
			$DBData = $this->wpdb->get_row(
				$this->wpdb->prepare(
					sprintf('SELECT * FROM %s WHERE %s = %%s', $this->TblName, $Column),
					$Val
				),
				ARRAY_A
			);

			if (isset($DBData['id']))
				unset($DBData['id']);

			$this->Data = $this->Data->merge($DBData);
		}
	}

	function insertData($ColumnFormat = [])
	{
		return $this->insert(
			$this->Data->toArray(),
			empty($ColumnFormat) ? $this->DefaultFormat : $ColumnFormat
		);
	}

	function upsertData($where, $ColumnFormat = [])
	{
		return $this->upsert(
			$this->Data->toArray(),
			$where,
			empty($ColumnFormat) ? $this->DefaultFormat : $ColumnFormat
		);
	}
}
