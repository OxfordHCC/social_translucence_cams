import React from 'react';
import { useEffect, useState } from 'react';
import { connect } from 'react-redux';
import LibraryList from './LibraryList';
import { getCameraStream } from '~/src/lib/remote';

function CameraPage({ camera, recordings }){
    const [ streamUrl, setStreamUrl ] = useState();
    
    useEffect(() => {
        (async () => {
            const streamInfo = await getCameraStream(camera.id);
            setStreamUrl(streamInfo.url);
        })();
    },[camera]);
    
    return (
        <div className="camera">
          <h1>{camera.name}</h1>
          <h2>Live feed</h2>
          {
              (streamUrl)?
                  <img src={streamUrl}/>
              : "Live stream not available"
          }
          <h2>Recordings</h2>
          <LibraryList recordings = {recordings}/>
        </div>
    );
};

const stateToProps = ({ cameras, library }, props) => {
    const cameraId = props.match.params.id;
    const camera = cameras.find(cam => cam.id === cameraId);
    const recordings = library.filter(lib => lib.camera === cameraId);
    
    return {
        camera,
        recordings
    };
};

export default connect(stateToProps)(CameraPage);
