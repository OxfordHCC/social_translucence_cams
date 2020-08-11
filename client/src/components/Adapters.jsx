import React from 'react';
import AddAdapter from './AddAdapter';
import Button from '@material-ui/core/Button';
import GridList from '@material-ui/core/GridList';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import { AdapterTile } from './AdapterTile';
import { connect } from 'react-redux';
import { Route, Switch, Link, useRouteMatch } from 'react-router-dom';
import AddIcon from '@material-ui/icons/Add';

function Adapters({ adapters }){
    const { path, url } = useRouteMatch();

    const getRows = () => adapters
          .map(adapter => ({ ...adapter, type: adapter.adapter_type }))
          .map(adapter => <AdapterTile adapter={adapter} key={adapter.id}/>);

    const getList = () => {
        if(adapters.length === 0){
            return "No adapters";
        }
        return <GridList cellHeight={180}>
                 {getRows()}
               </GridList>;
    };
    return (
        <React.Fragment>
          <Toolbar>
            <Link to="/add-adapter" className="no-decoration">
              <Button startIcon={<AddIcon/>}>Add adapter</Button>
            </Link>
          </Toolbar>
          { getList() }
        </React.Fragment>
    );
}

const stateToProps = ({ adapters }) => ({
    adapters
});

export default connect(stateToProps)(Adapters);



