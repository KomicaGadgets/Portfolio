<?php

namespace MauticPlugin\{*PluginName_NoSpace*}Bundle\EventListener;

use Mautic\{
	PluginBundle\Helper\IntegrationHelper,
	LeadBundle\Model\LeadModel
};
use Mautic\CampaignBundle\{
	CampaignEvents,
	Event as Events,
	Event\CampaignExecutionEvent
};
// use MauticPlugin\{*PluginName_NoSpace*}Bundle\Form\Type\AdjustLeadFieldNumberType;

class CampaignSubscriber implements \Symfony\Component\EventDispatcher\EventSubscriberInterface
{
	const ACTION_NAME = '{*PluginName_UpperShortOrNoSpace*}.AdjustLeadFieldNumber';

	/**
	 * @var IntegrationHelper
	 */
	private $integrationHelper;

	private $leadModel;

	/**
	 * CampaignSubscriber constructor.
	 *
	 * @param IntegrationHelper $integrationHelper
	 */
	public function __construct(IntegrationHelper $integrationHelper, LeadModel $leadModel)
	{
		$this->integrationHelper = $integrationHelper;
		$this->leadModel = $leadModel;
		$this->{*PluginName_UpperShortOrNoSpace*}Key = $this->integrationHelper->getIntegrationObject('{*PluginName_UpperShortOrNoSpace*}')->getKeys();
	}

	/**
	 * @return array
	 */
	static public function getSubscribedEvents()
	{
		return [
			CampaignEvents::CAMPAIGN_ON_BUILD => ['onCampaignBuild', 0],
			'{*PluginName_LowerOrUnderline*}.on_campaign_trigger_action' => [
				['onCampaignTriggerActionAdjustLeadFieldNumber', 0]
			],
		];
	}

	/**
	 * Add campaign decision and actions
	 *
	 * @param Events\CampaignBuilderEvent $event
	 */
	public function onCampaignBuild(Events\CampaignBuilderEvent $event)
	{
		$Action = [
			'label'	=>	'{*PluginName_LowerOrUnderline*}.adjust_lead_field_number',
			'description'	=>	'{*PluginName_LowerOrUnderline*}.adjust_lead_field_number_descr',
			'formType'	=>	AdjustLeadFieldNumberType::class,
			'formTheme'	=>	'{*PluginName_NoSpace*}Bundle:FormTheme\FieldNumberAction',
			'eventName'	=>	'{*PluginName_LowerOrUnderline*}.on_campaign_trigger_action',
		];

		$event->addAction(self::ACTION_NAME, $Action);
	}

	/**
	 * @param CampaignExecutionEvent $event
	 */
	public function onCampaignTriggerActionAdjustLeadFieldNumber(CampaignExecutionEvent $event)
	{
		if (!$event->checkContext(self::ACTION_NAME))
			return;

		$Contact = $event->getLead();
		$LeadDetail = $this->leadModel->getLeadDetails($Contact);

		$TargetLeadField = $event->getConfig()['field'];
		$LeadFieldOriginalValue = $LeadDetail['core'][$TargetLeadField]['value'];
		$AdjustValue = $event->getConfig()['number_val'];

		$this->leadModel->setFieldValues($Contact, [
			$TargetLeadField	=>	$LeadFieldOriginalValue + $AdjustValue
		], false, false);

		$this->leadModel->saveEntity($Contact);

		return $event->setResult(true);
	}
}
