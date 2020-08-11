import {
	SET_ADAPTERS,
	ADD_ADAPTER
} from '../actions/adapterActions.js';

const defaultState = [];

export default function(state = defaultState, action){
	switch(action.type){
	case SET_ADAPTERS:
		return action.adapters;
	case ADD_ADAPTER:
		return state.concat([ action.adapter ]);
	default:
		return state;
	}
}
