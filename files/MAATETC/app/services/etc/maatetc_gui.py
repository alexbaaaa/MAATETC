#!/usr/bin/env python3
import random
from pathlib import Path

import matplotlib

# Required for web backends (no local GUI display).
matplotlib.use("Agg")

import matplotlib as mpl
import numpy as np
from astropy import units as u
from astropy.modeling.physical_models import BlackBody
from matplotlib import pyplot as plt
from scipy import interpolate

mpl.rcParams["image.interpolation"] = "nearest"
mpl.rcParams["image.origin"] = "lower"
mpl.rcParams["image.aspect"] = "equal"
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.size"] = 12
mpl.rcParams["lines.linewidth"] = 1

cspeed = 2.99792458e18  # A/s
hplanck = 6.626068e-27  # cm2 g / s == erg s
telearea = 73e4  # GTC effective collecting area in cm2

MAATETC_DIR = Path(__file__).resolve().parent


# --------------------------------------------------------------------
# From Chris Benn signal.f
# Zenith extinction for La Palma, taken from the ING Observers' Guide
# = constant (wavelength-dependent) gas + variable (grey) dust (= 0.05)
# Used for version 11.0 onwards.
# --------------------------------------------------------------------
def extinction(wv, am):
    extin0 = np.array([0.4554, 0.2175, 0.1020, 0.0575, 0.0157, 0.0087, 0.0087])  # WEAVE
    rep = interpolate.interp1d(np.array([3600, 4300, 5500, 6500, 8200, 9500, 10000]), extin0)
    newval = rep(wv)
    return 10.0 ** (-0.4 * float(am) * newval)


# --------------------------------------------------------------------
# Moon contribution to sky background (in mag/arcsec2)
# --------------------------------------------------------------------
def getsky(wv, moon):
    dark = np.array([22.0, 22.7, 21.9, 21.0, 20.0, 18.8, 18.8])
    grey = np.array([2.1, 1.1, 0.4, 0.3, 0.2, 0.2, 0.2])
    bright = np.array([5.0, 3.2, 1.8, 1.0, 0.7, 0.7, 0.7])
    if moon in ("grey", "gray"):
        dark = dark - grey
    if moon == "bright":
        dark = dark - bright
    repm = interpolate.interp1d(np.array([3600, 4300, 5500, 6500, 8200, 9500, 10000]), dark)
    return repm(wv)


# --------------------------------------------------------------------
# Reads required grating efficiency and interpolates to the dispersion
# Returns efficiency as function of new wavelength, and the value of dispersion
# --------------------------------------------------------------------
def getgrating(grating):
    gratings = np.array(
        ["R300B", "R300R", "R500B", "R500R", "R1000B", "R1000R", "R2000B", "R2500U", "R2500V", "R2500R", "R2500I"]
    )
    dispersion = np.array([2.60, 4.02, 1.87, 2.58, 1.13, 1.40, 0.46, 0.33, 0.44, 1.56, 1.73])
    igr = np.where(gratings == grating)[0][0]
    wv, eff = np.loadtxt(MAATETC_DIR / "efficiency" / f"{gratings[igr]}.txt", unpack=True, usecols=(0, 1))
    rep = interpolate.interp1d(wv, eff)
    wvi = np.arange(wv[0], wv[-1], dispersion[igr])
    effi = rep(wvi)
    return wvi, effi, dispersion[igr]


# --------------------------------------------------------------------
# General function to extrapolate wavelength range ends
# --------------------------------------------------------------------
def extend(x, y, wv):
    if x[0] > wv[0]:
        x = np.concatenate(([wv[0]], x))
        y = np.concatenate(([0], y))
    if x[-1] < wv[-1]:
        x = np.concatenate((x, [wv[-1]]))
        y = np.concatenate((y, [0]))
    return x, y


# --------------------------------------------------------------------
# Generate SED template for target
# --------------------------------------------------------------------
def getsed(sedtemplate, redz, wv):
    if sedtemplate == "ones":
        flam0 = np.ones(len(wv))  # erg/cm2/s/A
    elif sedtemplate.split()[0] == "blackbody":
        temp = float(sedtemplate.split()[1])
        bt = BlackBody(temp * u.K, scale=1.0 * u.Unit("erg / (cm2 s AA sr)"))
        flam0 = bt(wv * u.AA).value
    else:
        x, y = np.loadtxt(MAATETC_DIR / "seds" / f"{sedtemplate}.txt", unpack=True)
        x = (1 + redz) * x
        x, y = extend(x, y, wv)
        rep = interpolate.interp1d(x, y)
        flam0 = rep(wv)
    return flam0


