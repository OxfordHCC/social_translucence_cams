const REMOTE_URL = 'http://localhost:5000';

//UTILS

const pathJoin = (...paths) => paths.join('/');

const post = async (url, data) => {
	const res = await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(data)
	});
	
	return res.json();
}

const get = async (url) => {
	const res = await fetch(url);
	return res.json();
}

//API

function getLibrary(){
	return get(pathJoin(REMOTE_URL,'library'));
}

function getAdapters(){
	return get(pathJoin(REMOTE_URL,'adapter'));
}

async function getAdapterClasses(){
	return get(pathJoin(REMOTE_URL,'adapter-types'));
}

function getCameras(){
	return get(pathJoin(REMOTE_URL, 'camera'));
}

function postAdapter(adapter){
	return post(pathJoin(REMOTE_URL, 'adapter'), adapter);
}

export default {
	getLibrary,
	getAdapters,
	getAdapterClasses,
	getCameras,
	postAdapter
}
