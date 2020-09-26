import React from 'react';
import { Link, Switch, Route, useRouteMatch, useParams } from 'react-router-dom';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import Container from '@material-ui/core/Container';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import { AdapterTile } from '~/src/components/AdapterTile';
import AddAdapterForm from '~/src/components/AddAdapterForm';
import { connect } from 'react-redux';


function AddAdapter({ adapterClasses }){

    const { path, url } = useRouteMatch();

    const getTile = adapterClass => (
        <Link to={`${path}/${adapterClass.type}`} key={adapterClass.type} >
          <AdapterTile adapter={adapterClass} />
        </Link>
    );
    
    const getList = () => <GridList>{ adapterClasses.map(getTile) }</GridList>;

    return (
        <div className="add-adapter">
          <Toolbar>
            <Link to="/adapter">
              <IconButton aria-label="search" color="inherit">
                <ArrowBackIcon />
              </IconButton>
            </Link>
          </Toolbar>
          <Container>
            <Switch>
              <Route exact path={`${url}`}>
                { getList() }
              </Route>
              <Route path={`${url}/:adapterType`}>
                <AddAdapterForm/>
              </Route>
            </Switch>
          </Container>
        </div>
    );
}


const stateToProps = ({ adapterClasses }) => ({
    adapterClasses
});

export default connect(stateToProps)(AddAdapter);
