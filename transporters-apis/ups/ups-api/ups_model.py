import os
import pandas as pd

data_dir = '../data-output'
sending_tariffs_path = 'sending-tariffs'
zones_sending = pd.read_pickle(os.path.join(data_dir, 'zones-sending.pickle'))
# print(zones_sending.head())

tbl_df_ups_express_doc_max_2_5kg_except_ups_express_envelopes = pd.read_pickle(os.path.join(data_dir,sending_tariffs_path, 'tbl_df_ups_express_doc_max_2_5kg_except_ups_express_envelopes.pickle'))
tbl_df_ups_express_plus_doc_max_2_5kg_except_ups_express_envelopes = pd.read_pickle(os.path.join(data_dir,sending_tariffs_path, 'tbl_df_ups_express_plus_doc_max_2_5kg_except_ups_express_envelopes.pickle'))
tbl_ups_expedited_meer_dan_100kg = pd.read_pickle(os.path.join(data_dir, sending_tariffs_path, 'tbl_ups_expedited_meer_dan_100kg.pickle'))
tbl_ups_expedited_pakketten = pd.read_pickle(os.path.join(data_dir, sending_tariffs_path, 'tbl_ups_expedited_pakketten.pickle'))
tbl_ups_expres_doc_min_2_5kg_and_parcels = pd.read_pickle(os.path.join(data_dir, sending_tariffs_path, 'tbl_ups_expres_doc_min_2_5kg_and_parcels.pickle'))
tbl_ups_expres_plus_doc_min_2_5kg_and_parcels = pd.read_pickle(os.path.join(data_dir, sending_tariffs_path, 'tbl_ups_expres_plus_doc_min_2_5kg_and_parcels.pickle'))
tbl_ups_expres_saver_doc_min_2_5kg_and_parcels = pd.read_pickle(os.path.join(data_dir, sending_tariffs_path, 'tbl_ups_expres_saver_doc_min_2_5kg_and_parcels.pickle'))
tbl_ups_express_more_than_70kg = pd.read_pickle(os.path.join(data_dir, sending_tariffs_path, 'tbl_ups_express_more_than_70kg.pickle'))
tbl_ups_express_plus_more_than_70kg = pd.read_pickle(os.path.join(data_dir, sending_tariffs_path, 'tbl_ups_express_plus_more_than_70kg.pickle'))
tbl_ups_express_plus_ups_expres_envelopes = pd.read_pickle(os.path.join(data_dir, sending_tariffs_path, 'tbl_ups_express_plus_ups_expres_envelopes.pickle'))
tbl_ups_express_saver_doc_max_2_5kg_except_ups_express_envelopes = pd.read_pickle(os.path.join(data_dir, sending_tariffs_path, 'tbl_ups_express_saver_doc_max_2_5kg_except_ups_express_envelopes.pickle'))
tbl_ups_express_saver_more_than_70kg = pd.read_pickle(os.path.join(data_dir, sending_tariffs_path, 'tbl_ups_express_saver_more_than_70kg.pickle'))
tbl_ups_express_standard_een_pakketzendingen = pd.read_pickle(os.path.join(data_dir, sending_tariffs_path, 'tbl_ups_express_standard_een_pakketzendingen.pickle'))
tbl_ups_express_standard_meer_dan_200kg = pd.read_pickle(os.path.join(data_dir, sending_tariffs_path, 'tbl_ups_express_standard_meer_dan_200kg.pickle'))
tbl_ups_express_standard_multi_pakketzendingen = pd.read_pickle(os.path.join(data_dir, sending_tariffs_path, 'tbl_ups_express_standard_multi_pakketzendingen.pickle'))
tbl_ups_express_ups_expres_envelopes = pd.read_pickle(os.path.join(data_dir, sending_tariffs_path, 'tbl_ups_express_ups_expres_envelopes.pickle'))
tbl_ups_express_ups_expres_saver_envelopes = pd.read_pickle(os.path.join(data_dir, sending_tariffs_path, 'tbl_ups_express_ups_expres_saver_envelopes.pickle'))

def get_zone(country_code, service, sending):
    return sending.set_index('ISO-Code') .loc[country_code, service]

def has_added_cost(country_code, tbl):
    return '+' == tbl.set_index('ISO-Code') .loc[country_code, 'Add']

def get_row(val, series):
    for i in range(len(series)):    
        if val <= series[i]:
            return i
    raise ValueError('No row found')

def estimate_deliver_costs(charge_type, service_type, package_type, weight, zone):
    if charge_type == 0:
        print('Charge type is sending')
        cost = estimate_based_on_sending(service_type, package_type, weight, zone)
    elif charge_type == 1:
        print('Charge type is receiving')
        raise NotImplementedError('Receiving charge not implemented.')
    else:
        raise ValueError('Unkown charge type')
    return cost 

