import VideosView from './imports/VideosView.js';
import ReactDOM from 'react-dom';
import React from 'react';

Meteor.startup(() => {
  const appElement = document.querySelector('.app');
  Tracker.autorun(() => {
    ReactDOM.render(<VideosView />, appElement);
  });
});
