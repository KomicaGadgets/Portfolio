window.onload = function () {

	var form = document.getElementById('setting_form');
	form.addEventListener('keydown', (e) => {
		if (e.keyCode === 13 && e.target.nodeName === 'INPUT') {

			//...
			var IsNameExist = (['controller_address', 'address', 'netmask', 'gateway', 'dns'].indexOf(e.target.name) > -1);
			if (!IsNameExist || (IsNameExist && e.target.value !== "")) {
				e.preventDefault();
				var form = e.target.form,
					index = [].indexOf.call(form, e.target),
					len = form.elements.length,
					plus_index = index + 1;
				if (len > plus_index)
					form.elements[plus_index].focus();
			}
		}
	})


	$(function () {
		var availableTags = [
			"255.255.255.255",
			"255.255.255.254",

			//...

			"192.0.0.0",
			"128.0.0.0",
			"0.0.0.0"
		];
		$("#netmask").autocomplete({
			source: availableTags
		});
	});


	$(function () {
		$("#clear_confirm_buttom").on('click', function () {
			$('#clear_confirm').modal('hide');
		});
		$('#save_confirm_buttom').on('click', function () {
			$('#save_confirm').modal('hide');
		});
	});
}

//...
