import geopandas as gpd
import pandas as pd


def arealwt(source, target, cols = [None], suffix = ''):
    """
    Interpolates values from source polygons into target polygons using simple
    areal weighting.
    Parameters
    ----------
    source : DataFrame
        Dataframe with values for interpolation.
    target : DataFrame
        DataFrame with polygons obtaining interpolated values.
    cols : list
        Column(s) from source to be interpolated. 
    suffix : str, optional
        New name for interpolated columns. The default is ''.
    Returns
    -------
    final : Dataframe
        Target dataframe with interpolated columns added.
    """
    #reindex for sum of interpolated results to merge later
    target['_index'] = target.index
    
    #calculate source areas
    print("calculating source area")
    source['source_area'] = source.geometry.area
    
    #intersect source and target
    print("calculating target area")
    joined1 = gpd.overlay(source, target, how = 'intersection')
    
    #calculate intersected areas
    print("calculating intersected area")
    joined1['intersect_area'] = joined1.geometry.area
    
    #calculate areal weight per intersected polygon
    print("calculating areal weight")
    joined1["AREAL_WT"] = joined1['intersect_area'] / joined1['source_area']    
    
    #interpolate designated columns, create list to include in target dataframe
    print("interpolating designated fields")
    new_cols = []
    for col in cols:
        new_col = col + suffix
        new_cols.append(new_col)
        joined1[new_col] = joined1["AREAL_WT"] * joined1[col]
    
    #merge interpolated results to target dataframe
    print("merging results")
    results = joined1.groupby('_index').sum()
    final = pd.merge(target, results[new_cols], on='_index')
    del final['_index']
    return final

def binary_vector(source, ancillary, exclude_col=(), 
                  exclude_val= [None], suffix= '', cols= [None]):
    """Calculates areal weight using the binary dasymmetric method.
    
    :param source: Name of Dataframe that contains values that should be interpolated
    :type source: string
    :param ancillary: Name of dataframe containing ancillary geometry data, used to mask source dataframe
    :type ancillary: string
    :param exclude_col: Column name from ancillary dataframe that contains exclusionary values
    :type exclude_col: string
    :param exclude_val: Values from exclude_col that should be removed during binary mask operation
    :type exclude_val: list
    :param suffix: Suffix that should be added to the column names that are interpolated
    :type suffix: string
    :param cols: Column names that should be interpolated
    :type cols: list
    
    :return: Source dataframe with interpolated columns added
    :rtype: dataframe
    """    
    # index group 
    source['division'] = source.index
           
    #drop excluded rows from ancillary data
    print("masking")
    binary_mask = ancillary[exclude_col].isin(exclude_val)
    ancillary = ancillary[~binary_mask]
    
    #drop all columns except geometry before join (don't want data from ancillary in final df)
    ancillary = ancillary[['geometry']]
          
    #intersect source file and ancillary file
    print("overlaying shapefiles")
    mask = gpd.overlay(source, ancillary, how='intersection')
    
    #calculate and store areas of intersected zone
    print("calculating intersected areas")
    mask['intersectarea'] = (mask.area)  

    #calculate sum of polygon areas by tract
    masksum = mask.groupby('division')['intersectarea'].sum()
    
    # merge summmed areas back to main dataframe
    print("merging dataframes")
    target = mask.merge(masksum, on='division')
    
    # calculate areal weight of areas
    print("calculating areal weight")
    target["AREAL_WT"] = target['intersectarea_x'] / target['intersectarea_y']

    # loop through columns that user wants to interpolate, add suffix
    new_cols = []
    for col in cols:
        new_col = col + suffix
        new_cols.append(new_col)
        target[new_col] = target["AREAL_WT"] * target[col]
    
    # drop generated columns
    output = target
    output = output.drop(['division','intersectarea_x','intersectarea_y', 'AREAL_WT'], axis=1)
    return output

