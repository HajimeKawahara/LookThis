import pandas as pd
from astroquery.simbad import Simbad
import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia

dat=pd.read_csv("sb9/Main.dta",delimiter="|",dtype={"System Number":"int","1900.0 coordinates":"str","2000.0 coordinates":"str","Component":"str","Magnitude of component 1":"float","Filter component 1":"str","Magnitude of component 2":"float","Filter component 2":"str","Spectral type component 1":"str","Spectral type component 2":"str"})

#GAIA distance
f=open("sb9_position.txt","w")
f.write("System Number|ra (degree)|dec (degree)|distance (pc)"+"\n")
for i,sysi in enumerate(dat["System Number"]):
    pradec=dat["2000.0 coordinates"][i]
    c=SkyCoord.from_name("J"+pradec, parse=True)
    ra=c.ra.degree
    dec=c.dec.degree
    try:
        print(sysi)
        width = u.Quantity(5, u.arcsec)
        height = u.Quantity(5, u.arcsec)
        #GAIA
        r = Gaia.query_object_async(coordinate=c, width=width, height=height)
        plx=r["parallax"].item()
        if plx == plx:
            f.write(str(sysi)+"|"+str(ra)+"|"+str(dec)+"|"+str(1000.0/plx)+"\n")
        else:
            print(plx)
            Simbad.SIMBAD_URL = "http://simbad.u-strasbg.fr/simbad/sim-script"
            result_table = Simbad.query_region(c, radius='0d0m5s')
            print(result_table)
            plx=result_table["PLX_VALUE"].item()
            if plx == plx:
                f.write(str(sysi)+"|"+str(ra)+"|"+str(dec)+"|"+str(1000.0/plx)+"\n")

    except:
        f.write(str(sysi)+"|"+str(ra)+"|"+str(dec)+"|"+"\n")
f.close()


#dat2=pd.read_csv("../database/sb9/Orbits.dta",delimiter="|",dtype={"System number":"int","Orbit number for that system":"int","Period (d)":"float","error on P (d)":"float","Periastron time (JD-2400000)":"float","error on Periastron time":"float","Flag on periastron time":"str","eccentricity":"float","error on eccentricity":"float","argument of periastron (deg)":"float","error on omega":"float","K1 (km/s)":"float","error on K1 (km/s)":"float","K2 (km/s)":"float","error on K2 (km/s)":"float","systemic velocity (km/s)":"float","error on V0 (km/s)":"float","rms RV1 (km}":"float","rms RV2 (km/s)":"float","RV1":"float","RV2":"float","Grade":"float","Bibcode":"str","Contributor":"str","Accessibility":"str","Reference adopted for the times (JD or MJD)":"str"},na_values = "NaN")


#dat3=pd.read_csv("../database/sb9/Alias.dta",delimiter="|",dtype={"System number":"int","Catalog name":"str","ID in that catalog":"str"})

#dat.to_pickle("../database/pickles/sb9.Main.pickle")
#dat2.to_pickle("../database/pickles/sb9.Orbits.pickle")
#dat3.to_pickle("../database/pickles/sb9.Alias.pickle")
