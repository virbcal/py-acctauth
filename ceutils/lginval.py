# ---------------------------------------------------------------------
# Copyright (c) 2001-2020 CALIMLIM Enterprises. All rights reserved.
#
# Author: Virgilio B Calimlim, 2020/12
# ---------------------------------------------------------------------
# Progname   : lginval.py
# Description: Login validation program
# System     : General
# Purpose    : Authentication function
# Functions and parameters:
#  version     Script version number
#           -  none
#  cons        Define constants
#         key  (opt)                        (def: '')
#  getusrf     Get usrfile
#         usr  (rqd) userid
#  valpwd      Validate passwords
#         pwd  (rqd) old password
#        npwd  (opt) new password           (def: '')
#  valdtls     Validate user details
#         nam  (rqd) user name
#         adr  (opt) user address           (def: '')
#         phn  (opt) user phone             (def: '')
#         eml  (opt) user email             (def: '')
#  verusr      Verify userid & password
#         usr  (rqd) userid
#         pwd  (rqd) password
#  addusr      Add new user
#         nam  (rqd) user name
#         usr  (rqd) new userid
#         pwd  (rqd) new password
#         adr  (opt) user address           (def: '')
#         phn  (opt) user phone             (def: '')
#         eml  (opt) user email             (def: '')
#         rmv  (opt) remove userfile        (def: False)
#  chgpwd      Change password
#         usr  (rqd) userid
#         pwd  (rqd) old password
#        npwd  (rqd) new password
#  getdtls     Get user details
#         usr  (rqd) userid
#         pwd  (rqd) password
#  upddtls     Update user details
#         usr  (rqd) userid
#         pwd  (rqd) password
#         nam  (rqd) user name
#         adr  (opt) user address           (def: '')
#         phn  (opt) user phone             (def: '')
#         eml  (opt) user email             (def: '')
#         rmv  (opt) remove userfile        (def: False)
# ---------------------------------------------------------------------
# Revisions  :
# 0.0   2020-12-17 virbcal  Initial release;
# 0.1   2021-01-08 virbcal  converted cons() to a functon;
#                           added getusrf() & getdtls();
# 0.2   2021-01-09 virbcal  inserted rectyp field in usrfile;
# 0.3   2021-01-11 virbcal  streamline getusrf() usage;
#                           added upddtls() & valdtls();
# ---------------------------------------------------------------------

from passlib.hash import pbkdf2_sha256 as sha
from ceutils import ufilefunc as uff
import os

def version():
    # Function: Return version number.
    return os.path.basename(__file__)[:-3]+' 0.3'


def cons(key=''):
    """ Define constants """
    if key == 'appsdir':
        return os.environ.get('APPSDIR')
    elif key == 'usrsdir':
        return os.path.join(cons('appsdir'),key)
    elif key == 'orgsha':
        return 'pbkdf2-sha256'
    elif key == 'encsha':
        return uff.vsiper(cons('orgsha'))
    return None


def getusrf(usr):
    """ Get usrfile """
    sipusr = uff.vsiper(usr)
    if len(usr) < 4 or not sipusr:
        return 4, "Error: (uf) Invalid userid."
    usrfile = os.path.join(cons('usrsdir'), sipusr)
    return 0, usrfile


def valpwd(pwd, npwd=''):
    """ Validate pwd & npwd """
    if npwd and (len(npwd) < 8 or pwd == npwd or ' ' in npwd):
        return 4, "Error: (vp) Invalid new password."
    if len(pwd) < 8 or ' ' in pwd:
        return 4, "Error: (vp) Invalid password."
    return 0, ''


def valdtls(nam, adr='', phn='', eml=''):
    """ Validate user details """
    sipnam = uff.vsiper(nam,v=2)
    if not sipnam:
        return 4, "Error: (vd) Invalid user name."
    sipadr = uff.vsiper(adr,v=2)
    if adr and not sipadr:
        return 4, "Error: (vd) Invalid user address."
    sipphn = uff.vsiper(phn)
    if phn and not sipphn:
        return 4, "Error: (vd) Invalid user phone."
    sipeml = uff.vsiper(eml,v=3)
    if eml and not sipeml:
        return 4, "Error: (vd) Invalid user email."
    return 0, [sipnam, sipadr, sipphn, sipeml]


def verusr(usr, pwd):
    """ Verify usr & pwd """
    # Verify usrid
    rc, usrfile = getusrf(usr)
    if rc:
        return rc, usrfile
    if not os.path.isfile(usrfile):
        return 8, "Error: (vu) Userid does not exist."
    # Validate pwd
    rc, msg = valpwd(pwd)
    if rc:
        return rc, msg
    with open(usrfile, 'r') as ifl:
        lines = list(ifl)
    ifl.close()
    for i in range(len(lines)-1,-1,-1):
        svline = lines[i]
        dtls = svline.split('|')
        if dtls[2] == 'pwd':   # rectyp
            hash = svline[svline.find('$'):].strip('\n')
            hash = hash.replace(cons('encsha'),cons('orgsha'))
            if sha.verify(pwd, hash):
                return 0, "Passed authentication."
            else:
                return 2, "Authentication failed."


