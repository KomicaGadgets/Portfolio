<?php

namespace MauticPlugin\{*PluginName_NoSpace*}Bundle\EventListener;

use Mautic\EmailBundle\{
	EmailEvents,
	EmailBuilderEvent,
	EmailSendEvent
};
use Mautic\CoreBundle\Helper\{
	BuilderTokenHelper,
	UrlHelper
};
use Mautic\{
	LeadBundle\Helper\TokenHelper,
	PluginBundle\Helper\IntegrationHelper
};

class EmailSubscriber implements \Symfony\Component\EventDispatcher\EventSubscriberInterface
{
	/**
	 * @var IntegrationHelper
	 */
	private $integrationHelper;

	function __construct(IntegrationHelper $integrationHelper)
	{
		$this->integrationHelper = $integrationHelper;
		$this->{*PluginName_UpperShortOrNoSpace*}Key = $this->integrationHelper->getIntegrationObject('{*PluginName_UpperShortOrNoSpace*}')->getKeys();
		$this->HMACKey = empty($this->{*PluginName_UpperShortOrNoSpace*}Key['hmac_key'])
			? '✫✬✭✮✯✰✡⁂⇒⇐↾↿↼⥘⥙⤞⤝⤠⤟⇏⇍⇎⇕⇗⇖⇘⇙➾⇛⇚⇝⇜⇞⇟⇨⇩⇪⌅⌆⌤⏎☇☈☊☋☌☍➳➷➸➹➺➻➼➽'
			: $this->{*PluginName_UpperShortOrNoSpace*}Key['hmac_key'];
	}

	/**
	 * @return array
	 */
	public static function getSubscribedEvents()
	{
		return [
			EmailEvents::EMAIL_ON_BUILD => ['onEmailBuild', 0],
			EmailEvents::EMAIL_ON_SEND => ['onEmailGenerate', 0],
			EmailEvents::EMAIL_ON_DISPLAY => ['onEmailGenerate', 0],
		];
	}

	/**
	 * @param EmailBuilderEvent $event
	 *
	 * @throws \InvalidArgumentException
	 * @throws \RuntimeException
	 */
	public function onEmailBuild(EmailBuilderEvent $event)
	{ }

	/**
	 * Search and replace tokens with content
	 *
	 * @param EmailSendEvent $event
	 */
	public function onEmailGenerate(EmailSendEvent $event)
	{
		$Lead = $event->getLead();
		$tokenList = TokenHelper::findLeadTokens($event->getContent() . $event->getPlainText(), $Lead);

		if (array_key_exists('{contactfield=ev_link}', $tokenList)) {
			$TokenValidHours = empty($this->DOIKey['token_valid_hours'])
				? 2
				: (int) $this->DOIKey['token_valid_hours'];

			$ContactID = $Lead['id'];
			$Expiration = time() + ($TokenValidHours * 60 * 60);

			$Sign = hash_hmac('whirlpool', sprintf('%d|%d', $ContactID, $Expiration), $this->HMACKey);

			$RootURL = empty($this->DOIKey['root_url'])
				? 'https://localhost/Mautic'
				: rtrim($this->DOIKey['root_url'], '/');

			$SignedURLSuffix = sprintf(
				'doi/ev/%d/%d/%s',
				$ContactID,
				$Expiration,
				$Sign
			);

			$SignedURL = sprintf('%s/%s', $RootURL, $SignedURLSuffix);

			$event->setContent(str_replace('{contactfield=ev_link}', $SignedURL, $event->getContent()));
			$event->setPlainText(str_replace('{contactfield=ev_link}', $SignedURL, $event->getPlainText()));
		}
	}
}
