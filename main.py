import argparse
from config.settings import CAMERA_SOURCE, default_params
from gui import run as gui_run
from dashboard.routes import app as dashboard_app
from motion.camera import VideoSource
from motion.detector import MotionDetector
from ai.gemma_runner import GemmaRunner

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--gui', action='store_true')
    p.add_argument('--dash', action='store_true')
    p.add_argument('--source', default=CAMERA_SOURCE)
    args = p.parse_args()

    if args.gui:
        gui_run(args.source)
    elif args.dash:
        dashboard_app.run(debug=False)
    else:
        params = default_params()
        detector = MotionDetector(**params)
        gemma = GemmaRunner()
        for frame in VideoSource(args.source):
            res = detector.check(frame)
            if res.detected:
                print(gemma.describe_images(res.paths))
        VideoSource(args.source).cleanup()