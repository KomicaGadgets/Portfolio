<?php

namespace PostStatusBroadcaster\admin\ConfigPages;

use PostStatusBroadcaster\Tsukuyomi\Blueprint\ConfigElementBlueprint;

class PostWebhookSetting extends ConfigElementBlueprint
{
	function __construct()
	{
		$this->APFOptKey = 'PostStatusBroadcaster_PostWebhookSetting';
		$this->IDPrefix = psb_tsukuyomi()->env('PLUGIN_VAR_PREFIX');

		parent::__construct($this->APFOptKey);
	}

	public function setUp()
	{
		$this->setRootMenuPage(psb_tsukuyomi()->env('PLUGIN_NAME'));

		$this->addSubMenuItems(
			[
				'title'	=>	'動作與文章狀態對應設定',
				'page_slug'	=>	'PostStatusBroadcaster_PostWebhookSetting',
			]
		);

		$this->addSettingSections(
			'PostStatusBroadcaster_PostWebhookSetting',
			[
				'section_id'	=>	'webhook_setting_section',
				'title'	=>	'文章狀態廣播群組',
				'description'	=>	'This section is for text fields.',
				'repeatable'	=>	true,
				'sortable'	=>	true,
				'collapsible'	=>	[
					'toggle_all_button'	=>	['top-left', 'bottom-left'],
					'container'	=>	'section',
				],
			]
		);
	}

	public function load_PostStatusBroadcaster_PostWebhookSetting($oAdminPage)
	{
		$this->addSettingFields(
			'webhook_setting_section',
			[
				'field_id'	=>	'setting_name',
				'type'	=>	'section_title',
				'label'	=>	'<h4>文章狀態廣播群組 :: </h4>',
				'attributes'	=>	[
					'size'	=>	50,
					'placeholder'	=>	'自訂群組名稱，例如：新文章通知電子報系統寄信',
				]
			],
			[
				'field_id'	=>	'old_status',
				'title'	=>	'舊文章狀態',
				'description'	=>	'選擇要觸發此組連線的舊文章狀態，一旦有文章從舊狀態轉變成新狀態時，系統就會向目標網址傳送連線請求。',
				'type'	=>	'select',
				'default'	=>	'future',
				'label'	=>	$this->PostStatusList(),
			],
			[
				'field_id'	=>	'new_status',
				'title'	=>	'新文章狀態',
				'description'	=>	'選擇要觸發此組連線的新文章狀態，一旦有文章從舊狀態轉變成新狀態時，系統就會向目標網址傳送連線請求。',
				'type'	=>	'select',
				'default'	=>	'publish',
				'label'	=>	$this->PostStatusList(),
			],
			[
				'field_id'	=>	'authentication_method',
				'title'	=>	'驗證方式',
				'description'	=>	'在此選擇目標網址要如何驗證連線來源。',
				'type'	=>	'select',
				'default'	=>	0,
				'label'	=>	[
					0	=>	'純密鑰',
					1	=>	'HMAC-SHA256'
				],
				'attributes'	=>	[
					'select'	=>	[
						'class'	=>	'AuthMethodSlct',
					]
				]
			],
			[
				'field_id'	=>	'secret_key_mixed',
				'type'	=>	'inline_mixed',
				'title'	=>	'密鑰',
				'description'	=>	'輸入要用於驗證此組連線的密鑰／密碼。',
				'content'	=>	[
					[
						'field_id'	=>	'secret_key',
						'type'	=>	'text',
						'attributes'	=>	[
							'size' =>	70,
							'placeholder'	=>	'例如：UN3jf3zBHeZNZhSNY9arCUh4dj2EvAvk',
						]
					],
					[
						'field_id'	=>	'copy_secret_key_btn',
						'label'	=>	'複製密鑰',
						'type'	=>	'submit',
						'save'	=>	false,
						'attributes'	=>	[
							'class'	=>	'button button-primary CopySecretKeyBtn',
							'data-tippy-content'	=>	'複製密鑰',
							'fieldset'	=>	[
								'style'	=>	'display: inline-block; vertical-align: top;',
							],
						]
					],
					[
						'field_id'	=>	'make_secret_key_btn',
						'label'	=>	'自動產生密鑰',
						'type'	=>	'submit',
						'save'	=>	false,
						'attributes'	=>	[
							'class'	=>	'button button-primary MakeSecretKeyBtn',
							'fieldset'	=>	[
								'style'	=>	'display: inline-block; vertical-align: top;',
							],
						]
					]
				],
			],
			[
				'field_id'	=>	'expiration_mixed',
				'type'	=>	'inline_mixed',
				'title'	=>	'有效時限',
				'description'	=>	'輸入經 HMAC-SHA256 結合密鑰所計算出之連線驗證碼的有效期限，預設值為 5 分鐘，若網路環境不佳導致連線緩慢則可提高有效時限避免逾時。',
				'attributes'	=>	[
					'fieldrow'	=>	[
						'class'	=>	'ExpirationField'
					]
				],
				'content'	=>	[
					[
						'field_id'	=>	'exp_num',
						'type'	=>	'number',
						'default'	=>	5,
						'attributes'	=>	[
							'size' =>	20,
							'placeholder'	=>	'例如：5',
						]
					],
					[
						'field_id'	=>	'exp_unit',
						'type'	=>	'select',
						'label_min_width'	=>	'',
						'label'	=>	[
							'second'	=>	'秒',
							'minute'	=>	'分鐘',
							'hour'	=>	'小時'
						],
						'default'	=> 'minute',
					]
				],
			],
			[
				'field_id'	=>	'request_method',
				'title'	=>	'連線請求方式',
				'description'	=>	'在此選擇要送出什麼類型的請求給目標網址。',
				'type'	=>	'select',
				'default'	=>	'GET',
				'label'	=>	[
					'GET'	=>	'GET',
					'POST'	=>	'POST',
					'HEAD'	=>	'HEAD',
					'PUT'	=>	'PUT',
					'DELETE'	=>	'DELETE',
					'OPTIONS'	=>	'OPTIONS',
					'PATCH'	=>	'PATCH'
				]
			],
			[
				'field_id'	=>	'target_url',
				'type'	=>	'text',
				'title'	=>	'目標網址',
				'description'	=>	'在此輸入你要傳送請求的目標網址。',
				'attributes'	=>	[
					'size' =>	70,
					'placeholder'	=>	'例如：https://www.example.com/listener.php?id=344',
				]
			],
			[
				'field_id'	=>	'parameters',
				'type'	=>	'textarea',
				'title'	=>	'傳輸參數',
				'description'	=>	'在此輸入你要傳送給目標網址的參數，使用 JSON 格式來呈現所有要傳送的參數。',
				'attributes'	=>	[
					'rows' => 15,
					'cols' => 120,
					'class'	=>	'ParamsTextarea',
					'placeholder'	=>	$this->ExampleJSON()
				],
				'after_input'	=>	'<p class="post-status-broadcaster-fields-description"><strong>' .
					'<span id="ValidatingJSONMsg" style="display: none;">正在驗證 JSON 格式...</span>' .
					'<span id="ValidateJSONSuccessAlert" style="display: none; color: #5cb85c;">JSON 格式已通過驗證！</span>' .
					'<span id="ValidateJSONFailedAlert" style="display: none; color: #d9534f;">JSON 驗證失敗！<br>繼續使用可能會導致資料損毀。</span></strong></p>'
			]
		);
	}

