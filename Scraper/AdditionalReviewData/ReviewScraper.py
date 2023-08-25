import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import os

original_hotel_links = ['https://www.tripadvisor.com/Hotel_Review-g29092-d75532-Reviews-The_Anaheim_Hotel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d19842738-Reviews-The_Westin_Anaheim_Resort-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d78944-Reviews-Grand_Legacy_At_The_Park-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75680-Reviews-Howard_Johnson_by_Wyndham_Anaheim_Hotel_and_Water_Playground-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d240870-Reviews-Capri_Laguna_On_The_Beach-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d10372357-Reviews-Candlewood_Suites_Anaheim_Resort_Area_an_IHG_Hotel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d8072745-Reviews-Homewood_Suites_by_Hilton_Anaheim_Resort_Convention_Center-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d77481-Reviews-The_Inn_At_Laguna_Beach-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d281302-Reviews-Cortona_Inn_Suites_Anaheim_Resort-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d73678-Reviews-La_Casa_del_Camino-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d4860373-Reviews-SpringHill_Suites_by_Marriott_Anaheim_Maingate-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75677-Reviews-Hotel_Indigo_Anaheim_an_IHG_Hotel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d285523-Reviews-Pacific_Edge_Hotel-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d222948-Reviews-Holiday_Inn_Suites_Anaheim_1_Blk_Disneyland-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d217214-Reviews-Sheraton_Park_Hotel_at_the_Anaheim_Resort-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d77484-Reviews-Surf_Sand_Resort-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75525-Reviews-Hilton_Anaheim-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d222952-Reviews-Kings_Inn_Anaheim-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75784-Reviews-Tropicana_Inn_Suites-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32589-d662460-Reviews-Laguna_Hills_Lodge-Laguna_Hills_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d601379-Reviews-DoubleTree_Suites_by_Hilton_Hotel_Anaheim_Resort_Convention_Center-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d225491-Reviews-Sonesta_Simply_Suites_Orange_County_Airport-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d225014-Reviews-Anaheim_Majestic_Garden_Hotel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d555840-Reviews-Lemon_Tree_Hotel_and_Suites-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75493-Reviews-Four_Points_by_Sheraton_Anaheim-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75502-Reviews-Embassy_Suites_by_Hilton_Anaheim_North-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32589-d77488-Reviews-Sonesta_Select_Laguna_Hills_Irvine_Spectrum-Laguna_Hills_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d8704117-Reviews-Castaway_Motel-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d76650-Reviews-La_Quinta_Inn_by_Wyndham_Costa_Mesa_Newport_Beach-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33198-d271588-Reviews-Key_Inn-Tustin_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d217219-Reviews-Hyatt_Regency_Orange_County-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32279-d224779-Reviews-Waldorf_Astoria_Monarch_Beach-Dana_Point_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d15588914-Reviews-Hampton_Inn_Suites_Anaheim_Resort_Convention_Center-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d252509-Reviews-Hyatt_Regency_Huntington_Beach_Resort_Spa-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d9566846-Reviews-Pasea_Hotel_Spa-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75490-Reviews-Castle_Inn_Suites-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d11679262-Reviews-SunCoast_Park_Hotel_Anaheim_Tapestry_Collection_by_Hilton-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33067-d82132-Reviews-The_Pacific_Inn-Seal_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d225008-Reviews-Ayres_Hotel_Anaheim-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d113856-Reviews-Fairfield_by_Marriott_Anaheim_Resort-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d76237-Reviews-DoubleTree_by_Hilton_Buena_Park-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d119488-Reviews-Laguna_Beach_House-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d17738446-Reviews-Cambria_Hotel_Suites_Anaheim_Resort_Area-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d119437-Reviews-Anaheim_Marriott-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32279-d76716-Reviews-Dana_Point_Marina_Inn-Dana_Point_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75726-Reviews-Clementine_Hotel_Suites_Anaheim-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d486918-Reviews-Laguna_Riviera-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d239350-Reviews-Best_Western_Plus_Park_Place_Inn_Mini_Suites-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d225493-Reviews-La_Quinta_Inn_Suites_by_Wyndham_Orange_County_Airport-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d19266128-Reviews-JW_Marriott_Anaheim_Resort-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75732-Reviews-Super_8_by_Wyndham_Anaheim_Disneyland_Drive-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d21373092-Reviews-Travel_Inn_Motel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d1395212-Reviews-Riviera_Motel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d558850-Reviews-Huntington_Beach_Inn-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d4232816-Reviews-Best_Inn_and_Suites_Buena_Park-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d223234-Reviews-Sonesta_Anaheim_Resort_Area-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d78985-Reviews-Quality_Inn_Suites_Maingate-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d77298-Reviews-Hotel_Huntington_Beach-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d5462084-Reviews-Rainbow_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d506378-Reviews-Anaheim_Executive_Inn_Suites-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d10259462-Reviews-Hyatt_House_at_Anaheim_Resort_Convention_Center-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d8019374-Reviews-Courtyard_by_Marriott_Anaheim_Theme_Park_Entrance-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d119385-Reviews-Casa_Laguna_Hotel_Spa-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d23155746-Reviews-Hotel_Lulu-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d1231115-Reviews-Kimpton_Shorebreak_Huntington_Beach_Resort-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d13156370-Reviews-Hampton_Inn_Suites_Irvine_Orange_County_Airport-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d208755-Reviews-Disney_s_Grand_Californian_Hotel_Spa-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d78657-Reviews-VEA_Newport_Beach_A_Marriott_Resort_Spa-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32406-d5274418-Reviews-Ayres_Hotel_Fountain_Valley-Fountain_Valley_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d225743-Reviews-Anaheim_Marriott_Suites-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75522-Reviews-Desert_Palms_Hotel_Suites-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75661-Reviews-Eden_Roc_Inn_Suites-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d10517842-Reviews-Residence_Inn_by_Marriott_at_Anaheim_Resort_Convention_Center-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d20483506-Reviews-The_Viv_Hotel_Anaheim_a_Tribute_Portfolio_Hotel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d78769-Reviews-Peacock_Suites-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d8778649-Reviews-Great_Wolf_Lodge_Southern_California_Garden_Grove-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32279-d499011-Reviews-The_Beachfront_Inn_Suites_At_Dana_Point-Dana_Point_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d77306-Reviews-The_Waterfront_Beach_Resort_a_Hilton_Hotel-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d7802561-Reviews-Holiday_Inn_Express_Suites_Anaheim_Resort_Area_an_IHG_Hotel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32591-d239825-Reviews-Ayres_Hotel_Laguna_Woods-Laguna_Woods_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32722-d1554686-Reviews-Ayres_Suites_Mission_Viejo-Mission_Viejo_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d119415-Reviews-Anaheim_Portofino_Inn_Suites-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d1216751-Reviews-Holiday_Inn_Express_San_Clemente_N_Beach_Area-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d263459-Reviews-Americas_Best_Value_Inn_Suites_Anaheim_Convention_Center-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d607413-Reviews-Courtyard_by_Marriott_Anaheim_Resort_Convention_Center-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d78214-Reviews-Embassy_Suites_by_Hilton_Anaheim_Orange-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d78671-Reviews-Renaissance_Newport_Beach_Hotel-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d84025-Reviews-Newport_Beach_Marriott_Bayview-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32406-d84020-Reviews-Sonesta_ES_Suites_Huntington_Beach_Fountain_Valley-Fountain_Valley_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32406-d76968-Reviews-Sonesta_Select_Huntington_Beach_Fountain_Valley-Fountain_Valley_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75513-Reviews-Alamo_Inn_Suites-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d6609508-Reviews-Hyatt_Place_at_Anaheim_Resort_Convention_Center-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d209310-Reviews-Delta_Hotels_by_Marriott_Anaheim_Garden_Grove-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d1146335-Reviews-The_Resort_at_Pelican_Hill-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d113858-Reviews-Alpine_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d78419-Reviews-DoubleTree_by_Hilton_Hotel_Irvine_Spectrum-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d78851-Reviews-Disneyland_Hotel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33298-d226149-Reviews-Ayres_Suites_Yorba_Linda-Yorba_Linda_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d84037-Reviews-Balboa_Bay_Resort-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d78639-Reviews-Holiday_Inn_Express_Newport_Beach_an_IHG_Hotel-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75498-Reviews-Anaheim_Desert_Inn_and_Suites-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d7024015-Reviews-Ayres_Hotel_Orange-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32581-d76252-Reviews-La_Quinta_Inn_Suites_by_Wyndham_Buena_Park-La_Palma_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32596-d1427181-Reviews-Hilton_Garden_Inn_Irvine_Spectrum_Lake_Forest-Lake_Forest_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32279-d76723-Reviews-Best_Western_Plus_Marina_Shores_Hotel-Dana_Point_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d113859-Reviews-Knott_s_Berry_Farm_Hotel-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d225013-Reviews-Camelot_Inn_Suites-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d275319-Reviews-Hotel_Marguerite_Trademark_Collection_by_Wyndham-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d504424-Reviews-The_Tides_Laguna_Beach-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d78221-Reviews-DoubleTree_by_Hilton_Hotel_Anaheim_Orange_County-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32722-d235438-Reviews-Ayres_Hotel_Spa_Mission_Viejo-Mission_Viejo_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d14084379-Reviews-Hampton_Inn_Suites_Buena_Park-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32722-d12591938-Reviews-Hampton_Inn_Suites_Mission_Viejo-Mission_Viejo_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d92503-Reviews-La_Quinta_Inn_Suites_by_Wyndham_Irvine_Spectrum-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d614001-Reviews-Crescent_Bay_Inn-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d78570-Reviews-Good_Nite_Inn_Buena_Park-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32416-d1139042-Reviews-DoubleTree_by_Hilton_Fullerton-Fullerton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d217224-Reviews-La_Quinta_Inn_Suites_by_Wyndham_Anaheim-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d76224-Reviews-Colony_Inn-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d243898-Reviews-Motel_6_Anaheim_CA_Fullerton_East-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d10373297-Reviews-Homewood_Suites_by_Hilton_Irvine_John_Wayne_Airport-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d240061-Reviews-DoubleTree_by_Hilton_Hotel_Santa_Ana_Orange_County_Airport-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d113860-Reviews-Ayres_Hotel_Costa_Mesa_Newport_Beach-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d7398951-Reviews-Hilton_Garden_Inn_Irvine_Orange_County_Airport-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75604-Reviews-Best_Western_Plus_Stovall_s_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d76675-Reviews-Avenue_of_the_Arts_Costa_Mesa_A_Tribute_Portfolio_Hotel-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d76641-Reviews-Hilton_Orange_County_Costa_Mesa-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d79849-Reviews-Hampton_Inn_Suites_San_Clemente-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d78646-Reviews-Bay_Shores_Peninsula_Hotel-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32279-d78319-Reviews-Laguna_Cliffs_Marriott_Resort_Spa-Dana_Point_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32276-d590364-Reviews-Hampton_Inn_Los_Angeles_Orange_County_Cypress-Cypress_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d76227-Reviews-Courtyard_by_Marriott_Anaheim_Buena_Park-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d78652-Reviews-Hyatt_Regency_Newport_Beach-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75630-Reviews-Capri_Suites_Anaheim-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d84710-Reviews-Sonesta_Irvine-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d225981-Reviews-San_Clemente_Inn-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32107-d76180-Reviews-Embassy_Suites_by_Hilton_Brea_North_Orange_County-Brea_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d12451359-Reviews-Marriott_Irvine_Spectrum-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d78938-Reviews-Days_Inn_by_Wyndham_Anaheim_Near_the_Park-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d224310-Reviews-Embassy_Suites_by_Hilton_Anaheim_South-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d24071843-Reviews-Sonder_La_Ensenada-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75553-Reviews-Travelodge_Inn_Suites_by_Wyndham_Anaheim_on_Disneyland_Dr-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75705-Reviews-Clarion_Hotel_Anaheim_Resort-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d78082-Reviews-Comfort_Inn_Suites_Orange_County_John_Wayne_Airport-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d222951-Reviews-Motel_6_Anaheim_Maingate-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d12214492-Reviews-SpringHill_Suites_Huntington_Beach_Orange_County-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33067-d815971-Reviews-Hampton_Inn_and_Suites_Seal_Beach-Seal_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75727-Reviews-Beachside_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75649-Reviews-Anaheim_Del_Sol_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33022-d78096-Reviews-Best_Western_Capistrano_Inn-San_Juan_Capistrano_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d76653-Reviews-Costa_Mesa_Marriott-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75578-Reviews-Best_Western_Plus_Anaheim_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32279-d76720-Reviews-DoubleTree_Suites_by_Hilton_Hotel_Doheny_Beach_Dana_Point-Dana_Point_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d124332-Reviews-Anaheim_Discovery_Inn_Suites_at_the_Park-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d11914822-Reviews-AC_Hotel_by_Marriott_Irvine-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d78781-Reviews-Wyndham_Anaheim-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32596-d20019653-Reviews-Hampton_Inn_Irvine_Spectrum_Lake_Forest-Lake_Forest_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d76649-Reviews-Crowne_Plaza_Costa_Mesa_Orange_County_an_IHG_Hotel-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33067-d252923-Reviews-Ayres_Hotel_Seal_Beach-Seal_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d77346-Reviews-Embassy_Suites_by_Hilton_Irvine_Orange_County_Airport-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d77356-Reviews-Hilton_Irvine_Orange_County_Airport-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32279-d76724-Reviews-The_Ritz_Carlton_Laguna_Niguel-Dana_Point_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d217225-Reviews-ALO_Hotel_by_Ayres-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d3468716-Reviews-14_West_Boutique_Hotel-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32276-d76708-Reviews-Courtyard_Cypress_Anaheim_Orange_County-Cypress_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d78047-Reviews-Best_Western_Plus_Orange_County_Airport_North-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d250125-Reviews-Marriott_s_Newport_Coast_Villas-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d84706-Reviews-Sonder_Solarena-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32416-d10190605-Reviews-Holiday_Inn_Express_Fullerton_Anaheim_an_IHG_Hotel-Fullerton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75673-Reviews-Fairfield_Inn_by_Marriott_Anaheim_Hills_Orange_County-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d223235-Reviews-Sonesta_ES_Suites_Anaheim_Resort_Area-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d78789-Reviews-Sonesta_Simply_Suites_Anaheim-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75653-Reviews-Queens_Inn_Anaheim-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d13962323-Reviews-Holiday_Inn_Express_Suites_Santa_Ana_Orange_County-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75637-Reviews-Days_Inn_Suites_by_Wyndham_Anaheim_at_Disneyland_Park-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d81861-Reviews-Hampton_Inn_Suites_Santa_Ana_Orange_County_Airport-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32596-d78441-Reviews-Sonesta_Simply_Suites_Irvine_East_Foothill-Lake_Forest_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d243900-Reviews-Motel_6_Buena_Park_Knotts_Berry_Farm_Disneyland-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d81852-Reviews-Motel_6_Irvine_Orange_County_Airport-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33125-d82233-Reviews-Motel_6_Stanton-Stanton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d7171596-Reviews-The_Ranch_at_Laguna_Beach-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d267104-Reviews-Montage_Laguna_Beach-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32279-d78365-Reviews-Best_Western_Plus_Dana_Point_Inn_By_The_Sea-Dana_Point_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75686-Reviews-Anaheim_Islander_Inn_and_Suites-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d226136-Reviews-The_Art_Hotel-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d76630-Reviews-Best_Western_Plus_Newport_Mesa_Inn-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d78112-Reviews-The_Volare_an_Ascend_Hotel_Collection_Member-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d77293-Reviews-Best_Western_Surf_City-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d78127-Reviews-Casablanca_Inn-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d76671-Reviews-The_Westin_South_Coast_Plaza_Costa_Mesa-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d81841-Reviews-Embassy_Suites_by_Hilton_Santa_Ana_Orange_County_Airport-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d10198308-Reviews-Staybridge_Suites_Anaheim_at_the_Park_an_IHG_Hotel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d84716-Reviews-Ramada_by_Wyndham_Costa_Mesa_Newport_Beach-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d643869-Reviews-Hotel_Joaquin-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32722-d78258-Reviews-Fairfield_by_Marriott_Mission_Viejo_Orange_County-Mission_Viejo_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75701-Reviews-Home2_Suites_by_Hilton_Anaheim_Resort-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d77353-Reviews-Irvine_Marriott-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d618612-Reviews-Newport_Beach_Hotel-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d78034-Reviews-DoubleTree_by_Hilton_Orange_County_Airport-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d76644-Reviews-Holiday_Inn_Express_Suites_Costa_Mesa_an_IHG_Hotel-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32897-d79305-Reviews-Best_Western_Plus_Anaheim_Orange_County_Hotel-Placentia_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d84099-Reviews-Ocean_Surf_Inn_Suites-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d17812353-Reviews-Staybridge_Suites_Irvine_An_IHG_Hotel-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d6528899-Reviews-National_Inn_Garden_Grove-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d239824-Reviews-Seaside_Laguna_Inn_Suites-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d265511-Reviews-Quality_Inn_Suites_Buena_Park_Anaheim-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d76208-Reviews-Buena_Park_Grand_Hotel_Suites-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d78395-Reviews-Sonesta_Simply_Suites_Irvine_Spectrum-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d1682070-Reviews-Big_A_Motel-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32416-d217217-Reviews-Howard_Johnson_by_Wyndham_Fullerton_Anaheim_Conference_Cntr-Fullerton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d593856-Reviews-Hotel_Pepper_Tree_Boutique_Kitchen_Studios_Anaheim-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d225012-Reviews-Extended_Stay_America_Orange_County_Anaheim_Convention_Center-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d12832333-Reviews-Lido_House_Autograph_Collection-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33260-d81138-Reviews-Best_Western_Westminster_Inn-Westminster_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d78060-Reviews-Holiday_Inn_Santa_ANA_Orange_Co_Arpt_an_IHG_Hotel-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d12140024-Reviews-Hyatt_House_Irvine_John_Wayne_Airport-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d78216-Reviews-Best_Western_Plus_Meridian_Inn_Suites_Anaheim_Orange-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d6615543-Reviews-Courtyard_by_Marriott_Irvine_Spectrum-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d78664-Reviews-Newport_Channel_Inn-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33022-d20376435-Reviews-Inn_at_the_Mission_San_Juan_Capistrano_Autograph_Collection-San_Juan_Capistrano_Califo.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75514-Reviews-Anaheim_Carriage_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32416-d77073-Reviews-Fullerton_Marriott_at_California_State_University-Fullerton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d78923-Reviews-TownePlace_Suites_by_Marriott_Anaheim_Maingate_Near_Angel_Stadium-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d1529194-Reviews-Anaheim_Lodge-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32279-d675118-Reviews-Riviera_Beach_Resort-Dana_Point_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32416-d84713-Reviews-Days_Inn_Suites_by_Wyndham_Fullerton-Fullerton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d217220-Reviews-Homewood_Suites_by_Hilton_Anaheim_Main_Gate_Area-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d6934980-Reviews-SpringHill_Suites_at_Anaheim_Resort_Convention_Center-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d81855-Reviews-Motel_6_Santa_Ana-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d78076-Reviews-Courtyard_by_Marriott_Costa_Mesa_South_Coast_Metro-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d21224981-Reviews-Hilton_Garden_Inn_Anaheim_Resort-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d1159588-Reviews-Hotel_Miramar-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32596-d235433-Reviews-Quality_Inn_Suites_Irvine_Spectrum-Lake_Forest_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33260-d82618-Reviews-Motel_6_Westminster_North-Westminster_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d77294-Reviews-Comfort_Inn_Suites_Huntington_Beach-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d12593006-Reviews-House_of_Trestles-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d266285-Reviews-Rodeway_Inn_San_Clemente_Beach-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d76246-Reviews-Days_Inn_by_Wyndham_Buena_Park-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33022-d235450-Reviews-Americas_Best_Value_Laguna_Inn_Suites-San_Juan_Capistrano_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d101533-Reviews-Balboa_Inn-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75517-Reviews-Stanford_Inn_Suites-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d78836-Reviews-Hampton_Inn_Suites_Anaheim_Garden_Grove-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29079-d8750055-Reviews-Homewood_Suites_by_Hilton_Aliso_Viejo_Laguna_Beach-Aliso_Viejo_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d217216-Reviews-Hyatt_Regency_John_Wayne_Airport_Newport_Beach-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32107-d1164658-Reviews-Chase_Suite_Hotel_Brea-Brea_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d1129632-Reviews-Sheraton_Garden_Grove_Anaheim_South_Hotel-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75563-Reviews-Best_Western_Courtesy_Inn_Anaheim_Park_Hotel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d280811-Reviews-Hotel_414_Anaheim-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d79852-Reviews-Sea_Horse_Resort-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32276-d78526-Reviews-HYATT_house_Cypress_Anaheim-Cypress_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d23982201-Reviews-SCP_Seven4One-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33198-d4451826-Reviews-Fairfield_Inn_Suites_by_Marriott_Tustin_Orange_County-Tustin_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32589-d77489-Reviews-The_Hills_Hotel-Laguna_Hills_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32651-d126524-Reviews-Best_Western_Los_Alamitos_Inn_Suites-Los_Alamitos_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d613202-Reviews-Best_Western_Harbour_Inn_Suites-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d4994085-Reviews-Tropic_Lodge-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d20502404-Reviews-Element_Anaheim_Resort_Convention_Center-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d1199559-Reviews-Harbor_Inn_Suites-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33260-d119927-Reviews-Hotel_39_Westminster-Westminster_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d12436971-Reviews-Magnolia_Tree_Hotel_in_Anaheim-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d951171-Reviews-Budget_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d249726-Reviews-Residence_Inn_by_Marriott_Anaheim_Hills_Yorba_Linda-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32897-d78466-Reviews-Quality_Inn_Placentia_Anaheim-Placentia_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d76235-Reviews-Fairfield_Inn_Suites_Anaheim_North_Buena_Park-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d92498-Reviews-Residence_Inn_by_Marriott_Irvine_Spectrum-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32107-d217223-Reviews-Extended_Stay_America_Orange_County_Brea-Brea_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d294727-Reviews-Anaheim_Maingate_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33198-d271587-Reviews-Bel_Air_Motor_Hotel-Tustin_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d272674-Reviews-Signature_Anaheim_Maingate-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d84718-Reviews-Vagabond_Inn_Costa_Mesa_Orange_County_Airport-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75671-Reviews-Comfort_Inn_Anaheim_Resort-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32279-d76718-Reviews-Blue_Lantern_Inn_A_Four_Sisters_Inn-Dana_Point_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75717-Reviews-Ramada_by_Wyndham_Anaheim_Maingate_North-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32596-d20001584-Reviews-Homewood_Suites_by_Hilton_Irvine_Spectrum_Lake_Forest-Lake_Forest_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32897-d23258803-Reviews-Springhill_Suites_Anaheim_Placentia_Fullerton-Placentia_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33260-d82620-Reviews-Best_Western_Palm_Garden_Inn-Westminster_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d661863-Reviews-Huntington_Surf_Inn-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d251739-Reviews-Doryman_s_Inn-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32596-d78407-Reviews-Hampton_Inn_Irvine_East_Lake_Forest-Lake_Forest_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32596-d282461-Reviews-Hilton_Garden_Inn_Irvine_East_Lake_Forest-Lake_Forest_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d76660-Reviews-Residence_Inn_by_Marriott_Costa_Mesa_Newport_Beach-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d1631585-Reviews-SpringHill_Suites_Irvine_John_Wayne_Airport_Orange_County-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d78883-Reviews-Best_Western_Orange_Plaza-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d113248-Reviews-Casa_Tropicana-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d119482-Reviews-Club_Wyndham_Dolphin_s_Cove-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32596-d78411-Reviews-Extended_Stay_America_Orange_County_Lake_Forest-Lake_Forest_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33298-d275533-Reviews-Extended_Stay_America_Orange_County_Yorba_Linda-Yorba_Linda_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d142005-Reviews-Travelodge_by_Wyndham_Sunset_Huntington_Beach_Ocean_Front-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32416-d84711-Reviews-Travelodge_by_Wyndham_Fullerton_Near_Anaheim-Fullerton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d78641-Reviews-Travelodge_by_Wyndham_Orange_County_Airport_Costa_Mesa-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d217221-Reviews-Extended_Stay_America_Orange_County_Irvine_Spectrum-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d76662-Reviews-Costa_Mesa_Inn-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d208754-Reviews-Disney_s_Paradise_Pier_Hotel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d217227-Reviews-Motel_6_Anaheim_CA_Convention_Center-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d84097-Reviews-Extended_Stay_America_Orange_County_Huntington_Beach-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d76248-Reviews-Howard_Johnson_by_Wyndham_Buena_Park-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d1474313-Reviews-Motel_6_Costa_Mesa_CA_Newport_Beach-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d564609-Reviews-Cozy_Inn_Costa_Mesa-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d20930345-Reviews-Holiday_Inn_Express_Anaheim_West-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d10683209-Reviews-Morada_Inn-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32596-d78435-Reviews-Best_Western_Plus_Irvine_Spectrum_Hotel-Lake_Forest_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d78016-Reviews-MainStay_Suites_Orange_County_John_Wayne_Airport-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d248146-Reviews-Americas_Best_Value_Astoria_Inn_and_Suites-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d75789-Reviews-Hilton_Garden_Inn_Anaheim_Garden_Grove-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d225782-Reviews-Extended_Stay_America_Orange_County_John_Wayne_Airport-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75592-Reviews-Best_Western_Plus_Raffles_Inn_Suites-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32576-d271318-Reviews-Vagabond_Inn_La_Habra-La_Habra_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33022-d2411007-Reviews-Residence_Inn_by_Marriott_Dana_Point_San_Juan_Capistrano-San_Juan_Capistrano_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75621-Reviews-Best_Western_Plus_Pavilions-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d7949307-Reviews-Nomads_Hotel-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d5452770-Reviews-Oceanfront_Hacienda-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33260-d82623-Reviews-Quality_Inn_Suites_Westminster_Seal_Beach-Westminster_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d78662-Reviews-BLVD_Hotel_Costa_Mesa-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d75724-Reviews-Ramada_Plaza_by_Wyndham_Garden_Grove_Anaheim_South-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32416-d1486389-Reviews-Grand_Inn-Fullerton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33260-d1801654-Reviews-Princess_Inn_Westminster_Huntington_Beach-Westminster_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32596-d258971-Reviews-Holiday_Inn_Express_Suites_Lake_Forest_Irvine_East_an_IHG_Hotel-Lake_Forest_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d78120-Reviews-Comfort_Suites_San_Clemente_Beach-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d1484565-Reviews-SureStay_Hotel_By_Best_Western_Buena_Park_Anaheim-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33198-d271589-Reviews-Tustin_Motor_Lodge-Tustin_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d225912-Reviews-Extended_Stay_America_Orange_County_Katella_Ave-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d625684-Reviews-Surfbreak_Hotel-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32406-d76971-Reviews-Motel_6_Fountain_Valley_Huntington_Beach_Area-Fountain_Valley_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d1048491-Reviews-Travelodge_by_Wyndham_Costa_Mesa_Newport_Beach_Hacienda-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d78809-Reviews-Days_Inn_by_Wyndham_Anaheim_West-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d76655-Reviews-Motel_6_Costa_Mesa-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d5002973-Reviews-Oceana_Boutique_Hotel-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d626275-Reviews-Abby_s_Anaheimer_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32416-d596607-Reviews-Fullerton_Inn-Fullerton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d225745-Reviews-Oceanview_Motel-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d2091199-Reviews-Courtyard_by_Marriott_Santa_Ana_Orange_County-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d278035-Reviews-Residence_Inn_Anaheim_Resort_Area_Garden_Grove-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d23996957-Reviews-Element_Irvine-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32651-d258700-Reviews-Residence_Inn_by_Marriott_Cypress_Los_Alamitos-Los_Alamitos_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d251954-Reviews-Beachcomber_Inn-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32596-d609553-Reviews-Staybridge_Suites_Irvine_East_Lake_Forest_an_IHG_Hotel-Lake_Forest_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29079-d1100077-Reviews-Renaissance_ClubSport_Aliso_Viejo_Laguna_Beach_Hotel-Aliso_Viejo_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32279-d1172925-Reviews-Riviera_Shores_Resort-Dana_Point_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d7404288-Reviews-Kona_Inn_Motel_Anaheim-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d78100-Reviews-Travelodge_by_Wyndham_San_Clemente_Beach-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d596336-Reviews-San_Clemente_Cove_Resort-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d1758207-Reviews-The_Patriots_Boutique_Motel-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75624-Reviews-Brookhurst_Plaza_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d1173341-Reviews-Americas_Best_Value_Inn_San_Clemente_Beach-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32596-d293295-Reviews-Courtyard_Foothill_Ranch_Irvine_East_Lake_Forest-Lake_Forest_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d567898-Reviews-Always_Inn_San_Clemente_B_B-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32279-d119387-Reviews-Capistrano_Surfside_Inn-Dana_Point_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d78655-Reviews-Little_inn_By_The_Bay-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32651-d21309717-Reviews-Fairfield_Inn_Suites_Anaheim_Los_Alamitos-Los_Alamitos_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d601300-Reviews-Surf_City_Inn-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32276-d217222-Reviews-Extended_Stay_America_Orange_County_Cypress-Cypress_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d249725-Reviews-Extended_Stay_America_Orange_County_Anaheim_Hills-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d1557290-Reviews-Inn_at_Calafia_Beach-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32107-d1115726-Reviews-Travelodge_by_Wyndham_Brea-Brea_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75755-Reviews-Americas_Best_Value_Inn_Suites-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33125-d5327803-Reviews-Chester_Inn_Motel-Stanton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33260-d82619-Reviews-Motel_6_Westminster_South-Westminster_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d6533215-Reviews-Calico_Motel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d225468-Reviews-Sandpiper_Motel-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d502116-Reviews-Motel_6_Garden_Grove-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d77478-Reviews-Laguna_Beach_Lodge-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32897-d78444-Reviews-Residence_Inn_Anaheim_Placentia_Fullerton-Placentia_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d77344-Reviews-Courtyard_by_Marriott_Irvine_John_Wayne_Airport_Orange_County-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d223891-Reviews-Residence_Inn_Irvine_John_Wayne_Airport_Orange_County-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d5522711-Reviews-Sahara_Motel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32107-d2090468-Reviews-Regency_Motel-Brea_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d12593072-Reviews-Westward_Wagon_Inn_Theme_Park_Entrance-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32276-d1235777-Reviews-Rodeway_Inn_Cypress-Cypress_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d22965111-Reviews-Red_Roof_Inn_Santa_Ana-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d1392238-Reviews-WorldMark_Anaheim-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d279768-Reviews-Motel_6_Anaheim-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d1200531-Reviews-Orange_Tustin_Inn-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32596-d23280596-Reviews-SpringHill_Suites_by_Marriott_Irvine_Lake_Forest-Lake_Forest_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75747-Reviews-Quality_Inn_Suites_Anaheim_at_the_Park-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d1657433-Reviews-West_Coast_Motel_Santa_Ana-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33125-d82231-Reviews-Dixie_Orange_County_Hotel-Stanton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d78209-Reviews-Casa_Blanca_Hotel_Suites-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d15001599-Reviews-American_Inn_Suites-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32576-d271316-Reviews-La_harbra_Hyland_motel-La_Habra_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32276-d5954170-Reviews-Studio_6_Cypress-Cypress_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d76221-Reviews-Buena_Park_Inn-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d76244-Reviews-The_Berry_Inn-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32276-d674907-Reviews-Super_8_by_Wyndham_Cypress_Buena_Park_Area-Cypress_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d4580705-Reviews-Motel_6_Orange_Anaheim-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d3339567-Reviews-Harbor_Motel-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d78224-Reviews-Days_Inn_by_Wyndham_Orange_Anaheim-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75742-Reviews-Motel_6_Anaheim_Hills-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75528-Reviews-Ramada_by_Wyndham_Anaheim_Convention_Center-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d1638473-Reviews-Best_Inn_Suites-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d1224982-Reviews-Santa_Ana_Travel_Inn-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33198-d4451235-Reviews-Residence_Inn_by_Marriott_Tustin_Orange_County-Tustin_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d15273502-Reviews-Parkside_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d218752-Reviews-Candy_Cane_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d5523946-Reviews-Century_Motel-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d12132023-Reviews-The_Retreat_in_Laguna-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32596-d18721058-Reviews-TownePlace_Suites_Irvine_Lake_Forest-Lake_Forest_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d676681-Reviews-Anaheim_Harbor_RV_Park-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d222949-Reviews-Little_Boy_Blue_Motel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d78398-Reviews-ATRIUM_HOTEL-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d1163345-Reviews-Sunset_Cove_Villas-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d76638-Reviews-Sunset_Inn-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d2110543-Reviews-Pacific_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d292236-Reviews-Manzanita_Cottages-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d75697-Reviews-Park_Vue_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32107-d507603-Reviews-Hyland_Motel-Brea_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d78361-Reviews-Holiday_Inn_Laguna_Beach_An_IHG_hotel-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d258701-Reviews-Laguna_Shores-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32416-d77066-Reviews-The_Hotel_Fullerton_Anaheim-Fullerton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d1224980-Reviews-Royal_Grand_Inn-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33260-d82617-Reviews-Los_Angeles_Days_Inn_Westminster-Westminster_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d1955301-Reviews-Arabella_Laguna-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d670734-Reviews-Villa_Del_Mar-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d1648540-Reviews-Newport_Bay_Inn-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d1644642-Reviews-Travelodge_by_Wyndham_Buena_Park-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d14774002-Reviews-Frontier_Motel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d575082-Reviews-Legacy_Inn_and_Suites-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d1741625-Reviews-777_Motor_Inn-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d4579114-Reviews-Best_Budget_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32576-d271317-Reviews-La_Habra_Motel-La_Habra_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32416-d77077-Reviews-Willow_Tree_Lodge-Fullerton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d4009786-Reviews-Orangeland_RV_Park-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d618704-Reviews-Crystal_Cove_Beach_Cottages-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d664713-Reviews-Crystal_Cove_State_Park-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d1770010-Reviews-The_Pearl_Laguna-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d1012193-Reviews-Casa_de_Balboa_Beachfront-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d119447-Reviews-Sun_n_Sands_Motel-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d1206741-Reviews-Garden_Cottage_at_the_Green_B_B-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d240059-Reviews-Four_Seasons_Pacifica-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32651-d271454-Reviews-Don_s_Turf_Motel_Los_Alamitos-Los_Alamitos_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33067-d226157-Reviews-Eaves_Seal_Beach-Seal_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d119394-Reviews-Newport_Dunes_Waterfront_Resort_Marina-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d647321-Reviews-San_Clemente_State_Beach-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33183-d5027375-Reviews-O_Neill_Regional_Park_Camping-Trabuco_Canyon_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d488006-Reviews-Laguna_Surf-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32416-d1150698-Reviews-HI_Los_Angeles_Fullerton-Fullerton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d665351-Reviews-Lower_Moro_Campsite-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32279-d8409032-Reviews-Doheny_State_Beach_Campground-Dana_Point_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d2064478-Reviews-Beso_del_Sol-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d208328-Reviews-San_Mateo_Campground-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d23548962-Reviews-OC_Hotel-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d2648485-Reviews-Ruta_s_Old_Town_Inn-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d119378-Reviews-Woods_Cove_Inn-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d8473193-Reviews-The_Holidays-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d665353-Reviews-Upper_Moro_Campsite-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32596-d23783652-Reviews-Hampton_Inn_By_Hilton-Lake_Forest_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d2014292-Reviews-Motel_Moonlight-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d1628881-Reviews-Harbor_Bay_Motel-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d7131162-Reviews-Canyon_RV_Park-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d1860785-Reviews-Sky_Palm_Motel-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d324408-Reviews-Rodeway_Inn-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d77289-Reviews-Beach_Inn_Motel-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32589-d77486-Reviews-Laguna_Hills_Inn_At_Irvine_Spectrum-Laguna_Hills_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d12288298-Reviews-C_Vu_Motel-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d222950-Reviews-Quality_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d21145675-Reviews-Kasa_Orange_County-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d119376-Reviews-The_French_Inn-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32576-d271319-Reviews-Sunset_Inn-La_Habra_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32107-d4332644-Reviews-Chino_Hills_Campground-Brea_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d15208440-Reviews-Omg_House-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d16647168-Reviews-House_near_Disney_Land-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d12431279-Reviews-Aqua_Motel_Santa_Ana-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32249-d19851059-Reviews-Seaview_Getaways-Corona_del_Mar_Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d77301-Reviews-Huntington_Suites-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d226145-Reviews-Oakwood_At_The_Charter-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d142251-Reviews-Econo_Lodge_Anaheim_North-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d3262113-Reviews-Little_Saigon_Inn-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32596-d1206695-Reviews-The_Room_Downstairs-Lake_Forest_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d1647954-Reviews-CC_Camperland_RV_Park-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d15680730-Reviews-Oceanfront_Oceana_Penthouse-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32722-d275361-Reviews-Oakwood_at_Archstone_Mission_Viejo-Mission_Viejo_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d74007-Reviews-Casa_de_Flores_Bed_and_Breakfast-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d7694074-Reviews-Sunland_Motel-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d5571169-Reviews-Town_House_Motel-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d119448-Reviews-Sunset_Bed_and_Breakfast-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d8434179-Reviews-Waterfront_RV_Park-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32576-d271315-Reviews-Beach_La_Habra_Motel-La_Habra_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32122-d4702332-Reviews-Coral_Motel-Buena_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d1645234-Reviews-Americana_Motel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d6005446-Reviews-Grove_Motel-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d268237-Reviews-Oakwood_at_Park_Newport-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d1681901-Reviews-Polynesian_Motel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d1641432-Reviews-Akua_Motor_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d8423421-Reviews-California_Lodge_Suites_Hotel-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d1647111-Reviews-Twin_Cypress_Motel-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33260-d278061-Reviews-Westminster_Motor_Inn-Westminster_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d15201182-Reviews-M_Residence_Hotel-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d1629748-Reviews-Hospitality_Inn-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d12075942-Reviews-Global_Luxury_Suites_at_The_Village-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d1224976-Reviews-Golden_West_Lodge-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d6034291-Reviews-Villa_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d6034031-Reviews-Trade_Winds_Motel-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33125-d6160464-Reviews-Villa_Motel-Stanton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d84722-Reviews-The_Katella_Palms_Hotel_at_Disneyland_Resort-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d7867978-Reviews-EL_Cortez_Lodge-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d3347098-Reviews-Welcome_Inn_Suites_Anaheim-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d78071-Reviews-Guest_Inn_Suites-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32416-d2442851-Reviews-Oakwood_At_Las_Palmas_Apartment-Fullerton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d12910409-Reviews-Crashpod-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d283198-Reviews-Ali_Baba_Motel-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33125-d9767365-Reviews-Stanton_Inn_Suites-Stanton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d8622358-Reviews-Peach_Blossom_Across_from_the_Beach-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d12290103-Reviews-Studio_6_Anaheim-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d2553691-Reviews-La_Vista_Inn_Motel-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d4609833-Reviews-Anaheim_National_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32416-d1224962-Reviews-Fullerton_Motor_Lodge-Fullerton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d113867-Reviews-Coast_Inn-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33125-d6212996-Reviews-Riviera_Motel-Stanton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32279-d119475-Reviews-Dana_Point_Harbor_Inn-Dana_Point_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d78878-Reviews-Motel_6_Anaheim_Stadium_Orange-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d78669-Reviews-Ana_Mesa_Inn-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32276-d17495974-Reviews-Royal_Inn-Cypress_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d12103376-Reviews-Robinhood_Motel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d24914119-Reviews-Bposhtels_Anaheim-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32576-d23850264-Reviews-3rd_Avenue_Inn-La_Habra_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d23698696-Reviews-Hotel_Europa-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d23325235-Reviews-Homes_for_the_Soul_SA-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32107-d25151005-Reviews-Residence_Inn_Anaheim_Brea-Brea_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d25195690-Reviews-La_Casa_Motel_Garden_Grove-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d21193561-Reviews-Lovely_Private_House_Close_By_Disney-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d13103286-Reviews-Super_7_Motel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33260-d5532782-Reviews-Executive_Suites_Inn-Westminster_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d21374965-Reviews-25_Steps_to_the_Beach-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32406-d23273760-Reviews-Central_OC_Homestay-Fountain_Valley_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d24006964-Reviews-Home2_Suites_By_Hilton_Garden_Grove_Anaheim-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d274123-Reviews-Boat_and_Breakfast_Newport-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d13794108-Reviews-Orange_Villa_Park_Motel-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d78022-Reviews-Civic_Center_Inn_Santa_Ana-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d23342099-Reviews-Phoenix_East_by_Brett_Robinson_Vacations-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d78072-Reviews-Budget_Inn_Santa_Ana-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d23342097-Reviews-Phoenix_X_by_Brett_Robinson-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d23887316-Reviews-Little_Inn_By_The_Beach-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g659482-d21324922-Reviews-Lakeside_Haven-Orange_County_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d23287692-Reviews-Huntington_Beach_House-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32513-d1643610-Reviews-Rancho_Bolsa_Chica_Inn-Huntington_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d20931371-Reviews-Irvine_Memorable_Stay-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d17443066-Reviews-Astoria_at_Central_Park_West_Apartments-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d252362-Reviews-Seven_Crown_Resorts-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d7608341-Reviews-Irvine_Guest_House-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d3683129-Reviews-Oakwood_at_Kelvin_Court-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32530-d16639839-Reviews-Irvine_Luxury_House-Irvine_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33125-d1528944-Reviews-Tahiti_Motel-Stanton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32946-d12796052-Reviews-Via_Tortuga-Rancho_Santa_Margarita_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32279-d21029195-Reviews-Doheny_Beach_Casa_Manzanita-Dana_Point_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32279-d2435874-Reviews-Casitas_at_the_Sea-Dana_Point_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32107-d1466718-Reviews-Brea_Bed_and_Breakfast-Brea_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32576-d12652907-Reviews-Happy_family-La_Habra_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d268236-Reviews-Oakwood_at_Irvine_Avenue-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32780-d20949555-Reviews-Dignitary_Discretion_Newport_Beach-Newport_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d665348-Reviews-Deer_Canyon_Campground-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d23873474-Reviews-Best_Western_Plus_Laguna_Brisas_Hotel-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d1199582-Reviews-Best_Laguna_Vacations_II-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d23983895-Reviews-Hotel_Laguna-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32588-d24126475-Reviews-Laguna_Brisas_A_Beach_Hotel-Laguna_Beach_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32406-d24028694-Reviews-SCANDI_Room_In_A_Shared_House_Quiet_Free_Access_To_Living_Room_Kitchen_30_Mins_To_Disn.html',
'https://www.tripadvisor.com/Hotel_Review-g32406-d24031039-Reviews-Glamping_Retreat_BBBQ_Next_Mile_Square_Park_15_To_Beaches-Fountain_Valley_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33198-d1146067-Reviews-National_at_Archstone_Tustin-Tustin_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33198-d74262-Reviews-Royal_Hotel-Tustin_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32416-d20116074-Reviews-Fullerton_Apartments-Fullerton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32416-d20109399-Reviews-770_South_Harbor-Fullerton_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d25181304-Reviews-Days_Inn_Anaheim_Near_Conv_Ctr-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32420-d77086-Reviews-Guesthouse_International_Garden_Grove-Garden_Grove_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d1173082-Reviews-Always_San_Clemente_Beach_Studio-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d208335-Reviews-Echo_Arch-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33012-d7148753-Reviews-Algodon_Motel-San_Clemente_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d25211589-Reviews-Aspire_Inn_Suites-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d23417651-Reviews-Quality_Jack_Room_Near_Disneyland_Anaheim_Convention-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d15306143-Reviews-Anaheim_Vacation_Villa_3_Bedroom_House_Near_Disney-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d23107459-Reviews-Chestnut_Hill_Bed_Breakfast-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32825-d21349684-Reviews-Summer_House_On_Romar_Beach_II-Orange_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33226-d1466764-Reviews-Two_Palms_at_the_Grove-Villa_Park_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d268528-Reviews-Oakwood_At_Hampton_Point-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d20930372-Reviews-Super_8_Motel_Anaheim_Near_Disneyland-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d1634239-Reviews-Anaheim_Angel_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d15201681-Reviews-Anchor_Motel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d17641542-Reviews-Western_Room_Suit-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d24960603-Reviews-Studio_6_Anaheim_Hills_CA-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d15881095-Reviews-The_Kraemer_Building-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d23849309-Reviews-Buena_Vista_Inn-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d20930763-Reviews-Luxurious_Cosmopolitan_Suites_By_Disney-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d17627728-Reviews-Hilltop_View_Home_Close_to_Disney-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d1644695-Reviews-Mardi_Gras_Motel-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g29092-d1528985-Reviews-Station_Inn_Suites-Anaheim_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d19632589-Reviews-South_Coast_Dr_Apartment-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32253-d17765340-Reviews-Mesa_Motel-Costa_Mesa_California.html',
'https://www.tripadvisor.com/Hotel_Review-g1931746-d20930774-Reviews-Luxury_Getaway_Resort_With_Great_Views-Ladera_Ranch_California.html',
'https://www.tripadvisor.com/Hotel_Review-g33043-d1224972-Reviews-California_Palm-Santa_Ana_California.html',
'https://www.tripadvisor.com/Hotel_Review-g32276-d6595354-Reviews-Cloud_9_Motel-Cypress_California.html',
]

