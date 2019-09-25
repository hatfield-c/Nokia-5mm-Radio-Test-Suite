
class calc_ver():

    RF_Start = 37.0
    RF_Stop = 40.0

    def __init__(self, center_freq_ghz, ch_bw_mhz, rbw, sweep_time = 0.2 ):

          #each frequency has 4 spans. Will be stored as a dictionary of tuples.
          #enter Center Frequency from the beginning.
          self.fc = center_freq_ghz #convert to hz.
          self.ch_bw_mhz = int(ch_bw_mhz)
          self.rbw = int(rbw)
          self.sweep_time = sweep_time

          #channel start and stop around fc calculated from offset to bandwidth
          self.ch_start = self.fc -((self.ch_bw_mhz/1000)/2)
          self.ch_stop = self.ch_start +(self.ch_bw_mhz/1000)

          #span of the bw
          self.span = int((self.ch_stop - self.ch_start)*(10**9))

          #calc min number points. Cannot be lower than 1001
          self.points = int(2*(self.ch_bw_mhz/self.span))
          if(self.points < 1001):
              self.points = int(1001) #minimum number of pts.

          self.span_list = self.calc_spans() #lets just see whats happening

          print("\n")
          for span in self.span_list:
              print(span)
              #note: floats are being expanded beyond significant figures
              #in output version extra hz are truncated by formatter.

    def calc_spans(self):

        #spans go in order of increasing frequency but unlike the
        #SC OBUE Results Calculation Tests spreadsheet here we
        #       S T A R T  I N D E X I N G  A T  0      #

        #spans will be stored as a list where index denotes span number
        span = []

        #span0
        start0 = self.RF_Start - 1.5
        stop0 = self.ch_start - (0.1 * (self.ch_bw_mhz/1000)) + (0.5/1000)
        span0 = (start0, stop0)
        span.append(span0)

        #span1
        start1 = stop0
        stop1 = self.ch_start-(0.5/1000)
        span1 = (start1, stop1)
        span.append(span1)

        #span2
        start2 = self.ch_stop+(0.5/1000)
        stop2 = self.ch_stop+(0.1*(self.ch_bw_mhz/1000)) + (0.5/1000)
        span2 = (start2, stop2)
        span.append(span2)

        #span3 TODO: come back to this so it isn't hardcoded to 40.
        start3 = stop2
        stop3 = 40
        span3 = (start3, stop3)
        span.append(span3)

        #return list of spans. Each span is a tuple consisiting of
        #the start and then the stop fq in float GHz
        return span



if __name__ == '__main__':

        testcase = calc_ver(37.40034, 100, 1000000, 0.2)
        #run stubbed out version of init command.
