import littlecms as lc

PERCEPTUAL = lc.INTENT_PERCEPTUAL
RELATIVE_COLORIMETRIC = lc.INTENT_RELATIVE_COLORIMETRIC
SATURATION = lc.INTENT_SATURATION
ABSOLUTE_COLORIMETRIC = lc.INTENT_ABSOLUTE_COLORIMETRIC

# Modified from the following:
# https://stackoverflow.com/a/56621786/2297141

def rgb2lab(in_val, profile_rgb=None, intent=RELATIVE_COLORIMETRIC) :
    white = lc.cmsD50_xyY()    # Set white point for D50
    if profile_rgb != None:
        prgb = lc.cmsOpenProfileFromFile(profile_rgb, 'r') # cmsCreate_sRGBProfile()
    else:
        prgb = lc.cmsCreate_sRGBProfile()
    plab = lc.cmsCreateLab4Profile(white)
    transform = lc.cmsCreateTransform(prgb, lc.TYPE_RGB_8, plab, lc.TYPE_Lab_DBL,
                                  intent,
                                  lc.cmsFLAGS_NOCACHE|lc.cmsFLAGS_NOOPTIMIZE|lc.cmsFLAGS_BLACKPOINTCOMPENSATION|lc.cmsFLAGS_HIGHRESPRECALC)
    n_pixels = 1
    in_comps = 3
    out_comps = 3
    buf_in = lc.uint8Array(in_comps * n_pixels)
    buf_out = lc.doubleArray(out_comps * n_pixels)
    for i in range(in_comps):
        buf_in[i] = in_val[i]
    lc.cmsDoTransform(transform, buf_in, buf_out, n_pixels)
    lc.cmsCloseProfile(prgb)
    lc.cmsCloseProfile(plab)
    lc.cmsDeleteTransform(transform)
    return tuple(buf_out[i] for i in range(out_comps * n_pixels))

def lab2rgb(in_val, profile_rgb=None, intent=RELATIVE_COLORIMETRIC) :
    white = lc.cmsD50_xyY()    # Set white point for D50
    if profile_rgb != None:
        prgb = lc.cmsOpenProfileFromFile(profile_rgb, 'r')
    else:
        prgb = lc.cmsCreate_sRGBProfile()
    plab = lc.cmsCreateLab4Profile(white)
    transform = lc.cmsCreateTransform(plab, lc.TYPE_Lab_DBL, prgb, lc.TYPE_RGB_8,
                                  intent,
                                  lc.cmsFLAGS_NOCACHE|lc.cmsFLAGS_NOOPTIMIZE|lc.cmsFLAGS_BLACKPOINTCOMPENSATION|lc.cmsFLAGS_HIGHRESPRECALC)
    n_pixels = 1
    in_comps = 3
    out_comps = 3
    buf_in = lc.doubleArray(in_comps * n_pixels)
    buf_out = lc.uint8Array(out_comps * n_pixels)
    for i in range(in_comps):
        buf_in[i] = in_val[i]
    lc.cmsDoTransform(transform, buf_in, buf_out, n_pixels)
    lc.cmsCloseProfile(prgb)
    lc.cmsCloseProfile(plab)
    lc.cmsDeleteTransform(transform)
    return tuple(buf_out[i] for i in range(out_comps * n_pixels))

def cmyk2lab(in_val, profile_cmyk, intent=RELATIVE_COLORIMETRIC) :
    white = lc.cmsD50_xyY()    # Set white point for D50
    plab = lc.cmsCreateLab4Profile(white)
    pcmyk = lc.cmsOpenProfileFromFile(profile_cmyk, 'r')
    transform = lc.cmsCreateTransform(pcmyk, lc.TYPE_CMYK_8, plab, lc.TYPE_Lab_DBL,
                                  intent,
                                  lc.cmsFLAGS_NOCACHE|lc.cmsFLAGS_NOOPTIMIZE|lc.cmsFLAGS_BLACKPOINTCOMPENSATION|lc.cmsFLAGS_HIGHRESPRECALC)
    n_pixels = 1
    in_comps = 4
    out_comps = 3
    buf_in = lc.uint8Array(in_comps * n_pixels)
    buf_out = lc.doubleArray(out_comps * n_pixels)
    for i in range(in_comps):
        buf_in[i] = max(0, min(255, round(in_val[i] / 100 * 255)))
    lc.cmsDoTransform(transform, buf_in, buf_out, n_pixels)
    lc.cmsCloseProfile(plab)
    lc.cmsCloseProfile(pcmyk)
    lc.cmsDeleteTransform(transform)
    return tuple(buf_out[i] for i in range(out_comps * n_pixels))