user_agent = ({'User-Agent':
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
			AppleWebKit/537.36 (KHTML, like Gecko) \
			Chrome/90.0.4430.212 Safari/537.36',
			'Accept-Language': 'en-US, en;q=0.5'})

# hotel_review_links = []
page_contents = []
review_contents = []

#Review data
helpful_votes = []
contributions = []
overall_ratings = []
location_ratings = []
cleanliness_ratings = []
service_ratings = []
value_ratings = []
rooms_ratings = []
sleep_quality_ratings = []
review_summary_headings = []
review_summaries = []
date_of_stays = []
room_tips = []
trip_types = []
manager_responses = []
usernames = []
indices = []


def get_page_contents(reviewPageUrl):
    print("Getting page contents")
    page = requests.get(reviewPageUrl, headers = user_agent)
    return BeautifulSoup(page.text, 'html.parser')

def get_review_contents(soup):
    for review in soup.find_all('div',{'class':'YibKl MC R2 Gi z Z BB pBbQr'}):
        review_contents.append(review)

def get_helpful_votes(soup, index):
    word = 'helpful'
    found = False

    for helpful_vote in soup.find_all('span',{'class':'phMBo'}):
        if word in helpful_vote.text.strip():
            helpful_votes.insert(index, helpful_vote.text.strip())
            found = True
            print("HELPFUL VOTE FOUND")
            break
            
    if found == False:
        print("HELPFUL VOTE NOT FOUND")
        helpful_votes.insert(index, 'none')