def addusr(usr, pwd, pwc, nam, adr='', phn='', eml='', rmv=False):
    """ Add new user """
    if len(usr) < 4:
        return 8, "Error: (au) Invalid userid."
    rc, usrfile = getusrf(usr)
    if rc:
        return rc, usrfile
    if os.path.isfile(usrfile):
        return 8, "Error: (au) Userid already exists."
    # Validate password
    if pwd != pwc:
        return 4, "Error: (au) Password and confirmation do not match."
    rc, msg = valpwd(pwd)
    if rc:
        return rc, msg
    try:
        hash = sha.hash(pwd).replace(cons('orgsha'),cons('encsha'))
    except:
        return 4, "SevereError: (au) Hash exception - report to administrator."
    # Validate details
    rc, msg = valdtls(nam, adr, phn, eml)
    if rc:
        return rc, msg
    sipnam = msg[0]
    sipadr = msg[1]
    sipphn = msg[2]
    sipeml = msg[3]
    with open(usrfile, 'a') as ofl:
        rc, dt = uff.uniqstr()
        if rc:
            return rc, dt
        ofl.write('|'+dt+'|dtl|'+sipnam+'|'+sipadr+'|'+sipphn+'|'+sipeml+'\n')
        ofl.write('|'+dt+'|pwd|'+hash+'\n')
    ofl.close()
    rc, msg = verusr(usr, pwd)
    if rc:
        return 12, "SevereError: (au) Unexpected - report to administrator."
    else:
        if type(rmv) == bool and rmv:
            os.remove(usrfile)
        return 0, "New user created."


def chgpwd(usr, pwd, npwd):
    """ Change pwd """
    rc, usrfile = getusrf(usr)
    if rc:
        return rc, usrfile
    rc, msg = verusr(usr, pwd)
    if rc:
        return rc, msg
    rc, msg = valpwd(pwd, npwd)
    if rc:
        return rc, msg
    try:
        hash = sha.hash(npwd).replace(cons('orgsha'),cons('encsha'))
        rc, dt = uff.uniqstr()
    except:
        return 4, "SevereError: (cp) Hash exception - report to administrator."
    with open(usrfile, 'a') as ofl:
        ofl.write('|'+dt+'|pwd|'+hash+'\n')
    ofl.close()
    rc, msg = verusr(usr, npwd)
    if rc:
        return 12, "SevereError: (cp) Unexpected - report to administrator."
    else:
        return 0, "Password changed."


def getdtls(usr, pwd):
    """ Get user details """
    rc, usrfile = getusrf(usr)
    if rc:
        return rc, usrfile
    rc, msg = verusr(usr, pwd)
    if rc:
        return rc, msg
    with open(usrfile, 'r') as ifl:
        lines = list(ifl)
    ifl.close()
    for i in range(len(lines)-1,-1,-1):
        dtls = lines[i].strip('\n').split('|')
        if dtls[2] == 'dtl':   # rectyp
            dte = dtls[1]
            nam = uff.vdesiper(dtls[3],v=2)
            adr = uff.vdesiper(dtls[4],v=2)
            phn = uff.vdesiper(dtls[5])
            eml = uff.vdesiper(dtls[6],v=3)
            return 0, [dte,nam,adr,phn,eml]


def upddtls(usr, pwd, nam='', adr='', phn='', eml='', npwd='', npwc='', rmv=False):
    """ Update user details """
    rc, usrfile = getusrf(usr)
    if rc:
        return rc, usrfile
    rc, msg = verusr(usr, pwd)
    if rc:
        return rc, msg
    # Delete routine
    if type(rmv) == bool and rmv:
        os.remove(usrfile)
        return 0, "Account deleted."
    # Validate details
    rc, msg = getdtls(usr, pwd)  # [dte,nam,adr,phn,eml]
    if rc:
        return rc, msg
    if nam != msg[1] or adr != msg[2] or phn != msg[3] or eml != msg[4]:
        dtlupd = True
        rc, msg = valdtls(nam, adr, phn, eml)
        if rc:
            return rc, msg
        sipnam = msg[0]
        sipadr = msg[1]
        sipphn = msg[2]
        sipeml = msg[3]
    else:
        dtlupd = False
    # Validate new password
    if npwd or npwc:
        if npwd != npwc:
            return 4, "Error: (ud) New password and confirmation do not match."
        rc, msg = valpwd(pwd, npwd)
        if rc:
            return rc, msg
        try:
            hash = sha.hash(npwd).replace(cons('orgsha'),cons('encsha'))
        except:
            return 4, "SevereError: (ud) Hash exception - report to administrator."
    if not npwd and not dtlupd:
        return 1, "Nothing to update."
    # Update records
    with open(usrfile, 'a') as ofl:
        if npwd:
            rc, dt = uff.uniqstr()
            if rc:
                return rc, dt
            ofl.write('|'+dt+'|pwd|'+hash+'\n')
        if dtlupd:
            rc, dt = uff.uniqstr()
            if rc:
                return rc, dt
            ofl.write('|'+dt+'|dtl|'+sipnam+'|'+sipadr+'|'+sipphn+'|'+sipeml+'\n')
    ofl.close()
    if npwd:
        rc, msg = verusr(usr, npwd)
        if rc:
            return 12, "SevereError: (ud) Unexpected - report to administrator."
    return 0, "Details updated."


def main():
    nam = 'virbcal'
    adr = 'qc'
    phn = '09234924240'
    eml = '@gmail.com'
    usr = 'usrTe$t&'
    pwd = 'pwdTe$t@'
    rmv = True
    rc, msg = addusr(nam,usr,pwd,adr=adr,phn=phn,eml=eml,rmv=rmv)
    if rc:
        print(msg)


if __name__ == '__main__':
    main()
