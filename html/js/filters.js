metadata.filter('range', function() {
    return function(arr, lower, upper) {
        for (var i = lower; i <= upper; i++){
            arr.push(i);
        }
        return arr;
    };
});

metadata.filter('chicagoStyle', ['JsonData', '$filter', function(JsonData, $filter) {
    return function(bib) {
        var settings = JsonData.citation.chicago;
        var citation = '';
        var compiler = '';
        var endsWith = function(str, suffix) {
            if(str){
                return str.indexOf(suffix, str.length - suffix.length) !== -1;
            }else{
                return str;
            }
        };
        var capitalize = function(str){
            if(str){
                return str.charAt(0).toUpperCase() + str.slice(1);
            }else{
                return str;
            }
        };
        var formatName = function(obj, order){
            console.log('in formatName function!');
            console.log(obj, order);
            var ret = '';
            if(angular.isString(obj)){ // if author name unstructured
                ret += obj;
            }
            if(angular.isObject(obj)){ // if only one author name given
                if(order === 1){ // last name, first name
                    if(obj.hasOwnProperty['surname']){
                        ret += obj['surname'];
                        if(obj.hasOwnProperty['given-names']){
                            ret += ', '+obj['given-names'];
                        }
                    }
                    console.log('order1: '+ret);
                }else if(order === 2){ // first name last name
                    if(obj.hasOwnProperty['given-names']){
                        ret += obj['given-names']+' ';
                    }
                    if(obj.hasOwnProperty['surname']){
                        ret += obj['surname'];
                    }
                    console.log('order2: '+ret);
                }
            }
            if(angular.isArray(obj)){ // if multiple authors given
                if(obj.length <= settings['etal']){
                    angular.forEach(obj, function(author, index){
                        if(obj.hasOwnProperty['surname']){
                            ret += bib['name']['surname'];
                            if(obj.hasOwnProperty['given-names']){
                                ret += ', '+obj['given-names'];
                            }
                        }
                        if(index + 1 === obj.length - 1){
                            ret += ', '+settings['and']+' '
                        } else if(index + 1 !== obj.length){
                            ret += ', '
                        }
                    });
                } else {
                    ret = obj[0]['surname']+', '+obj[0]['given-names']+' et al'
                }
            }
            return ret;
        };
        if(angular.isObject(bib)){
            if(bib.hasOwnProperty('person-group')){ // required
                if(angular.isObject(bib['person-group'])){ // if only one person group given
                    citation += formatName(bib['person-group']['string-name'], settings['nameOrder']);
                    console.log(bib['person-group']);
                    console.log(citation);
                    if(bib['person-group']['@person-group-type'] == 'translator'){
                            citation += ', trans';
                    } else if(bib['person-group']['@person-group-type'] == 'editor'){
                        if(angular.isArray(bib['person-group']['string-name']) && bib['person-group']['string-name'].length >= 1){
                            citation += ', eds';
                        } else {
                            citation += ', ed'
                        }
                    }
                } else if(angular.isArray(bib['person-group'])){
                    angular.forEach(bib['person-group'], function(group, index){
                        switch(group['@person-group-type']){
                            case 'author':
                                citation += formatName(group['string-name'], settings['nameOrder']);
                                break;
                            case 'editor':
                                compiler = (bib['chapter-title'])? 'e': 'E'+'dited by '+formatName(group['string-name'], 2)+(bib['fpage'])? ', ': '. ';
                                break;
                            case 'translator':
                                compiler = (bib['chapter-title'])? 't': 'T'+'ranslated by '+formatName(group['string-name'], 2)+(bib['fpage'])? ', ': '. ';
                                break;
                            default:
                                citation += formatName(group['string-name'], settings['nameOrder']);
                                break;
                        }
                    });
                }
                if(!endsWith(citation, '.')){
                    citation += '. ';
                }
            }
            if(bib.hasOwnProperty('chapter-title')){ // optional
                citation += '"'+bib['chapter-title']+'" In ';
            }
            if(bib.hasOwnProperty('source')){ // required
                citation += '<i>'+bib['source']+'</i>'+(bib['chapter-title'])? ', ': '. ';
            }
            console.log('after source: '+citation);
            citation += compiler;
            if(bib.hasOwnProperty('fpage')){
                citation += bib['fpage'];
                if(bib.hasOwnProperty('lpage') && bib['fpage'] !== bib['lpage']){
                    citation += '-'+bib['lpage']+'. ';
                }
            }
            if(bib.hasOwnProperty('publisher-loc')){ // required
                citation += bib['publisher-loc']+': ';
            }
            if(bib.hasOwnProperty('publisher-name')){ // required
                citation += bib['publisher-name']+', ';
            }
            if(bib.hasOwnProperty('year')){ // required
                citation += bib['year']+'. ';
            }
            if(bib.hasOwnProperty('date-in-citation')){
                citation += capitalize(bib['date-in-citation']['@content-type'])+' '+$filter('date')(new Date(bib['date-in-citation']['#text']), 'MMM dd yyyy')+'. ';
            }
            if(bib.hasOwnProperty('ext-link')){ // required
                citation += bib['ext-link']['#text']+'. ';
            }
            if(endsWith(citation, ' ')){
                citation.slice(0, -1);
            }
        } else {
            citation = bib;
        }
        return citation;
    };
}]);
