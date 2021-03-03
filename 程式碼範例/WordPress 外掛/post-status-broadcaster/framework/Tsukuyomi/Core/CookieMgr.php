<?php

namespace PostStatusBroadcaster\Tsukuyomi\Core;

use \Delight\Cookie\Cookie;
use \Carbon\Carbon;

use PostStatusBroadcaster\Tsukuyomi\Core\Independent\{
	CarbonProxy,
	Encrypter,
	OptionsMgr
};

class CookieMgr
{
	function __construct($Name, Encrypter $Encrypter, OptionsMgr $OptionsMgr, CarbonProxy $CarbonProxy)
	{
		$this->CookieName = $Name;
		$this->Encrypter = $Encrypter;
		$this->OptionsMgr = $OptionsMgr;
		$this->CbnProxy = $CarbonProxy;

		$this->CookieKeyOptName = 'tsukuyomi_cookie_key';
		$this->CookieKey = null;

		$this->IsCookieExist = Cookie::exists($this->CookieName);
		$this->Cookie = new Cookie($this->CookieName);

		$this->EnsureCookieKey();
		$this->CookieValue = collect(
			$this->IsCookieExist
				? $this->Encrypter->LaraDecrypt(Cookie::get($this->CookieName), $this->CookieKey, [])
				: []
		);

		$this->MaxAge = 60 * 60 * 24;
		$this->Domain = '';
		$this->HttpOnly = true;
		$this->SecureOnly = false;
		$this->SameSite = 'Strict';
	}

	function EnsureCookieKey()
	{
		if ($this->OptionsMgr->IsOptionExist($this->CookieKeyOptName)) {
			$this->CookieKey = get_option($this->CookieKeyOptName);
		} else {
			$NewKey = $this->Encrypter->RandomHex(32);
			update_option($this->CookieKeyOptName, $NewKey, true);
			$this->CookieKey = $NewKey;
		}
	}

	function put(...$Arguments)
	{
		$this->CookieValue->put(...$Arguments);
		return $this;
	}

	function get(...$Arguments)
	{
		return $this->CookieValue->get(...$Arguments);
	}

	function Manipulate($Method, ...$Arguments)
	{
		$this->Cookie->$Method(...$Arguments);
		return $this;
	}

	function Save(Carbon $ExpiryDateTime = null)
	{
		$SecureContent = $this->Encrypter->LaraEncrypt($this->CookieValue->all(), $this->CookieKey);

		if (!$this->IsCookieExist) {
			if (!empty($this->Domain))
				$this->Cookie->setDomain($this->Domain);

			$this->Cookie->setSecureOnly($this->SecureOnly);
			$this->Cookie->setSameSiteRestriction($this->SameSite);
		}

		if (!is_null($ExpiryDateTime))
			$this->MaxAge = $ExpiryDateTime->diffInSeconds($this->CbnProxy->now());

		$this->Cookie->setMaxAge($this->MaxAge);
		$this->Cookie->setValue($SecureContent)->save();
	}
}