def get_num_of_bubbles(list,list_data, index):
    found = False
    data = ['5.0 of 5 bubbles','4.0 of 5 bubbles', '3.0 of 5 bubbles', 
     '2.0 of 5 bubbles','1.0 of 5 bubbles']

    if(list_data == 'bubble_50'):
        list.insert(index, data[0])
        found = True
        print("DATA FOUND")
        
    if(list_data == 'bubble_40'):
        list.insert(index, data[1])
        found = True
        print("DATA FOUND")
        
    if(list_data == 'bubble_30'):
        list.insert(index, data[2])
        found = True
        print("DATA FOUND")
        
    if(list_data == 'bubble_20'):
        list.insert(index, data[3])
        found = True
        print("DATA FOUND")
        
    if(list_data == 'bubble_10'):
        list.insert(index, data[4])
        found = True
        print("DATA FOUND")

    if found == False:
        print("DATA NOT FOUND") 
        list.insert(index, 'none')  
    

def get_contributions(soup, index):
    word = 'contributions'
    word2 = 'contribution'
    found = False
    for contribution in soup.find_all('span',{'class':'phMBo'}):
        if (word in contribution.text.strip()) or (word2 in contribution.text.strip()):
            contributions.insert(index, contribution.text.strip())
            found = True
            print("CONTRIBUTION FOUND") 
            break

    if found == False:
        print("CONTRIBUTION NOT FOUND") 
        contributions.insert(index, 'none')

