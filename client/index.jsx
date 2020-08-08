import React from 'react';
import ReactDOM from 'react-dom';
import { MaterialApp } from './src/app';
import { Provider } from 'react-redux';
import store from './src/store';
import { syncLibrary } from './src/actions/libraryActions';
import { syncAdapters } from './src/actions/adapterActions'; 
import { syncCameras } from './src/actions/cameraActions';
const root = document.getElementById("root");

syncLibrary();
syncAdapters();
syncCameras();

const RootComponent = (
    <Provider store={store}>
      <MaterialApp/>
    </Provider>
);

ReactDOM.render(RootComponent, root);
