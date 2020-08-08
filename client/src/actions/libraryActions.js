import remote from '../lib/remote';

export const SET_LIBRARY = "SET_LIBRARY";
export function setLibrary(library){
	return {
		type: SET_LIBRARY,
		library
	}
}

export function syncLibrary(library){
	return async (dispatch) => {
		const library = await remote.getLibrary();
		return dispatch(setLibrary(library));
	}
}
