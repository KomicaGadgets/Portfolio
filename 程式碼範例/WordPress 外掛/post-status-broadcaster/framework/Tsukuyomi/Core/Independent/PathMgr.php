<?php

namespace PostStatusBroadcaster\Tsukuyomi\Core\Independent;

class PathMgr
{
	function __construct()
	{
		$this->tsukuyomi_root = plugin_dir_path($this->RecallDir(2));
		$this->plugin_root = null;
		$this->framework_root = null;
		$this->admin_root = null;
		$this->admin_config_pages_root = null;
		$this->admin_page_framework_file = null;
	}

	function tsukuyomi_root()
	{
		return $this->tsukuyomi_root;
	}

	function plugin_root()
	{
		if ($this->plugin_root === null)
			$this->plugin_root = plugin_dir_path($this->RecallDir(2, $this->tsukuyomi_root()));

		return $this->plugin_root;
	}

	function framework_root()
	{
		if ($this->framework_root === null)
			$this->framework_root = $this->plugin_root() . 'framework/';

		return $this->framework_root;
	}

	function admin_root()
	{
		if ($this->admin_root === null)
			$this->admin_root = $this->plugin_root() . 'admin/';

		return $this->admin_root;
	}

	function admin_config_pages_root()
	{
		if ($this->admin_config_pages_root === null)
			$this->admin_config_pages_root = $this->admin_root() . 'ConfigPages/';

		return $this->admin_config_pages_root;
	}

	function admin_page_framework_file()
	{
		if ($this->admin_page_framework_file === null)
			$this->admin_page_framework_file = $this->framework_root() . 'admin-page-framework/admin-page-framework.php';

		return $this->admin_page_framework_file;
	}

	function RecallDir($Times = 0, $RecallPath = null)
	{
		if (is_null($RecallPath))
			$RecallPath = __FILE__;
		elseif (is_dir($RecallPath) && $Times > 0)
			$Times -= 1;	// 避免目錄被多跳一層

		for ($i = 0; $i < $Times; $i++) {
			$RecallPath = dirname($RecallPath);
		}

		return $RecallPath;
	}
}
