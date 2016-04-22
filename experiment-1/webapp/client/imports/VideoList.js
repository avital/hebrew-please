import React, {Component, PropTypes} from 'react';

import VideoSegments from './VideoSegments.js'

class Video extends Component {
  render() {
    const {url, isLargelyObjectionable, videoId, state, onReprocess, onExtractSegment} = this.props;
    return (
      <div className="video">
        <iframe width="200" height="200" src={"http://www.youtube.com/embed/" + videoId} />

        {isLargelyObjectionable ? "BUZZ!!" : "...yawn..."}
        {" | "}
        {state}

        <button onClick={onReprocess.bind(null, videoId)}>
          reprocess
        </button>
        <button onClick={onExtractSegment.bind(null, videoId)}>
          extract segment
        </button>

        <div className="segments" style={{marginLeft: 40, marginBottom: 40}}>
          Segments
          <VideoSegments segments={LabelledSegments.find({videoId}).fetch()} />
        </div>
      </div>
    );
  }
}

var baseVideoPropTypes = {
  url: PropTypes.string.isRequired,
  isLargelyObjectionable: PropTypes.bool.isRequired,
  videoId: PropTypes.string.isRequired,
  state: PropTypes.string.isRequired
};

Video.propTypes = {
  ...baseVideoPropTypes,
  onReprocess: PropTypes.func.isRequired,
  onExtractSegment: PropTypes.func.isRequired
};

class VideoList extends Component {
  render() {
    const {videos, onReprocess, onExtractSegment} = this.props;

    const renderedVideos = videos.map(
      ({url, isLargelyObjectionable, videoId, state}) =>
          <Video key={url} {...{url, isLargelyObjectionable, videoId, state, onReprocess, onExtractSegment}} />);

    return (
      <div className="video-list">
        {renderedVideos}
      </div>
    );
  }
}

VideoList.propTypes = {
  videos: PropTypes.arrayOf(
    PropTypes.shape(baseVideoPropTypes)).isRequired,
  onReprocess: PropTypes.func.isRequired,
  onExtractSegment: PropTypes.func.isRequired
};

export default VideoList;
