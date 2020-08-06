import React from 'react';
import ReactDOM from 'react-dom';
import { MaterialApp } from './src/app';
import { Provider } from 'react-redux';
import store from './src/store';
import { syncLibrary } from './src/actions/libraryActions';
import { syncAdapters } from './src/actions/adapterActions';

const root = document.getElementById("root");

syncLibrary();
syncAdapters();

const RootComponent = (
    <Provider store={store}>
      <MaterialApp/>
    </Provider>
);

ReactDOM.render(RootComponent, root);
