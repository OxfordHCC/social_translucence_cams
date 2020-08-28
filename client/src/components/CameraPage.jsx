import React from 'react';
import { connect } from 'react-redux';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';


function LibraryList({recordings}){
    const genLibraryListItem = rec => (
        <ListItem key={rec.id}>
          <ListItemText>
            {rec.name}
          </ListItemText>
        </ListItem>
    );

    if(recordings.length === 0){
        return 'No recordings';
    }
    
    return <List>
             { recordings.map(genLibraryListItem) }
           </List>;

}
//on the camera page, we want to have
//list of library entries

function CameraPage({ camera, recordings }){
    return (
        <div className="camera">
          <LibraryList recordings = {recordings}/>
        </div>
    );
}

const stateToProps = ({ cameras, library }, props) => {
    console.log(props);
    const cameraId = props.match.params.cameraId;
    const camera = cameras.find(cam => cam.id === cameraId);
    const recordings = library.filter(lib => lib.camera === cameraId);
    
    return {
        camera,
        recordings
    };
};

export default connect(stateToProps)(CameraPage);