def get_cost_at(weight, zone, tbl):
    idx = get_row(weight, list(tbl.index))
    return tbl.iloc[idx][zone]

def compute_cost_by_weight_with_minimum(weight, zone, tbl):
    price_per_kg = tbl.loc['Prijs per kg', zone]
    return max(price_per_kg * weight, tbl.loc['Minimumtarief', zone]) 


def estimate_based_on_UPS_Express_Parcel(weight, zone):
    if weight <= 2.5:
        cost = get_cost_at(weight, zone, tbl_df_ups_express_doc_max_2_5kg_except_ups_express_envelopes)
        # raise ValueError('Parcel below 2.5 kg is not accepted.')
    elif weight > 2.5 and weight <= 70.0:
        cost = get_cost_at(weight, zone, tbl_ups_expres_doc_min_2_5kg_and_parcels)
    elif weight > 70.0:
        cost = compute_cost_by_weight_with_minimum(weight, zone, tbl_ups_express_more_than_70kg)
    return cost

def estimate_based_on_UPS_Express_Document(weight, zone):
    if weight <= 2.5:
       cost = get_cost_at(weight, zone, tbl_df_ups_express_doc_max_2_5kg_except_ups_express_envelopes) 
    elif weight > 2.5 and weight <= 70.0:
        cost = get_cost_at(weight, zone, tbl_ups_expres_doc_min_2_5kg_and_parcels)
    elif weight > 70.0:
        cost = compute_cost_by_weight_with_minimum(weight, zone, tbl_ups_express_more_than_70kg)
    return cost

def estimate_based_on_UPS_Express_Envelopes(weight, zone):    
    return tbl_ups_express_ups_expres_envelopes.loc[0,zone]    

def estimate_based_on_UPS_Express(package_type, weight, zone):
    if package_type == 'envelope':
        cost = estimate_based_on_UPS_Express_Envelopes(weight, zone)
    elif package_type == 'document':
        cost = estimate_based_on_UPS_Express_Document(weight, zone)
    elif package_type == 'parcel':
        cost = estimate_based_on_UPS_Express_Parcel(weight, zone)
    else:
        raise ValueError('Unknown value for package_type')

    return cost

def estimate_based_on_UPS_Express_Plus_Parcel(weight, zone):
    if weight <= 2.5:
       cost = get_cost_at(weight, zone, tbl_df_ups_express_plus_doc_max_2_5kg_except_ups_express_envelopes) 
    elif weight > 2.5 and weight <= 70.0:
        cost = get_cost_at(weight, zone, tbl_ups_expres_plus_doc_min_2_5kg_and_parcels)
    elif weight > 70.0:
        cost = compute_cost_by_weight_with_minimum(weight, zone, tbl_ups_express_plus_more_than_70kg)
    return cost

def estimate_based_on_UPS_Express_Plus_Document(weight, zone):
    if weight <= 2.5:
       cost = get_cost_at(weight, zone, tbl_df_ups_express_plus_doc_max_2_5kg_except_ups_express_envelopes) 
    elif weight > 2.5 and weight <= 70.0:
        cost = get_cost_at(weight, zone, tbl_ups_expres_plus_doc_min_2_5kg_and_parcels)
    elif weight > 70.0:
        cost = compute_cost_by_weight_with_minimum(weight, zone, tbl_ups_express_plus_more_than_70kg)
    return cost

def estimate_based_on_UPS_Express_Plus_Envelopes(weight, zone):    
    return tbl_ups_express_plus_ups_expres_envelopes.loc[0,zone]  

def estimate_based_on_UPS_Express_Plus(package_type, weight, zone): 
    if package_type == 'envelope':
        cost = estimate_based_on_UPS_Express_Plus_Envelopes(weight, zone)
    elif package_type == 'document':
        cost = estimate_based_on_UPS_Express_Plus_Document(weight, zone)
    elif package_type == 'parcel':
        cost = estimate_based_on_UPS_Express_Plus_Parcel(weight, zone)
    else:
        raise ValueError('Unknown value for package_type')
    return cost

def estimate_based_on_UPS_Express_Saver_Envelopes(weight, zone):    
    return tbl_ups_express_ups_expres_saver_envelopes.loc[0,zone]  

def estimate_based_on_UPS_Express_Saver_Document(weight, zone):
    if weight <= 2.5:
       cost = get_cost_at(weight, zone, tbl_df_ups_express_plus_doc_max_2_5kg_except_ups_express_envelopes) 
    elif weight > 2.5 and weight <= 70.0:
        cost = get_cost_at(weight, zone, tbl_ups_expres_saver_doc_min_2_5kg_and_parcels)
    elif weight > 70.0:
        cost = compute_cost_by_weight_with_minimum(weight, zone, tbl_ups_express_saver_more_than_70kg)
    return cost

