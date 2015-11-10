import argparse
import os
import urllib2  # Documentation and examples: https://docs.python.org/2/howto/urllib2.html

GMAPS_KEY = "AIzaSyBVATyH6TTwMyVhxAsmII7gbXAX0U3bRhY"   # Carlos' Google Maps API key
MAP_X_SHIFT = 0.00085
MAP_Y_SHIFT = 0.00066

def parse_coords_file(file_name):
    with open(file_name, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    return lines

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-file', type=str, default='coordinates-manual_WIP.txt',
                       help='path to file that contains substation coordinates')
    parser.add_argument('-radius', type=int, default=5,
                       help='distance (in image widths) around the substation center within which we want to get images')
    parser.add_argument('-zoom', type=int, default=20,
                       help='zoom level at which to get the satellite images')
    args = parser.parse_args()

    coords = parse_coords_file(args.file)
    cnt_subs = 0
    for coord in coords:
        [y_ctr, x_ctr] = [float(a) for a in coord.split(',')]
        cnt_subs += 1
        if not os.path.exists("substation_" + str(cnt_subs)):   # Make sure directory "substation_N" exists
            os.makedirs("substation_" + str(cnt_subs))          # Otherwise create it

        for x in range(-args.radius, args.radius+1):
            x_curr = x_ctr + x * MAP_X_SHIFT
            for y in range(-args.radius, args.radius+1):
                y_curr = y_ctr + y * MAP_Y_SHIFT
                cnt_img = 1 + (y+args.radius) + (x+args.radius)*(2*args.radius+1)

                req = urllib2.Request("https://maps.googleapis.com/maps/api/staticmap?maptype=satellite&center=" +
                        str(y_curr) + "," + str(x_curr) + "&zoom=" + str(args.zoom) + "&size=640x640&key=" + GMAPS_KEY)
                image = urllib2.urlopen(req).read()
                out_file_name = "substation_" + str(cnt_subs) + "/" + "substation_" + str(cnt_subs) + "_img" + str(cnt_img) + "_y" + str(y_curr) + "_x" + str(x_curr) + "_z" + str(args.zoom) + ".png"

                with open(out_file_name, 'wb') as f:
                    f.write(image)

                if x == 0 and y == 0:
                    out_file_name = "substation_" + str(cnt_subs) + "_y" + str(y_curr) + "_x" + str(x_curr) + "_z" + str(args.zoom) + ".png"
                    with open(out_file_name, 'wb') as f:
                        f.write(image)

                print "\tImage " + str(cnt_img) + "/" + str((2*args.radius + 1)**2) + " saved as '" + out_file_name + "'"

        print str(cnt_subs) + "/" + str(len(coords)) + " - Received satellite images centered at (" + coord + ")"
