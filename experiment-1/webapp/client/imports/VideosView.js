import VideoList from "./VideoList.js";
import AddVideoForm from "./AddVideoForm.js";
import ReduxStore from './ReduxStore.js';
import React, {Component} from 'react';

function handleAdd() {
  var form = ReduxStore.getState().form.addVideo;
  const url = form.url.value;
  const isLargelyObjectionable = form.isLargelyObjectionable.value === "y";
  Meteor.call("labelVideo", {url, isLargelyObjectionable});
}

function handleReprocess(videoId) {
  Meteor.call("reprocessVideo", videoId);
}

function handleExtractSegment(videoId) {
  Meteor.call("extractSegment", videoId);
}

class VideosView extends Component {
  render() {
    return <div>
      <VideoList videos={LabelledVideos.find().fetch()} onReprocess={handleReprocess} onExtractSegment={handleExtractSegment} />
      <hr />
      <AddVideoForm store={ReduxStore} onSubmit={handleAdd} />
    </div>
  }
}

export default VideosView;