def get_overall_ratings(soup, index):
    found = False
    for overall_rating in soup.find_all('div',{'class':'Hlmiy F1'}):
          span = overall_rating.find('span')
          if(span):
            get_num_of_bubbles(overall_ratings, span["class"][1], index)
            found = True
            print("OVERALL RATINGS FOUND") 
            break
    if found == False:
        print("OVERALL RATINGS NOT FOUND") 
        overall_ratings.insert(index, 'none')  

def get_review_summary_headings(soup, index):
    found = False
    for review_summary_heading in soup.find_all('a',{'class':'Qwuub'}):
        if (review_summary_heading.find('span')):
            review_summary_headings.insert(index, review_summary_heading.text.strip())
            found = True
            print("REVIEW SUMMARIES FOUND") 
            break
    if found == False:
        print("REVIEW SUMMARIES NOT FOUND") 
        review_summary_headings.insert(index, 'none')

def get_review_summary(soup, index):
    found = False
    for review_summary in soup.find_all('span',{'class':'QewHA H4 _a'}): 
        if (review_summary.find('span')):
            review_summaries.insert(index, review_summary.find('span').text.strip())
            found = True
            print("REVIEW SUMMARIES FOUND") 
            break
    if found == False:
        print("REVIEW SUMMARIES NOT FOUND") 
        review_summaries.insert(index, 'none')

