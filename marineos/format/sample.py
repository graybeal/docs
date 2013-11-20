from datetime import datetime 
import re
from ast import literal_eval

import numpy as np
from pup import *
import coards


records = []
state = "header"
cast_id = 0
with open("97080060.ctd") as fp:
    for line in fp:
        # a simple state machine for parsing 
        if line.startswith("*PRES   TEMP   PSAL"):
            state = "data"
            cast_id += 1
            continue
        elif line.startswith("*"):
            state = "header"

        # get positional info
        if line.startswith("*DATE"):
            time = datetime.strptime(line[:22], "*DATE=%d%m%Y TIME=%H%M")

            # parse latitude and longitude
            parts = re.search("LAT=(N|S)(\d\d) (\d\d\.\d\d)", line).groups()
            latitude = literal_eval(parts[1]) + literal_eval(parts[2])/60.
            if parts[0] == "S":
                latitude *= -1
            parts = re.search("LON=(W|E)(\d\d\d) (\d\d\.\d\d)", line).groups()
            longitude = literal_eval(parts[1]) + literal_eval(parts[2])/60.
            if parts[0] == "W":
                longitude *= -1

        if state == "data":
            depth, temp, salt, flag = map(literal_eval, line.split())
            if flag != 999:
                records.append(
                    (time, cast_id, latitude, longitude, depth, temp, salt))

data = np.rec.fromrecords(
    records, names=[
        "time",
        "cast_id",
        "latitude",
        "longitude",
        "depth",
        "temperature",
        "salinity"]
)


