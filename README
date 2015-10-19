Vienna url:

http://openls.geog.uni-heidelberg.de/testing2015/route?Start=8.6817521,49.4173462&End=8.6828883,49.4067577&Via=&lang=de&distunit=KM&routepref=Fastest&avoidAreas=&useTMC=false&noMotorways=false&noTollways=false&instructions=false

http://wiki.openstreetmap.org/wiki/OpenRouteService

cat input/cities_europe.txt | xargs -n 2 -I {} python scripts/geocode.py -d geocodes_europe "{}"
cat input/cities_nca.txt | xargs -n 2 -I {} python scripts/geocode.py -d geocodes_nca "{}"
cat input/cities_sa.txt | xargs -n 2 -I {} python scripts/geocode.py -d geocodes_sa "{}"
cat input/cities_africa.txt | xargs -n 2 -I {} python scripts/geocode.py -d geocodes_africa "{}"
cat input/cities_asia.txt | xargs -n 2 -I {} python scripts/geocode.py -d geocodes_asia "{}"
cat input/cities_australia_and_oceania.txt | xargs -n 2 -I {} python scripts/geocode.py -d geocodes_australia_and_oceania "{}"

mv geocodes_europe/zürich geocodes_europe/zurich

mv geocodes_nca/new\ york geocodes_nca/new_york
mv geocodes_nca/los\ angeles geocodes_nca/los_angeles
mv geocodes_nca/san\ diego geocodes_nca/san_diego
mv geocodes_nca/san\ francisco geocodes_nca/san_francisco
mv geocodes_nca/panama\ city geocodes_nca/panama_city
mv geocodes_nca/san\ salvador geocodes_nca/san_salvador
mv geocodes_nca/san\ jose geocodes_nca/san_jose
mv geocodes_nca/mexico\ city geocodes_nca/mexico_city
mv geocodes_nca/guatemala\ city geocodes_nca/guatemala_city

mv geocodes_sa/buenos\ aires geocodes_sa/buenos_aires
mv geocodes_sa/rio\ de\ janeiro geocodes_sa/rio_de_janeiro
mv geocodes_sa/sao\ paolo geocodes_sa/sao_paolo
mv geocodes_sa/la\ paz geocodes_sa/la_paz

mv geocodes_africa/n\'djamena geocodes_africa/n_djamena
mv geocodes_africa/dar\ es\ salaam geocodes_africa/dar_es_salaam
mv geocodes_africa/porto\ novo geocodes_africa/porto_novo
mv geocodes_africa/cape\ town geocodes_africa/cape_town

mv geocodes_asia/phnom\ penh geocodes_asia/phnom_penh
mv geocodes_asia/st\ petersburg geocodes_asia/st_petersburg
mv geocodes_asia/tel\ aviv geocodes_asia/tel_aviv
mv geocodes_asia/new\ delhi geocodes_asia/new_delhi
mv geocodes_asia/abu\ dhabi geocodes_asia/abu_dhabi
mv geocodes_asia/kuwait\ city geocodes_asia/kuwait_city

mv geocodes_australia_and_oceania/port\ moresby geocodes_australia_and_oceania/port_moresby

ls geocodes_sa/ > cities_sa.txt
ls geocodes_africa/ > cities_africa.txt
ls geocodes_asia/ > cities_asia.txt
ls geocodes_nca/ > cities_nca.txt
ls geocodes_europe/ > cities_europe.txt
ls geocodes_australia_and_oceania/ > cities_australia_and_oceania.txt

#### Create the grid