# --------------------------------------------------------------------
# This function implements the computations made by Paco to scale the old-to-new Osiris
# --------------------------------------------------------------------
def old2newfac(wv):
    # wavelength and quantum efficiency of new CCD "deepdepletion_multi2"
    wnew = 10 * np.array(
        [
            300.6502,
            331.2442,
            359.4971,
            370.6928,
            378.7841,
            389.2324,
            398.5372,
            409.4083,
            429.636,
            441.7027,
            467.3995,
            490.361,
            509.4329,
            530.0577,
            549.1202,
            570.5182,
            599.6917,
            614.0843,
            644.4245,
            678.2694,
            700.4447,
            725.7345,
            744.0247,
            757.6469,
            775.9435,
            793.0764,
            810.604,
            828.5303,
            842.9545,
            859.7242,
            875.3294,
            888.213,
            900.3148,
            915.938,
            940.1554,
            959.6883,
            982.7231,
            1001.0658,
            1023.6836,
            1036.1558,
            1051.3489,
            1067.3101,
            1083.6554,
            1099.9992,
        ]
    )
    qenew = np.array(
        [
            1.64509e-01,
            3.51165e-01,
            5.46141e-01,
            6.59807e-01,
            7.62386e-01,
            8.36311e-01,
            8.79738e-01,
            9.10225e-01,
            9.17595e-01,
            9.12036e-01,
            8.91674e-01,
            8.86101e-01,
            8.78686e-01,
            8.75889e-01,
            8.80489e-01,
            8.84161e-01,
            8.96141e-01,
            9.01670e-01,
            9.14574e-01,
            9.23777e-01,
            9.28373e-01,
            9.31116e-01,
            9.28323e-01,
            9.23686e-01,
            9.12574e-01,
            8.96843e-01,
            8.73717e-01,
            8.38576e-01,
            8.03439e-01,
            7.54437e-01,
            7.01738e-01,
            6.46271e-01,
            5.95425e-01,
            5.19621e-01,
            4.00370e-01,
            3.00532e-01,
            2.00690e-01,
            1.30429e-01,
            6.66320e-02,
            3.98150e-02,
            1.66920e-02,
            6.50700e-03,
            2.79200e-03,
            9.24000e-04,
        ]
    )
    qenewi = interpolate.interp1d(wnew, qenew)(wv)

    # (i) wavelength and quantum efficiency of old CCD "OSIRIS-QE_old"
    wold = 10 * np.array([350.0, 400.0, 450.0, 500.0, 550.0, 600.0, 650.0, 700.0, 750.0, 800.0, 850.0, 900.0, 950.0, 1000.0])
    qeold = np.array([0.2, 0.4, 0.55, 0.63, 0.72, 0.77, 0.85, 0.87, 0.86, 0.85, 0.8, 0.6, 0.37, 0.17])
    qeoldi = interpolate.interp1d(wold, qeold)(wv)

    # (ii) wavelength and efficiency of GTC M3 "Aluminium_GTC"
    w3 = 10 * np.array(
        [
            300.0,
            350.0,
            400.0,
            450.0,
            500.0,
            550.0,
            600.0,
            650.0,
            700.0,
            750.0,
            775.0,
            800.0,
            825.0,
            850.0,
            875.0,
            900.0,
            925.0,
            950.0,
            1000.0,
            1200.0,
        ]
    )
    qe3 = np.array(
        [
            9.208e-01,
            9.205e-01,
            9.194e-01,
            9.175e-01,
            9.162e-01,
            9.157e-01,
            9.117e-01,
            9.057e-01,
            8.977e-01,
            8.862e-01,
            8.773e-01,
            8.676e-01,
            8.657e-01,
            8.677e-01,
            8.744e-01,
            8.908e-01,
            9.075e-01,
            9.243e-01,
            9.402e-01,
            9.637e+03,
        ]
    )
    qe3i = interpolate.interp1d(w3, qe3)(wv)

    # (iii) wavelength and efficiency of MAAT Winlight 20211011
    wifu, qifu1, qifu2, qifu3 = np.loadtxt(
        MAATETC_DIR / "efficiency" / "MAAT_trans_Winlight_20211011_1S5D_2S4D_3S3D.txt",
        unpack=True,
    )
    qifu = qifu1
    qifui = interpolate.interp1d(wifu, qifu)(wv)

    # global efficiency old-to-new for MAAT and for longslit
    return (qenewi * qifui) / (qeoldi * qe3i), (qenewi) / (qeoldi * qe3i)


