import { SET_ADAPTER_CLASSES } from '../actions/adapterActions.js';

const defaultState = [];

export default function(state = defaultState, action){
	switch(action.type){
	case SET_ADAPTER_CLASSES:
		return action.classes;
	default:
		return state;
	}
}
