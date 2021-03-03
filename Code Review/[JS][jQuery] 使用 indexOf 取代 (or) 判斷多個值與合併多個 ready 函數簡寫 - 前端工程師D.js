window.onload = function () {

	var form = document.getElementById('setting_form');
	form.addEventListener('keydown', (e) => {
		if (e.keyCode === 13 && e.target.nodeName === 'INPUT') {

			//...

			if (e.target.name == "controller_address" | e.target.name == "address" | e.target.name == "netmask" | e.target.name == "gateway" | e.target.name == "dns") {
				if (e.target.value !== "") {
					e.preventDefault();
					var form = e.target.form;
					var index = [].indexOf.call(form, e.target);
					var len = form.elements.length;
					if (len > index + 1) {
						form.elements[index + 1].focus();
					}
				}
			} else {
				e.preventDefault();
				var form = e.target.form;
				var index = [].indexOf.call(form, e.target);
				var len = form.elements.length;
				if (len > index + 1) {
					form.elements[index + 1].focus();
				}
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
	});


	$(function () {
		$('#save_confirm_buttom').on('click', function () {
			$('#save_confirm').modal('hide');
		});
	});
}

//...