# --------------------------------------------------------------------
# Read SED template and flux scale to input fluxval
# --------------------------------------------------------------------
def scaleflux(fluxtype, fluxval, refwv, fwhmA, disp, sedtemplate, redz, msky, wv):
    flam0 = getsed(sedtemplate, redz, wv)
    if fluxtype == "emline":
        flam0 = getsed("ones", redz, wv)

    wvind = np.where(abs(wv - refwv) == abs(wv - refwv).min())[0][0]
    fluxval0ref = 0.1
    fluxval0 = fluxval

    if fluxval0 > fluxval0ref:
        abmag = -2.5 * np.log10(flam0) - 2.402 - 5.0 * np.log10(wv)
        abmag = abmag + fluxval0 - abmag[wvind]
        flam = 10.0 ** (-0.4 * (abmag + 2.402 + 5.0 * np.log10(wv)))
        if fluxtype == "emline":
            print(
                "!!!***###***!!! Why would you give emission line flux in magnitudes? "
                "If code does not break, results will be definitely WRONG !!!***###***!!!"
            )
    elif fluxval0 <= fluxval0ref:
        if fluxtype == "emline":
            npixspec = 3.25  # Assumed spectral resolution fwhm in spectral pixels.
            fluxval0 = (fluxval / np.sqrt(fwhmA**2 + (npixspec * disp) ** 2)) * disp
        flam = fluxval0 * flam0 / flam0[wvind]
    else:
        print("It is IMPOSSIBLE in this universe that this sentence is ever printed!")

    flamsk = 10.0 ** (-0.4 * (msky + 2.402 + 5.0 * np.log10(wv)))
    return flam, flamsk


# --------------------------------------------------------------------
# Computes fraction of light within a given geometry for gaussian and moffat 2D functions
# --------------------------------------------------------------------
def moffatgauss(fwhm, nsigmas, slitwidth, plotPSF):
    b = 3  # Moffat b parameter
    scale = 10  # 1 arcsec = 10 model pixels
    fwhm = fwhm * scale
    width = 10  # how many fwhm has the simulated 2D array on a side
    nx, ny = int(width * fwhm + 0.5) + 1, int(width * fwhm + 0.5) + 1
    xc, yc = int(0.5 * width * fwhm), int(0.5 * width * fwhm)
    m = np.zeros((nx, ny))
    g = np.zeros((nx, ny))
    xy = np.zeros((nx, ny))
    sigma = fwhm / 2.3548
    a = fwhm / (2.0 * np.sqrt(2 ** (1.0 / b) - 1.0))

    k = -1
    for i in range(nx):
        k += 1
        for j in range(ny):
            r = np.sqrt((i - xc) ** 2 + (j - yc) ** 2)
            m[j, i] = (1.0 / (1.0 + (r / a) ** 2)) ** b
            g[j, i] = np.exp(-0.5 * (r / sigma) ** 2)
            xy[j, i] = r
    m = m / m.sum().sum()
    g = g / g.sum().sum()
    dis = xy

    dd = int(np.ceil(nsigmas * sigma))
    slithalf = int(np.ceil(0.5 * slitwidth * scale))

    gsum0 = g[np.where(dis <= dd)].sum() / g.sum()
    gslit3 = g[yc - dd : yc + dd, xc - slithalf : xc + slithalf].sum() / g.sum()

    if plotPSF:
        fig = plt.figure()
        plt.clf()
        ax = fig.add_subplot(111)
        extent = [-xc / scale, xc / scale, -yc / scale, yc / scale]
        ims = np.sqrt(np.sqrt(g))
        ax.imshow(ims, extent=extent, cmap="gray_r", vmin=ims.min(), vmax=ims.max())
        ax.set_title(f"fwhm={fwhm / scale}, slitwidth={slitwidth}, Nsigma={nsigmas}")
        ax.set_xlabel("arcsec")
        ax.set_ylabel("arcsec")
        plt.draw()

    return gsum0, gslit3


