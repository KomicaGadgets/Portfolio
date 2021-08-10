<?php

return [
	'name'        => '{*PluginChName*}',
	'description' => '{*PluginDesc*}',
	'version'     => '1.0',
	'author'      => 'Software Author',
	'routes' => [
		'public' => [
			// 'mautic_{*PluginName_LowerShortOrUnderline*}_test' => [
			// 	'path' => '/{*PluginName_LowerShortOrUnderline*}/t',
			// 	'controller' => '{*PluginName_NoSpace*}Bundle:Public:test',
			// ],
		],
	],
	'services'    => [
		<FormService>'forms'  => [
			'plugin.{*PluginName_LowerShortOrLowerNoSpace*}.form.type.adjust_lead_field_number' => [
				'class' => 'MauticPlugin\{*PluginName_NoSpace*}Bundle\Form\Type\AdjustLeadFieldNumberType',
				'arguments' => [
					'translator',
					'mautic.lead.model.lead',
					'mautic.lead.model.field'
				],
				'alias' => 'campaignevent_adjust_lead_field_number'
			]
		],</FormService>
		'events' => [
			<CampaignSub>'plugin.{*PluginName_LowerShortOrLowerNoSpace*}.campaignbundle.subscriber' => [
				'class' => 'MauticPlugin\{*PluginName_NoSpace*}Bundle\EventListener\CampaignSubscriber',
				'arguments' => [
					'mautic.helper.integration',
					'mautic.lead.model.lead',
					'translator',
				],
			],</CampaignSub>
			<EmailSub>'plugin.{*PluginName_LowerShortOrLowerNoSpace*}.emailbundle.subscriber' => [
				'class' => 'MauticPlugin\{*PluginName_NoSpace*}Bundle\EventListener\EmailSubscriber',
				'arguments' => [
					'mautic.helper.integration',
				],
			],</EmailSub>
			<LeadSub>'plugin.{*PluginName_LowerShortOrLowerNoSpace*}.leadbundle.subscriber' => [
				'class' => 'MauticPlugin\{*PluginName_NoSpace*}Bundle\EventListener\LeadSubscriber',
				'arguments' => [
					'mautic.helper.integration',
					'logger',
					'mautic.email.model.email',
				],
			],</LeadSub>
		],
		'integrations' => [
			'mautic.integration.{*PluginName_LowerShortOrLowerNoSpace*}' => [
				'class'	=>	\MauticPlugin\{*PluginName_NoSpace*}Bundle\Integration\{*PluginName_UpperShortOrNoSpace*}Integration::class,
				'arguments' => [
					'event_dispatcher',
					'mautic.helper.cache_storage',
					'doctrine.orm.entity_manager',
					'session',
					'request_stack',
					'router',
					'translator',
					'logger',
					'mautic.helper.encryption',
					'mautic.lead.model.lead',
					'mautic.lead.model.company',
					'mautic.helper.paths',
					'mautic.core.model.notification',
					'mautic.lead.model.field',
					'mautic.plugin.model.integration_entity',
					'mautic.lead.model.dnc',
				],
			],
		],
	],
];
