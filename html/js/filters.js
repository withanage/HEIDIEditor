metadata.filter('range', function() {
    return function(arr, lower, upper) {
        for (var i = lower; i <= upper; i++){
            arr.push(i);
        }
        return arr;
    };
});

metadata.filter('chicagoStyleBook', function() {
    return function(bib) {
        var citation = '';
        if(angular.isObject(bib)){
            if(bib.hasOwnProperty('person-group-type')){
                if(bib.hasOwnProperty('name')){ // author
                    if(angular.isString(bib['name'])){
                        citation += bib['name']+'. ';
                    }
                    if(angular.isObject(bib['name'])){ // if only one author given
                        if(bib['name'].hasOwnProperty['surname']){
                            citation += bib['name']['surname'];
                            if(bib['name'].hasOwnProperty['given-names']){
                                citation += ', '+bib['name']['given-names'];
                            }
                            citation += '. ';
                        }
                    }
                    if(angular.isArray(bib['name'])){ // if multiple authors given
                        angular.forEach(bib['name'])
                        if(bib['name'].hasOwnProperty['surname']){
                            citation += bib['name']['surname'];
                            if(bib['name'].hasOwnProperty['given-names']){
                                citation += ', '+bib['name']['given-names'];
                            }
                            citation += '. ';
                        }
                    }
                }
            }
            if(bib.hasOwnProperty('year')){
                citation += bib['year']+'. ';
            }
            if(bib.hasOwnProperty('source')){
                citation += '<i>'+bib['source']+'</i>. ';
            }
            if(bib.hasOwnProperty('publisher-loc')){
                citation += bib['publisher-loc']+': ';
            }
            if(bib.hasOwnProperty('publisher-name')){
                citation += bib['publisher-name']+'.';
            }
        } else {
            citation = bib;
        }
        return citation;
    };
});
