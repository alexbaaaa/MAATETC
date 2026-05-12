#!/usr/bin/env python3
import matplotlib
#----- IMPORTANTE PARA WEB ---
matplotlib.use('Agg')
#---------------
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import PySimpleGUI as sg # PySimpleGUIWeb PySimpleGUI
# import io
# import os
#matplotlib.use('TkAgg')

#--------------------------------------------------------------------

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as p
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

from scipy import interpolate
import sys, getopt
import pathlib
import random
import os
from astropy.modeling.physical_models import BlackBody
from astropy import units as u

#--------------------------------------------------------------------
mpl.rcParams['image.interpolation'] = 'nearest'
mpl.rcParams['image.origin'] = 'lower'
mpl.rcParams['image.aspect'] ='equal'
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.size'] = 12
mpl.rcParams['lines.linewidth'] = 1
#--------------------------------------------------------------------

cspeed = 2.99792458e18 # A/s
hplanck = 6.626068e-27 # cm2 g / s  ==  erg s

telearea = 73e4 # GTC effective collecting area in cm2

# ----- Cambio de la ruta ------

maatetcdir = str( os.getcwd() + "/app/services/etc/" )

# maatetcdir = str(pathlib.Path('maatetc_gui.py').parent.absolute()) + "/"
# print(maatetcdir)


#--------------------------------------------------------------------

# Not for WEB
# sg.theme('SystemDefault')
# sg.set_options(element_padding=(0, 0))


def draw_figure(element, figure):
    """
    Draws the previously created "figure" in the supplied Image Element

    :param element: an Image Element
    :param figure: a Matplotlib figure
    :return: The figure canvas
    """


    plt.close('all')        # erases previously drawn plots
    canv = FigureCanvasTkAgg(figure)
    buf = io.BytesIO()
    canv.print_figure(buf, format='png')
    if buf is None:
        return None
    buf.seek(0)
    element.update(data=buf.read())
    return canv

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

#--------------------------------------------------------------------
# From Chris Benn signal.f
# Zenith extinction for La Palma, taken from the ING Observers' Guide
# = constant (wavelength-dependent) gas + variable (grey) dust (= 0.05)
# Used for version 11.0 onwards.
# The values for other sites are similar.  For CTIO, Frogel 1998,
# PASP 110 200 gives .11, .06 and .09 in J, H and K.
#

def extinction(wv,am):
  #extin = np.array([0.55,0.25,0.15,0.09,0.06,0.05]) # Chris benn
  extin0 = np.array([0.4554,0.2175,0.1020,0.0575,0.0157,0.0087,0.0087]) # WEAVE
  rep = interpolate.interp1d( np.array([3600,4300,5500,6500,8200,9500,10000]) , extin0 )
  newval = rep(wv)
  oops = 10.**(-0.4*float(am)*newval)
  return oops

#--------------------------------------------------------------------
# Identify photom band and index
# This is not used yet 20210803

def waveband(band):
  bandname = np.array(['U','B','V','R','I','Z'])
  wind = np.where(bandname==band.upper())[0][0]
  wave = np.array([3600,4300,5500,6500,8200,9500])
  return wind,wave[ind]

#--------------------------------------------------------------------
# Moon contribution to sky background (in mag/arcsec2)
# Dark values and sky spectrum from Chris Benn
# sky spectrum in microJy/arcsec2

def getsky(wv,moon):
  dark   = np.array([22.0,22.7,21.9,21.0,20.0,18.8,18.8])
# Moon contribution to sky background (in mag/arcsec2)
  grey   = np.array([2.1,1.1,0.4,0.3,0.2,0.2,0.2])
  bright = np.array([5.0,3.2,1.8,1.0,0.7,0.7,0.7])
  if moon=='grey' or moon=='gray'  : dark = dark-grey
  if moon=='bright' : dark = dark-bright
  repm = interpolate.interp1d(np.array([3600,4300,5500,6500,8200,9500,10000]),dark)
  moonlight = repm(wv)

  #x,y = np.loadtxt(maatetcdir+'ORM_nightsky_all.txt',unpack=True)
  #reps = interpolate.interp1d(x,y)
  #spsk = reps(wv)

  # Sky spectrum needs to be scaled in broad band chunks
  # Do NOT scale in spectral pixels to avoid spiky sky emission lines 

  return moonlight

#--------------------------------------------------------------------
# Reads required grating efficiency and interpolates to the dispersion
# Returns efficiency as function of new wavelength, and the value of dispersion

def getgrating(grating):
  gratings = np.array(['R300B','R300R','R500B','R500R','R1000B','R1000R','R2000B','R2500U','R2500V','R2500R','R2500I'])
  dispersion = np.array([2.60,4.02,1.87,2.58,1.13,1.40,0.46,0.33,0.44,1.56,1.73])
  #Osiris longslit : dispersion = np.array([4.96,7.74,3.54,4.88,2.12,2.62,0.62,0.86,0.80,1.04,1.36])
  igr = np.where(gratings==grating)[0][0]
  wv,eff = np.loadtxt(maatetcdir+'efficiency/'+gratings[igr]+'.txt',unpack=True,usecols=(0,1))
  rep = interpolate.interp1d(wv,eff)
  wvi = np.arange(wv[0],wv[-1],dispersion[igr])
  effi = rep(wvi)
  return wvi,effi,dispersion[igr]

#--------------------------------------------------------------------
# General function to extrapolate wavelength range ends
# This patches the possible mismatch in wavelength ranges from different variables

