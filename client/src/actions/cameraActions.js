import remote from '../lib/remote';

export const SET_CAMERAS = "SET_CAMERAS";
export function setCanmeras(cameras){
	return {
		type: SET_CAMERAS,
		cameras
	};
}

export function syncCameras(){
	return async (dispatch) => {
		const cameras = await remote.getCameras();
		return dispatch(setCameras(cameras));
	}
}
