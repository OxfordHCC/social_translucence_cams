import { combineReducers } from 'redux';
import library from './libraryReducer';
import adapters from './adapterReducer';
import cameras from './cameraReducer';

export default combineReducers({
	library,
	adapters,
	cameras
});
