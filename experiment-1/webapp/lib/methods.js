function parseUrl(url) {
  var videoId;
  [, , videoId] = url.match(/^.*(youtu.be\/|v\/|e\/|u\/\w+\/|embed\/|v=)([^#\&\?]*).*/);
  return {videoId, canonical: `https://www.youtube.com/watch?v=${videoId}`};
}

Meteor.methods({
  labelVideo: function({url, isLargelyObjectionable}) {
    const {videoId, canonical} = parseUrl(url);

    LabelledVideos.insert({
      url: canonical,
      isLargelyObjectionable,
      videoId,
      state: 'NEW',
      segmentsTrained: 0 // XXX why is this here?
    });
  },
  reprocessVideo: function(videoId) {
    console.log("reprocessVideo", videoId);
    LabelledVideos.update({videoId}, {
      $set: {state: 'NEW'},
      $unset: {processingByWorker: ""}
    });
  }
});
