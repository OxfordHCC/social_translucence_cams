import React from 'react';

import GridList from '@material-ui/core/GridList';
import { AdapterTile } from './AdapterTile';
import { Link } from 'react-router-dom';

export function AdapterList({ adapters }){
    const getTiles = () => adapters
          .map(adapter => ({ ...adapter, type: adapter.adapter_type }))
          .map(adapter =>
               <Link to={`adapter/${adapter.id}`} key={adapter.id}>
                 <AdapterTile adapter={adapter} key={adapter.id}/>n
               </Link>
          );

    if(adapters.length === 0){
        return "No adapters";
    }
    return <GridList cellHeight={180}>
             { getTiles() }
           </GridList>;
};
