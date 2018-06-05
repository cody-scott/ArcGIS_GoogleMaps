import arcpy
import pythonaddins

import threading
import webbrowser

class GoogleStreetViewClass(object):
    location_a = None

    """Implementation for GoogleMaps_addin.tool (Tool)"""
    urlDCT = {"StreetView":"",
              "DDD":""}

    def __init__(self):
        self.enabled = True
        self.shape = "NONE" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
        self.cursor = 3
    def onMouseDown(self, x, y, button, shift):
        pass

    # @logging_decorator(tool_used="Google Street View Button")
    def onMouseDownMap(self, x, y, button, shift):
        point = self.create_point(x, y)
        print(point.JSON)
        self.location_a = point

    def onMouseUp(self, x, y, button, shift):
        pass
    def onMouseUpMap(self, x, y, button, shift):
        url_flag = "StreetView"
        if shift > 0:
            url_flag = "DDD"

        point = self.create_point(x, y)
        
        angle = self.get_directions(self.location_a, point)
        google_point = self.reproject_point(point)
        url = self.build_url(google_point, url_flag, angle)
        self.location_a = None

        self.open_browser(url)

    def onMouseMove(self, x, y, button, shift):
        pass
    def onMouseMoveMap(self, x, y, button, shift):
        pass
    def onDblClick(self):
        pass
    def onKeyDown(self, keycode, shift):
        pass
    def onKeyUp(self, keycode, shift):
        pass
    def deactivate(self):
        pass
    def onCircle(self, circle_geometry):
        pass
    def onLine(self, line_geometry):
        pass
    def onRectangle(self, rectangle_geometry):
        pass

    #Extra functions
    def get_directions(self, pg_a, pg_b):
        result = pg_a.angleAndDistanceTo(pg_b)
        if result[0] < 0:
            return (float(result[0])+180)+180
        else:
            return float(result[0])

    def build_url(self, point, urlType, angle=1):
        gmap = (point.centroid.X, point.centroid.Y, angle)
        print(gmap)
        url = ""
        if urlType == "DDD":
            url = (
                "https://www.google.com/maps/@{0},{1},299a,20y,{2}h,59.06t/data=!3m1!1e3".format(
                    gmap[1] - 0.004, gmap[0], gmap[2])
                )
        else:
            url = (
                "https://maps.google.com/maps?ll={0},{1}&layer=c&cbll={0},{1}&cbp=13,267.13,,0,5&q={0},{1}".format(
                    gmap[1], gmap[0]
                    )
                )
        print(url)
        return url

    def create_point(self, x, y):
        md = arcpy.mapping.MapDocument("CURRENT")
        fromSR = md.activeDataFrame.spatialReference
        new_point = arcpy.PointGeometry(arcpy.Point(x, y), fromSR)
        return new_point

    def reproject_point(self, point):
        toSR = arcpy.SpatialReference(4326)
        new_point = point.projectAs(toSR)
        return new_point

    def open_browser(self, url):
        threading.Thread(target=webbrowser.get().open, args=(url,)).start()