# --------------------------------------------------------------------
# Compute SN/Texpo arrays for one configuration
# --------------------------------------------------------------------
def doloop(
    compute,
    value,
    psf,
    fluxtype,
    extin,
    disp,
    breadth,
    toverhd,
    sedtemplate,
    redz,
    refwv,
    msky,
    fluxval,
    fwhmA,
    seeing,
    area,
    longslitw,
    wv,
    eff,
    effslit,
):
    plotPSF = False

    if psf == "pointsource":
        seeing_fwhm = seeing
        seeing_sigma = seeing_fwhm / 2.355
        seeing_sigmas = 2

        signalfac, slitfac = moffatgauss(seeing_fwhm, seeing_sigmas, longslitw, plotPSF)

        signalarea = np.pi * (seeing_sigmas * seeing_sigma) ** 2
        signalareaslit = longslitw * (2 * seeing_sigmas * seeing_sigma)

        signalarea_pix = signalarea / 0.127**2
        signalareaslit_pix = signalareaslit / 0.127**2

        signalarea_obj = 1
        signalareaslit_obj = 1
    else:
        signalarea = area**2
        signalareaslit = longslitw * area
        signalfac = 1.0
        slitfac = 1.0
        signalarea_obj = signalarea
        signalarea_pix = signalarea / 0.127**2
        signalareaslit_obj = signalareaslit
        signalareaslit_pix = signalareaslit / 0.127**2

    # CCD
    dc = 3 / 3600  # e/pixel/s
    ron = 3
    RON2 = ron**2 * signalarea_pix
    RON2slit = ron**2 * signalareaslit_pix

    flam, flamsk = scaleflux(fluxtype, fluxval, refwv, fwhmA, disp, sedtemplate, redz, msky, wv)

    specpixsA = np.max([disp, breadth])

    Sobj = flam * (wv / (cspeed * hplanck)) * eff * extin * telearea * specpixsA * signalarea_obj * signalfac
    Ssky = flamsk * (wv / (cspeed * hplanck)) * eff * telearea * specpixsA * signalarea
    Sobjslit = flam * (wv / (cspeed * hplanck)) * effslit * extin * telearea * specpixsA * signalareaslit_obj * slitfac
    Sskyslit = flamsk * (wv / (cspeed * hplanck)) * effslit * telearea * specpixsA * signalareaslit

    if compute == "SN":
        Texpo = value
        SN = Sobj * Texpo / np.sqrt(Sobj * Texpo + Ssky * Texpo + dc**2 * Texpo + RON2)
        flamnoisy = np.array([flam[i] * (1 + random.normalvariate(0.0, 1.0) / SN[i]) for i in range(len(wv))])

        Texposlit = Texpo - toverhd
        SNslit = Sobjslit * Texposlit / np.sqrt(Sobjslit * Texposlit + Sskyslit * Texposlit + dc**2 * Texposlit + RON2slit)
        return SN, SNslit, flam, flamnoisy, specpixsA

    SN = value
    Texpo = (SN**2 * (Sobj + Ssky + dc**2) + np.sqrt(SN**4 * (Sobj + Ssky + dc**2) + 4 * SN**2 * Sobj**2 * RON2)) / (
        2 * Sobj**2
    )
    flamnoisy = np.array([flam[i] * (1 + random.normalvariate(0.0, 1.0) / SN) for i in range(len(wv))])
    return Texpo, flam, flamnoisy, specpixsA


def _get_optional_float(values, key, default_value, default_message):
    raw = values.get(key, "")
    if raw is None or str(raw).strip() == "":
        print(default_message)
        return default_value
    return float(raw)


def _build_empty_figure(message):
    fig = matplotlib.figure.Figure(figsize=(7, 7), dpi=100)
    ax = fig.add_subplot(111)
    ax.text(0.5, 0.5, message, ha="center", va="center", wrap=True)
    ax.set_axis_off()
    return fig