def extend(x,y,wv):
  if x[0]>wv[0] : 
    x = np.concatenate(([wv[0]],x))
    y = np.concatenate(([0],y))
  if x[-1]<wv[-1] : 
    x = np.concatenate((x,[wv[-1]]))
    y = np.concatenate((y,[0]))
  return(x,y)

#--------------------------------------------------------------------
# Generate SED template for target

def getsed(sedtemplate,redz):  
  if sedtemplate=='ones' : 
    flam0 = np.ones(len(wv)) # erg/cm2/s/A , normalized spectrum to be scaled with fluxval0
  elif sedtemplate.split()[0]=='blackbody' :
    temp = float(sedtemplate.split()[1]) 
    bt = BlackBody(temp*u.K, scale=1.*u.Unit('erg / (cm2 s AA sr)'))
    flam0 = bt(wv * u.AA).value
  else :
    x,y = np.loadtxt(maatetcdir+'seds/'+sedtemplate+'.txt',unpack=True)
    x = (1+redz)*x
    x,y = extend(x,y,wv)
    rep = interpolate.interp1d(x,y)
    flam0 = rep(wv)
  return flam0

#--------------------------------------------------------------------
# This function implements the computations made by Paco to scale the old-to-new Osiris
# Takes into account three component changes:
#   (i) new CCD quantum efficiency
#  (ii) the removal of M3 after relocation from Nasmyth to Cassegrain
# OUTDATED (iii) the MAAT efficiency in the design computed by Robert Content
# (iii) the MAAT efficiency in the first design from Winlight 20211011 

def old2newfac(wv):
  # wavelength and quantum efficiency of new CCD "deepdepletion_multi2"
  wnew = 10*np.array([ 300.6502,  331.2442,  359.4971,  370.6928,  378.7841,  389.2324,
        398.5372,  409.4083,  429.636 ,  441.7027,  467.3995,  490.361 ,
        509.4329,  530.0577,  549.1202,  570.5182,  599.6917,  614.0843,
        644.4245,  678.2694,  700.4447,  725.7345,  744.0247,  757.6469,
        775.9435,  793.0764,  810.604 ,  828.5303,  842.9545,  859.7242,
        875.3294,  888.213 ,  900.3148,  915.938 ,  940.1554,  959.6883,
        982.7231, 1001.0658, 1023.6836, 1036.1558, 1051.3489, 1067.3101,
       1083.6554, 1099.9992])
  qenew = np.array([1.64509e-01, 3.51165e-01, 5.46141e-01, 6.59807e-01, 7.62386e-01,
       8.36311e-01, 8.79738e-01, 9.10225e-01, 9.17595e-01, 9.12036e-01,
       8.91674e-01, 8.86101e-01, 8.78686e-01, 8.75889e-01, 8.80489e-01,
       8.84161e-01, 8.96141e-01, 9.01670e-01, 9.14574e-01, 9.23777e-01,
       9.28373e-01, 9.31116e-01, 9.28323e-01, 9.23686e-01, 9.12574e-01,
       8.96843e-01, 8.73717e-01, 8.38576e-01, 8.03439e-01, 7.54437e-01,
       7.01738e-01, 6.46271e-01, 5.95425e-01, 5.19621e-01, 4.00370e-01,
       3.00532e-01, 2.00690e-01, 1.30429e-01, 6.66320e-02, 3.98150e-02,
       1.66920e-02, 6.50700e-03, 2.79200e-03, 9.24000e-04])
  qenewi = interpolate.interp1d(wnew,qenew)(wv)

  # (i) wavelength and quantum efficiency of old CCD "OSIRIS-QE_old"
  wold = 10*np.array([ 350., 400., 450., 500., 550., 600., 650., 700., 750., 800., 850., 900., 950., 1000.])
  qeold = np.array([0.2, 0.4, 0.55, 0.63, 0.72, 0.77, 0.85, 0.87, 0.86, 0.85, 0.8, 0.6, 0.37, 0.17])
  qeoldi = interpolate.interp1d(wold,qeold)(wv)

  # (ii) wavelength and efficiency of GTC M3 "Aluminium_GTC"
  w3 = 10*np.array([ 300., 350., 400., 450., 500., 550., 600., 650., 700., 750., 775., 800., 825., 850., 875., 900., 925., 950., 1000., 1200.])
  qe3 = np.array([9.208e-01, 9.205e-01, 9.194e-01, 9.175e-01, 9.162e-01, 9.157e-01, 9.117e-01, 9.057e-01, 8.977e-01, 8.862e-01, 8.773e-01, 8.676e-01, 8.657e-01, 8.677e-01, 8.744e-01, 8.908e-01, 9.075e-01, 9.243e-01, 9.402e-01, 9.637e+03])
  qe3i = interpolate.interp1d(w3,qe3)(wv)

  # (iii) wavelength and efficiency of MAAT "IFU_efficiency_averg55nm" from Robert Content first guess
  #wifu = np.array([3600., 4000., 4500., 5000., 5500., 6000., 6500., 7000., 7500., 8000., 8500., 9000., 9500.,10000.])
  #fudgefactor = 1.0 # to artifically reduce MAAT efficiency
  #qifu = fudgefactor * np.array([0.939, 0.9537, 0.9506, 0.9376, 0.9205, 0.913, 0.9191, 0.9177, 0.9088, 0.9066, 0.9067, 0.9111, 0.9075, 0.9075])
  #qifui = interpolate.interp1d(wifu,qifu)(wv)

  # wavelength and efficiency of MAAT Winlight 20211011 
  # 2S4D with spherical slit mirrors and 3S3D with toroidal slit mirrors
  
  # I have added the variable maatetcdir
  wifu, qifu1,qifu2,qifu3 = np.loadtxt(maatetcdir + 'efficiency/MAAT_trans_Winlight_20211011_1S5D_2S4D_3S3D.txt',unpack=True)
  qifu = qifu1 # choose optimal transmission case as default
  qifui = interpolate.interp1d(wifu,qifu)(wv)

  # global efficiency old-to-new for MAAT and for longslit
  return (qenewi*qifui) / (qeoldi*qe3i) , (qenewi) / (qeoldi*qe3i)

