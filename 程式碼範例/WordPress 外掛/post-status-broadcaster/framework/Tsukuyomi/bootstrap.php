<?php

require __DIR__ . '/vendor/autoload.php';

require_once (new \PostStatusBroadcaster\Tsukuyomi\Core\Independent\PathMgr)->admin_page_framework_file();

if (file_exists($DevFunc = plugin_dir_path(__FILE__) . 'DevFunc.php'))
	require_once $DevFunc;
