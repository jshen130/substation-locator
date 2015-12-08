__author__ = 'Carlos'

import argparse
import urllib2  # Documentation and examples: https://docs.python.org/2/howto/urllib2.html

import os
import time

GMAPS_KEY = "AIzaSyBVATyH6TTwMyVhxAsmII7gbXAX0U3bRhY"   # Carlos' Google Maps API key
MAP_X_SHIFT = 0.00085
MAP_Y_SHIFT = 0.00066

def frange(x, y, jump):
    while x < y:
        yield x
        x += jump

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download a region of Google Maps.')
    parser.add_argument('-startX', type=float, default=-122.07394123077393,
                       help='x coordinate of the bottom-left corner of the region')
    parser.add_argument('-startY', type=float, default=37.336196830686575,
                       help='y coordinate of the bottom-left corner of the region')
    parser.add_argument('-endX', type=float, default=-121.98828220367432,
                       help='x coordinate of the upper-right corner of the region')
    parser.add_argument('-endY', type=float, default=37.43058597092234,
                       help='y coordinate of the upper-right corner of the region')
    parser.add_argument('-zoom', type=int, default=20,
                       help='zoom level at which to get the satellite images')
    parser.add_argument('-prefix', type=str, default="sunnyvale_region_map",
                       help='label to identify this region')
    args = parser.parse_args()
    args.startY, args.startX = 37.693813, -122.512677
    args.endY, args.endX = 37.832921, -122.357514
    args.prefix = "SF_region_map"

    cnt_X = int((args.endX - args.startX)/MAP_X_SHIFT)
    cnt_Y = int((args.endY - args.startY)/MAP_Y_SHIFT)
    print "%d tiles wide, %d tiles high" % (cnt_X, cnt_Y)

    cnt_img = 0
    if not os.path.exists("../" + args.prefix):   # Make sure directory "../prefix" exists
        os.makedirs("../" + args.prefix)          # Otherwise create it

    for y in frange(args.startY, args.endY, MAP_Y_SHIFT):
        for x in frange(args.startX, args.endX, MAP_X_SHIFT):
            cnt_img += 1

            req = urllib2.Request("https://maps.googleapis.com/maps/api/staticmap?maptype=satellite&center=" +
                    str(y) + "," + str(x) + "&zoom=" + str(args.zoom) + "&size=640x640&key=" + GMAPS_KEY)
            try:
                image = urllib2.urlopen(req).read()
            except KeyboardInterrupt as e:
                raise e
            except:
                print "Error downloading image. Retrying."
                image = urllib2.urlopen(req).read()

            out_file_name = "../" + args.prefix + "/" + args.prefix + "_" + str(cnt_img) + "_y" + str(y) + "_x" + str(x) + "_z" + str(args.zoom) + ".png"
            with open(out_file_name, 'wb') as f:
                f.write(image)

            print "\tImage " + str(cnt_img) + "/" + str(cnt_X*cnt_Y) + " saved as '" + out_file_name + "'. @" + time.strftime("%H:%M:%S")
    print "YAAAY, DONE! :)"
