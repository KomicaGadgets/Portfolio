<?php

class TestReportController extends Controller
{
	/**
	 * checks the request content and user permission, then call the report generator function, return HTTP status
	 */
	public function store(Request $request)
	{
		$Response = [
			[
				'message' => 'invalid data, permission error.'
			],
			401
		];

		if (Auth::check()) {
			$Response = [
				[
					'message' => 'invalid data, request data error.'
				],
				400
			];

			if ($request->has(['id', 'type'])) {

				//...

				$id = (int) $request->id;
				$cases = json_decode(app('App\Http\Controllers\TestProjectController')->genProjectCaseList($id, 1), true);

				//...

				if (empty($cases)) {
					$Response = [
						[
							'message' => 'invalid data, project not exist error.'
						],
						400
					];
				}

				//...
			}
		}

		return response()->json(...$Response);
	}
}
