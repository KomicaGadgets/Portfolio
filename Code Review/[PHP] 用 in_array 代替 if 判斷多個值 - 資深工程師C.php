<?php

class License
{

	//...

	public static function isExpired()
	{
		if (self::mode() == self::None || self::mode() == self::MockActive) {
			return false;
		} else if (self::mode() == self::MockExpire) {
			return true;
		}
		$expire = self::expirationDate();
		$now = Carbon::Now();
		return $now->diffInHours($expire, false) < 0;
	}

	//...

}