def parcel_method(zone, parcel, tu_col, ru_col, ba_col, ra_col, cols = [None]):     
   
    """Interpolates values using the parcel based method.
    
    :param zone: DataFrame to be interpolated
    :type zone: DataFrame
    :param parcel: Parcel DataFrame
    :type parcel: DataFrame
    :param tu_col: Column name from parcel DataFrame containing total number of units
    :type tu_col: string
    :param ru_col: Column name from parcel DataFrame containing number of residential units
    :type ru_col: string
    :param ba_col: Column name from parcel DataFrame containing building area
    :type ba_col: string
    :param ra_col: Column name from parcel DataFrame containing residential area
    :type ra_col: string
    :param cols: Column names from Zone DataFrame containing values to interpolate. Can accept one or more columns.
    :type intp_col: list
    
    :return: The parcel level DataFrame with two interpolated fields added for each column of input: One derived from residential units, and another derived from adjusted residential area
    :rtype: DataFrame
    """    
    
    # make copies of zone and parcel dataframes
    ara_parcel = parcel.copy()
    zonecopy = zone.copy()
    
    # calculate ara for parcels
    print("calculating adjusted residential area")
    ara_parcel['M'] = ara_parcel.apply(lambda x: 1 if x[ra_col]==0 and x[ru_col] !=0 else 0, axis=1)
    ara_parcel['ara'] = (ara_parcel['M'] *((ara_parcel[ba_col] * ara_parcel[ru_col]) / ara_parcel[tu_col])) + ara_parcel[ra_col]
    
    # sum ara for zone
    print("summing adjusted residential area")
    zonecopy['_bindex'] = zonecopy.index
    ara_zone = gpd.overlay(zonecopy, ara_parcel, how='intersection')
    ara_zone = ara_zone.groupby('_bindex')['ara'].sum().reset_index(name='ara_zone')         
            
    # calculate RU for zone
    print("calculating residential units")
    ru_zone = gpd.overlay(zonecopy, parcel, how='intersection')
    ru_zone = ru_zone.groupby('_bindex')[ru_col].sum().reset_index(name='ru_zone')  
    
    # Calculate dasymetrically derived populations based on RU and ara
    print("interpolating based on residential units")
    intp_zone = gpd.overlay(zonecopy, ara_parcel, how='intersection')
    intp_zone = intp_zone.merge(ru_zone, on='_bindex')
    intp_zone = intp_zone.merge(ara_zone, on='_bindex')
    new_cols = []
    for col in cols:
        new_col = 'ru_derived_' + col 
        new_cols.append(new_col)
        intp_zone[new_col] = intp_zone[col] * intp_zone[ru_col] / intp_zone['ru_zone']
    print("interpolating based on adjusted residential area")
    new_cols = []    
    for col in cols:
        new_col = 'ara_derived_' + col 
        new_cols.append(new_col)
        intp_zone[new_col] = intp_zone[col] * intp_zone['ara'] / intp_zone['ara_zone']
    
    # drop generated columns that were just for calculations and indexing
    intp_zone.drop(['M', '_bindex', 'ara', 'ru_zone', 'ara_zone'], axis=1, inplace = True)
    return intp_zone

def expert_system(large_zone, small_zone, parcel, tu_col, ru_col, ba_col, ra_col, intp_col):
        
    """Determines whether to use the residential unit or adjusted residential area dasymetric calculations
    for the parcel based method based on the expert system implementation. 
    Large and small interpolation zones must share the same column names for columns used in the arguments.
    Small intepolation zones must nest within large interpolation zones.
    
    :param large_zone: DataFrame with larger geography
    :type large_zone: Dataframe
    :param small_zone: DataFrame with smaller geography
    :type small_zone: Dataframe
    :param parcel: Parcel DataFrame
    :type parcel: DataFrame
    :param tu_col: Column name from parcel DataFrame containing total number of units
    :type tu_col: string
    :param ru_col: Column name from parcel DataFrame containing number of residential units
    :type ru_col: string
    :param ba_col: Column name from parcel DataFrame containing building area
    :type ba_col: string
    :param ra_col: Column name from parcel DataFrame containing residential area
    :type ra_col: string
    :param intp_col: Column name from Zone DataFrame containing values to interpolate. Only accepts one column
    :type intp_col: string
    
    :return: Dataframe at parcel level containing interpolated values based on expert system implementation
    :rtype: dataframe
    """    
    
    # index small_zone
    small_zone['index_s'] = small_zone.index
    
    # call parcel method on large interpolation zone
    print("performing parcel method on large zone")
    expert_large = parcel_method(large_zone, parcel, tu_col, ru_col, ba_col, ra_col, [intp_col])    
    # call parcel method on small interpolation zone
    print("performing parcel method on small zone")
    expert_small = parcel_method(small_zone, parcel, tu_col, ru_col, ba_col, ra_col, [intp_col])
       
    # overlay the interpolated large zone with small zone, so that it can later by grouped by small zone index
    print("overlaying shapefiles")
    expert = gpd.overlay(expert_large, small_zone, how='intersection')
    
    # sum ara at small zone level
    print("summing adjusted residential area at small zone")
    expert_ara = expert.groupby('index_s')['ara_derived_' + intp_col].sum().reset_index(name='expert_ara')    
    # sum ru at small zone level
    print("summing residential units at small zone")
    expert_ru = expert.groupby('index_s')['ru_derived_' + intp_col].sum().reset_index(name='expert_ru')
    
    # merge ru and ara into same dataframe
    print("merging dataframes")
    expert_parcel = expert_ara.merge(expert_ru, on = 'index_s')
    
    # pop diff calculation
    print("calculating absolute values")
    expert_parcel['ara_diff'] = abs(expert_small[intp_col] - expert_parcel['expert_ara'])
    expert_parcel['ru_diff'] = abs(expert_small[intp_col] - expert_parcel['expert_ru'])
    
    # merge the aggregated data back with the small zone interpolated parcel dataframe
    print("merging dataframes")
    expert_parcel = expert_small.merge(expert_parcel, on='index_s')
    
    # apply the expert system
    expert_parcel['expert_system_interpolation'] = expert_parcel.apply(lambda x: x['ru_derived_' + intp_col] 
                                                           if x['ru_diff']<=x['ara_diff']
                                                           else x['ara_derived_' + intp_col], axis=1)
    expert_parcel.drop(['index_s', 'expert_ara', 'expert_ru', 'ara_diff', 'ru_diff'], axis=1, inplace = True)
    return expert_parcel