def run_etc(values, text_elem, image_element):
    del image_element  # Not used in web mode; kept for interface compatibility.

    fluxtype = values["fluxtype"]
    fluxval = float(values["fluxval"])
    refwv = float(values["refwv"])
    sedtemplate = values["sedtemplate"]
    moon = values["moon"]
    grating = values["grating"]
    compute = values["compute"]
    seeing = float(values["seeing"])
    area = float(values["area"])
    psf = values["psf"]
    texpoSN = float(values["texpoSN"])

    fwhmA = _get_optional_float(values, "fwhmA", 0, "Will use fwhmA=0")
    redz = _get_optional_float(values, "redz", 0, "Will use redshift=0")
    toverhd = _get_optional_float(values, "toverhd", 300, "Will use overhead time = 300 s (only for longslit calculations)")
    airmass = _get_optional_float(values, "airmass", 1, "Will use airmass=1")
    breadth = _get_optional_float(values, "breadth", 0, "Will use breadth=0, i.e., compute in disp Angstroms")

    if compute == "SN":
        Texpo = texpoSN
    else:
        SN_input = texpoSN

    wv, efff, disp = getgrating(grating)
    eff_maat, eff_slit = old2newfac(wv)
    eff = efff * eff_maat
    effslit = efff * eff_slit

    if (refwv < wv[0]) or (refwv > wv[-1]):
        warning = (
            "WARNING: reference wavelength is outside grating range. "
            f"{refwv} is not within [{wv[0]}, {wv[-1]}]."
        )
        text_elem.update(value=warning)
        return _build_empty_figure(warning), text_elem

    # reference wavelengths
    iefmx = np.where(eff == eff.max())[0][0]
    wveffmax = wv[iefmx]
    wveffwv = (wv * eff).sum() / eff.sum()
    wvcen = (wv[-1] + wv[0]) / 2
    iefwv = np.where(wv <= wveffwv)[0][-1]
    iwvcen = np.where(wv <= wvcen)[0][-1]
    iwvinf = np.where(wv <= refwv)[0][-1]
    wvind = np.where(abs(wv - refwv) == abs(wv - refwv).min())[0][0]

    extin = extinction(wv, airmass)
    msky = getsky(wv, moon)

    longslitw = 0.6

    if compute == "SN":
        SN, SNslit, flam, flamnoisy, specpixsA = doloop(
            compute,
            Texpo,
            psf,
            fluxtype,
            extin,
            disp,
            breadth,
            toverhd,
            sedtemplate,
            redz,
            refwv,
            msky,
            fluxval,
            fwhmA,
            seeing,
            area,
            longslitw,
            wv,
            eff,
            effslit,
        )
        if psf == "pointsource":
            text_elem.update(
                value=(
                    "Integrating a pointsource of fwhm %.2f arcsec\n"
                    "S/N resulting from exposure time %.1f sec\n"
                    "%.2f at wavelength of maximum efficiency %.1f\n"
                    "%.2f at efficiency weighted wavelength %.1f\n"
                    "%.2f at range mid wavelength %.1f\n"
                    "%.2f at input reference wavelength %.1f"
                    % (seeing, Texpo, SN[iefmx], wveffmax, SN[iefwv], wveffwv, SN[iwvcen], wvcen, SN[iwvinf], refwv)
                )
            )
        else:
            text_elem.update(
                value=(
                    "Integrating in square box of side %.2f arcsec\n"
                    "S/N resulting from exposure time %.1f sec\n"
                    "%.2f at wavelength of maximum efficiency %.1f\n"
                    "%.2f at efficiency weighted wavelength %.1f\n"
                    "%.2f at range mid wavelength %.1f\n"
                    "%.2f at input reference wavelength %.1f"
                    % (area, Texpo, SN[iefmx], wveffmax, SN[iefwv], wveffwv, SN[iwvcen], wvcen, SN[iwvinf], refwv)
                )
            )
    else:
        Texpo, flam, flamnoisy, specpixsA = doloop(
            compute,
            SN_input,
            psf,
            fluxtype,
            extin,
            disp,
            breadth,
            toverhd,
            sedtemplate,
            redz,
            refwv,
            msky,
            fluxval,
            fwhmA,
            seeing,
            area,
            longslitw,
            wv,
            eff,
            effslit,
        )
        if psf == "pointsource":
            text_elem.update(
                value=(
                    "Integrating a pointsource of fwhm %.2f arcsec\n"
                    "Exposure time (sec) resulting from S/N %.1f\n"
                    "%.2f at wavelength of maximum efficiency %.1f\n"
                    "%.2f at efficiency weighted wavelength %.1f\n"
                    "%.2f at range mid wavelength %.1f\n"
                    "%.2f at input reference wavelength %.1f"
                    % (
                        seeing,
                        SN_input,
                        Texpo[iefmx],
                        wveffmax,
                        Texpo[iefwv],
                        wveffwv,
                        Texpo[iwvcen],
                        wvcen,
                        Texpo[iwvinf],
                        refwv,
                    )
                )
            )
        else:
            text_elem.update(
                value=(
                    "Integrating in square box of side %.2f arcsec\n"
                    "Exposure time (sec) resulting from S/N %.1f\n"
                    "%.2f at wavelength of maximum efficiency %.1f\n"
                    "%.2f at efficiency weighted wavelength %.1f\n"
                    "%.2f at range mid wavelength %.1f\n"
                    "%.2f at input reference wavelength %.1f"
                    % (
                        area,
                        SN_input,
                        Texpo[iefmx],
                        wveffmax,
                        Texpo[iefwv],
                        wveffwv,
                        Texpo[iwvcen],
                        wvcen,
                        Texpo[iwvinf],
                        refwv,
                    )
                )
            )

    fig = matplotlib.figure.Figure(figsize=(7, 7), dpi=100)
    ax = fig.add_subplot(211)

    if compute == "SN":
        if fluxtype == "continuum":
            ax.plot(wv, SN, "k-", lw=0.5)
        if fluxtype == "emline":
            ax.plot([wv[wvind], wv[wvind]], [0, SN[wvind]], "-", lw=1)
            ax.axhline(0)
        ax.set_ylabel(f"S/N in {specpixsA} " + r"$\mathrm{\AA}$")
        if psf == "pointsource":
            ax.set_title(
                f"{sedtemplate}, {grating}, mag[{refwv}]={fluxval}. Texpo={int(Texpo)},  {psf} {seeing}\"",
                fontsize=10,
            )
        else:
            ax.set_title(
                f"{sedtemplate}, {grating}. Flux[{refwv}]={fluxval}. Texpo={int(Texpo)},  {psf} {area}\"",
                fontsize=10,
            )
    else:
        if fluxtype == "continuum":
            ax.plot(wv, Texpo, "k-", lw=0.5)
        if fluxtype == "emline":
            ax.plot([wv[wvind], wv[wvind]], [0, Texpo[wvind]], "-", lw=1)
            ax.axhline(0)
        ax.set_ylabel("exposure time (s)")
        if psf == "pointsource":
            ax.set_title(
                f"{sedtemplate}, {grating}, mag[{refwv}]={fluxval}. S/N={int(SN_input)},  {psf} {seeing}\"",
                fontsize=10,
            )
        else:
            ax.set_title(
                f"{sedtemplate}, {grating}. Flux[{refwv}]={fluxval}. S/N={int(SN_input)},  {psf} {area}\"",
                fontsize=10,
            )
    ax.grid(ls=":", color="k", lw=0.5)

    ax1 = fig.add_subplot(212)
    flam_plot = flam * 1e17
    flamnoisy_plot = flamnoisy * 1e17
    ax1.plot(wv, flamnoisy_plot, "0.7", lw=1)
    ax1.plot(wv, flam_plot, "k-", lw=1)
    siglim = flamnoisy_plot.mean() - flamnoisy_plot[flamnoisy_plot < flamnoisy_plot.mean()].mean()
    ax1.set_ylim(flamnoisy_plot.mean() - 4 * siglim, flamnoisy_plot.mean() + 4 * siglim)
    ax1.set_ylabel(r"$\mathrm{F_{\lambda}\ (10^{-17} erg s^{-1} cm^{-2} \AA^{-1}}$)")
    ax1.set_xlabel(r"wavelength ($\mathrm{\AA}$)")

    return fig, text_elem

