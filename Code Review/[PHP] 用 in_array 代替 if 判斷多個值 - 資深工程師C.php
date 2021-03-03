<?php

class License
{

	//...

	public static function isExpired()
	{
		if (in_array(self::mode(), [self::None, self::MockActive]))
			return false;

		if (self::mode() == self::MockExpire)
			return true;

		$expire = self::expirationDate();
		return now()->diffInHours($expire, false) < 0;
	}

	//...

}
