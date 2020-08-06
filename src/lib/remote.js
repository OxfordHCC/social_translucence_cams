const REMOTE_URL = 'localhost:5000';

const pathJoin = (...paths) => paths.join('/');

function getLibrary(){
	return fetch(pathJoin(REMOTE_URL,'library'));
}

function getAdapters(){
	return fetch(pathJoin(REMOTE_URL,'adapter'));
}

function getCameras(){
	return fetch(pathJoin(REMOTE_URL, 'camera'));
}

export default {
	getLibrary,
	getAdapters,
	getCameras
}
