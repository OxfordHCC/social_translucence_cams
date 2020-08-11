import React from 'react';
import ReactDOM from 'react-dom';
import { MaterialApp } from './src/app';
import { Provider } from 'react-redux';
import store from './src/store';
import { syncLibrary } from './src/actions/libraryActions';
import { syncAdapters, syncAdapterClasses } from './src/actions/adapterActions'; 
import { syncCameras } from './src/actions/cameraActions';

//styles
import '~/src/style/common.less';

const root = document.getElementById("root");

store.dispatch(syncLibrary());
store.dispatch(syncAdapters());
store.dispatch(syncCameras());
store.dispatch(syncAdapterClasses());

const RootComponent = (
    <Provider store={store}>
      <MaterialApp/>
    </Provider>
);

ReactDOM.render(RootComponent, root);
