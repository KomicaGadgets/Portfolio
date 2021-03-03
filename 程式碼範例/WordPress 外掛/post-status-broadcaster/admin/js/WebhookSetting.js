WebhookSetting = {
	BtnTextCache: null,
	CopySecretKey: function (btn) {
		var sk_input = btn.closest('.post-status-broadcaster-field-inline_mixed').find('input[type="text"]:eq(0)');
		sk_input.select();
		document.execCommand("copy");

		var tp = tippy(btn[0]);
		tp.hide();
		tp.setContent('已複製密鑰！');
		tp.show();

		setTimeout(function () {
			tp.hide();
			setTimeout(function () {
				tp.setContent('複製密鑰');
			}, 1000);
		}, 3000);
	},
	MakeSecretKey: function (btn) {
		this.BtnTextCache = btn.val();
		btn.val('產生中...');
		jQuery.post(poststatusbroadcaster_ajax_object.ajax_url, {
			action: 'MakeSecretKey'
		}, function (resp) {
			btn.closest('.post-status-broadcaster-field-inline_mixed').find('input[type="text"]:eq(0)').val(resp);
			btn.val(WebhookSetting.BtnTextCache);
		}, 'json');
	},
	ValidateJSON: function (text_area) {
		jQuery('span#ValidateJSONSuccessAlert').hide();
		jQuery('span#ValidateJSONFailedAlert').hide();
		jQuery('span#ValidatingJSONMsg').show();

		try {
			JSON.parse(text_area.val());
		} catch (e) {
			jQuery('span#ValidatingJSONMsg').hide();
			jQuery('span#ValidateJSONFailedAlert').show();
			return false;
		}

		jQuery.post(poststatusbroadcaster_ajax_object.ajax_url, {
			action: 'TestParamJSON',
			param_json: text_area.val()
		}, function (resp) {
			jQuery('span#ValidatingJSONMsg').hide();

			if (resp.type == 'success')
				jQuery('span#ValidateJSONSuccessAlert').show();
			else
				jQuery('span#ValidateJSONFailedAlert').show();
		}, 'json');
	},
	ToggleSettingField: function (auth_method_select) {
		var ClosestExpirationField = auth_method_select.closest('.post-status-broadcaster-section-table').find('tr.ExpirationField');

		if (auth_method_select.val() == 0)
			ClosestExpirationField.hide();
		else
			ClosestExpirationField.show();
	},
	ToggleAllAuthMethod: function () {
		jQuery('.AuthMethodSlct').each(function (key, elm) {
			WebhookSetting.ToggleSettingField(jQuery(elm));
		});
	}
};

(function ($) {
	'use strict';

	$(function () {
		$$('div.post-status-broadcaster-sections').on('click', '.CopySecretKeyBtn', function (e) {
			e.preventDefault();
			WebhookSetting.CopySecretKey($(this));
		});

		$$('div.post-status-broadcaster-sections').on('click', '.MakeSecretKeyBtn', function (e) {
			e.preventDefault();
			WebhookSetting.MakeSecretKey($(this));
		});

		$$('div.post-status-broadcaster-sections').on('change', '.AuthMethodSlct', function (e) {
			WebhookSetting.ToggleSettingField($(this));
		});

		$$('div.post-status-broadcaster-sections').on('change', '.ParamsTextarea', function (e) {
			WebhookSetting.ValidateJSON($(this));
		});

		tippy('[data-tippy-content]');

		WebhookSetting.ToggleAllAuthMethod();
	});

})(jQuery);