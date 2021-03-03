<?php

namespace PostStatusBroadcaster;

class HookMgr
{
	function __construct($APFLoader = null)
	{
		$this->APFLoader = $APFLoader;
		$this->IsAjaxRegistered = 0;
		$this->IsFilterRegistered = 0;
	}

	private function CronActions()
	{
		return [];
	}

	private function AjaxActions()
	{
		return [
			[0, ['MakeSecretKey', psb_authenticate_setting(), 'Ajax_MakeSecretKey']],
			[0, ['TestParamJSON', psb_post_transition_broadcaster(), 'Ajax_TestParamJSON']]
		];
	}

	private function CoreActions()
	{
		return [
			['transition_post_status', psb_post_transition_broadcaster(), 'PostTransitionListener', 10, 3]
		];
	}

	private function APFFilters()
	{
		return [];
	}

	function SetCronAction()
	{
		foreach ($this->CronActions() as $action) {
			$WPCronAction = $action;
			$WPCronAction[0] = psb_tsukuyomi()->env('PLUGIN_VAR_PREFIX') . '_' . $action[0];

			$this->APFLoader->add_action(...$WPCronAction);
		}
	}

	function SetAjaxAction()
	{
		$WPDebugEnabled = (defined('WP_DEBUG') && WP_DEBUG === true);

		foreach ($this->AjaxActions() as $action) {
			$IsPublic = $action[0];
			$WPAction = $action[1];

			$WPAjaxPrefix = 'wp_ajax_' . ($IsPublic ? 'nopriv_' : '');
			$WPAction[0] = $WPAjaxPrefix . $WPAction[0];

			$this->APFLoader->add_action(...$WPAction);

			if ($IsPublic && $WPDebugEnabled) {
				$WPAction = $action[1];
				$WPAction[0] = 'wp_ajax_' . $WPAction[0];
				$this->APFLoader->add_action(...$WPAction);
			}
		}
	}

	function SetCoreAction()
	{
		foreach ($this->CoreActions() as $action) {
			$this->APFLoader->add_action(...$action);
		}
	}

	function SetFilter()
	{
		foreach ($this->APFFilters() as $filter) {
			$this->APFLoader->add_filter(...$filter);
		}
	}

	function Run()
	{
		if (!is_null($this->APFLoader)) {
			$this->SetCronAction();

			if (!$this->IsAjaxRegistered) {
				$this->SetAjaxAction();
				$this->IsAjaxRegistered = 1;
			}

			$this->SetCoreAction();

			if (!$this->IsFilterRegistered) {
				$this->SetFilter();
				$this->IsFilterRegistered = 1;
			}
		}
	}
}
