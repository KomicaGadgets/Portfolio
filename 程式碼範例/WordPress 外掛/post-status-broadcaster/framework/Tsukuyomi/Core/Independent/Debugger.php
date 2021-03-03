<?php

namespace PostStatusBroadcaster\Tsukuyomi\Core\Independent;

use \Monolog\Logger;
use \Monolog\Handler\StreamHandler;

use PostStatusBroadcaster\Tsukuyomi\Core\Independent\PathMgr;

class Debugger
{
	function __construct(PathMgr $PathMgr)
	{
		$this->LogName = 'TsukuyomiDebugger';
		$this->LogFile = $PathMgr->tsukuyomi_root() . 'tsukuyomi_error_log.txt';

		$this->log = new Logger($this->LogName);
		$this->log->pushHandler(new StreamHandler($this->LogFile, Logger::DEBUG));
	}

	function logger()
	{
		return $this->log;
	}
}