def lab2cmyk(in_val, profile_cmyk, intent=RELATIVE_COLORIMETRIC) :
    white = lc.cmsD50_xyY()    # Set white point for D50
    plab = lc.cmsCreateLab4Profile(white)
    pcmyk = lc.cmsOpenProfileFromFile(profile_cmyk, 'r')
    transform = lc.cmsCreateTransform(plab, lc.TYPE_Lab_DBL, pcmyk, lc.TYPE_CMYK_8,
                                  intent,
                                  lc.cmsFLAGS_NOCACHE|lc.cmsFLAGS_NOOPTIMIZE|lc.cmsFLAGS_BLACKPOINTCOMPENSATION|lc.cmsFLAGS_HIGHRESPRECALC)
    n_pixels = 1
    in_comps = 3
    out_comps = 4
    buf_in = lc.doubleArray(in_comps * n_pixels)
    buf_out = lc.uint8Array(out_comps * n_pixels)
    for i in range(in_comps):
        buf_in[i] = in_val[i]
    lc.cmsDoTransform(transform, buf_in, buf_out, n_pixels)
    lc.cmsCloseProfile(plab)
    lc.cmsCloseProfile(pcmyk)
    lc.cmsDeleteTransform(transform)
    return tuple(round(buf_out[i] / 255 * 100) for i in range(out_comps * n_pixels))

def rgb2cmyk(in_val, profile_rgb=None, profile_cmyk=None, intent=RELATIVE_COLORIMETRIC) :
    if profile_rgb != None:
        prgb = lc.cmsOpenProfileFromFile(profile_rgb, 'r') # cmsCreate_sRGBProfile()
    else:
        prgb = lc.cmsCreate_sRGBProfile()
    pcmyk = lc.cmsOpenProfileFromFile(profile_cmyk, 'r')
    transform = lc.cmsCreateTransform(prgb, lc.TYPE_RGB_8, pcmyk, lc.TYPE_CMYK_8,
                                  intent,
                                  lc.cmsFLAGS_NOCACHE|lc.cmsFLAGS_NOOPTIMIZE|lc.cmsFLAGS_BLACKPOINTCOMPENSATION|lc.cmsFLAGS_HIGHRESPRECALC)
    n_pixels = 1
    in_comps = 3
    out_comps = 4
    buf_in = lc.uint8Array(in_comps * n_pixels)
    buf_out = lc.uint8Array(out_comps * n_pixels)
    for i in range(in_comps):
        buf_in[i] = in_val[i]
    lc.cmsDoTransform(transform, buf_in, buf_out, n_pixels)
    lc.cmsCloseProfile(prgb)
    lc.cmsCloseProfile(pcmyk)
    lc.cmsDeleteTransform(transform)
    return tuple(round(buf_out[i] / 255 * 100) for i in range(out_comps * n_pixels))

def cmyk2rgb(in_val, profile_rgb=None, profile_cmyk=None, intent=RELATIVE_COLORIMETRIC) :
    if profile_rgb != None:
        prgb = lc.cmsOpenProfileFromFile(profile_rgb, 'r') # cmsCreate_sRGBProfile()
    else:
        prgb = lc.cmsCreate_sRGBProfile()
    pcmyk = lc.cmsOpenProfileFromFile(profile_cmyk, 'r')
    transform = lc.cmsCreateTransform(pcmyk, lc.TYPE_CMYK_8, prgb, lc.TYPE_RGB_8,
                                  intent,
                                  lc.cmsFLAGS_NOCACHE|lc.cmsFLAGS_NOOPTIMIZE|lc.cmsFLAGS_BLACKPOINTCOMPENSATION|lc.cmsFLAGS_HIGHRESPRECALC)
    n_pixels = 1
    in_comps = 4
    out_comps = 3
    buf_in = lc.uint8Array(in_comps * n_pixels)
    buf_out = lc.uint8Array(out_comps * n_pixels)
    for i in range(in_comps):
        buf_in[i] = max(0, min(255, round(in_val[i] / 100 * 255)))
    lc.cmsDoTransform(transform, buf_in, buf_out, n_pixels)
    lc.cmsCloseProfile(prgb)
    lc.cmsCloseProfile(pcmyk)
    lc.cmsDeleteTransform(transform)
    return tuple(buf_out[i] for i in range(out_comps * n_pixels))
