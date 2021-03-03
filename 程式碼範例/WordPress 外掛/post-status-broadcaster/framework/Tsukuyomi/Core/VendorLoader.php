<?php

namespace PostStatusBroadcaster\Tsukuyomi\Core;

use PostStatusBroadcaster\Tsukuyomi\Core\Independent\PathMgr;

class VendorLoader
{
	function __construct(PathMgr $PathMgr)
	{
		$this->loaded_vendors = [];

		$this->PathMgr = $PathMgr;

		$this->VendorFileMap = [
			// 'ActionScheduler'	=>	['woocommerce/action-scheduler/action-scheduler.php']
		];
	}

	function Load($VendorTag)
	{
		if (!in_array($VendorTag, $this->loaded_vendors)) {
			$PathPrefix = sprintf('%svendor/', $this->PathMgr->tsukuyomi_root());

			foreach ($this->VendorFileMap[$VendorTag] as $File) {
				require_once $PathPrefix . $File;
			}

			$this->loaded_vendors[] = $VendorTag;
		}
	}

	function MultiLoad($VendorTagList = [])
	{
		foreach ($VendorTagList as $VendorTag) {
			$this->Load($VendorTag);
		}
	}
}
