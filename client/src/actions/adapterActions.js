import remote from '../lib/remote';
import { setError } from './errorActions';

export const SET_ADAPTERS = "SET_ADAPTERS";
export function setAdapters(adapters){
	return {
		type: SET_ADAPTERS,
		adapters
	};
}

export function syncAdapters(){
	return async (dispatch) => {
		const adapters = await remote.getAdapters();
		return dispatch(setAdapters(adapters));
	}
}

export const SET_ADAPTER_CLASSES = "SET_ADAPTER_CLASSES";
export function setAdapterClasses(classes){
	return {
		type: SET_ADAPTER_CLASSES,
		classes
	};
}

export function syncAdapterClasses(){
	return async (dispatch) => {
		const classes = await remote.getAdapterClasses();
		dispatch(setAdapterClasses(classes));
	}
}

export const ADD_ADAPTER = "ADD_ADAPTER";
export function addAdapter(adapter){
	return {
		type: ADD_ADAPTER,
		adapter
	}
}

export function postAdapter(adapter){
	return async (dispatch) => {
		await remote.postAdapter(adapter);
		dispatch(addAdapter(adapter));
	}
}
