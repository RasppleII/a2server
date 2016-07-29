#!/usr/bin/env python
'''CLOCK.PATCH by Greg Branche implemented in Python 2/3 for A2SERVER

This is a line-for-line conversion of an edited version of CLOCK.PATCH
from the System Tools 2 disk in GS/OS 6.0.1. It's not good Python,
but I thought it would be an interesting exercise. In general
I have tried replicate each line as closely to BASIC as possible.

Because BASIC substrings are 1-based and python's are 0-based, various
indexes are minus one of their BASIC equivalents.

The one change is that you can optionally pass the day and date by
command line argument (e.g "Wed 3/13/15"). I also improved error
checking. These are in the BASIC lines that don't end in 0.

Rather than modifying PRODOS, this outputs a string of comma-separated
year values for a calling script (the a2server-setup installer),
followed by a space and a dd-Mmm-yy date string.
'''

# imports for python 3 code compatibility
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

# other imports
import sys
import datetime

# substitute raw_input for input in Python2
try: input = raw_input
except NameError: pass

dow_str = None
day = None
if len(sys.argv) > 2:
    dow_str = sys.argv[1] # day of week passed on command line
    day     = sys.argv[2] # date passed on command line

                                                # 60000  REM  # of days in each month
data = [31,28,31,30,31,30,31,31,30,31,30]       # 60010  DATA  31,28,31,30,31,30,31,31,30,31,30
                                                # 60020  REM  Names of days of week
data += [                                       # 60030  DATA  SUN,MON,TUE,WED,THU,FRI,SAT
  "SUN","MON","TUE","WED","THU","FRI","SAT"]
data = iter(data)
                                                # 110  REM  cu() = cumulative # of days in year
cu = [0] * 13                                   # 120  DIM CU(12)
                                                # 130  REM  fill array with # of days in year
cu[1] = 0                                       # 140 CU(1) = 0: REM  January
for i in range(2,13):                           # 150  FOR I = 2 TO 12
    x = next(data)                              # 160  READ X
    cu[i] = cu[i-1] + x                         # 170 CU(I) = CU(I - 1) + X
                                                # 180  NEXT I

                                                # 200  REM  DN$() = Names for days of week
dn = [""] * 8                                   # 210  DIM DN$(7)
                                                # 220  REM  fill array with names of days of week
for i in range(1,8):                            # 230  FOR I = 1 TO 7
    dn[i] = next(data)                          # 240  READ DN$(I)
                                                # 250  NEXT I

                                                # 270  REM  yt() is the year table values
yt = [0] * 8                                    # 280  DIM YT(7)

def mod7(x):                                    # 340  DEF  FN MOD7(X) =  INT (((X / 7) -  INT (X / 7)) * 7 + .5)
    return int(((x / 7) -  int(x / 7)) * 7 + .5)

def find_slash_pos(day):                        # 799  REM  Finds position of / within date string
    x = -1                                      # 800 X = 0: REM On exit, contains position of /, or 0 if none found
    for i in range(0,3):                        # 810  FOR I = 1 TO 3
        if day[i:i+1] == "/": x = i; break      # 820  IF  MID$ (DAY$,I,1) = "/" THEN X = I:I = 3
                                                # 830  NEXT I
    return x                                    # 840  RETURN

while True:                                     # 999  REM  get the user's input and convert
    if not day:
        print(                                  # 1010  PRINT "Please enter today's date (mm/dd/yy)"
          "Please enter today's date (mm/dd/yy)")
        day = input("-> ")                      # 1020  INPUT "-> ";DAY$
    x = find_slash_pos(day)                     # 1030  GOSUB 800: REM  find slash separator
    input_ok = False
    while not input_ok:
        if not (x != -1):                       # 1040  IF X <  > 0 THEN 1080
            print(                              # 1050  PRINT "Invalid date entered.  Please try again."; CHR$ (7)
              "Invalid date entered.  Please try again.\x07")
            break                               # 1060  GOTO 1010
                                                # 1070  REM  Convert month value to numeric variable
        mo = int(day[0:0+x])                    # 1080 MO =  VAL ( MID$ (DAY$,1,X - 1))
        day = day[x+1:]                         # 1090 DAY$ =  MID$ (DAY$,X + 1)
        if mo < 1 or mo > 12: x = -1; continue  # 1100  IF MO < 1 OR MO > 12 THEN 1050: REM Range check the month value
        x = find_slash_pos(day)                 # 1110  GOSUB 800: REM Parse out the current day
        if x == -1: continue                    # 1120  IF X = 0 THEN 1050
                                                # 1130  REM  Convert day string into numeric value
        da = int(day[0:0+x])                    # 1140 DA =  VAL ( MID$ (DAY$,1,X - 1))
        day = day[x+1:]                         # 1150 DAY$ =  MID$ (DAY$,X + 1)
        if da < 1 or da > 31: x = -1; continue  # 1160  IF DA < 1 OR DA > 31 THEN 1050: REM Range check the day value
        if mo == 2 and da > 29:                 # 1161  IF MO = 2 AND DA > 29 THEN 1050
            x = -1; continue
        if (mo == 4 or                          # 1162  IF (MO = 4 OR MO = 6 OR MO = 9 OR MO = 11) AND DA > 30 THEN 1050
            mo == 6 or
            mo == 9 or
            mo == 11) and da > 30: x = -1; continue
                                                # 1170  REM  Convert year string into numeric value
        yr = int(day)                           # 1180 YR =  VAL (DAY$)
        if yr < 0 or yr > 99: x = -1; continue  # 1190  IF YR < 0 OR YR > 99 THEN 1050: REM Only allow 0-99
        if yr > 39: yr = yr + 1900              # 1200  IF YR > 39 THEN YR = YR + 1900: REM 40-99 must be 1940-1999
        if yr < 40: yr = yr + 2000              # 1210  IF YR < 40 THEN YR = YR + 2000: REM 0-39 must be 2000-2039
        if ((yr / 4) != int(yr / 4) and         # 1211  IF ((YR / 4) <  >  INT(YR / 4)) AND MO = 2 AND DA > 28 THEN 1050
            mo == 2 and
            da > 28): x = -1; continue
        input_ok = True
    if x != -1: break
    else: dow_str = ""; day = ""

