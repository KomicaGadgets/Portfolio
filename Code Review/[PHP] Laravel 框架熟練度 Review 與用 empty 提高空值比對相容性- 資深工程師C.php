<?php

class TestReportController extends Controller
{
	/**
	 * checks the request content and user permission, then call the report generator function, return HTTP status
	 */
	public function store(Request $request)
	{
		if (Auth::user()) {
			if (isset($request['id']) && isset($request['type'])) {

				//...

				$id = (int) $request['id'];
				$cases = json_decode(app('App\Http\Controllers\TestProjectController')->genProjectCaseList($id, 1), true);

				//...

				if ($cases == null) {
					return response()->json(
						[
							'message' => 'invalid data, project not exist error.'
						],
						400
					);
				}

				//...

			} else {
				return response()->json(
					[
						'message' => 'invalid data, request data error.'
					],
					400
				);
			}
		} else {
			return response()->json(
				[
					'message' => 'invalid data, permission error.'
				],
				401
			);
		}
	}
}
