import ical2newsletter as i2n
from datetime import datetime, date 
import unittest as unittest

class ical2newsletterTest(unittest.TestCase):

	def testSeparatePrettyDatetimeDateOnly(self):
		self.failUnlessEqual('Saturday 27 September', i2n.separate_pretty_datetime(datetime(1975,9,27,0,0)))

	def testSeparatePrettyDatetimeHourAM(self):
		self.failUnlessEqual('Saturday 27 September, 1AM', i2n.separate_pretty_datetime(datetime(1975,9,27,1,0)))

	def testSeparatePrettyDatetimeHourPM(self):
		self.failUnlessEqual('Saturday 27 September, 1PM', i2n.separate_pretty_datetime(datetime(1975,9,27,13,0)))

	def testSeparatePrettyDatetimeMinuteAM(self):
		self.failUnlessEqual('Saturday 27 September, 1.30AM', i2n.separate_pretty_datetime(datetime(1975,9,27,1,30)))

	def testSeparatePrettyDatetimeMinutePM(self):
		self.failUnlessEqual('Saturday 27 September, 1.30PM', i2n.separate_pretty_datetime(datetime(1975,9,27,13,30)))

	def testPrettyDateRangeOneWholeDay(self):
		self.failUnlessEqual(i2n.pretty_date_range(datetime(1975,9,27,0,0), datetime(1975,9,28,0,0)), 'Saturday 27 September')

	def testPrettyDateRangeAMtoAM(self):
		self.failUnlessEqual(i2n.pretty_date_range(datetime(1975,9,27,8,0), datetime(1975,9,27,11,0)), 'Saturday 27 September, 8-11AM')

	def testPrettyDateRangeAMtoPM(self):
		self.failUnlessEqual(i2n.pretty_date_range(datetime(1975,9,27,9,0), datetime(1975,9,27,17,0)), 'Saturday 27 September, 9-5PM')

	def testPrettyDateRangeMinToHour(self):
		self.failUnlessEqual(i2n.pretty_date_range(datetime(1975,9,27,18,30), datetime(1975,9,27,23,0)), 'Saturday 27 September, 6.30-11PM')	

	def testPrettyDateRangeHourToMin(self):
		self.failUnlessEqual(i2n.pretty_date_range(datetime(1975,9,27,18,0), datetime(1975,9,27,22,30)), 'Saturday 27 September, 6-10.30PM')	

	def testPrettyDateRangeAmbiguous(self):
		self.failUnlessEqual(i2n.pretty_date_range(datetime(1975,9,27,7,0), datetime(1975,9,27,23,0)), 'Saturday 27 September, 7AM-11PM')

	def testPrettyDateRangeTwoWholeDays(self):
		self.failUnlessEqual(i2n.pretty_date_range(datetime(1975,9,27,0,0), datetime(1975,9,29,0,0)), '27-28 September')

	def testPrettyDateRangeAcrossMonths(self):
		self.failUnlessEqual(i2n.pretty_date_range(datetime(1975,9,27,0,0), datetime(1975,10,27,0,0)), '27 September - 27 October')

	def testPrettyDateRangeTwoPartDaysHour(self):
		self.failUnlessEqual(i2n.pretty_date_range(datetime(1975,9,27,8,0), datetime(1975,9,29,10,0)), '27 September, 8AM - 29 September, 10AM')

	def testPrettyDateRangeTwoPartDaysMinutes(self):
		self.failUnlessEqual(i2n.pretty_date_range(datetime(1975,9,27,8,30), datetime(1975,9,29,10,45)), '27 September, 8.30AM - 29 September, 10.45AM')

	def testPrettyPrintDateType(self):
		self.failUnlessEqual(i2n.pretty_date_range(date(1975,9,27), date(1975,9,28)), '27-28 September')

		# self.failUnlessEqual(i2n.pretty_date_range(datetime(1975,9,27,10,0), datetime(1975,9,27,16,0)), 'Saturday 27 September, 10-4PM')
		# self.failUnlessEqual(i2n.pretty_date_range(datetime(1975,9,27,8,0), datetime(1975,9,27,20,0)),'Saturday 27 September, 8AM-8PM')
		# self.failUnlessEqual(i2n.pretty_date_range(datetime(1975,9,27,0,0), datetime(1975,9,28,0,0)),'Saturday 27 September') # is this how whole day is represented?
		# self.failUnlessEqual(i2n.pretty_date_range(datetime(1975,9,27,0,0), datetime(1975,9,30,0,0)),'Saturday 27 September - Tuesday 30 September') # is this how whole day is represented?
  

if __name__ == "__main__":
	unittest.main()