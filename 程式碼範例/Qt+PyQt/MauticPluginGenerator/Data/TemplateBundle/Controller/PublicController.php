<?php

namespace MauticPlugin\{*PluginName_NoSpace*}Bundle\Controller;

use MauticPlugin\{*PluginName_NoSpace*}Bundle\Integration\{*PluginName_UpperShortOrNoSpace*}Integration;

class PublicController extends \Mautic\CoreBundle\Controller\CommonController
{
	public function testAction()
	{
		$this->SNFeatSetting = $this->get('mautic.helper.integration')
			->getIntegrationObject({*PluginName_UpperShortOrNoSpace*}Integration::NAME)
			->GetFeatureSettings();

		dd($this->SNFeatSetting);

		exit();
	}
}
