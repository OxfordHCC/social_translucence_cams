import React from 'react';
import { useState, useEffect } from 'react';
import { connect } from 'react-redux';
import { getRecordingURL } from '~/src/lib/remote';

function RecordingPage({ recording }){
    const [videoURL, setVideoURL] = useState();

    useEffect(() => {
        (async () => {
            const url = getRecordingURL(recording.id);
            setVideoURL(url);
        })();
    }, [recording]);
    
    if(!recording){
        return 'Loading...';
    }
    
    return (
        <div className="library-page">
          <h1>{recording.name}</h1>
          <video src={videoURL} controls/>
        </div>
    );
}


const stateToProps = (state, ownProps) => {
    //try getting
    let recording = ownProps?.location?.state?.recording;
    
    if(!recording){
        const recordingId = ownProps?.match.params.id;
        recording = state.library.find(lib => lib.id === recordingId);
    }
    
    return { recording };
};

export default connect(stateToProps)(RecordingPage);