resolution=600; for city in $(cat cities_sa.txt); do parallel -q --colsep ' ' python  scripts/create_grid_skeleton.py -r ${resolution} --center-x {3} --center-y {4} > grid_skeletons/grid_${city}_${resolution}.ssv :::: geocodes_sa/${city}; done;
resolution=600; for city in $(cat cities_africa.txt); do parallel -q --colsep ' ' python  scripts/create_grid_skeleton.py -r ${resolution} --center-x {3} --center-y {4} > grid_skeletons/grid_${city}_${resolution}.ssv :::: geocodes_africa/${city}; done;
resolution=600; for city in $(cat cities_asia.txt); do parallel -q --colsep ' ' python  scripts/create_grid_skeleton.py -r ${resolution} --center-x {3} --center-y {4} > grid_skeletons/grid_${city}_${resolution}.ssv :::: geocodes_asia/${city}; done;
resolution=600; for city in $(cat cities_nca.txt); do parallel -q --colsep ' ' python  scripts/create_grid_skeleton.py -r ${resolution} --center-x {3} --center-y {4} > grid_skeletons/grid_${city}_${resolution}.ssv :::: geocodes_nca/${city}; done;
resolution=600; for city in $(cat cities_europe.txt); do parallel -q --colsep ' ' python  scripts/create_grid_skeleton.py -r ${resolution} --center-x {3} --center-y {4} > grid_skeletons/grid_${city}_${resolution}.ssv :::: geocodes_europe/${city}; done;
resolution=600; for city in $(cat cities_australia_and_oceania.txt); do parallel -q --colsep ' ' python  scripts/create_grid_skeleton.py -r ${resolution} --center-x {3} --center-y {4} > grid_skeletons/grid_${city}_${resolution}.ssv :::: geocodes_australia_and_oceania/${city}; done;

#### Query the routing server

resolution=600; for city in $(cat cities_sa.txt); do parallel -q --colsep ' ' node scripts/get_directions.js -c --output-dir directions_sa/${city} \"{3}\" \"{4}\" \"{5}\" \"{6}\" :::: geocodes_sa/${city} :::: grid_skeletons/grid_${city}_${resolution}.ssv; find directions_sa/${city} -name "*.json" | xargs -n 1 gzip; done;
resolution=600; for city in $(cat cities_africa.txt); do parallel -q --colsep ' ' node scripts/get_directions.js -c --output-dir directions_africa/${city} \"{3}\" \"{4}\" \"{5}\" \"{6}\" :::: geocodes_africa/${city} :::: grid_skeletons/grid_${city}_${resolution}.ssv; find directions_africa/${city} -name "*.json" | xargs -n 1 gzip; done;
resolution=600; for city in $(cat cities_asia.txt); do parallel -q --colsep ' ' node scripts/get_directions.js -c --output-dir directions_asia/${city} \"{3}\" \"{4}\" \"{5}\" \"{6}\" :::: geocodes_asia/${city} :::: grid_skeletons/grid_${city}_${resolution}.ssv; find directions_asia/${city} -name "*.json" | xargs -n 1 gzip; done;
resolution=600; for city in $(cat cities_nca.txt); do parallel -q --colsep ' ' node scripts/get_directions.js -c --output-dir directions_nca/${city} \"{3}\" \"{4}\" \"{5}\" \"{6}\" :::: geocodes_nca/${city} :::: grid_skeletons/grid_${city}_${resolution}.ssv; find directions_nca/${city} -name "*.json" | xargs -n 1 gzip; done;
resolution=600; for city in $(cat cities_europe.txt); do parallel -q --colsep ' ' node scripts/get_directions.js -c --output-dir directions_europe/${city} \"{3}\" \"{4}\" \"{5}\" \"{6}\" :::: geocodes_europe/${city} :::: grid_skeletons/grid_${city}_${resolution}.ssv; find directions_europe/${city} -name "*.json" | xargs -n 1 gzip; done;
resolution=600; for city in $(cat cities_australia_and_oceania.txt); do parallel -q --colsep ' ' node scripts/get_directions.js -c --output-dir directions_australia_and_oceania/${city} \"{3}\" \"{4}\" \"{5}\" \"{6}\" :::: geocodes_australia_and_oceania/${city} :::: grid_skeletons/grid_${city}_${resolution}.ssv; find directions_australia_and_oceania/${city} -name "*.json" | xargs -n 1 gzip; done;

city=vienna; node scripts/get_directions.js -c --output-dir directions/${city} \"-0.686646\" \"45.752193\" \"-0.32959\" \"46.229253\"

#### Check to make sure everything went OK

ls geocodes_africa/ | sort > geocodes_list.txt
ls directions_africa/ | sort > directions_list.txt
diff directions_list.txt geocodes_list.txt

