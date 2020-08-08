import remote from '../lib/remote';

export const SET_ADAPTERS = "SET_ADAPTERS";
export function setAdapters(adapters){
	return {
		type: SET_ADAPTERS,
		adapters
	};
}

export function syncAdapters(){
	return async (dispatch) => {
		console.log('aaa');
		const adapters = await remote.getAdapters();
		console.log('adapters from remote', adapters);
		return dispatch(setAdapters(adapters));
	}
}
