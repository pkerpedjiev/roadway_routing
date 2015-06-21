var http = require('http');
var fs = require('fs');
var path = require('path');
var mkdirp = require('mkdirp');

var replacePoints = function(json) {
    var paths = json.paths;

    for (var i = 0; i < paths.length; i++) {
        var points = paths[i].points;
        var parsedPoints = decodePath(points);
        paths[i].points = [];
        paths[i].startPoint = {'lon': parsedPoints[0][0],
                               'lat': parsedPoints[0][1]};
        paths[i].endPoint = {'lon': parsedPoints[parsedPoints.length-1][0],
                             'lat': parsedPoints[parsedPoints.length-1][1]};

    }

    return json;
};

var storeResults = function(json, outPath, outDir) {
    var fs = require('fs');

    if (!fs.existsSync(outDir)) {
        console.log('creating dir', outDir);
        mkdirp.sync(outDir);
        //fs.mkdirSync(outPath);
    }

    console.log('outPath', outPath);
    fs.writeFile(outPath, JSON.stringify(json), function(err) {
        if(err) {
            return console.log(err);
        }
    }); 
};

var main = function() {
    var argv = require('minimist')(process.argv.slice(2));

    // where we store all of the returned requests
    if (!('output-dir' in argv)) {
        argv['output-dir'] = '.';
    }

    if (argv._.length < 4) {
        console.log('Not enough arguments:', argv._);
    }

    //remove the double quotes from the arguments;
    for (var i = 0; i < argv._.length; i++) {
        argv._[i] = argv._[i].replace(/['"]+/g, '');
    }

    // prepare the http request
    var options = {
      host: 'localhost',
      port: 8989,
      path: '/route?point=' + argv._[1] + '%2C' + argv._[0] + '&point=' + argv._[3] + '%2C' + argv._[2] //%2C13.930664&point=47.027195%2C12.322712
    };

    http.get(options, function(resp){
        resp.setEncoding('utf-8');
        var responseParts = [];

      resp.on('data', function(chunk){
          responseParts.push(chunk);
      });

      resp.on('end', function() {
        //do something with chunk
        try {
            var json = JSON.parse(responseParts.join(''));

            if ('paths' in json) {
                json = replacePoints(json);
                storeResults(json,
                            path.join(argv['output-dir'] ,argv._.join('_') + '.json' ),
                            argv['output-dir']);
            }   
        } catch (err) {
            console.log('ERROR: path:', options.path);
            console.log('err:', err);
            //console.log(responseParts.join(''));
        }
      });

    }).on("error", function(e){
      console.log("Got error: " + e.message);
    });

};

if (require.main === module) {
    main();
}

function decodePath(encoded, is3D) {
    // var start = new Date().getTime();
    var len = encoded.length;
    var index = 0;
    var array = [];
    var lat = 0;
    var lng = 0;
    var ele = 0;

    while (index < len) {
        var b;
        var shift = 0;
        var result = 0;
        do {
            b = encoded.charCodeAt(index++) - 63;
            result |= (b & 0x1f) << shift;
            shift += 5;
        } while (b >= 0x20);
        var deltaLat = ((result & 1) ? ~(result >> 1) : (result >> 1));
        lat += deltaLat;

        shift = 0;
        result = 0;
        do {
            b = encoded.charCodeAt(index++) - 63;
            result |= (b & 0x1f) << shift;
            shift += 5;
        } while (b >= 0x20);
        var deltaLon = ((result & 1) ? ~(result >> 1) : (result >> 1));
        lng += deltaLon;

        if (is3D) {
            // elevation
            shift = 0;
            result = 0;
            do
            {
                b = encoded.charCodeAt(index++) - 63;
                result |= (b & 0x1f) << shift;
                shift += 5;
            } while (b >= 0x20);
            var deltaEle = ((result & 1) ? ~(result >> 1) : (result >> 1));
            ele += deltaEle;
            array.push([lng * 1e-5, lat * 1e-5, ele / 100]);
        } else
            array.push([lng * 1e-5, lat * 1e-5]);
    }
    // var end = new Date().getTime();
    // console.log("decoded " + len + " coordinates in " + ((end - start) / 1000) + "s");
    return array;
}