ls geocodes_asia/ | sort > geocodes_list.txt
ls directions_asia/ | sort > directions_list.txt
diff directions_list.txt geocodes_list.txt

ls geocodes_nca/ | sort > geocodes_list.txt
ls directions_nca/ | sort > directions_list.txt
diff directions_list.txt geocodes_list.txt

ls geocodes_europe/ | sort > geocodes_list.txt
ls directions_europe/ | sort > directions_list.txt
diff directions_list.txt geocodes_list.txt

#### Consolidate the connections

parallel 'find directions_africa/{}/ -type f  > file_lists/file_list_{}.txt; python scripts/parse_directions.py -l file_lists/file_list_{}.txt > all_connections/all_connections_{}.json' ::: $(cat cities_africa.txt)
parallel 'find directions_asia/{}/ -type f  > file_lists/file_list_{}.txt; python scripts/parse_directions.py -l file_lists/file_list_{}.txt > all_connections/all_connections_{}.json' ::: $(cat cities_asia.txt)
parallel 'find directions_europe/{}/ -type f  > file_lists/file_list_{}.txt; python scripts/parse_directions.py -l file_lists/file_list_{}.txt > all_connections/all_connections_{}.json' ::: $(cat cities_europe.txt)
parallel 'find directions_australia_and_oceania/{}/ -type f  > file_lists/file_list_{}.txt; python scripts/parse_directions.py -l file_lists/file_list_{}.txt > all_connections/all_connections_{}.json' ::: $(cat cities_australia_and_oceania.txt)
parallel 'find directions_nca/{}/ -type f  > file_lists/file_list_{}.txt; python scripts/parse_directions.py -l file_lists/file_list_{}.txt > all_connections/all_connections_{}.json' ::: $(cat cities_nca.txt)
parallel 'find directions_sa/{}/ -type f  > file_lists/file_list_{}.txt; python scripts/parse_directions.py -l file_lists/file_list_{}.txt > all_connections/all_connections_{}.json' ::: $(cat cities_sa.txt)

#### Create the grid

ln -s ~/projects/oebb/scripts/create_grid.py scripts/
method=time; walkspeed=5; resolution=300; parallel /usr/bin/time python scripts/create_grid.py all_connections/all_connections_{}.json -r ${resolution} --method ${method} --walking-speed ${walkspeed} {} '>' grids/grid_${method}_{}_${resolution}_${walkspeed}.json ::: $(cat cities_africa.txt)
method=time; walkspeed=5; resolution=300; parallel /usr/bin/time python scripts/create_grid.py all_connections/all_connections_{}.json -r ${resolution} --method ${method} --walking-speed ${walkspeed} {} '>' grids/grid_${method}_{}_${resolution}_${walkspeed}.json ::: $(cat cities_asia.txt)
method=time; walkspeed=5; resolution=300; parallel /usr/bin/time python scripts/create_grid.py all_connections/all_connections_{}.json -r ${resolution} --method ${method} --walking-speed ${walkspeed} {} '>' grids/grid_${method}_{}_${resolution}_${walkspeed}.json ::: $(cat cities_europe.txt)
method=time; walkspeed=5; resolution=300; parallel /usr/bin/time python scripts/create_grid.py all_connections/all_connections_{}.json -r ${resolution} --method ${method} --walking-speed ${walkspeed} {} '>' grids/grid_${method}_{}_${resolution}_${walkspeed}.json ::: $(cat cities_australia_and_oceania.txt)
method=time; walkspeed=5; resolution=300; parallel /usr/bin/time python scripts/create_grid.py all_connections/all_connections_{}.json -r ${resolution} --method ${method} --walking-speed ${walkspeed} {} '>' grids/grid_${method}_{}_${resolution}_${walkspeed}.json ::: $(cat cities_nca.txt)
method=time; walkspeed=5; resolution=300; parallel /usr/bin/time python scripts/create_grid.py all_connections/all_connections_{}.json -r ${resolution} --method ${method} --walking-speed ${walkspeed} {} '>' grids/grid_${method}_{}_${resolution}_${walkspeed}.json ::: $(cat cities_sa.txt)

