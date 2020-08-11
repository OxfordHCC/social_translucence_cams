import { combineReducers } from 'redux';
import library from './libraryReducer';
import adapters from './adapterReducer';
import cameras from './cameraReducer';
import adapterClasses from './adapterClassReducer';

export default combineReducers({
	library,
	adapters,
	cameras,
	adapterClasses
});
