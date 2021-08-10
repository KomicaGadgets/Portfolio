<?php

namespace MauticPlugin\{*PluginName_NoSpace*}Bundle\Integration;

use Mautic\{
	LeadBundle\Form\Type\LeadListType,
	EmailBundle\Form\Type\EmailListType
};

use Symfony\Component\Validator\Constraints\NotBlank;

class {*PluginName_UpperShortOrNoSpace*}Integration extends \Mautic\PluginBundle\Integration\AbstractIntegration
{
	public const NAME	=	'{*PluginName_UpperShortOrNoSpace*}';
	public const DISPLAY_NAME	=	'{*PluginChName*}';

	/**
	 * @return string
	 */
	public function getName(): string
	{
		return self::NAME;
	}

	/**
	 * @return string
	 */
	public function getDisplayName(): string
	{
		return self::DISPLAY_NAME;
	}

	public function getIcon(): string
	{
		return 'plugins/{*PluginName_NoSpace*}Bundle/Assets/img/plugin-icon.png';
	}

	/**
	 * Return's authentication method such as oauth2, oauth1a, key, etc.
	 *
	 * @return string
	 */
	public function getAuthenticationType()
	{
		// Just use none for now and I'll build in "basic" later
		return 'none';
	}

	/**
	 * Return array of key => label elements that will be converted to inputs to
	 * obtain from the user.
	 *
	 * @return array
	 */
	public function getRequiredKeyFields()
	{
		return [
			// 'secret' => 'mautic.integration.gmail.secret',
			// 'notification_email_id'	=>	'{*PluginName_LowerShortOrUnderline*}.notification_email_id',
		];
	}

	/**
	 * @param \Mautic\PluginBundle\Integration\Form|FormBuilder $builder
	 * @param array                                             $data
	 * @param string                                            $formArea = keys|features|integration
	 */
	public function appendToForm(&$builder, $data, $formArea)
	{
		if ($formArea === 'features') {
			$builder->add(
				'notification_email_id',
				EmailListType::class,
				[
					'label'      => '{*PluginName_LowerShortOrUnderline*}.notification_email',
					'label_attr' => ['class' => 'control-label'],
					'attr'       => [
						'class'    => 'form-control',
						'tooltip'  => '{*PluginName_LowerShortOrUnderline*}.tooltip',
						// 'onchange' => 'Mautic.disabledEmailAction(window, this)',
					],
					'multiple'    => false,
					'required'    => true,
					'constraints' => [
						new NotBlank(
							['message' => '{*PluginName_LowerShortOrUnderline*}.constraints.message']
						),
					],
				]
			);

			$builder->add(
				$builder->create(
					'notify_segment_list',
					LeadListType::class,
					[
						'label'      => '{*PluginName_LowerShortOrUnderline*}.notify_segment_list',
						'label_attr' => ['class' => 'control-label'],
						'attr'       => [
							'class'        => 'form-control',
							// 'data-show-on' => '{"emailform_segmentTranslationParent":[""]}',
						],
						'multiple' => true,
						'expanded' => false,
						'required' => true,
					]
				)
			);
		}
	}

	/*************************************************
	 ****************Custom Functions*****************
	 *************************************************/

	function IsPublished()
	{
		return $this->getIntegrationSettings()->getIsPublished();
	}

	function GetAPIKeys()
	{
		return $this->getKeys();
	}

	function GetFeatureSettings()
	{
		return $this->getIntegrationSettings()->getFeatureSettings();
	}
}
