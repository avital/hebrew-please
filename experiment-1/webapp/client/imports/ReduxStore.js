import { createStore, combineReducers } from 'redux';
import { reducer as formReducer } from 'redux-form';

const reducers = {
  // ... your other reducers here ...
  form: formReducer
};

const reducer = combineReducers(reducers);
const store = createStore(reducer);

export default store;
