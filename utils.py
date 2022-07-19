import astropy.units as u
from astropy.coordinates import SkyCoord
import pandas as pd

def match(df_1, df_2, pixel, df1_name):
    """
    匹配两个表
    :param df_1:
    :param df_2:
    :return:
    """
    sdss = SkyCoord(ra=df_1.ra * u.degree, dec=df_1.dec * u.degree)
    decals = SkyCoord(ra=df_2.ra * u.degree, dec=df_2.dec * u.degree)
    idx, d2d, d3d = sdss.match_to_catalog_sky(decals)
    max_sep = pixel * 0.262 * u.arcsec
    distance_idx = d2d < max_sep
    sdss_matches = df_1.iloc[distance_idx]
    matches = idx[distance_idx]
    decal_matches = df_2.iloc[matches]
    test = sdss_matches.loc[:].rename(columns={"ra":"%s" % df1_name[0], "dec":"%s" % df1_name[1]})
    test.insert(0, 'ID', range(len(test)))
    decal_matches.insert(0, 'ID', range(len(decal_matches)))
    new_df = pd.merge(test, decal_matches, how="inner", on=["ID"])
    return new_df.drop("ID", axis=1)