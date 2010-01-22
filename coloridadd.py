#!/usr/bin/env python

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Affero, Inc., either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.fsf.org/licensing/licenses/agpl-3.0.html>.

###############################################################################################
# Coloridadd is a script to generate SVG shapes representing colors, 
# using the ColorAdd code developped by Miguel Neiva: http://coloradd.net 
# The ColorAdd code is a monochromatic Graphical Code allowing colorblind to recognize colors.
###############################################################################################

import xml.dom.minidom as minidom

class ColorIdAdd:

	def __init__(self,primitives="primitives.svg"):
		self.load(primitives)
		self.parseShapes()
		self.removeShapes()


	def getElementById( self, elements, id ):
		for e in elements:
			if e.getAttribute("id") == id:
				return e
		return None


	def load( self, filename ):
		self.dom = minidom.parse(filename)


	def parseShapes(self):
		paths = self.dom.getElementsByTagName("path")
		rects = self.dom.getElementsByTagName("rect")
		forms = paths + rects

		self.shapes = {}

		for id in ["yellow", "yellow-dark", "blue", "blue-dark", "red", "red-dark", "dark", "light", "grey", "grey-dark", "shine"]:
			self.shapes[id] = self.getElementById( forms, id )
		

	def removeShapes(self):
		gs = self.dom.getElementsByTagName("g")
		for g in gs:
			for e in g.childNodes:
				if e.nodeType == e.ELEMENT_NODE:
					g.removeChild(e)


	def add(self,id):
		g = self.dom.getElementsByTagName("g")[0]
		g.appendChild( self.shapes[id] )


	def encode(self,pigments):
		"""'pigments' must be a dictionary with the following keys:
			blue, red, yellow, black, grey, shine"""

		suffix = ""

		if pigments.black:
			self.add("dark")
			suffix = "-dark"
		else:
			self.add("light")

		if pigments.grey and not pigments.blue and not pigments.red and not pigments.yellow:
			self.add("grey"+suffix)

		if pigments.blue:
			self.add("blue"+suffix)

		if pigments.red:
			self.add("red"+suffix)

		if pigments.yellow:
			self.add("yellow"+suffix)

		if pigments.shine:
			self.add("shine")


if __name__=="__main__":
	import sys
	from optparse import OptionParser
	
	parser = OptionParser()

	parser.add_option("-r", "--red", action="store_true", dest="red",
		help="add red pigment")

	parser.add_option("-b", "--blue", action="store_true", dest="blue",
		help="add blue pigment")

	parser.add_option("-y", "--yellow", action="store_true", dest="yellow",
		help="add yellow pigment")

	parser.add_option("-k", "--black", action="store_true", dest="black",
		help="add black pigment")

	parser.add_option("-e", "--grey", action="store_true", dest="grey",
		help="add grey pigment")

	parser.add_option("-s", "--shine", action="store_true", dest="shine",
		help='add the "shine" special pigment')

	parser.add_option("-o", "--output", dest="filename",
		help="write shape to FILE instead of standard output", metavar="FILE")

	parser.add_option("-p", "--primitives", dest="primitives", default="primitives.svg",
		help="use FILE as the SVG file containing primitives", metavar="FILE")

	(options, args) = parser.parse_args()


	cia = ColorIdAdd( options.primitives )

	cia.encode(options)

	if options.filename:
		f = open( options.filename, 'w' )
		f.write( cia.dom.toprettyxml() )
		f.close()
	else:
		print cia.dom.toprettyxml()