def  lim_var(source, ancillary, class_col, class_dict, cols = [None], source_identifier = '', suffix = ''):
    """
    Interpolates values into disaggregated source polygons using limiting variable method 
    with ancillary data. Thresholds are set for desired area-class categories.  Remaining
    values are interpolated into area-class(es) with threshold designated as 0 or None.  Area
    classes with no intended data should be left out of dictionary.
    
    Parameters
    ----------
    source : DataFrame
        DataFrame with values for interpolation.
    ancillary : DataFrame
        DataFrame with area-class map categories.
    class_col : str
        Area-class categories.
    class_dict : dict
        Area-class categories with assigned thresholds per square unit. 
        Classes with no threshold should be assigned None.
        Classes with no data should not be included in dictionary.
    cols : list
        Column(s) from source to be interpolated.
    source_identifier : str, optional
        Column that identifies source polygons. The default is ''.
    suffix : str, optional
        New name for interpolated columns. The default is ''.
    Returns
    -------
    target : DataFrame
        Target dataframe with interpolated columns.
    """
    #calculate source area
    print("calculating source area")
    source['source_area'] = source.geometry.area
    
    #reindex for summing excess data and used area per source polygon
    source['_index'] = source.index
    
    #intersect source and ancillary
    print("overlaying shapefiles")
    join1 = gpd.overlay(source, ancillary, how='intersection')
    
    #calculate intersected areas
    print("calculating intersected areas")
    join1['intersect_area']=join1.geometry.area
    
    #Assign thresholds to area classes
    print("assigning thresholds to area classes")
    for key, value in class_dict.items():
        join1.loc[join1[class_col]== key, 'threshold']=value
    
    #start interpolation for designated columns; create new_cols for target dataframe
    new_cols = []
    for col in cols:
        source_copy = col + 'copy'
        if suffix:
            new_col = col + suffix
        else:
            new_col = '_' + col
        new_cols.append(new_col)
        
        #calculate areal weight
        print("calculating areal weight")
        join1['arealwt']=join1['intersect_area']/join1['source_area']
    
        #copy column for interpolation (lambda in loop doesn't work first time without this)
        join1[source_copy] = join1[col]
        
        #set new_col to 0 (lambda in loop doesn't work first time without this)
        join1[new_col] = 0
        
        #create used area column - move area that will never be used
        join1['used_area'] = join1.apply(lambda x: x['intersect_area'] if x[class_col] not in class_dict.keys() else 0, axis=1)
    
        #create copy of class_dict for multiple columns, drop values of None
        class_dict_copy = {key:val for key, val in class_dict.items() if val != None and val != 0}
        
        print("performing interpolation")
        while class_dict_copy != {}:
        
            #interpolate
            join1[new_col] = join1.apply(lambda x: x['arealwt']*x[source_copy] if x[class_col] == min(class_dict_copy, key = class_dict_copy.get) else x[new_col], axis=1)
        
            #if new column exceeds threshold, new column gets threshold density
            join1[new_col] = join1[new_col].clip(upper = join1['threshold']*join1['intersect_area'])
               
            #add up successfully interpolated data and decrement
            totals = join1.groupby('_index')[new_col].sum()
            totals.rename('temp_sum', inplace=True)
            join1 = join1.merge(totals, on='_index')
            join1[source_copy] = join1[col] - join1['temp_sum']
            
            #copy used area for decrementing
            join1['used_area'] = join1.apply(lambda x: x['intersect_area'] if x[class_col] == min(class_dict_copy, key = class_dict_copy.get) else x['used_area'], axis=1)
            
            #add up successfully interpolated areas and decrement 
            totals2 = join1.groupby('_index')['used_area'].sum()
            totals2.rename('temp_area_sum', inplace=True)
            join1 = join1.merge(totals2, on ='_index')
            join1['source_area_copy'] = join1['source_area'] - join1['temp_area_sum']
            
            #recalculate areal weight
            join1['arealwt'] = join1['intersect_area']/join1['source_area_copy']
            
            #remove tempsum
            del join1['temp_sum']
            
            #remove temp_area_sum
            del join1['temp_area_sum']
            
            #remove minimum from dictionary
            del class_dict_copy[min(class_dict_copy, key = class_dict_copy.get)]

        #replace null values with 0 for classes with no restriction
        join1.fillna(0, inplace=True)
        
        #interpolate least restrictive
        join1[new_col] = join1.apply(lambda x: x['arealwt']*x[source_copy] if x[class_col] in class_dict and x['threshold'] == 0 else x[new_col], axis=1)

    #filter target dataframe
    if source_identifier:
        target = join1[[source_identifier, class_col, "geometry", *new_cols]]
    else:
        target = join1[[class_col, "geometry", *new_cols]]
        
    return target

