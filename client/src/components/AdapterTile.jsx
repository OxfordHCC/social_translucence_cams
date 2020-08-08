import React from 'react';
import GridListTile from '@material-ui/core/GridListTile';
import GridListTileBar from '@material-ui/core/GridListTileBar';
import arloImg from '../img/arlo.png';


export function AdapterTile(adapter){
    return <GridListTile key={adapter.id}>
             <img src={arloImg}></img>
             <GridListTileBar
               title={adapter.name}
               subtitle={adapter.type}
             />
           </GridListTile>;
}    
    
