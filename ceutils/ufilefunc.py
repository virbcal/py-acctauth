# ---------------------------------------------------------------------
# Copyright (c) 2001-2021 CALIMLIM Enterprises. All rights reserved.
#
# Author: Virgilio B Calimlim, 2020/09
# ---------------------------------------------------------------------
# Progname   : ufilefunc.py
# Description: Integrated file-related utilities
# System     : General
# Purpose    : File-related functions
# Functions and parameters:
#  version     Script version number
#           -  none
#  text2bits   Convert Unicode text chars to binary
#        text  (rqd) text string to be coverted
#    encoding  (opt) input format           (def: utf-8)
#      errors  (opt) errors option          (def: surrogatepass)
#  bits2text   Convert binary to Unicode text chars
#        bits  (rqd) binary string to be coverted
#    encoding  (opt) input format           (def: utf-8)
#      errors  (opt) errors option          (def: surrogatepass)
#  genans      Generate sorted AlpaNumericSpecial chars list
#           v  (opt) spec chars version     (def: 0)
#  vsiper      Encrypt plain text
#        ptxt  (rqd) text string to be encrypted (def: test)
#         key  (rqd) cipher key             (def: 14)
#           v  (opt) spec chars version     (def: 0)
#  vdesiper    Decode encrypted text
#        ctxt  (rqd) text string to be decoded (def: test)
#         key  (rqd) cipher key             (def: 14)
#           v  (opt) spec chars version     (def: 0)
#  getsetting  Get the setting value for the corresponding setting key
#    setgfile  (opt) setting file           (def: settings.cfg)
#         key  (opt) key attribute          (def: timezone)
#  getwkdir    Get the common applications work directory
#         key  (opt) key attribute          (def: workdir)
#  uniqstr     Generate a unique string qualifier
#         len  (opt) output string length   (def: 21 'yyyymmdd.HHMMSSnnnnnn')
#  genuniqfnam Generate a unique filename
#        odir  (opt) ofil directory         (def: apps work directory)
#        pnam  (opt) ofil primary name qual (def: function name)
#        mqal  (opt) ofil middle name qual  (def: blank)
#         ext  (opt) ofil extension         (def: .dat)
#  parsSysargv Parse sys.argv
#       sargs  (opt) sys.argv list
#        keys  (opt) keys list
# ---------------------------------------------------------------------
# Revisions  :
# 0.0   2020-09-01 virbcal  Initial release;
# 0.1   2020-09-06 virbcal  added realign();
# 0.1.1 2020-09-25 virbcal  integrated getsetting(), timestamp() & uniqstr();
#                           added savelist();
# 0.1.2 2020-10-02 virbcal  added compact();
#                           renamed realign() to uncompact();
#                           improved code logic for better performance;
# 0.1.3 2020-10-20 virbcal  added APPSDIR verification in getsetting();
#                           added writelog();
# 0.1.4 2020-12-14 virbcal  added text2bits() & bits2text();
#                           added siper() & desiper();
#                           added genans(), vsiper() & vdesiper();
# 0.1.5 2020-12-18 virbcal  add key2 in vsiper() & vdesiper();
#                           removed siper() & desiper();
# 0.1.6 2021-01-07 virbcal  added getfiledate() & getfileattr();
#                           mod genans() to include other spec chars;
# 0.1.6a 2021-01-12 virbcal inserted a spec char that was missed out;
# 0.1.7  2021-01-16 virbcal added parsSysargs();
# ---------------------------------------------------------------------

import sys
import os
import re
import datetime as dt
import time
import pytz
import platform


def version():
    # Function: Return version number.
    return os.path.basename(__file__)[:-3]+' 0.1.6a'


