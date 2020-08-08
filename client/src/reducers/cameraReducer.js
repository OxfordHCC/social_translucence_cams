import { SET_CAMERAS } from '../actions/cameraActions.js';

const defaultState = [];

export default function(state = defaultState, action){
	switch(action.type){
	case SET_CAMERAS:
		return action.cameras;
	default:
		return state;
	}
}