#--------------------------------------------------------------------
# Read SED template and flux scale to input fluxval

def scaleflux(fluxtype,fluxval,refwv,wvind,fwhmA,disp,sedtemplate,redz,msky):

# Input spectrum normalized to unity at refwv; this example is constant Flambda 
  flam0 = getsed(sedtemplate,redz)
  if fluxtype == 'emline' : flam0 = getsed('ones',redz) # temporal patch until a better idea for scaling emlines, 
                                                   # this formula below is sentitive to em.lines spikes  flam = fluxval0 * flam0/flam0[wvind]

# find index where wv is closest to wavelength refwv of requested fluxval0 
  wvind = np.where(abs(wv-refwv)==abs(wv-refwv).min())[0][0] 

# Scale normalized SED input spectrum (flam0) to requested input fluxval
# Interprets fluxval as ABmag or as (SB)Flambda depending on value wrt (arbitrary) fluxval0ref:

  fluxval0ref = 0.1 # reference value to interpret fluxval as ABmag or as (SB)Flambda

  fluxval0 = fluxval    

  if fluxval0 > fluxval0ref :            # fluxval0 is in ABmag
    # Convert flam0 [ergs/cm2/s/A] to AB mag, then scale to requested input fluxval0 at refwv, and then back to Flambda
    abmag = -2.5*np.log10(flam0) -  2.402 - 5.0 * np.log10(wv)
    abmag = abmag + fluxval0-abmag[wvind]
    flam = 10.**(-0.4*(abmag+2.402+5.0*np.log10(wv)))     
    if fluxtype == 'emline' : 
      print('!!!***###***!!!  Why would you give emission line flux in magnitudes? This is a bad mistake. \n',\
      'If code does not break, results will be definitely WRONG !!!***###***!!! ')
  elif fluxval0 <= fluxval0ref:          # fluxval0 is in (SB)Flambda
    if fluxtype == 'emline' : 
      npixspec = 3.25 # fwhm of spectral resolution is assumed to be 3.25 spectral pixels, according to Robert Content
      fluxval0 = ( fluxval / np.sqrt(fwhmA**2+(npixspec*disp)**2) ) * disp # compute emline intensity per spectral pixel; # use quadratic width (fwhmA,resolution).
      #fluxval0 = ( fluxval / max(fwhmA,npixspec*disp) ) * disp # compute emline intensity per spectral pixel; # choose resolution element if fwhmA is less than resolution element.
    flam = fluxval0 * flam0/flam0[wvind] # normalizes sed flam0 at wvind and scales to requested input flux
  else:
    print("It is IMPOSSIBLE in this universe that this sentence is ever printed!")

# the sky is in mag/arcsec2, so just transform to Flambda; mksy is in mag/arcsec2 so flamsk is in ergs/cm2/s/A/arcsec2
  flamsk = 10.**(-0.4*(msky+2.402+5.0*np.log10(wv))) 
  
  return flam, flamsk

#-------------------------------------------------------------------------------------------------
# Computes fraction of light within a given geometry for gaussian and moffat 2D functions
# As an option plotPSF, it plots the 2d PSF and the MAAT and SLIT modes geometries