#### Create the contours

ln -s ~/projects/oebb/python_contours/scripts/grid_to_contours.py scripts/
resolution=300; walkspeed=5; parallel python scripts/grid_to_contours.py grids/grid_time_{}_${resolution}_${walkspeed}.json  '>' contours/{}.json ::: $(cat cities_africa.txt)
resolution=300; walkspeed=5; parallel python scripts/grid_to_contours.py grids/grid_time_{}_${resolution}_${walkspeed}.json  '>' contours/{}.json ::: $(cat cities_asia.txt)
resolution=300; walkspeed=5; parallel python scripts/grid_to_contours.py grids/grid_time_{}_${resolution}_${walkspeed}.json  '>' contours/{}.json ::: $(cat cities_europe.txt)
resolution=300; walkspeed=5; parallel python scripts/grid_to_contours.py grids/grid_time_{}_${resolution}_${walkspeed}.json  '>' contours/{}.json ::: $(cat cities_australia_and_oceania.txt)
resolution=300; walkspeed=5; parallel python scripts/grid_to_contours.py grids/grid_time_{}_${resolution}_${walkspeed}.json  '>' contours/{}.json ::: $(cat cities_nca.txt)
resolution=300; walkspeed=5; parallel python scripts/grid_to_contours.py grids/grid_time_{}_${resolution}_${walkspeed}.json  '>' contours/{}.json ::: $(cat cities_sa.txt)

### Copy the contours to the emptypipes web site

cp contours/* ~/projects/emptypipes/jsons/isochrone_driving_contours/

### Create page templates

parallel python scripts/create_isochrone_driving_template.py geocodes_africa/{} '>' page_templates/{}.html ::: $(cat cities_africa.txt)
parallel python scripts/create_isochrone_driving_template.py geocodes_asia/{} '>' page_templates/{}.html ::: $(cat cities_asia.txt)
parallel python scripts/create_isochrone_driving_template.py geocodes_europe/{} '>' page_templates/{}.html ::: $(cat cities_europe.txt)
parallel python scripts/create_isochrone_driving_template.py geocodes_nca/{} '>' page_templates/{}.html ::: $(cat cities_nca.txt)
parallel python scripts/create_isochrone_driving_template.py geocodes_australia_and_oceania/{} '>' page_templates/{}.html ::: $(cat cities_australia_and_oceania.txt)
parallel python scripts/create_isochrone_driving_template.py geocodes_sa/{} '>' page_templates/{}.html ::: $(cat cities_sa.txt)

### Copy Page Template

cp page_templates/* ~/projects/emptypipes/supp/isochrone_driving/

### Create the cities list 

python scripts/create_city_list_table.py $(cat cities_africa.txt) > ~/projects/emptypipes/_includes/africa_isochrone_driving_cities_list.html
python scripts/create_city_list_table.py $(cat cities_sa.txt) > ~/projects/emptypipes/_includes/south_america_isochrone_driving_cities_list.html
python scripts/create_city_list_table.py $(cat cities_asia.txt) > ~/projects/emptypipes/_includes/asia_isochrone_driving_cities_list.html
python scripts/create_city_list_table.py $(cat cities_europe.txt) > ~/projects/emptypipes/_includes/europe_isochrone_driving_cities_list.html
python scripts/create_city_list_table.py $(cat cities_nca.txt) > ~/projects/emptypipes/_includes/nca_isochrone_driving_cities_list.html
python scripts/create_city_list_table.py $(cat cities_australia_and_oceania.txt) > ~/projects/emptypipes/_includes/australia_and_oceania_isochrone_driving_cities_list.html















LATEST ISSUES:

resolution=300; walkspeed=5; parallel python scripts/grid_to_contours.py grids/grid_time_{}_${resolution}_${walkspeed}.json  '>' contours/{}.json ::: asuncion bogota cayenne georgetown lima manaus montevideo paramaribo quito sao_paolo ushuaia buenos_aires caracas cartagena santiago atlanta belmopan charlotte chicago dallas denver edmonton fairbanks guatemala_city houston juneau lincoln los_angeles managua mexico_city miami minneapolis montreal new_york nome
