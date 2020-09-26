import React from 'react';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import { Link } from 'react-router-dom';

export default function LibraryList({ recordings }){

    //construct react router location object to pass to Link's "to" attr
    //we pass the recording as is to state to avoid having to look it up
    //in redux. We also pass the id the url as a fallback.
    const routerLocation = (recording) => ({
        pathname: `/library/${recording.id}`,
        state: { recording } 
    });
    
    const toLibraryListItem = rec => (
        <Link to={routerLocation(rec)} key={rec.id}>
          <ListItem >
            <ListItemText>
              {rec.name}
            </ListItemText>
          </ListItem>
        </Link>
    );

    if(recordings.length === 0){
        return 'No recordings';
    }

    return <List>
             { recordings.map(toLibraryListItem) }
           </List>;

}
