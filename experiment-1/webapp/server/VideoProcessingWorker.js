import Fiber from 'fibers';
import Future from 'fibers/future';
import child_process from 'child_process';

const sleep = Meteor._sleepForMs;

class VideoProcessingWorker {
  constructor() {
    this.id = Random.id();
  }

  processSingleVideo() {
    const worker = this;
    const video = LabelledVideos.findOne({state: 'NEW'});
    if (!video) {
      // all videos being processed, or done processing
      return;
    }

    var numModifiedDocs = LabelledVideos.update(
      {_id: video._id, state: 'NEW'},
      {$set: {
        state: 'PROCESSING',
        processingByWorker: worker.id
      }});

    if (numModifiedDocs === 0) {
      // another worker already started processing this video
      return;
    }

    console.log(`Worker ${worker.id}: Processing ${video.url}`);

    const cp = child_process.exec(
      `python3 ${process.env.PWD}/../process-video/process-video.py ${video.videoId}`,
      function(err, stdout, stderr) {
        Fiber(() => {
          if (err) {
            LabelledVideos.update(video._id, {$set: {state: 'ERROR'}});

            console.error(`Worker ${worker.id}: Error processing ${video.url}.`);
          } else {
            LabelledVideos.update(video._id, {$set: {state: 'PROCESSED'}});

            console.log(`Worker ${worker.id}: Finished processing ${video.url}.`);
          }
        }).run();
      });

    cp.stdout.pipe(process.stdout);
    cp.stderr.pipe(process.stderr);
  }

  run() {
    Fiber(() => {
      for (;;) {
        try {
          this.processSingleVideo();
        } catch (e) {
          console.error(e);
        }

        sleep(2000);
      }
    }).run();
  }
}

new VideoProcessingWorker().run();
