<?php

namespace PostStatusBroadcaster\Tsukuyomi;

use PostStatusBroadcaster\Tsukuyomi\{
	IndependentMod,
	Prefab\Model
};

use PostStatusBroadcaster\Tsukuyomi\Core\{
	AdminConfigPage,
	CookieMgr,
	Proxies\APFProxy,
	VendorLoader
};

class Tsukuyomi extends APFProxy
{
	function __construct($PluginNamespace = null)
	{
		$this->PluginNamespace = $PluginNamespace;
		$this->IndependentMod = new IndependentMod;

		$this->PluginDomain = $this->IndependentMod->EnvMgr->get('PLUGIN_DOMAIN');
		$this->IsLangLoaded = 0;

		$this->AdminConfigPage = null;
	}

	function TestLangLoaded()
	{
		if (!$this->IsLangLoaded) {
			$TranslationRelPath = $this->PluginDomain . '/framework/Tsukuyomi/Translations/';

			load_plugin_textdomain(
				$this->PluginDomain,
				false,
				$TranslationRelPath
			);
		}

		$Original = 'Tsukuyomi Framework';
		$Translation = __('Tsukuyomi Framework', $this->PluginDomain);

		if (strcmp($Original, $Translation) === 0) {
			$ErrorMsg = sprintf(
				'未正確讀取到翻譯檔，請檢查程式設定或檔案位置是否正確。<br>翻譯測試原文：%s<br>翻譯測試結果：%s',
				$Original,
				$Translation
			);

			$this->apf_admin_notice($ErrorMsg, array('class' => 'error'));

			return;
		}

		$this->IsLangLoaded = 1;
	}

	function AdminCfgPages()
	{
		if ($this->AdminConfigPage === null)
			$this->AdminConfigPage = new AdminConfigPage(
				$this->IndependentMod->Str,
				$this->IndependentMod->PathMgr
			);

		return $this->AdminConfigPage;
	}

	function apf_admin_notice(...$Arguments)
	{
		$ANClass = '\\' . $this->env('PLUGIN_APF_PREFIX') . '_AdminPageFramework_AdminNotice';
		return new $ANClass(...$Arguments);
	}

	function EnqueueOnce(...$QueueArguments)
	{
		$this->IndependentMod->WP->enqueue_script_once(...$QueueArguments);
	}

	function Indept()
	{
		return $this->IndependentMod;
	}

	function env(...$Arguments)
	{
		return $this->IndependentMod->EnvMgr->get(...$Arguments);
	}

	function carbon_proxy()
	{
		return $this->IndependentMod->CbnProxy;
	}

	function carbon(...$Arguments)
	{
		return $this->IndependentMod->CbnProxy->carbon(...$Arguments);
	}

	function now()
	{
		return $this->IndependentMod->CbnProxy->now();
	}

	function str()
	{
		return $this->IndependentMod->Str;
	}

	function logr()
	{
		return $this->IndependentMod->Debugger->logger();
	}

	function wp()
	{
		return $this->IndependentMod->WP;
	}

	function lib()
	{
		return $this->IndependentMod->LibShortcut;
	}

	function ip()
	{
		return $this->lib()->getIp();
	}

	function plugin_path()
	{
		return $this->IndependentMod->PathMgr->plugin_root();
	}

	function blade($View = null, $Cache = null)
	{
		return $this->IndependentMod->Blade($View, $Cache);
	}

	function encrypter()
	{
		return $this->IndependentMod->Encrypter;
	}

	function option()
	{
		return $this->IndependentMod->OptionsMgr;
	}

	function transient()
	{
		return $this->IndependentMod->TransientMgr;
	}

	function model($TblName, $DefaultFormat = [], $IsPrependPrefix = 1)
	{
		return new Model($TblName, $DefaultFormat, $IsPrependPrefix, $this->IndependentMod->EnvMgr);
	}

	function vendor_loader()
	{
		return new VendorLoader($this->IndependentMod->PathMgr);
	}

	function plugin_cookie($Suffix = null)
	{
		if (!is_null($Suffix))
			$Suffix = '_' . $Suffix;

		return new CookieMgr(
			$this->env('PLUGIN_APF_PREFIX') . $Suffix,
			$this->encrypter(),
			$this->option(),
			$this->carbon_proxy()
		);
	}
}