class MarinexploreStandard(NetCDF):

    # global required
    Conventions = "Marinexplore 1.0.2"
    Metadata_Convention = "Marinexplore 1.0.2"
    mx_primary_contact_email = "roberto@marinexplore.com"
    mx_primary_contact_individual = "Roberto De Almeida"
    mx_primary_contact_organization = "Marinexplore Inc."
    mx_primary_contact_role = "publisher"
    title = "CTD casts from the SAMBA 3 cruise."

    # global recommended
    geospatial_lat_max = max(data.latitude)
    geospatial_lat_min = min(data.latitude)
    geospatial_lon_max = max(data.longitude)
    geospatial_lon_min = min(data.longitude)
    geospatial_vertical_max = max(data.depth)
    geospatial_vertical_min = min(data.depth)
    geospatial_vertical_positive = "down"
    geospatial_vertical_units = "dbar"
    geospatial_bounds = [
        geospatial_lat_min, 
        geospatial_lon_min,
        geospatial_vertical_min,
        geospatial_lat_max,
        geospatial_lon_max,
        geospatial_vertical_max,
    ]
    license = "Public data"
    mx_character_set = "utf-8"
    mx_data_quality_control = "User QC"
    mx_data_policy_lookup_date = datetime.today()
    mx_data_policy_source_url = ""  # leave empty if new policy? XXX
    mx_data_stream_doc_url = "http://www.ifremer.fr/sismer/program/seasearch/htql/campagnea.htql?CRNO=97080060"
    mx_data_stream_key = "SAMBA3.CTD"
    mx_data_stream_url = ""  # leave empty if new stream? XXX
    mx_language = "en"
    mx_measurement_frequency = "Variable"
    mx_sampling_feature_type = "trajectoryProfile"
    mx_spatial_resolution = "Variable"
    mx_streaming_status = "Closed"
    mx_topic_category = "oceans"
    platform = "35NC R/V NADIR"
    publisher = "Roberto De Almeida"
    publisher_email = "roberto@marinexplore.com"
    publisher_institution = "Marinexplore Inc."
    publisher_project = "SAMBA3"
    summary = """This stream contains CTD data from the SAMBA3 cruise. Data was
provided to Dr. Roberto De Almeida since he participated in the cruise."""

    # global level 3
    acknowledgement = ""
    comment = ""
    coverage_content_type = "physicalMeasurement"
    creator = "Cortes Norbert"
    creator_email = "Norbert.Cortes@ifremer.fr"
    creator_institution = "Ifremer"
    creator_project = "SAMBA3"
    date_modified = datetime.today()
    history = """Converted to Marinexplore canonical NetCDF from the original
file 97080060.ctd by Roberto De Almeida on %s.""" % datetime.today()
    mx_data_level = "Binned data"
    mx_data_policy_uid = ""
    mx_instrument_deployment = "SAMBA3.CTD"
    mx_observational_origin = "Insitu measurements with CTD"
    mx_owner_individual = "Cortes Norbert"
    mx_owner_institution = "Ifremer"
    mx_owner_project = "SAMBA3"
    mx_platform_deployment = "CTD"
    naming_authority = "Marinexplore Inc."
    nodc_template_version = "Unknown"  # XXX unsure about versions for trajectoryProfile
    processing_level = "Data binned by pressure"
    references = "http://www.ifremer.fr/sismer/program/seasearch/htql/campagnea.htql?CRNO=97080060"
    time_coverage_end = data.time[-1]
    time_coverage_resolution = "Variable"
    time_coverage_start = data.time[0]
    time_coverage_duration = "%s days" % (
        time_coverage_end - time_coverage_start).days

    # global level 4
    additional_metadata = "http://www.ifremer.fr/sismer/program/seasearch/htql/campagnea.htql?CRNO=97080060"
    date_created = "Unknown"
    mx_data_access_protocols = "Direct data"
    mx_data_set_size = "605K"
    mx_relations_to_other_data = ""

    # global level 5
    cdm_data_type = "Trajectory"
    contributor_info = "Ifremer, FURG"
    contributor_name = "Cortes Norbert"  # how is this different than the previous? XXX
    contributor_role = "Chief Scientist"
    creator_institution_info = "Data collected by Ifremer"
    creator_project_info = """The project aims to describe the movement of 
Antarctic Intermediary Water at 800m depth during its northward journey, using
subsurface drifters."""
    creator_uri = "http://www.ifremer.fr/"
    featureType = "trajectoryProfile"  # how is this different than mx_samplingf_feature_type?
    geospatial_lat_resolution = "Variable"
    geospatial_lat_units = "degrees_north"
    geospatial_lon_resolution = "Variable"
    geospatial_lon_units = "degrees_east"
    geospatial_vertical_resolution = "1 dbar"
    id = "FI351997080060"
    institution = "Ifremer"  # why this again?
    instrument = "CTD"
    keywords_vocabulary = "CF Standard Names"
    mx_adhoc_metadata = "{}"
    mx_temporal_range = time_coverage_start, time_coverage_end  # again? XXX
    nodc_name = ""  # what is this?
    sea_name = 32  # South Atlantic Ocean (http://www.nodc.noaa.gov/General/NODC-Archive/seanamelist.txt)
    source = "CTD data" 
    standard_name_vocabulary = "CF Standard Names"  # how is this different than keywords_vocabulary? XXX
    uuid = ""

    # global avoided -- XXX why do we list this?
    #mx_source_data_model
    #publisher_institution_info
    #publisher_project_info
    #publisher_uri

    # add coordinates
    time = Variable(
        [coards.format(d, "microseconds since 1970-1-1") for d in data.time],
        record = True,

        # priority 1
        axis = "T",
        #positive
        variables = "",  # I don't understand this. XXX

        # priority 2
        #climatology
        #keywords
        long_name = "Time",
        standard_name = "time",

        # priority 3
        mx_measurement_type = "time",

        # no priority
        #bounds
        calendar = "gregorian",
        #cf_role
        #compress
        #_FillValue
        #formula_terms
        #leap_month
        #leap_year
        #missing_value
        #month_lengths
        units = "microseconds since 1970-1-1",
        #valid_max
        #valid_min
        #valid_range
    )

    cast_id = Variable(
        data.cast_id,
        (time,),
        long_name = "CTD Cast id",
        cf_role = "profile_id",
        standard_name = "",
        mx_measurement_type = "",
    )

    latitude = Variable(
        data.latitude,
        (time,),
        axis = "Y",
        long_name = "Latitude",
        standard_name = "latitude",
        mx_measurement_type = "latitude",
        units = "degrees_north",
        valid_max = 90.,
        valid_min = -90.,
        valid_range = (-90., 90.),
    )

    longitude = Variable(
        data.longitude,
        (time,),
        axis = "X",
        long_name = "longitude",
        standard_name = "longitude",
        mx_measurement_type = "longitude",
        units = "degrees_east",
        valid_max = -180.,
        valid_min = 180.,
        valid_range = (-180., 180.),
    )

    depth = Variable(
        data.depth,
        (time,),
        axis = "Z",
        positive = "down",
        long_name = "Seawater pressure",
        standard_name = "sea_water_pressure",
        mx_measurement_type = "sea_water.pressure",
        units = "dbar",
    )

    # add variables
    temperature = Variable(
        data.temperature,
        (time,),

        # priority 1
        variables = "",  # I don't understand this. XXX

        # priority 2
        #cell_methods
        long_name = "Seawater temperature",
        standard_name = "sea_water_temperature",

        # priority 3
        #comment
        mx_measurement_type = "sea_water.temperature",
        #references

        # no priority
        #add_offset = 0
        #ancillary_variables
        #cell_measures
        #coordinates
        #_FillValue
        #flag_masks
        #flag_meanings
        #flag_values
        #grid_mapping
        #instance_dimension
        institution = "Ifremer",
        #missing_value
        #sample_dimension
        #scale_factor = 1
        source = "CTD",
        #standard_error_multiplier
        units = "degC",
        valid_max = 100.,
        valid_min = -1.8,
        valid_range = (-1.8, 100.),
    )

    salinity = Variable(
        data.salinity,
        (time,),
        long_name = "Seawater salinity",
        standard_name = "sea_water_salinity",
        mx_measurement_type = "sea_water.salinity",
        institution = "Ifremer",
        source = "CTD",
        units = "psu",
    )

MarinexploreStandard.save("sample.nc")
