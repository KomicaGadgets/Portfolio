<?php

namespace PostStatusBroadcaster\Tsukuyomi\Core\Independent;

class WP
{
	function __construct()
	{
		$this->WPHost = null;
	}

	function enqueue_script_once(...$QueueArguments)
	{
		global $wp_scripts, $wp_styles;

		if (!empty($QueueArguments)) {
			$NotEnqueued = 1;

			$EnqueuedScripts = $wp_scripts->registered;

			foreach ($EnqueuedScripts as $WP_Dependency) {
				if ($QueueArguments[1] == $WP_Dependency->src) {
					$NotEnqueued = 0;
					break;
				}
			}

			if ($NotEnqueued)
				wp_enqueue_script(...$QueueArguments);
		}
	}

	function wp_host()
	{
		if ($this->WPHost === null)
			$this->WPHost = parse_url(get_home_url())['host'];

		return $this->WPHost;
	}
}