def moffatgauss(fwhm,nsigmas,slitwidth,plotPSF) : # number of +-sigmas to integrate along longslit (ref. MAAT)
	b = 3 # Moffat b parameter
	scale = 10 # factor to convert input arcsec to model pixels; 1 arcsec = 10 model pixels
	fwhm = fwhm*scale # fwhm in pixels; both G and M have the same fwhm
	width = 10 # how many fwhm has the simulated 2D array on a side
	nx, ny = int(width*fwhm+0.5)+1 , int(width*fwhm+0.5)+1
	xc , yc = int(0.5*width*fwhm) , int(0.5*width*fwhm)
	m = np.zeros((nx,ny))
	g = np.zeros((nx,ny))
	xy = np.zeros((nx,ny))
	sigma = fwhm/2.3548
	a = fwhm / (2.*np.sqrt(2**(1./b)-1.))
	k=-1
	for i in range(nx) : 
	  k +=1 
	  for j in range(ny) : 
	    r = np.sqrt( (i-xc)**2 + (j-yc)**2 )
	    m[j,i] = (1./(1. + (r/a)**2))**b
	    g[j,i] =  np.exp(-0.5*(r/sigma)**2)
	    xy[j,i] = r
	m = m / m.sum().sum()
	g = g / g.sum().sum()
	dis = xy

	#------------------------------------------------------------------------------------  
	# computes relative fraction of G or M model within different geometries
	
	dd = int(np.ceil(nsigmas*sigma))
	slithalf = int(np.ceil(0.5*slitwidth*scale))
	
	gsum0 = g[ np.where(dis<=dd) ].sum() / g.sum() # circular aperture of radius nsigmas*sigma
	msum0 = m[ np.where(dis<=dd) ].sum() / m.sum() #   

	gslit3 = g[ yc-dd:yc+dd , xc-slithalf:xc+slithalf ].sum() / g.sum()  # longslit of full width slit and length nsigmas*(2*dd)
	mslit3 = m[ yc-dd:yc+dd , xc-slithalf:xc+slithalf ].sum() / m.sum()  # 

	gsum = g[ yc-dd:yc+dd , xc-dd:xc+dd ].sum() / g.sum() # square aperture of side nsigmas*sigma
	msum = m[ yc-dd:yc+dd , xc-dd:xc+dd ].sum() / m.sum() #    

	gslit = g[ : , xc-slithalf:xc+slithalf ].sum() / g.sum() # longslit of full width slit and full length
	mslit = m[ : , xc-slithalf:xc+slithalf ].sum() / m.sum() # 

	#------------------------------------------------------------------------------------  
	if plotPSF :
	  fig1 = p.figure(10)
	  fig = p.figure()
	  p.clf()
	  ax = fig.add_subplot(111)
	  extent = [-xc/scale,xc/scale,-yc/scale,yc/scale]
	  ims = np.sqrt(np.sqrt(g))
	  im = ax.imshow(ims,extent=extent,cmap='gray_r',vmin=ims.min(),vmax=ims.max())
	  #cb = p.colorbar(im)
	  ax.set_title('fwhm='+str(fwhm/scale)+', slitwidth='+str(slitwidth)+', Nsigma='+str(nsigmas))
	  ax.set_xlabel('arcsec')
	  ax.set_ylabel('arcsec')
	  rc = Rectangle((-slithalf/scale,-dd/scale), slitwidth, 2*dd/scale, color='c', lw=0.5, fill=False)
	  ax.add_patch(rc)
	  c = Circle((0, 0), dd/scale , color='r', lw=0.5, fill=False)
	  ax.add_patch(c)
	  p.draw()
	
	# returns are temporarily set to these, but other could be chosen
	return gsum0 , gslit3
	

#--------------------------------------------------------------------
# This makes it possible to loop thru fluxval,seeing,longslitw

def doloop(compute,value,psf,fluxtype,extin,disp,breadth,toverhd,sedtemplate,redz,refwv,wvind,msky,fluxval,fwhmA,seeing,area,longslitw):
  
  plotPSF = False
  checkplot = False

  if psf=='pointsource':
    seeing_fwhm = seeing 
    seeing_sigma = seeing_fwhm/2.355
    seeing_sigmas = 2 # How many +-sigmas in total to integrate; max value is aperture.max()
    
    signalfac , slitfac = moffatgauss( seeing_fwhm , seeing_sigmas , longslitw , plotPSF )
    
    signalarea = np.pi*(seeing_sigmas*seeing_sigma)**2  # area (arcsec2) where pointsource signal is integrated  
    signalareaslit = longslitw*(2*seeing_sigmas*seeing_sigma) # area (arcsec2) where pointsource signal thru slit is integrated
    
    signalarea_pix = signalarea / 0.127**2          # in CCD pixels, used in RON below
    signalareaslit_pix = signalareaslit / 0.127**2  # in CCD pixels, used in RON below

    # a patch to use in generalized formula below
    signalarea_obj = 1     # for point sources do not use integration area for object (only for RON2)
    signalareaslit_obj = 1 # idem for slit
    
  if psf=='extended':
    signalarea = area**2            # area of square box of side 'area' where signal is integrated
    signalareaslit = longslitw*area # area interpreted as slit length

    signalfac = 1.0
    slitfac = 1.0
    
    signalarea_obj = signalarea
    signalarea_pix = signalarea / 0.127**2  # in CCD pixels, used in RON below

    signalareaslit_obj = signalareaslit
    signalareaslit_pix = signalareaslit / 0.127**2  # in CCD pixels, used in RON below
  
  # CCD:
  # dark current and readout noise
  dc = 3/3600  # e/pixel/s # CCD guide gives 3 e/pixel/hour   #  
  ron = 3 # 3e reading at 50kHz 
  RON2 = ron**2 * signalarea_pix  # this is what enters into the formula below
  RON2slit = ron**2 * signalareaslit_pix  # this is what enters into the formula below
  
  # Get scaled SED and effect all factors
   
  flam, flamsk = scaleflux(fluxtype,fluxval,refwv,wvind,fwhmA,disp,sedtemplate,redz,msky)
  
  # spectral pixels to sum: 
  # if breadth>disp then it assumes that the SN is computed in a large (larger than the dispersion) spectral breadth
  # if breadth<=disp then it assumes that the SN is computed in a dispersion element
  specpixsA = np.max([disp,breadth])

  #
  Sobj     = flam   * ( wv / (cspeed*hplanck) ) * eff     * extin * telearea * specpixsA * signalarea_obj*signalfac
  Ssky     = flamsk * ( wv / (cspeed*hplanck) ) * eff             * telearea * specpixsA * signalarea               
  
  Sobjslit = flam   * ( wv / (cspeed*hplanck) ) * effslit * extin * telearea * specpixsA * signalareaslit_obj*slitfac 
  Sskyslit = flamsk * ( wv / (cspeed*hplanck) ) * effslit         * telearea * specpixsA * signalareaslit 
  
  if compute=='SN' : 
    Texpo = value
    SN     = Sobj    *Texpo     / np.sqrt( Sobj    *Texpo     + Ssky    *Texpo     + dc**2*Texpo     + RON2 ) # from VIMOS ETC

    flamnoisy = np.array([ flam[i] * (1 + random.normalvariate(0.0,1.0) / SN[i]) for i in range(len(wv)) ])

    Texposlit = Texpo - toverhd
    SNslit = Sobjslit*Texposlit / np.sqrt( Sobjslit*Texposlit + Sskyslit*Texposlit + dc**2*Texposlit + RON2slit )
  
  if (compute=='SN') & checkplot:
    p.figure()
    p.clf()
    p.subplot(121)
    p.plot(wv,Sobj,'b-')
    p.plot(wv,Ssky,'b:')
    p.plot(wv,Sobjslit,'r-')
    p.plot(wv,Sskyslit,'r:')
    p.title('Signal MAAT SLIT Object Sky, '+str(fluxval)+', '+str(seeing)+', '+str(longslitw), fontsize=10)
    p.ylabel('Signal (photons/s/pixel)')
    p.subplot(122)
    p.plot(wv,SN,'b-')
    p.plot(wv,SNslit,'r-')
    p.xlabel('wavelength')
    p.ylabel('S/N')
    p.legend(('MAAT','SLIT'),loc=0)

  if compute=='texpo' :     
    SN = value
    Texpo = (  SN**2 * (Sobj+Ssky+dc**2) + np.sqrt( SN**4 * (Sobj+Ssky+dc**2) + 4*SN**2*Sobj**2*RON2 )  ) / (2*Sobj**2)
    flamnoisy = np.array([ flam[i] * (1 + random.normalvariate(0.0,1.0) / SN) for i in range(len(wv)) ])

  if compute=='SN' : return SN, SNslit, flam, flamnoisy, specpixsA
  if compute=='texpo' : return Texpo, flam, flamnoisy, specpixsA