	public function do_PostStatusBroadcaster_PostWebhookSetting()
	{
		echo '<script>
	!function ($, n) { var r, e, t = {}, c = {}; $$ = function (f, u) { return u ? ((r = u.selector) && (u = r), e = c[u], e === n && (e = c[u] = {}), r = e[f], r !== n ? r : e[f] = $(f, $$(u))) : (r = t[f], r !== n ? r : t[f] = $(f)) }, $$clear = function ($, e) { e ? ((r = e.selector) && (e = r), $ && (r = c[e]) && (r[$] = n), c[e] = n) : $ ? (t[$] = n, c[$] = n) : (t = {}, c = {}) }, $$fresh = function ($, n) { return $$clear($, n), $$($, n) }, $.fn.$$ = function ($) { return $$($, this) }, $.fn.$$clear = function ($) { $$clear($, this) }, $.fn.$$fresh = function ($) { return $$fresh($, this) } }(jQuery)
</script>';
		echo sprintf('<script defer src="%sadmin/js/WebhookSetting.js"></script>', plugin_dir_url(dirname(__DIR__)));
		echo '<script defer src="https://unpkg.com/@popperjs/core@2"></script>';
		echo '<script defer src="https://unpkg.com/tippy.js@6"></script>';

		submit_button();
	}

	function PostStatusList()
	{
		return [
			'new'	=>	'新文章',
			'publish'	=>	'已發佈',
			'pending'	=>	'待審閱',
			'draft'	=>	'草稿',
			'auto-draft'	=>	'自動草稿',
			'future'	=>	'已排程',
			'private'	=>	'私密',
			'inherit'	=>	'內容修訂或附件',
			'trash'	=>	'回收桶'
		];
	}

	function ExampleJSON()
	{
		return <<<'EOT'
		{
		  "key1": "value1",
		  "key2": "value2",
		  "key3": "value3"
		}
		EOT;
	}
}
