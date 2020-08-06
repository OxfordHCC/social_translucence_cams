import { combineReducers } from 'redux';
import libraryReducer from './libraryReducer';
import adapterReducer from './adapterReducer';

export default combineReducers({
	libraryReducer,
	adapterReducer
});
