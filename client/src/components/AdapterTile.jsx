import React from 'react';
import GridListTile from '@material-ui/core/GridListTile';
import GridListTileBar from '@material-ui/core/GridListTileBar';
import arloImg from '../img/arlo.png';

const typeImgMap = {
    'arlo': arloImg
};

export function AdapterTile({ adapter }){
    
    return <GridListTile>
    <img src={typeImgMap[adapter.type]}></img>
             <GridListTileBar
               title={ adapter.name }
               subtitle={ adapter.type }
             />
           </GridListTile>;
}    
    
