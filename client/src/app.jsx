import React from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from 'react-router-dom';
import { ThemeProvider } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import { Settings } from './settings';
import Adapters from './components/Adapters';
import { createMuiTheme } from '@material-ui/core/styles';
import AddAdapter from './components/AddAdapter';
import AdapterPage from '~/src/components/AdapterPage';
import CameraPage from '~/src/components/CameraPage';


const theme = createMuiTheme({
  props: {
    MuiTypography: {
      variantMapping: {
        h1: 'h2',
        h2: 'h2',
        h3: 'h2',
        h4: 'h2',
        h5: 'h2',
        h6: 'h2',
        subtitle1: 'h2',
        subtitle2: 'h2',
        body1: 'span',
        body2: 'span',
      },
    },
  },
});

export function MaterialApp(){
    return <ThemeProvider theme={theme}>
             <CssBaseline/>
             <App/>
           </ThemeProvider>;
}

function App(){
    return (
        <Router>
          <div>
            <nav>
              <ul>
                <li>
                  <Link to="/">Home</Link>
                </li>
                <li>
                  <Link to="/adapter">Adapters</Link>
                </li>
                <li>
                  <Link to="/settings">Settings</Link>
                </li>
              </ul>
            </nav>
          </div>
          <Switch>
            <Route path="/settings">
              <Settings />
            </Route>

            <Route path="/adapter/:id" component={AdapterPage}/>

            <Route path="/camera/:id" component={CameraPage}/>

            <Route path="/adapter">
              <Adapters/>
            </Route>
            
            <Route path="/add-adapter">
              <AddAdapter />
            </Route>

            <Route path="/add-adapter">
              <AddAdapter />
            </Route>

            <Route path="/">
              <Home />
            </Route>
            
          </Switch>
        </Router>
    );
};

function Home(){
    return <h2>aaa</h2>;
}