def get_date_of_stays(soup, index):
    found = False
    empty_word = 'Date of stay: '
    for date_of_stay in soup.find_all('span',{'class':'teHYY _R Me S4 H3'}):
        if (date_of_stay):
            # Phrase out the word 'Date of stay: '
            phraseData = str(date_of_stay.text.strip())
            phraseData = phraseData.replace(empty_word,"")

            date_of_stays.insert(index, phraseData)
            found = True
            print("DATE OF STAYS FOUND") 
            break
    if found == False:
        print("DATE OF STAYS NOT FOUND") 
        date_of_stays.insert(index, 'none')

def get_room_tips(soup, index):
    found = False
    empty_word = 'Room Tip: '
    for room_tip in soup.find_all('div',{'class':'Pb'}):
        if (room_tip.find('span')):
            # Phrase out the word 'Room Tip: '
            phraseData = str(room_tip.text.strip())
            phraseData = phraseData.replace(empty_word,"")

            room_tips.insert(index, phraseData)
            found = True
            print("ROOM TIPS FOUND") 
            break
    if found == False:
        print("ROOM TIPS NOT FOUND") 
        room_tips.insert(index, 'none')

def get_trip_types(soup, index):
    found = False
    empty_word = 'Trip type: '
    for trip_type in soup.find_all('span',{'class':'TDKzw _R Me'}):
        if (trip_type):
            # Phrase out the word 'Room Tip: '
            phraseData = str(trip_type.text.strip())
            phraseData = phraseData.replace(empty_word,"")

            trip_types.insert(index, phraseData)
            found = True
            print("TRIP TYPES FOUND") 
            break
    if found == False:
        print("TRIP TYPES NOT FOUND") 
        trip_types.insert(index, 'none')

