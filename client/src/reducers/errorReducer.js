import { SET_ERROR } from '../actions/errorActions';

export default function(state=undefined, action){
	switch(action.type){
	case SET_ERROR:
		return action.error;
	default:
		return state;
	}
}
