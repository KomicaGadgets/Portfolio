<?php

use PostStatusBroadcaster\Proxies\{
	TsukuyomiProxy
};

use PostStatusBroadcaster\Core\{
	AuthenticateSetting,
	PostTransitionBroadcaster
};

if (!function_exists('psb_tsukuyomi')) {
	function psb_tsukuyomi()
	{
		return TsukuyomiProxy::getInstance();
	}
}

if (!function_exists('psb_authenticate_setting')) {
	function psb_authenticate_setting()
	{
		return AuthenticateSetting::getInstance();
	}
}

if (!function_exists('psb_post_transition_broadcaster')) {
	function psb_post_transition_broadcaster()
	{
		return PostTransitionBroadcaster::getInstance();
	}
}
