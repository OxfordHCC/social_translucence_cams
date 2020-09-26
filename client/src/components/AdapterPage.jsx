import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';

function CameraList({ cameras }){

    const CameraListItem = camera => (
        <Link to={`/camera/${camera.id}`} key={camera.id}>
          <ListItem>
            <ListItemText primary={camera.name} />
          </ListItem>
        </Link>
    );
    
    return <List>
             { cameras.map(CameraListItem) }
           </List>;
}

//what will the adapter page contain?
//settings pane (change name, options etc)
//list of cameras

function AdapterPage({ adapter, adapterCams }){

    if(!adapter){
        return 'Loading...';
    }
    
    const adapterCameras = adapterCams.filter(cam => cam.adapter === adapter.id);
    
    return <div className="adapter">
             <h1>{adapter.name}</h1>
             <h2>Cameras</h2>
             <CameraList cameras={ adapterCameras } />
             
           </div>;
}

const stateToProps = ({ adapters, cameras }, props) => {
    const adapterId = props.match.params.id;
    
    const adapter = adapters.find(ad => ad.id == adapterId);
    const adapterCams = cameras.filter(cam => cam.adapter == adapterId);

    return {
        adapter,
        adapterCams
    };
};

export default connect(stateToProps)(AdapterPage);
