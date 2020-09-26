const REMOTE_URL = 'http://localhost:5000';

//UTILS

const pathJoin = (...paths) => paths.join('/');

const apiTo = (endpoint) => {
	return [REMOTE_URL, endpoint].join('');
}

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

export function getRecordingURL(recordingId){
	return apiTo(`/library/${recordingId}`);
}

// API calls
export function getCameraStream(cameraId){
	return get(apiTo(`/camera/${cameraId}/stream_url`));
}

export function getLibrary(){
	return get(apiTo('/library'));
}

export function getAdapters(){
	return get(apiTo('/adapter'));
}

export async function getAdapterClasses(){
	return get(apiTo('/adapter-types'));
}

export function getCameras(){
	return get(apiTo('/camera'));
}

export function postAdapter(adapter){
	return get(apiTo('/adapter'));
}

export default {
	getCameraStream,
	getLibrary,
	getAdapters,
	getAdapterClasses,
	getCameras,
	postAdapter
}
