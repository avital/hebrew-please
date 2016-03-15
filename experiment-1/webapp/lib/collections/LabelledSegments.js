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
  spectrogram: {
    type: [[Number]],
    label: "Processed spectogram matrix; the input to the machine learning model"
  },
  isObjectionable: {
    type: Boolean,
    label: "Is this segment objectionable?"
  }
}));

