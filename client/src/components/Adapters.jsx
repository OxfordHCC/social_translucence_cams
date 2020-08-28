import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import Button from '@material-ui/core/Button';
import Toolbar from '@material-ui/core/Toolbar';
import AddIcon from '@material-ui/icons/Add';

import { AdapterList } from '~/src/components/AdapterList';

function Adapters({ adapters }){
    return (
        <React.Fragment>
          <Toolbar>
            <Link to="/add-adapter" className="no-decoration">
              <Button startIcon={<AddIcon/>}>Add adapter</Button>
            </Link>
          </Toolbar>
          <AdapterList adapters={adapters}/>
        </React.Fragment>
    );
}

const stateToProps = ({ adapters }) => ({
    adapters
});

export default connect(stateToProps)(Adapters);



