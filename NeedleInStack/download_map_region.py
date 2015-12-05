__author__ = 'Carlos'

import argparse
import urllib2  # Documentation and examples: https://docs.python.org/2/howto/urllib2.html

import os

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
    args = parser.parse_args()

    cnt_img = 0
    prefix = "sunnyvale_region_map"
    if not os.path.exists("../" + prefix):   # Make sure directory "../prefix" exists
        os.makedirs("../" + prefix)          # Otherwise create it

    for y in frange(args.startY, args.endY, MAP_Y_SHIFT):
        for x in frange(args.startX, args.endX, MAP_X_SHIFT):
            cnt_img += 1

            req = urllib2.Request("https://maps.googleapis.com/maps/api/staticmap?maptype=satellite&center=" +
                    str(y) + "," + str(x) + "&zoom=" + str(args.zoom) + "&size=640x640&key=" + GMAPS_KEY)
            image = urllib2.urlopen(req).read()

            out_file_name = "../" + prefix + "/" + prefix + "_" + str(cnt_img) + "_y" + str(y) + "_x" + str(x) + "_z" + str(args.zoom) + ".png"
            with open(out_file_name, 'wb') as f:
                f.write(image)

            print "\tImage " + str(cnt_img) + " saved as '" + out_file_name + "'"
    print "YAAAY, DONE! :)"
