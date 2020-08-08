import { SET_LIBRARY } from '../actions/libraryActions';

const defaultState = [];

export default function(state = defaultState, action){
	switch (action.type){
	case SET_LIBRARY:
		return action.library
	default:
		return state
	}
}