def get_location_ratings(soup, index):
    found = False

    for location_rating in soup.find_all('div',{'class':'hemdC S2 H2 WWOoy'}):
        span = location_rating.find_all('span')
        span_len = len(span) 
  
        if(span_len == 3 and span[2].text.strip() == 'Location'):
          bubbles = span[1]['class'][1]
          get_num_of_bubbles(location_ratings, bubbles, index)
          found = True
          print("LOCATION RATINGS FOUND") 
          break

    if found == False:
        print("LOCATION RATINGS NOT FOUND") 
        location_ratings.insert(index, 'none')      

def get_cleanliness_ratings(soup, index):
    found = False
    for cleanliness_rating in soup.find_all('div',{'class':'hemdC S2 H2 WWOoy'}):
        span = cleanliness_rating.find('span')
        span_len = len(span) 

        if(span_len == 3 and span[2].text.strip() == 'Cleanliness'):
            bubbles = span[1]['class'][1]
            get_num_of_bubbles(cleanliness_ratings, bubbles, index)
            found = True
            print("CLEALINESS RATINGS FOUND") 
            break
    if found == False:
        print("CLEALINESS RATINGS NOT FOUND") 
        cleanliness_ratings.insert(index, 'none') 

def get_service_ratings(soup, index):
    found = False
    for service_rating in soup.find_all('div',{'class':'hemdC S2 H2 WWOoy'}):
        span = service_rating.find('span')
        span_len = len(span) 

        if(span_len == 3 and span[2].text.strip() == 'Service'):
            bubbles = span[1]['class'][1]
            get_num_of_bubbles(service_ratings, bubbles, index)
            found = True
            print("SERVICE RATINGS FOUND") 
            break
    if found == False:
        print("SERVICE RATINGS NOT FOUND") 
        service_ratings.insert(index, 'none') 

