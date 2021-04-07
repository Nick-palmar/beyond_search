import logo from './logo.svg';
import './assets/css/App.css';
import { BrowserRouter as Router, Switch, Route, Redirect } from 'react-router-dom';
import MainPage from './pages/MainPage';

function App() {
  return (
    <div className='App'>
      <Router>
        <Switch> 
          <Route exact path="/">
            <Redirect to='/main' />
          </Route>

          <Route path='/main' component={MainPage} />
        </Switch>
      </Router>
    </div>
  );
}

export default App;
