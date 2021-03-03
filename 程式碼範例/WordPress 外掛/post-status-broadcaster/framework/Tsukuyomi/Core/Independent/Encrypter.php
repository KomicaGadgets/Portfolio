<?php

namespace PostStatusBroadcaster\Tsukuyomi\Core\Independent;

use phpseclib\Crypt\{
	AES,
	Random
};

class Encrypter
{
	function __construct()
	{
		$this->AESCtrller = new AES(AES::MODE_CBC);
		$this->AESBitSize = 128;
		$this->AESByteSize = $this->AESBitSize >> 3;
		$this->AESIV = null;
		$this->AESKey = null;

		$this->InitAES();
	}

	private function InitAES()
	{
		$this->SetEssential(null, null);
	}

	function RandomByte($Length = 1)
	{
		return Random::string($Length);
	}

	function RandomHex($ByteLength = 1)
	{
		return bin2hex($this->RandomByte($ByteLength));
	}

	function SetEssential($IV = null, $Key = null)
	{
		$this->AESIV = is_null($IV) ? Random::string($this->AESByteSize) : hex2bin($IV);
		$this->AESKey = is_null($Key) ? Random::string($this->AESByteSize) : hex2bin($Key);

		$this->AESCtrller->setKeyLength($this->AESBitSize);
		$this->AESCtrller->setKey($this->AESKey);
		$this->AESCtrller->setIV($this->AESIV);

		return $this;
	}

	function FormatCryptoOutput($RawOutput, $Format = 'base64')
	{
		$Output = $RawOutput;

		if (!is_null($Format)) {
			switch ($Format) {
				case 'base64':
					$Output = base64_encode($Output);
					break;
				case 'hex':
					$Output = bin2hex($Output);
					break;
			}
		}

		return $Output;
	}

	function QuickEncrypt($Input, $Format = null)
	{
		$Output = $this->AESCtrller->encrypt($Input);

		if (!is_null($Format))
			$Output = $this->FormatCryptoOutput($Output, $Format);

		return [
			'Output'	=>	$Output,
			'IV'	=>	bin2hex($this->AESIV),
			'Key'	=>	bin2hex($this->AESKey),
		];
	}

	function Decrypt($Input, $Key, $IV)	// $Input require binary
	{
		$this->SetEssential($IV, $Key);
		return $this->AESCtrller->decrypt(hex2bin($Input));
	}

	function LaraEncrypt($Input, $Key = null, $IV = null)
	{
		$this->SetEssential($IV, $Key);

		$Serialized = serialize($Input);
		$CipherInfo = $this->QuickEncrypt($Serialized, 'hex');
		$HMACTag = hash_hmac('sha256', $CipherInfo['Output'], $CipherInfo['Key']);

		$Result = [
			'iv'	=>	$CipherInfo['IV'],
			'value'	=>	$CipherInfo['Output'],
			'mac'	=>	$HMACTag
		];

		$Output = base64_encode(json_encode($Result));

		return $Output;
	}

	function LaraDecrypt($Input, $Key = null, $Default = null)
	{
		try {
			$Output = $Default;

			$CipherStruct = json_decode(base64_decode($Input));
			$ComputedHMACTag = hash_hmac('sha256', $CipherStruct->value, $Key);

			if (hash_equals($ComputedHMACTag, $CipherStruct->mac)) {
				$Decrypted = $this->Decrypt($CipherStruct->value, $Key, $CipherStruct->iv);

				$Output = unserialize($Decrypted);
			}

			return $Output;
		} catch (\Throwable $th) {
			return $Default;
		}
	}
}