def get_value_ratings(soup, index):
    found = False
    for value_rating in soup.find_all('div',{'class':'hemdC S2 H2 WWOoy'}):
        span = value_rating.find('span')
        span_len = len(span) 

        if(span_len == 3 and span[2].text.strip() == 'Value'):
            bubbles = span[1]['class'][1]
            get_num_of_bubbles(value_ratings, bubbles, index)
            found = True
            print("VALUE RATINGS FOUND") 
            break
    if found == False:
        print("VALUE RATINGS NOT FOUND") 
        value_ratings.insert(index, 'none') 

def get_rooms_ratings(soup, index):
    found = False
    for rooms_rating in soup.find_all('div',{'class':'hemdC S2 H2 WWOoy'}):
        span = rooms_rating.find('span')
        span_len = len(span) 

        if(span_len == 3 and span[2].text.strip() == 'Rooms'):
            bubbles = span[1]['class'][1]
            get_num_of_bubbles(rooms_ratings, bubbles, index)
            found = True
            print("ROOM RATINGS FOUND") 
            break
    if found == False:
        print("ROOM RATINGS NOT FOUND") 
        rooms_ratings.insert(index, 'none') 

def get_sleep_quality_ratings(soup, index):
    found = False
    for sleep_quality_rating in soup.find_all('div',{'class':'hemdC S2 H2 WWOoy'}):
        span = sleep_quality_rating.find('span')
        span_len = len(span) 

        if(span_len == 3 and span[2].text.strip() == 'Sleep Quality'):
            bubbles = span[1]['class'][1]
            get_num_of_bubbles(sleep_quality_ratings, bubbles, index)
            found = True
            print("SLEEP QULAITY RATINGS FOUND") 
            break
    if found == False:
        print("SLEEP QUALITY RATINGS NOT FOUND") 
        sleep_quality_ratings.insert(index, 'none') 


