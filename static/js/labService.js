/**
 * Created by filyushin_dv on 08.12.2015.
 */

var testsFn = function(){
    return{
        tests:
        [
            {
                    id: '100',
                    name: 'Hg'
            },
            {
                    id: '200',
                    name: 'Mk'
            }
        ]
    }
};
myApp.service('labService', testsFn);