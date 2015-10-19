Vienna url:

http://openls.geog.uni-heidelberg.de/testing2015/route?Start=8.6817521,49.4173462&End=8.6828883,49.4067577&Via=&lang=de&distunit=KM&routepref=Fastest&avoidAreas=&useTMC=false&noMotorways=false&noTollways=false&instructions=false

http://wiki.openstreetmap.org/wiki/OpenRouteService

cat input/cities.txt | xargs -n 2 -I {} python scripts/geocode.py -d geocodes "{}"
cat input/cities_us.txt | xargs -n 2 -I {} python scripts/geocode.py -d geocodes_us "{}"
cat input/cities_sa.txt | xargs -n 2 -I {} python scripts/geocode.py -d geocodes_sa "{}"
cat input/cities_africa.txt | xargs -n 2 -I {} python scripts/geocode.py -d geocodes_africa "{}"
cat input/cities_asia.txt | xargs -n 2 -I {} python scripts/geocode.py -d geocodes_asia "{}"

mv geocodes_us/new\ york geocodes_us/new_york
mv geocodes_us/los\ angeles geocodes_us/los_angeles
mv geocodes_us/san\ diego geocodes_us/san_diego
mv geocodes_us/san\ francisco geocodes_us/san_francisco

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

ls geocodes_sa/ > cities_sa.txt
ls geocodes_africa/ > cities_africa.txt
ls geocodes_asia/ > cities_asia.txt

#### Create the grid

resolution=600; for city in $(cat cities_sa.txt); do parallel -q --colsep ' ' python  scripts/create_grid_skeleton.py -r ${resolution} --center-x {3} --center-y {4} > grid_skeletons/grid_${city}_${resolution}.ssv :::: geocodes_sa/${city}; done;
resolution=600; for city in $(cat cities_africa.txt); do parallel -q --colsep ' ' python  scripts/create_grid_skeleton.py -r ${resolution} --center-x {3} --center-y {4} > grid_skeletons/grid_${city}_${resolution}.ssv :::: geocodes_africa/${city}; done;
resolution=600; for city in $(cat cities_asia.txt); do parallel -q --colsep ' ' python  scripts/create_grid_skeleton.py -r ${resolution} --center-x {3} --center-y {4} > grid_skeletons/grid_${city}_${resolution}.ssv :::: geocodes_asia/${city}; done;

#### Query the routing server

resolution=600; for city in $(cat cities_sa.txt); do parallel -q --colsep ' ' node scripts/get_directions.js -c --output-dir directions_sa/${city} \"{3}\" \"{4}\" \"{5}\" \"{6}\" :::: geocodes_sa/${city} :::: grid_skeletons/grid_${city}_${resolution}.ssv; find directions_sa/${city} -name "*.json" | xargs -n 1 gzip; done;


resolution=600; for city in $(cat cities_africa.txt); do parallel -q --colsep ' ' node scripts/get_directions.js -c --output-dir directions_africa/${city} \"{3}\" \"{4}\" \"{5}\" \"{6}\" :::: geocodes_africa/${city} :::: grid_skeletons/grid_${city}_${resolution}.ssv; find directions_africa/${city} -name "*.json" | xargs -n 1 gzip; done;

city=vienna; node scripts/get_directions.js -c --output-dir directions/${city} \"-0.686646\" \"45.752193\" \"-0.32959\" \"46.229253\"

#### Check to make sure everything went OK

ls geocodes_africa/ | sort > geocodes_list.txt
ls directions_africa/ | sort > directions_list.txt
diff directions_list.txt geocodes_list.txt

#### Consolidate the connections

parallel 'find directions_sa/{}/ -type f  > file_lists/file_list_{}.txt; python scripts/parse_directions.py -l file_lists/file_list_{}.txt > all_connections/all_connections_{}.json' ::: $(cat cities_sa.txt)
parallel 'find directions_africa/{}/ -type f  > file_lists/file_list_{}.txt; python scripts/parse_directions.py -l file_lists/file_list_{}.txt > all_connections/all_connections_{}.json' ::: $(cat cities_africa.txt)

#### Create the grid

ln -s ~/projects/oebb/scripts/create_grid.py scripts/
method=time; walkspeed=5; resolution=300; parallel /usr/bin/time python scripts/create_grid.py all_connections/all_connections_{}.json -r ${resolution} --method ${method} --walking-speed ${walkspeed} {} '>' grids/grid_${method}_{}_${resolution}_${walkspeed}.json ::: $(cat cities_africa.txt)

method=time; walkspeed=5; resolution=300; parallel /usr/bin/time python scripts/create_grid.py all_connections/all_connections_{}.json -r ${resolution} --min-x -12.4 --max-x 46.3 --min-y 33.1 --max-y 74.5 --method ${method} --walking-speed ${walkspeed} {} '>' grids/grid_${method}_{}_${resolution}_${walkspeed}.json ::: $(cat ~/projects/oebb/cities.txt)
method=time; walkspeed=5; resolution=300; parallel /usr/bin/time python scripts/create_grid.py all_connections/all_connections_{}.json -r ${resolution} --min-x -135.14 --max-x -63.9 --min-y 21.9 --max-y 62.2 --method ${method} --walking-speed ${walkspeed} {} '>' grids/grid_${method}_{}_${resolution}_${walkspeed}.json ::: $(cat ~/projects/oebb/cities_us.txt)

#### Create the contours

ln -s ~/projects/oebb/python_contours/scripts/grid_to_contours.py scripts/
resolution=300; parallel python scripts/grid_to_contours.py grids/grid_time_{}_${resolution}_5.json  '>' contours/{}.json ::: $(cat ~/projects/oebb/cities.txt)
resolution=300; parallel python scripts/grid_to_contours.py grids/grid_time_{}_${resolution}_5.json  '>' contours/{}.json ::: $(cat ~/projects/oebb/cities_us.txt)

resolution=300; parallel python scripts/grid_to_contours.py grids/grid_time_{}_${resolution}_5.json  '>' contours/{}.json ::: $(cat ~/projects/roadway_routing/cities_africa.txt)

### Copy the contours to the emptypipes web site

cp contours/* ~/projects/emptypipes/jsons/isochrone_driving_contours/

### Create page template

parallel python scripts/create_isochrone_driving_template.py geocodes_africa/{} '>' page_templates/{}.html ::: $(cat cities_africa.txt)

### Copy Page Template

cp page_templates/* ~/projects/emptypipes/supp/isochrone_driving/

### Create the cities list 

python scripts/create_city_list_table.py $(cat cities_africa.txt) > ~/projects/emptypipes/_includes/africa_isochrone_driving_cities_list.html
python scripts/create_city_list_table.py $(cat cities_sa.txt) > ~/projects/emptypipes/_includes/south_america_isochrone_driving_cities_list.html

