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

		//sort recordings by timestamp
		library.sort((a,b) => {
			return a.timestamp < b.timestamp
		});
		
		return dispatch(setLibrary(library));
	}
}
