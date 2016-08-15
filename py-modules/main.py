from objects import *
import crawler
import parser
import utils 


def main(): 
	'''Styles setup'''
	all_styles = {}

	'''Hops Setup'''
	#begin crawler for hops page
	baseurl = 'https://byo.com/resources/'
	styleslist = range(1,3)
	crawl_type = 'hops'

	pagecrawl = crawler.setupCrawler(baseurl,crawl_type)

	problem_child = 0
	for i in styleslist:
		pagecrawl,problem_child = crawler.crawlStyle(pagecrawl,i,problem_child,print_details=True)
		if problem_child > 2: 
			break
		style_name, names, output = pagecrawl.getTableContents()
		print style_name

		# check if the style object exists
		try: 
			all_styles[style_name]
		except KeyError: 
			all_styles[style_name] = Style(style_name)

		#parse the crawler
		hopper = parser.HopParser(names)
		hopper.parse(output)

		#add each hop to the style
		for profile in hopper.parsed: 
			all_styles[style_name].addHop(profile)


	pagecrawl.endDriver()	#close hop driver
	return all_styles 

# For each style in the hops list, 

#initialize style object

#for each hop being iterated, 
#if a hop object exists with the same name, add new style and new flavor to the object

#else, initialize new hop object with name, this style, flavors, and aa%