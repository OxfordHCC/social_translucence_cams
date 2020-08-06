import React from 'react';
import { AddAdapter } from './AddAdapter';
import Button from '@material-ui/core/Button';
import GridList from '@material-ui/core/GridList';
import { AdapterTile } from './AdapterTile';

const mockAdapters = [{ 'name': "Arlo adapter", type:'arlo', id:'id1' }];

export function Adapters(){

    const getRows = () => mockAdapters.map(adapter => AdapterTile(adapter));
    
    return <div className="adapters">
             <GridList cellHeight={180}>
               {getRows()}
             </GridList>
             <Button variant="contained">Test button</Button>
             
           </div>;
}