def n_class(source, ancillary, class_col, class_dict, cols = [None], source_identifier = '', suffix = ''):
    """
    Interpolates values into disaggregated source polygons using n_class method with ancillary data.  
    Parameters
    ----------
    source : DataFrame
        DataFrame with values for interpolation.
    ancillary : DataFrame
        DataFrame with area-class map categories.
    class_col : str
        Area-class categories.
    class_dict : dict
        Area-class categories with assigned percentages.
    cols : list
        Column(s) from source to be interpolated.
    source_identifier : str, optional
        Column that identifies source polygons. The default is ''.
    suffix : str, optional
        New name for interpolated columns. The default is ''.
    Returns
    -------
    target : DataFrame
        Target dataframe with interpolated columns.
    """
    #calculate source area
    print("calculating source area")
    source['source_area'] = source.geometry.area
    
    #reindex source for grouping sums later
    source['_index'] = source.index
    
    #assign percentages to landuse classes
    print("assigning percentages to classes")
    for key, value in class_dict.items():
        ancillary.loc[ancillary[class_col]== key, '_percent']=value
    
    #intersect source and ancillary data
    print("overlaying shapefiles")
    join1 = gpd.overlay(source, ancillary, how='intersection')
    
    #calculate intersected areas
    print("calculating intersected area")
    join1['intersect_area']=join1.geometry.area
    
    #calculate areal weight
    print("calculating areal weight")
    join1['arealwt']=join1['intersect_area']/join1['source_area']
    
    #multiply areal weight by user defined percentages
    print("modifying areal weight based on class percentages")
    join1['class_weight']=join1['_percent'] * join1['arealwt']
    
    #sum of areal weight times percentage per source polygon
    print("summing for source polygons")
    totals = join1.groupby('_index')['class_weight'].sum()
    totals.rename('temp_sum', inplace=True)
    join1 = join1.merge(totals, on ='_index')
    
    #fraction for interpolation
    join1['class_frac'] = join1['class_weight']/join1['temp_sum']
    
    #interpolate designated columns, create list to include in final dataframe
    print("interpolating designated fields")
    new_cols = []
    for col in cols:
        new_col = col + suffix
        new_cols.append(new_col)
        join1[new_col] = join1['class_frac']*join1[col]
    
    #filter target dataframe
    if source_identifier:
        target = join1[[source_identifier, class_col, "geometry", *new_cols]]
    else:
        target = join1[[class_col, "geometry", *new_cols]]
      
    return target