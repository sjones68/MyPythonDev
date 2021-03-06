# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# shCreateFeatureClassInScracth.py
# Created on: 2014-12-19 16:26:26.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy


arcpy.env.overwriteOutput = 1

# Local variables:
AucklandStravaMetro_Edges_NZTM = "D:\\TEMP\\scratch.gdb\\AucklandStravaMetro_Edges_NZTM"
CycleEvents = "D:\\TEMP\\scratch.gdb\\CycleEvents"
AllCycleEventsIn2013 = "AllCycleEventsIn2013"
AllCycleEventsIn2013FC = "D:\\TEMP\\scratch.gdb\\AllCycleEvents"

# Process: Make Query Table
arcpy.MakeQueryTable_management("D:\\TEMP\\scratch.gdb\\AucklandStravaMetro_Edges_NZTM;D:\\TEMP\\scratch.gdb\\CycleEvents", AllCycleEventsIn2013, "ADD_VIRTUAL_KEY_FIELD", "", "AucklandStravaMetro_Edges_NZTM.OBJECTID #;AucklandStravaMetro_Edges_NZTM.ID #;AucklandStravaMetro_Edges_NZTM.OSM_ID #;AucklandStravaMetro_Edges_NZTM.OSM_NAME #;AucklandStravaMetro_Edges_NZTM.OSM_META #;AucklandStravaMetro_Edges_NZTM.OSM_SOURCE #;AucklandStravaMetro_Edges_NZTM.OSM_TARGET #;AucklandStravaMetro_Edges_NZTM.CLAZZ #;AucklandStravaMetro_Edges_NZTM.FLAGS #;AucklandStravaMetro_Edges_NZTM.SOURCE #;AucklandStravaMetro_Edges_NZTM.TARGET #;AucklandStravaMetro_Edges_NZTM.KM #;AucklandStravaMetro_Edges_NZTM.KMH #;AucklandStravaMetro_Edges_NZTM.COST #;AucklandStravaMetro_Edges_NZTM.REVERSE_CO #;AucklandStravaMetro_Edges_NZTM.X1 #;AucklandStravaMetro_Edges_NZTM.Y1 #;AucklandStravaMetro_Edges_NZTM.X2 #;AucklandStravaMetro_Edges_NZTM.Y2 #;AucklandStravaMetro_Edges_NZTM.OID_1 #;AucklandStravaMetro_Edges_NZTM.EDGE_ID #;AucklandStravaMetro_Edges_NZTM.TRIDERCNT #;AucklandStravaMetro_Edges_NZTM.TRRIDERCNT #;AucklandStravaMetro_Edges_NZTM.TRIDECNT #;AucklandStravaMetro_Edges_NZTM.TRRIDECNT #;AucklandStravaMetro_Edges_NZTM.BIKECNT #;AucklandStravaMetro_Edges_NZTM.BIKETIME #;AucklandStravaMetro_Edges_NZTM.RBIKETIME #;AucklandStravaMetro_Edges_NZTM.COMMUTECNT #;AucklandStravaMetro_Edges_NZTM.AMRIDER #;AucklandStravaMetro_Edges_NZTM.AMRRIDER #;AucklandStravaMetro_Edges_NZTM.AMRIDE #;AucklandStravaMetro_Edges_NZTM.AMRRIDE #;AucklandStravaMetro_Edges_NZTM.AMBIKECNT #;AucklandStravaMetro_Edges_NZTM.AMBIKET #;AucklandStravaMetro_Edges_NZTM.AMRBIKET #;AucklandStravaMetro_Edges_NZTM.AMCOMMUTE #;AucklandStravaMetro_Edges_NZTM.PMRIDER #;AucklandStravaMetro_Edges_NZTM.PMRRIDER #;AucklandStravaMetro_Edges_NZTM.PMRIDE #;AucklandStravaMetro_Edges_NZTM.PMRRIDE #;AucklandStravaMetro_Edges_NZTM.PMBIKECNT #;AucklandStravaMetro_Edges_NZTM.PMBIKET #;AucklandStravaMetro_Edges_NZTM.PMRBIKET #;AucklandStravaMetro_Edges_NZTM.PMCOMMUTE #;AucklandStravaMetro_Edges_NZTM.IPRIDER #;AucklandStravaMetro_Edges_NZTM.IPRRIDER #;AucklandStravaMetro_Edges_NZTM.IPRIDE #;AucklandStravaMetro_Edges_NZTM.IPRRIDE #;AucklandStravaMetro_Edges_NZTM.IPBIKECNT #;AucklandStravaMetro_Edges_NZTM.IPBIKET #;AucklandStravaMetro_Edges_NZTM.IPRBIKET #;AucklandStravaMetro_Edges_NZTM.IPCOMMUTE #;AucklandStravaMetro_Edges_NZTM.Shape #;CycleEvents.OBJECTID #;CycleEvents.edge_id #;CycleEvents.year #;CycleEvents.day #;CycleEvents.hour #;CycleEvents.minute #;CycleEvents.athlete_count #;CycleEvents.rev_athlete_count #;CycleEvents.activity_count #;CycleEvents.rev_activity_count #;CycleEvents.total_activity_count #;CycleEvents.activity_time #;CycleEvents.rev_activity_time #;CycleEvents.commute_count #;CycleEvents.activity_count_norm #", "CycleEvents.edge_id = AucklandStravaMetro_Edges_NZTM.EDGE_ID")

# Process: Copy Features
arcpy.CopyFeatures_management(AllCycleEventsIn2013, AllCycleEventsIn2013FC, "", "0", "0", "0")