#--------------------------------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------


def run_etc(values,text_elem,image_element):

    fluxtype=values['fluxtype']
    fluxval=float(values['fluxval'])
    refwv=float(values['refwv'])
    sedtemplate=values['sedtemplate']
    moon=values['moon']
    grating=values['grating']
    compute=values['compute']
    seeing=float(values['seeing'])
    area=float(values['area'])
    psf=values['psf']
    texpoSN=float(values['texpoSN'])
    breadth=float(values['breadth'])

    if len(values['fwhmA']) == 0 : 
      fwhmA = 0
    else:
      fwhmA = float(values['fwhmA'])

    if len(values['redz']) == 0 : 
      redz = 0
      print('Will use redshift=0')
    else:
      redz = float(values['redz'])

    if len(values['toverhd']) == 0 : 
      toverhd = 300
      print('Will use overhead time = 300 s (only for longslit calculations)')
    else:
      toverhd = float(values['toverhd'])

    if len(values['airmass']) == 0 : 
      airmass = 1
      print('Will use airmass=1')
    else:
      airmass=float(values['airmass']) 
    
    if len(values['breadth']) == 0 : 
      breadth = 0
      print('Will use breadth=0, i.e., compute in disp Angstroms')
    else:
      breadth=float(values['breadth']) 

    global wv, eff, effslit
    
    #--------------------------------------------------------------------
    #

    if compute=='SN' : Texpo = texpoSN
    if compute=='texpo' : SN = texpoSN
    
    #--------------------------------------------------------------------
    #-------------------------
    # INSTRUMENT: 
    #  slit+IFU , Grism , CCD
    #-------------------------
    
    # Read grating numbers and correct from old-to-new system factor (CCD, M3, MAAT eff)
    # Note that eff contains the end-to-end global efficiency of the system, according to GTC manual (see above).
    wv, efff, disp = getgrating(grating)
    eff = efff * old2newfac(wv)[0]
    effslit = efff * old2newfac(wv)[1]

    #--------------------------------------------------------------------
    # compute various reference wavelengths

    iefmx = np.where(eff==eff.max())[0][0]
    wveffmax = wv[iefmx]                 # wavelength at max grating efficiency
    wveffwv = (wv*eff).sum()/eff.sum()   # efficiency-weighted wavelength
    wvcen = (wv[-1]+wv[0])/2             # central wavelength
    iefwv = np.where(wv<=wveffwv)[0][-1]
    iwvcen = np.where(wv<=wvcen)[0][-1]
    iwvinf = np.where(wv<=refwv)[0][-1]
    wvind = np.where(abs(wv-refwv)==abs(wv-refwv).min())[0][0] 

    #--------------------------------------------------------------------
    # simple check that input reference wavelength is inside grating range

    if ((refwv<wv[0]) or (refwv>wv[-1])):
      print('\n\
           --------------------------------------------------------------\n\
           *** WARNING: reference wavelength is otuside grating range ***\n',\
             '         ',refwv, 'is not within [',wv[0],',',wv[-1],']\n',\
             '          *** BAILING OUT *** \n',\
             '          --------------------------------------------------------------')
      sys.exit()


    #--------------------------------------------------------------------
    #-------------------------
    # Extinction and Sky:
    #  SB
    #-------------------------

    extin = extinction(wv,airmass)

    msky = getsky(wv,moon) # Sky brightness in mag/arcsec**2, interpolated from UBVRIZ to grating range


    #--------------------------------------------------------------------
    # NO ACCOUNT yet for in-CCD binning

    #--------------------------------------------------------------------
    #-------------------------
      
    fluxrange = np.array([fluxval])
    seeingrange = np.array([seeing])
    slitrange = np.array([0.6])
      
    y1 = np.zeros((len(fluxrange),len(seeingrange),len(slitrange)))
    y2 = np.zeros((len(fluxrange),len(seeingrange),len(slitrange)))
    y3 = np.zeros((len(fluxrange),len(seeingrange),len(slitrange)))
    y4 = np.zeros((len(fluxrange),len(seeingrange),len(slitrange)))
     
    k1 = -1
    for fluxval in fluxrange:
      k1 += 1
      k2 = -1
      for seeing in seeingrange:
        k2 += 1
        k3 = -1
        for longslitw in slitrange: 
          k3 += 1
          if (compute=='SN') : 
            SN , SNslit, flam, flamnoisy, specpixsA = doloop(compute,Texpo,psf,fluxtype,extin,disp,breadth,toverhd,sedtemplate,redz,refwv,wvind,msky,fluxval,fwhmA,seeing,area,longslitw)
            y1[k1,k2,k3] , y2[k1,k2,k3] , y3[k1,k2,k3] , y4[k1,k2,k3] = SN[iefwv] , SNslit[iefwv] , flam[iefwv], flamnoisy[iefwv]
            if psf=='pointsource' :
              text_elem.update(value='Integrating a pointsource of fwhm %.2f arcsec\n \
              S/N resulting from exposure time %.1f sec \n \
              %.2f at wavelength of maximum efficiency %.1f\n \
              %.2f at efficiency weighted wavelength %.1f\n \
              %.2f at range mid wavelength %.1f\n \
              %.2f at input reference wavelength %.1f' %(seeing, Texpo, SN[iefmx], wveffmax, SN[iefwv], wveffwv, SN[iwvcen], wvcen, SN[iwvinf], refwv))
            elif psf=='extended':
              text_elem.update(value='Integrating in square box of side %.2f arcsec\n \
              S/N resulting from exposure time %.1f sec \n \
              %.2f at wavelength of maximum efficiency %.1f\n \
              %.2f at efficiency weighted wavelength %.1f\n \
              %.2f at range mid wavelength %.1f\n \
              %.2f at input reference wavelength %.1f' %(area, Texpo, SN[iefmx], wveffmax, SN[iefwv], wveffwv, SN[iwvcen], wvcen, SN[iwvinf], refwv))
          if (compute=='texpo') : 
            Texpo, flam, flamnoisy, specpixsA = doloop(compute,SN,psf,fluxtype,extin,disp,breadth,toverhd,sedtemplate,redz,refwv,wvind,msky,fluxval,fwhmA,seeing,area,longslitw)
            y1[k1,k2,k3] , y3[k1,k2,k3] , y4[k1,k2,k3] = Texpo[iefwv] , flam[iefwv], flamnoisy[iefwv]
            if psf=='pointsource' :
              text_elem.update(value='Integrating a pointsource of fwhm %.2f arcsec\n \
              Exposure time (sec) resulting from S/N %.1f \n \
              %.2f at wavelength of maximum efficiency %.1f\n \
              %.2f at efficiency weighted wavelength %.1f\n \
              %.2f at range mid wavelength %.1f\n \
              %.2f at input reference wavelength %.1f' %(seeing, SN, Texpo[iefmx], wveffmax, Texpo[iefwv], wveffwv, Texpo[iwvcen], wvcen, Texpo[iwvinf], refwv))
            elif psf=='extended':
              text_elem.update(value='Integrating in square box of side %.2f arcsec\n \
              Exposure time (sec) resulting from S/N %.1f \n \
              %.2f at wavelength of maximum efficiency %.1f\n \
              %.2f at efficiency weighted wavelength %.1f\n \
              %.2f at range mid wavelength %.1f\n \
              %.2f at input reference wavelength %.1f' %(area, SN, Texpo[iefmx], wveffmax, Texpo[iefwv], wveffwv, Texpo[iwvcen], wvcen, Texpo[iwvinf], refwv))

    from datetime import datetime
    dtstr = datetime.now().strftime("%Y%m%d%H%M%S")

    if (compute=='SN') : 
      f = open('SN_'+dtstr+'.txt','w')
      print('check0')
      f.write('# '+fluxtype+' '+str(fluxval)+' '+str(refwv)+' '+sedtemplate+' '+moon+' '+grating+' '+compute+' '+str(seeing)+' '+str(area)+' '+psf+' '+str(texpoSN)+' '+str(breadth)+' '+str(fwhmA)+' '+str(redz)+' '+str(airmass)+'\n' ) 
      print('check1')
      [ f.write(str(wv[i])+' '+str(flam[i])+' '+str(flamnoisy[i])+' '+str(SN[i])+'\n') for i in range(len(wv))]
    if (compute=='texpo') : 
      f = open('Texpo_'+dtstr+'.txt','w')
      f.write('# '+fluxtype+' '+str(fluxval)+' '+str(refwv)+' '+sedtemplate+' '+moon+' '+grating+' '+compute+' '+str(seeing)+' '+str(area)+' '+psf+' '+str(texpoSN)+' '+str(breadth)+' '+str(fwhmA)+' '+str(redz)+' '+str(airmass)+'\n' ) 
      [ f.write(str(wv[i])+' '+str(flam[i])+' '+str(flamnoisy[i])+' '+str(Texpo[i])+'\n') for i in range(len(wv))]
    f.close()

    fig = matplotlib.figure.Figure(figsize=(7, 7), dpi=100)
    ax=fig.add_subplot(211)
    if (compute=='SN') : 
      if fluxtype=='continuum': 
        ax.plot(wv, SN, 'k-', lw=0.5)

        # Obtener índice de la longitud de onda más cercana a refwv
        idx_ref = np.abs(wv - refwv).argmin()

        # Obtener valor Y en esa longitud de onda
        y_ref = SN[idx_ref]

        # Limitar eje Y al doble del valor de referencia
        ax.set_ylim(0, y_ref * 2)

      if fluxtype=='emline':
        ax.plot([wv[wvind],wv[wvind]],[0,SN[wvind]],'-',lw=1)
        ax.axhline(0)
      ax.set_ylabel('S/N in '+str(specpixsA)+r' $\mathrm{\AA}$')
      if psf=='pointsource' : ax.set_title(sedtemplate+', '+grating+', mag['+str(refwv)+']='+str(fluxval)+'. Texpo='+str(int(Texpo))+',  '+psf+' '+str(seeing)+'"',fontsize=10)
      if psf=='extended' : ax.set_title(sedtemplate+', '+grating+'. Flux['+str(refwv)+']='+str(fluxval)+'. Texpo='+str(int(Texpo))+',  '+psf+' '+str(area)+'"',fontsize=10)


    if (compute=='texpo') : 
      if fluxtype=='continuum': 
          ax.plot(wv, Texpo, 'k-', lw=0.5)

          # Obtener índice de la longitud de onda más cercana a refwv
          idx_ref = np.abs(wv - refwv).argmin()

          # Obtener valor Y en esa longitud de onda
          y_ref = Texpo[idx_ref]

          # Limitar eje Y al doble del valor de referencia
          ax.set_ylim(0, y_ref * 2)

      if fluxtype=='emline':
        ax.plot([wv[wvind],wv[wvind]],[0,Texpo[wvind]],'-',lw=1)
        ax.axhline(0)
      ax.set_ylabel('exposure time (s)')
      if psf=='pointsource' : ax.set_title(sedtemplate+', '+grating+', mag['+str(refwv)+']='+str(fluxval)+'. S/N='+str(int(SN))+',  '+psf+' '+str(seeing)+'"',fontsize=10)
      if psf=='extended' : ax.set_title(sedtemplate+', '+grating+'. Flux['+str(refwv)+']='+str(fluxval)+'. S/N='+str(int(SN))+',  '+psf+' '+str(area)+'"',fontsize=10)
    ax.grid(ls=':',color='k',lw=0.5)

    ax1=fig.add_subplot(212)
    flam = flam*1e17
    flamnoisy = flamnoisy*1e17
    ax1.plot(wv,flamnoisy,'0.7',lw=1)
    ax1.plot(wv,flam,'k-',lw=1)
    siglim = flamnoisy.mean()-flamnoisy[flamnoisy<flamnoisy.mean()].mean()
    ax1.set_ylim(flamnoisy.mean()-4*siglim,flamnoisy.mean()+4*siglim) # flamnoisy.mean()+5*siglim) # flamnoisy.max())
    ax1.set_ylabel(r'$\mathrm{F_{\lambda}\ (10^{-17} erg s^{-1} cm^{-2} \AA^{-1}}$)')
    ax1.set_xlabel(r'wavelength ($\mathrm{\AA}$)')

    #By Alejandro -----------
    return fig, text_elem
    #------------

    # This method doesn't work for the web
    #draw_figure(image_element, fig)



