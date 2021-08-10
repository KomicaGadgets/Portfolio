<?php

namespace MauticPlugin\{*PluginName_NoSpace*}Bundle\EventListener;

use Mautic\{
	EmailBundle\Model\EmailModel,
	PluginBundle\Helper\IntegrationHelper,
};
use Mautic\LeadBundle\{
	Event\ListChangeEvent,
	LeadEvents,
};
use Psr\Log\LoggerInterface;

class LeadSubscriber implements \Symfony\Component\EventDispatcher\EventSubscriberInterface
{
	/**
	 * @var IntegrationHelper
	 */
	private $integrationHelper;

	/**
	 * @var LoggerInterface
	 */
	private $logger;

	private $emailModel;

	public function __construct(
		IntegrationHelper $integrationHelper,
		LoggerInterface $logger,
		EmailModel $emailModel
	) {
		$this->integrationHelper = $integrationHelper;
		$this->logger	=	$logger;
		$this->emailModel = $emailModel;
		$this->IntegrationObj = $this->integrationHelper->getIntegrationObject('{*PluginName_UpperShortOrNoSpace*}');
		$this->IsPublished = $this->IntegrationObj->IsPublished() ?? false;
		$this->FeatSettings = $this->IntegrationObj->GetFeatureSettings();
		$this->NotifyEmailID = (int)$this->FeatSettings['notification_email_id'];
		$this->NotifySegmentIDList = $this->FeatSettings['notify_segment_list'];
	}

	/**
	 * @return array
	 */
	public static function getSubscribedEvents()
	{
		// 透過標籤加入名單時要用 LEAD_LIST_BATCH_CHANGE 這個事件
		return [
			LeadEvents::LEAD_LIST_BATCH_CHANGE	=>	['onLeadListBatchChange', 0],
		];
	}

	public function onLeadListBatchChange(ListChangeEvent $event)
	{
		// $this->logger->error('$ListID', [$ListID]);
		// $this->logger->error('$LeadID', [$LeadID]);

		// $this->logger->error('BatchChange - wasAdded()', [$event->wasAdded()]);

		if ($this->IsPublished) {
			if ($event->wasAdded()) {
				$ListID = $event->getList()->getId();

				$Lead = is_null($event->getLead())
					? reset($event->getLeads())	// reset會回傳陣列裡第一個元素
					: $event->getLead();

				if (!empty($ListID) && !empty($Lead)) {
					if (in_array($ListID, $this->NotifySegmentIDList)) {
						$Output = $this->emailModel->sendEmail(
							$this->emailModel->getEntity($this->NotifyEmailID),
							$Lead
						);
					}
				}
			}
		}
	}
}