def get_manager_responses(soup, index):
    found = False
    for manager_response in soup.find_all('span',{'class':'MInAm _a'}):
        if (manager_response):
            manager_responses.insert(index, manager_response.text.strip())
            found = True
            print("MANAGER RESPONSES FOUND") 
            break
    if found == False:
        print("MANAGER RESPONSES NOT FOUND") 
        manager_responses.insert(index, 'none')

def get_usernames(soup, index):
    found = False
    for username in soup.find_all('a',{'class':'ui_header_link uyyBf'}):
        if (username):
            usernames.insert(index, username.text.strip())
            found = True
            print("USERNAME FOUND") 
            break
    if found == False:
        print("USERNAME NOT FOUND") 
        usernames.insert(index, 'none')

# Get all reviews 587 hotels 
for x in range(587):
    hotel_review_links = {}
    review_nums = []
    num = 1

    # Calculate the relative path to the CSV file
    df = pd.read_csv(os.path.join('..', '..', 'HotelReviewLinks', str(x) + '.csv'))

    hotel_review_links[x] = df['Hotel Link: ' + str(original_hotel_links[x])].to_list()
    print(hotel_review_links)

    for y in range(len(hotel_review_links[x])):
        print(hotel_review_links[x][y])
        formatted_link = hotel_review_links[x][y].replace("'","")
        soup = get_page_contents(formatted_link)
        page_contents.append(soup) 
       

    # Testing one page 
    # soup = get_page_contents("https://www.tripadvisor.com/Hotel_Review-g29092-d75532-Reviews-or30-The_Anaheim_Hotel-Anaheim_California.html#REVIEWS")
    # page_contents.append(soup)

    for y in range(len(page_contents)): 
       get_review_contents(page_contents[y]) 

    # Get data in review content from 10 reviews per page
    for y in range(len(review_contents)):
        # pass review content and index, so that results are in corresponding order of lists
        get_helpful_votes(review_contents[y], y)
        get_contributions(review_contents[y], y)
        get_overall_ratings(review_contents[y], y)
        get_review_summary_headings(review_contents[y], y)
        get_review_summary(review_contents[y], y)
        get_date_of_stays(review_contents[y], y)
        get_room_tips(review_contents[y], y)
        get_trip_types(review_contents[y], y)
        get_manager_responses(review_contents[y], y)
        get_location_ratings(review_contents[y], y)
        get_cleanliness_ratings(review_contents[y], y)
        get_service_ratings(review_contents[y], y)
        get_value_ratings(review_contents[y], y)
        get_rooms_ratings(review_contents[y], y)
        get_sleep_quality_ratings(review_contents[y], y)
        get_usernames(review_contents[y], y)
        
         # Hotel index 
        indices.append(x)

        review_nums.append(num)
        num += 1 

    # Create the dictionary.
    dict = {'Helpful Vote' : helpful_votes, 'Contributions' : contributions, 'Overall Rating' : overall_ratings, 'Summary Heading' : review_summary_headings,
    'Summary' : review_summaries, 'Date of Stay' : date_of_stays, 'Room tip' : room_tips, 'Trip Type' : trip_types, 'Manager Response' : manager_responses,
    'Location Rating' : location_ratings, 'Cleanliness Rating' : cleanliness_ratings, 'Service Rating' :service_ratings, 'Value Rating' : value_ratings,
    'Rooms Rating' : rooms_ratings, 'Sleep Quality Rating' : sleep_quality_ratings, 'Username' : usernames, 'Review Number' : review_nums, 'Index' : indices
    }

    # Create the dataframe.
    reviewsData = pd.DataFrame.from_dict(dict)
    reviewsData.head(10)
    # Convert dataframe to CSV file.
    reviewsData.to_csv(str(x) +'.csv', index=False, header=True)    

    #Clear all lists 
    page_contents.clear()
    review_contents.clear()
    review_nums.clear()

    helpful_votes.clear()
    contributions.clear()
    overall_ratings.clear()
    review_summary_headings.clear()
    review_summaries.clear()
    date_of_stays.clear()
    room_tips.clear()
    trip_types.clear()
    manager_responses.clear()
    location_ratings.clear()
    cleanliness_ratings.clear()
    service_ratings.clear()
    value_ratings.clear()
    rooms_ratings.clear()
    sleep_quality_ratings.clear()
    usernames.clear()
    indices.clear()
    print("Done")

    # print(helpful_votes)
    # print(len(helpful_votes))
    # print(contributions)
    # print(len(contributions))
    # print(overall_ratings)
    # print(len(overall_ratings))
    # print(review_summary_headings)
    # print(review_summaries)
    # print(len(review_summaries))
    # print(date_of_stays)
    # print(len(date_of_stays))
    # print(room_tips)
    # print(len(room_tips))
    # print(trip_types)
    # print(len(trip_types))
    # print(manager_responses)
    # print(len(manager_responses))
    # print(location_ratings)
    # print(len(location_ratings))
    # print(cleanliness_ratings)
    # print(len(cleanliness_ratings))
    # print(service_ratings)
    # print(len(service_ratings))
    # print(value_ratings)
    # print(len(value_ratings))
    # print(rooms_ratings)
    # print(len(rooms_ratings))
    # print(sleep_quality_ratings)
    # print(len(sleep_quality_ratings))
    # print(usernames)
    # print(len(usernames))