def estimate_based_on_UPS_Express_Saver_Parcel(weight, zone):
    if weight <= 2.5:
       cost = get_cost_at(weight, zone, tbl_df_ups_express_plus_doc_max_2_5kg_except_ups_express_envelopes) 
    elif weight > 2.5 and weight <= 70.0:
        cost = get_cost_at(weight, zone, tbl_ups_expres_saver_doc_min_2_5kg_and_parcels)
    elif weight > 70.0:
        cost = compute_cost_by_weight_with_minimum(weight, zone, tbl_ups_express_saver_more_than_70kg)
    return cost

def estimate_based_on_UPS_Express_Saver(package_type, weight, zone):
    if package_type == 'envelope':
        cost = estimate_based_on_UPS_Express_Saver_Envelopes(weight, zone)
    elif package_type == 'document':
        cost = estimate_based_on_UPS_Express_Saver_Document(weight, zone)
    elif package_type == 'parcel':
        cost = estimate_based_on_UPS_Express_Saver_Parcel(weight, zone)
    else:
        raise ValueError('Unknown value for package_type')
    return cost
    

def estimate_based_on_UPS_Standard_Een_Pakketzendingen(weight, zone):    
    return get_cost_at(weight, zone, tbl_ups_express_standard_een_pakketzendingen) 

def estimate_based_on_UPS_Standard_Multi_Pakketzendingen(weight, zone):    
    return get_cost_at(weight, zone, tbl_ups_express_standard_multi_pakketzendingen) 

def estimate_based_on_UPS_Standard_Meer_dan_200kg(weight, zone):
    return max(weight * tbl_ups_express_standard_meer_dan_200kg.loc['Prijs per kg', zone],  tbl_ups_express_standard_meer_dan_200kg.loc['Minimumtarief', zone])

def estimate_based_on_UPS_Standard(package_type, weight, zone):
    if weight <= 200.0:
        if package_type == 'een-pakketzendingen':
            cost = estimate_based_on_UPS_Standard_Een_Pakketzendingen(weight, zone)
        elif package_type == 'multi-pakketzendingen':
            cost = estimate_based_on_UPS_Standard_Multi_Pakketzendingen(weight, zone)
        else:
           raise ValueError('Unknown value for package_type') 
    else:
        cost = estimate_based_on_UPS_Standard_Meer_dan_200kg(weight, zone)    
    return cost

def estimate_based_on_UPS_Expedited_Pakketten(weight, zone):    
    return get_cost_at(weight, zone, tbl_ups_expedited_pakketten) 

def estimate_based_on_UPS_Expedited_Meer_dan_100kg(weight, zone):
    return max(weight * tbl_ups_expedited_meer_dan_100kg.loc['Prijs per kg', zone],  tbl_ups_expedited_meer_dan_100kg.loc['Minimumtarief', zone])

def estimate_based_on_UPS_Expedited(package_type, weight, zone):
    if weight <= 100.0: 
        if package_type == 'pakketten':       
            cost = estimate_based_on_UPS_Expedited_Pakketten(weight, zone)        
        else:
            raise ValueError('Does not know package type ' + package_type)
    else:
        cost = estimate_based_on_UPS_Expedited_Meer_dan_100kg(weight, zone)    
    return cost

def estimate_based_on_sending(service_type, package_type, weight, zone):
    if service_type == 'UPS Express':
        cost = estimate_based_on_UPS_Express(package_type, weight, zone)
    elif service_type == 'UPS Express Plus':
        cost = estimate_based_on_UPS_Express_Plus(package_type, weight, zone)
    elif service_type == 'UPS Express Saver':
        cost = estimate_based_on_UPS_Express_Saver(package_type, weight, zone)
    elif service_type == 'UPS Standard':
        cost = estimate_based_on_UPS_Standard(package_type, weight, zone)
    elif service_type == 'UPS Expedited':
        cost = estimate_based_on_UPS_Expedited(package_type, weight, zone)
    else:
        raise NotImplementedError('UPS Express not implemented for service type ' + service_type)
    return cost

def get_ups_countries_sending():   
    data = zones_sending.loc[:,['Land', 'name', 'ISO-Code']]
    return data.to_json(orient="records")



def main():
    pass
    # print(zones_sending)
    # print(tbl_ups_expedited_meer_dan_100kg)
    del_costs = estimate_deliver_costs(0, 'UPS Express','envelope', 20.0, '51')
    print(del_costs)


if __name__ == '__main__':
    main()