""" To support all Unicode characters in Python 3 """
# https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa
def text2bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def bits2text(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def genans(v=0):
    """ Generate sorted AlpaNumericSpecial chars list """
    alo = aup = ans = ''
    spc = "`~!@#$%^&()_-+={}[];',"
    if v==2:
       spc = spc+' .'                    # incl name/address
    if v==3:
       spc = spc+'.'                     # incl email
    num = "0123456789"
    for i in range(ord('a'),ord('z')+1):
        alo += chr(i)
    for i in range(ord('A'),ord('Z')+1):
        aup += chr(i)
    srtd = sorted(spc+num+aup+alo)
    for i in srtd:
        ans += i
    return ans


def vsiper(ptxt='test', key=21, v=0):
    """ The Virbcal Cipher Encryption algorithm """
    ans = genans(v)
    ansl = len(ans)
    ky2 = 0
    cipher_text = ""
    for letter in ptxt:
        idx = ans.find(letter)
        if idx == -1:
            return ''
        ky2 += 1
        nidx = (idx + key - ky2*7//2) % ansl
        cipher_text += ans[nidx]
    return cipher_text


def vdesiper(ctxt='test', key=21, v=0):
    """ The Virbcal Cipher Decoding algorithm """
    ans = genans(v)
    ansl = len(ans)
    ky2 = 0
    decode_text = ""
    for letter in ctxt:
        idx = ans.find(letter)
        if idx == -1:
            return ''
        ky2 += 1
        nidx = (idx - key + ky2*7//2) % ansl
        decode_text += ans[nidx]
    return decode_text


def getsetting(setgfile='settings.cfg', key='timezone'):
    if not os.path.isfile(setgfile):
        try:
            setgdir  = os.environ.get('APPSDIR')
            setgfile = os.path.join(setgdir, setgfile)
            if not os.path.isfile(setgfile):
                raise Exception
        except Exception as e:
            return 4, f"Error: File '{setgfile}' does not exist."

   #regx = '(^'+key+')((\s+)(.*?))+(\s+)(?#)'
    ptrn = '([\"|\'])(.*?)([\"|\'])'
    cmpl = re.compile(ptrn)
    with open(setgfile, 'rt') as inf:
        for line in inf:
            line = line.strip()
            if line.startswith(key):
                wdls = line.split()
                if wdls[0] in key:        # in faster than == ; perf
                    valu = line[len(key):].strip()
                    mat = cmpl.match(valu)
                    if mat != None:
                        return 0, valu[:mat.span()[1]].strip('\"\'')
                    comt = valu.find('#')
                    if comt == -1:
                        return 0, valu
                    return 0, valu[:comt].strip()
        return 4, f"Error: Key '{key}' not found."


def getwkdir(key='workdir'):
    rc, wkdir = getsetting(key=key)       # get work directory
    if rc:                                # rc != 0; perf
        return rc, wkdir
    if not os.path.exists(wkdir):
        return 4, f"Error: Work directory '{wkdir}' does not exist."
    return 0, wkdir


def uniqstr(len=21):
    return 0, dt.datetime.now().strftime('%Y%m%d.%H%M%S%f')[0:len] 


def genuniqfnam(odir='', pnam='', mqal='', ext='.dat'):
    if not odir:                          # blank; len == 0; perf
        rc, odir = getwkdir()
        if rc:                            # rc != 0; perf
            return rc, odir
    if not pnam or not pnam.strip() or pnam == '.':
        pnam = sys._getframe().f_code.co_name
    rc, unqstr = uniqstr()
    if rc:                                # rc != 0; perf
        return rc, unqstr
    uniqf = pnam+mqal+'_'+unqstr+ext
    try:
        file = os.path.join(odir,uniqf)
        return 0, file
    except Exception as e:
        return 4, f"osJoinError: '{file}'\n{str(e)}"


def main(args):
    pnam = args[1]
    if pnam == '.': 
        pnam = os.path.basename(__file__)[:-3]
    odir=mqal=''
    ext='.dat'
    if len(args) > 2:
        for n in range(2,len(args)):
            kw_lst = args[n].split('=')
            if len(kw_lst) == 2:
                if kw_lst[0] == 'odir':
                    odir = kw_lst[1]
                    continue
                if kw_lst[0] == 'mqal':
                    mqal = kw_lst[1]
                    continue
                if kw_lst[0] == 'ext':
                    ext = kw_lst[1]
                    continue
    rc, msg = genuniqfnam(odir, pnam, mqal, ext)
    print(msg)


""" Parse sys.argv """
# Note: Non-key/value arguments should follow the sequence of the keys arguments.
def parsSysargv(sargs, keys):
    lkeys = len(keys)
    if lkeys == 0:
        return 4, "Error: Required keys not found."
    if len(sargs) < 2:
        return 1, "Nothing to parse."

    args = sargs[1:]
    largs = len(args)
    vals = []
    for i in range(lkeys):
        vals.append('')

    for i in range(largs):
       #print(f'i={i}')                               # trace
        if '=' in args[i]:
            kw_lst = args[i].split('=')
            if len(kw_lst) == 2:
                for n in range(lkeys):
                   #print(f' n={n}')                  # trace
                    if kw_lst[0] == keys[n]:
                        vals[n] = kw_lst[1]
                       #print(f' val[{n}]={vals[n]}') # trace
                        break
            else:
                return 4, f"Error: Invalid parameter format '{args[i]}'"
        else:
            vals[i] = args[i]
    for n in range(lkeys):
        if '=' in vals[n]:
            return 4, f"Error: Invalid key found '{vals[n]}'"
    return 0, vals


if __name__ == '__main__':
    main(sys.argv)
