<?php

namespace PostStatusBroadcaster\Core;

class PostTransitionBroadcaster
{
	use \PostStatusBroadcaster\Proxies\SingletonBaseProxy;

	function __construct()
	{
		$this->FieldPrefix = psb_tsukuyomi()->env('PLUGIN_VAR_PREFIX');
		$this->OptMgr = psb_tsukuyomi()->option();
	}

	function SendSignal($Method = 'GET', $URL, $JSONParam = [])
	{
		$body = null;

		if (empty($JSONParam))
			$JSONParam = ['placeholder'	=>	'no_data'];

		$GuzOption = [
			'query'	=>	$JSONParam,
			'form_params'	=>	$JSONParam,
			'timeout'	=>	30
		];

		if (defined('WP_DEBUG') && WP_DEBUG === true)
			$GuzOption['verify'] = false;

		try {
			$Client = psb_tsukuyomi()->lib()->guzzle();
			$response = $Client->request($Method, $URL, $GuzOption);

			$body = json_decode($response->getBody()->getContents());
		} catch (\Throwable $th) { }

		return $body;
	}

	function BroadcastToWebhook($cfg)
	{
		$JSONParams = empty($cfg[$this->FieldPrefix . '_parameters'])
			? []
			: json_decode($cfg[$this->FieldPrefix . '_parameters'], true);

		if (
			isset($cfg[$this->FieldPrefix . '_secret_key_mixed']['secret_key']) &&
			!empty($cfg[$this->FieldPrefix . '_secret_key_mixed']['secret_key'])
		) {
			$AuthMethod = $cfg[$this->FieldPrefix . '_authentication_method'];
			$SecretKeyField = sprintf('wp_%s_auth_token', $this->FieldPrefix);

			switch ((int) $AuthMethod) {
				case 1:
					$ExpNum = (isset($cfg[$this->FieldPrefix . '_expiration_mixed']['exp_num']) &&
						!empty($cfg[$this->FieldPrefix . '_expiration_mixed']['exp_num']))
						? $cfg[$this->FieldPrefix . '_expiration_mixed']['exp_num']
						: 5;

					$ExpUnit = $cfg[$this->FieldPrefix . '_expiration_mixed']['exp_unit'];
					$Expiration = psb_tsukuyomi()->now()->add(
						sprintf('%d %s', $ExpNum, $ExpUnit)
					)->timestamp;

					$AuthToken = hash_hmac('sha256', $Expiration, $cfg[$this->FieldPrefix . '_secret_key_mixed']['secret_key']);
					$JSONParams[sprintf('wp_%s_expiration', $this->FieldPrefix)] = $Expiration;
					$JSONParams[$SecretKeyField] = $AuthToken;
					break;

				default:
					$JSONParams[$SecretKeyField] = $cfg[$this->FieldPrefix . '_secret_key_mixed']['secret_key'];
			}
		}

		$this->SendSignal(
			$cfg[$this->FieldPrefix . '_request_method'],
			$cfg[$this->FieldPrefix . '_target_url'],
			$JSONParams
		);
	}

	function PostTransitionListener($new_status, $old_status, $post)
	{
		if ($post->post_type !== 'post')
			return; // restrict the filter to a specific post type

		$WebhookSetting = $this->OptMgr->GetAPFOption('PostWebhookSetting');

		if (!empty($WebhookSetting)) {
			$WebhookSetting = $WebhookSetting['webhook_setting_section'];

			foreach ($WebhookSetting as $cfg) {
				if (!empty($cfg[$this->FieldPrefix . '_target_url'])) {
					if (
						$old_status === $cfg[$this->FieldPrefix . '_old_status'] &&
						$new_status === $cfg[$this->FieldPrefix . '_new_status']
					) {
						try {
							$this->BroadcastToWebhook($cfg);
						} catch (\Throwable $th) { }
					}
				}
			}
		}
	}

	function Ajax_TestParamJSON()
	{
		$ParamJSON = $_POST['param_json'];

		$Output = [
			'type'	=>	'success'
		];

		try {
			$Test = json_decode($ParamJSON, true);
		} catch (\Throwable $th) {
			$Output['type'] = 'fail';
		}

		wp_send_json($Output);
	}

	// function t()
	// {
	// 	$A = psb_tsukuyomi()->now()->add('100 minute')->timestamp;
	// 	$Client = psb_tsukuyomi()->lib()->guzzle();
	// 	$Post = $this->SendSignal(
	// 		'GET',
	// 		'apache2/Mautic/wpnpn/new_post_notify',
	// 		[
	// 			'campaign_id'	=>	3,
	// 			'wp_poststatusbroadcaster_expiration'	=>	$A,
	// 			'wp_poststatusbroadcaster_auth_token'	=>	hash_hmac('sha256', $A, 'Ycf7KNTGSRgZD4Md1b9PEFpGuKfji0cM')
	// 		]
	// 	);

	// 	dd($Post);
	// }
}
