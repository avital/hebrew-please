import React, {Component, PropTypes} from 'react';

class Video extends Component {
  render() {
    const {url, isLargelyObjectionable, videoId, state, onReprocess} = this.props;
    return (
      <div className="video">
        <iframe width="200" height="200" src={"http://www.youtube.com/embed/" + videoId} />

        {isLargelyObjectionable ? "BUZZ!!" : "...yawn..."}
        {" | "}
        {state}

        <button onClick={onReprocess.bind(null, videoId)}>
          reprocess
        </button>
      </div>
    );
  }
}

Video.propTypes = {
  url: PropTypes.string.isRequired,
  shouldAlert: PropTypes.bool.isRequired,
  processed: PropTypes.bool.isRequired,
  videoId: PropTypes.string.isRequired,
  processing: PropTypes.bool.isRequired
};

class VideoList extends Component {
  render() {
    const {videos, onReprocess} = this.props;

    const renderedVideos = videos.map(
      ({url, isLargelyObjectionable, videoId, state}) =>
          <Video key={url} {...{url, isLargelyObjectionable, videoId, state, onReprocess}} />);

    return (
      <div className="video-list">
        {renderedVideos}
      </div>
    );
  }
}

VideoList.propTypes = {
  videos: PropTypes.arrayOf(
    PropTypes.shape(Video.propTypes)).isRequired
};

export default VideoList;
