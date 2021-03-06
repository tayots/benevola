(function(){
'use strict';

angular.module('demoApp')
    .controller('addSectionController', ['$mdDialog', 'area', 'Sections', addSectionController]);

    function addSectionController ($mdDialog, area, Sections) {
        var vm = this;

        vm.section = {
            area: area,
            name: ''
        };

        vm.save = save;
        vm.cancel = cancel;

        /* Controller Functions here */

        function save () {
            Sections.post(vm.section)
                .then(function(response){
                    $mdDialog.hide(response);
                }, function(error){
                    console.log('Error: ', error);
                    // Show Errors
                });
        }

        function cancel () {
            $mdDialog.cancel();
        }

    }
}());