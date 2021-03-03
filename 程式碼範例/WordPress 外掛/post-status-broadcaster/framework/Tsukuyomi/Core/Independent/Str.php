<?php

namespace PostStatusBroadcaster\Tsukuyomi\Core\Independent;

use StringTemplate\Engine;

class Str
{
	function __construct()
	{
		$this->StringTemplateEngine = null;
	}

	function str_tpl_engine()
	{
		if ($this->StringTemplateEngine === null)
			$this->StringTemplateEngine = new Engine();

		return $this->StringTemplateEngine;
	}

	function startsWith($haystack, $needle)
	{
		return substr_compare($haystack, $needle, 0, strlen($needle)) === 0;
	}

	function endsWith($haystack, $needle)
	{
		return substr_compare($haystack, $needle, -strlen($needle)) === 0;
	}

	function finish($value, $cap)
	{
		$quoted = preg_quote($cap, '/');
		return preg_replace('/(?:' . $quoted . ')+$/', '', $value) . $cap;
	}

	function format($format_string, $replacement_field)
	{
		return $this->str_tpl_engine()->render($format_string, $replacement_field);
	}

	function random($length = 16)
	{
		$string = '';

		while (($len = strlen($string)) < $length) {
			$size = $length - $len;

			$bytes = random_bytes($size);

			$string .= substr(str_replace(['/', '+', '='], '', base64_encode($bytes)), 0, $size);
		}

		return $string;
	}
}