#--------------------------------------------------------------------
#    [sg.Text('SED template:',size=(30, 1), pad=((5, 0), 0)), sg.OptionMenu(values=('ones','blackbody','KNequatorial','KNpolar','pickles_O5V','pickles_B0V','pickles_A0V','pickles_F0V','pickles_G0V','pickles_K0V','pickles_M0V'),default_value='pickles_G0V', size=(10, 1),text_color='black',key='sedtemplate')],

def gui():
#Set-up GUI

    global fluxval, refwv, fwhmA, sedtemplate, redz, moon, airmass, grating, compute, texpoSN, psf, seeing, area, breadth
    
    sednames = [ item[:-4] for item in os.listdir(os.getcwd()+'/seds/') if item[-4:]=='.txt' ]
    sednames.sort(key=str.lower)

    left_col = [
    [sg.Text('fluxtype:', size=(30, 1), pad=((5, 0), 0)), sg.OptionMenu(values=('continuum', 'emline'), default_value='continuum', size=(10, 1),text_color='black',key='fluxtype')],
    [sg.Text('Flux (Magnitudes or ergs/cm2/s/A):',size=(30, 1), pad=((5, 0), 0)), sg.Input(size=(10, 1),background_color='white', text_color='black',key='fluxval')],
    [sg.Text('Reference wavelength (A):',size=(30, 1), pad=((5, 0), 0)), sg.Input(size=(10, 1),background_color='white', text_color='black',key='refwv')],
    [sg.Text('FWHM (A):',size=(30, 1), pad=((5, 0), 0)), sg.Input(size=(10, 1),background_color='white', text_color='black',key='fwhmA')],
    [sg.Text('SED template:',size=(30, 1), pad=((5, 0), 0)), sg.OptionMenu(values=(sednames),default_value='pickles_G0V', size=(10, 1),text_color='black',key='sedtemplate')],
    [sg.Text('Redshift:',size=(30, 1), pad=((5, 0), 0)), sg.Input(size=(10, 1),background_color='white', text_color='black',key='redz')],
    [sg.Text('Moon:',size=(30, 1), pad=((5, 0), 0)), sg.OptionMenu(values=('dark', 'grey','bright'), default_value='dark', size=(10, 1),text_color='black',key='moon')],
    [sg.Text('Airmass:',size=(30, 1), pad=((5, 0), 0)), sg.Input(size=(10, 1),background_color='white', text_color='black',key='airmass')],
    [sg.Text('Grating:',size=(30, 1), pad=((5, 0), 0)), sg.OptionMenu(values=('R300B','R300R','R500B','R500R','R1000B','R1000R','R2000B','R2500U','R2500V','R2500R','R2500I'),default_value='R1000R', size=(10, 1),text_color='black',key='grating')],
    [sg.Text('Compute mode:',size=(30, 1), pad=((5, 0), 0)), sg.OptionMenu(values=('SN', 'texpo'), default_value='SN', size=(10, 1),text_color='black',key='compute')],
    [sg.Text('Requested S/N or Texp:',size=(30, 1), pad=((5, 0), 0)), sg.Input(size=(10, 1), background_color='white', text_color='black',key='texpoSN')],
    [sg.Text('Overhead time:',size=(30, 1), pad=((5, 0), 0)), sg.Input(size=(10, 1), background_color='white', text_color='black',key='toverhd')],
    [sg.Text('PSF:',size=(30, 1), pad=((5, 0), 0)), sg.OptionMenu(values=('extended', 'pointsource'), default_value='pointsource', size=(10, 1),text_color='black',key='psf')],
    [sg.Text('Seeing:',size=(30, 1), pad=((5, 0), 0)), sg.Input(size=(10, 1),background_color='white', text_color='black',key='seeing')],
    [sg.Text('Area:',size=(30, 1), pad=((5, 0), 0)), sg.Input(size=(10, 1),background_color='white', text_color='black',key='area')],
    [sg.Text('Breadth:',size=(30, 1), pad=((5, 0), 0)), sg.Input(size=(10, 1),background_color='white', text_color='black',key='breadth')],
    [sg.Text("", size=(50, 10), pad=((5, 5), 10), key='text')]
    ]

    layout = [
    [sg.Column(left_col), sg.Image(key='-IMAGE-')],
    [sg.Button('Run ETC', button_color=('white', 'springgreen4'), key='-Run-', pad=((35, 30), 2)), sg.Button('Close', button_color=('white', 'springgreen4'), key='-Close-', pad=((30, 35), 2))] 
    ]
    
    
    window = sg.Window("MAAT ETC GUI", layout,
              default_element_size=(12, 1),
              text_justification='r',
              auto_size_text=False,
              auto_size_buttons=False,
              default_button_element_size=(12, 1),
              finalize=True)
    image_element = window['-IMAGE-']
    
    while True:
        event, values = window.read()
        text_elem = window['text']
        if event == sg.WIN_CLOSED:
            break
        elif event == '-Run-':
            #Put some checks here to make sure valid values are entered:
          try:
            if not values['fluxtype']: sg.popup('Choose a fluxtype!')
            if not values['fluxval'] or not isfloat(values['fluxval']): sg.popup('Enter a valid flux/magnitude!')
            if values['fluxtype']=='emline' and ( not values['fwhmA'] or not isfloat(values['fwhmA']) ): sg.popup('Enter a valid FWHM!')
            if not values['refwv'] or not isfloat(values['refwv']): sg.popup('Enter a valid reference wavelength!')
            if not values['sedtemplate']: sg.popup('Choose an SED template!')
            if not values['moon']: sg.popup('Choose a valid Moon brightness!')
            if not values['grating']: sg.popup('Choose a grating!')
            if not values['compute']: sg.popup('Choose a compute mode!')
            if not values['texpoSN'] or not isfloat(values['texpoSN']): sg.popup('Enter a valid Texp or S/N!')
            if not values['psf']: sg.popup('Choose a type of source geometry (psf) !')
            if not values['seeing'] or not isfloat(values['seeing']): sg.popup('Enter a valid seeing!')
            if not values['area'] or not isfloat(values['area']): sg.popup('Enter a valid area!')
            if not values['breadth'] or not isfloat(values['breadth']): sg.popup('Enter a valid breadth value!')
            run_etc(values,text_elem,image_element)
          except:
            if not values['fluxtype']: sg.popup('Choose a fluxtype!')
            if not values['fluxval'] or not isfloat(values['fluxval']): sg.popup('Enter a valid flux/magnitude!')
            if values['fluxtype']=='emline' and ( not values['fwhmA'] or not isfloat(values['fwhmA']) ): sg.popup('Enter a valid FWHM!')
            if not values['refwv'] or not isfloat(values['refwv']): sg.popup('Enter a valid reference wavelength!')
            if not values['sedtemplate']: sg.popup('Choose an SED template!')
            if not values['moon']: sg.popup('Choose a valid Moon brightness!')
            if not values['grating']: sg.popup('Choose a grating!')
            if not values['compute']: sg.popup('Choose a compute mode!')
            if not values['texpoSN'] or not isfloat(values['texpoSN']): sg.popup('Enter a valid Texp or S/N!')
            if not values['psf']: sg.popup('Choose a type of source geometry (psf) !')
            if not values['seeing'] or not isfloat(values['seeing']): sg.popup('Enter a valid seeing!')
            if not values['area'] or not isfloat(values['area']): sg.popup('Enter a valid area!')
            if not values['breadth'] or not isfloat(values['breadth']): sg.popup('Enter a valid breadth value!')
            event == '-Run-'
        elif event == '-Close-':
            break

    window.close()
   

#--------------------------------------------------------------------
# Run main
# 
# gui()


