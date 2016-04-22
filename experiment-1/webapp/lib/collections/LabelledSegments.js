LabelledSegments = new Mongo.Collection("segments");

LabelledSegments.attachSchema(new SimpleSchema({
  videoId: {
    type: String,
    label: "YouTube video ID"
  },
  startSeconds: {
    type: Number,
    label: "Segment starts <...> seconds into the video"
  },
  endSeconds: {
    type: Number,
    label: "Segment ends <...> seconds into the video"
  },
  state: {
    type: String,
    label: "One of: NEW, PROCESSING, PROCESSED, ERROR"
  },
  spectrogram: {
    type: [[Number]],
    label: "Processed spectogram matrix; the input to the machine learning model",
    optional: true
  },
  isObjectionable: {
    type: Boolean,
    label: "Is this segment objectionable?"
  }
}));

