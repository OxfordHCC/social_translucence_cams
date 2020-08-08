import { SET_ADAPTERS } from '../actions/adapterActions.js';

const defaultState = [];

export default function(state = defaultState, action){
	switch(action.type){
	case SET_ADAPTERS:
		return action.adapters;
	default:
		return state;
	}
}