while True:
    if not dow_str:
        print(
          "Please enter the day of the week")   # 1230  PRINT "Please enter the day of the week"
        dow_str = input("(e.g. Wed) -> ")       # 1240  INPUT "(e.g. Wed) -> ";DOW$
    input_ok = False
    while not input_ok:
        if not (len(dow_str) >= 3):             # 1250  IF  LEN (DOW$) >  = 3 THEN 1270: REM Must be at least 3 characters
            print(                              # 1260  PRINT "Invalid day of week.  Please try again."; CHR$ (7): GOTO 1230
                "Invalid day of week.  Please try again.\x07")
            break
        if len(dow_str) > 3:                    # 1270  IF  LEN (DOW$) > 3 THEN DOW$ =  LEFT$ (DOW$,3)
            dow_str = dow_str[0:0+3]
                                                # 1280  REM  Shift any lower case letters to upper case
        b = ""                                  # 1290 B$ = ""
        for i in range(0,3):                    # 1300  FOR I = 1 TO 3
            a = dow_str[i:i+1]                  # 1310 A$ =  MID$ (DOW$,I,1)
            if (                                # 1320  IF  ASC (A$) >  =  ASC ("a") AND  ASC (A$) <  =  ASC ("z") THEN A$ =  CHR$ ( ASC (A$) - ( ASC ("a") -  ASC ("A")))
              ord(a) >= ord("a") and ord(a) <= ord("z")): a = chr(ord(a) - (ord("a") -  ord("A")))
            b = b + a                           # 1330 B$ = B$ + A$
                                                # 1340  NEXT I
        dow_str = b                             # 1350 DOW$ = B$
                                                # 1360  REM  Now convert day-of-week string to numeric value
        dow_num = 0                             # 1370 DOW = 0
        for i in range (1,8):                   # 1380  FOR I = 1 TO 7
            if dow_str == dn[i]:                # 1390  IF DOW$ = DN$(I) THEN DOW = I:I = 7
                dow_num = i; i = 7
                                                # 1400  NEXT I
        if dow_num == 0: dow_str = ""; continue # 1410  IF DOW = 0 THEN 1260
        input_ok = True
    if len(dow_str) >= 3: break
    else: dow_str = ""; day = ""
                                                # 1430  REM  Calculate the number of days so far this year
dys = da + cu[mo]                               # 1440 DYS = DA + CU(MO)
oyr = yr
                                                # 1450  REM  Must account for extra day in leap year
if ((yr / 4) == int(yr / 4)) and (mo > 2):      # 1460  IF (YR / 4) =  INT (YR / 4) AND MO > 2 THEN DYS = DYS + 1
    dys = dys + 1

                                                # 1480  REM  Now calculate the index to use to fill in the table
idx = dow_num - mod7(dys) + 1                   # 1490 IDX = DOW -  FN MOD7(DYS) + 1
idx = abs(idx - 10)                             # 1500 IDX =  ABS (IDX - 10)
if idx > 7: idx = idx - 7                       # 1510  IF IDX > 7 THEN IDX = IDX - 7

                                                # 1530  REM  Now we can fill in the year table
for i in range(1,8):                            # 1540  FOR I = 1 TO 7
    if '_i' in vars() and i < (_i + 1): continue    # python: simulate change of i within loop
    x = yr - 1900                               # 1550 X = YR - 1900
    if x >= 100: x = x - 100                    # 1560  IF X >  = 100 THEN X = X - 100
    yt[idx] = x                                 # 1570 YT(IDX) = X: REM  store the year into table
    idx = idx - 1                               # 1580 IDX = IDX - 1
    if idx < 1: idx = 7                         # 1590  IF IDX < 1 THEN IDX = 7
    if not ((yr / 4) != int(yr / 4)):           # 1600  IF (YR / 4) <  >  INT (YR / 4) THEN 1660: REM  not a leap year
        i = i + 1; _i = i                       # 1610 I = I + 1: REM  update index
        if i > 7: continue                      # 1620  IF I > 7 THEN 1670: REM  if entire array done, exit
        yt[idx] = x                             # 1630 YT(IDX) = X: REM  duplicate entry for leap year
        idx = idx - 1                           # 1640 IDX = IDX - 1
        if idx < 1: idx = 7                     # 1650  IF IDX < 1 THEN IDX = 7
    yr = yr + 1                                 # 1660 YR = YR + 1
                                                # 1670  NEXT I

print(",".join([str(x) for x in yt[1:]]) + " " +
      str(da).encode("L1").decode("L1").zfill(2) + "-" +
      datetime.date(1900, mo, 1).strftime('%b') + "-" +
      str(oyr).encode("L1").decode("L1")[2:])
