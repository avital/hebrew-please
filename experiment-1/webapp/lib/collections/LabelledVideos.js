LabelledVideos = new Mongo.Collection("videos");

LabelledVideos.attachSchema(new SimpleSchema({
  url: {
    type: String,
    label: "URL to YouTube video"
  },
  videoId: {
    type: String,
    label: "YouTube video ID"
  },
  isLargelyObjectionable: {
    type: Boolean,
    label: "Is this video mostly known to contain large portions of objectionable content?"
  },
  state: {
    type: String,
    label: "One of: NEW, PROCESSING, PROCESSED, ERROR"
  },
  segmentsTrained: {
    type: Number,
    label: "Number of random segments used to train model so far"
  },
  processingByWorker: {
    type: String,
    label: "Worker ID processing this video",
    optional: true
  }
}));
