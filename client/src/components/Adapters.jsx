import React from 'react';
import { AddAdapter } from './AddAdapter';
import Button from '@material-ui/core/Button';
import GridList from '@material-ui/core/GridList';
import { AdapterTile } from './AdapterTile';
import { connect } from 'react-redux';

const mockAdapters = [{ 'name': "Arlo adapter", type:'arlo', id:'id1' }];

function Adapters({ adapters }){
    const getRows = () => mockAdapters.map(adapter => AdapterTile(adapter));

    const getList = () => {
        if(adapters.length === 0){
            return "No adapters";
        }
        return <GridList cellHeight={180}>
                 {getRows()}
               </GridList>;
    };
    return (
        <div className="adapters">
          {getList()} 
        </div>
    );
}

const mapStateToProps = (state) => {
    //Only reason we're not just returning state is so that we don't pass references
    //to other state variables...
    const { adapters } = state;
    return { adapters };
};

export default connect(mapStateToProps)(Adapters);



