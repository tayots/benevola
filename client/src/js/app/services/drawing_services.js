(function () {
    'use strict';

    angular.module('demoApp')
        .factory('drawingServices', ['gmapServices', '$rootScope', drawingServices]);

    function drawingServices(gmapServices, $rootScope) {

        var service = {};
        service.drawingManager = null;
        service.drawingCompleteListener = null;

        service.overlay = null;
        service.overlayType = '';
        service.overlayDataArray = [];

        service.strokeColor = '';

        service.duplicateLotPolygon = null;

        service.updateLotPolygon = null;

        /**
         * Functions
         */
        service.initDrawingManager = initDrawingManager;
        service.initDrawingListener = initDrawingListener;
        service.setPanControl = setPanControl;
        service.hideDrawingManager = hideDrawingManager;
        service.startDrawingMode = startDrawingMode;
        service.setListenerOfType = setListenerOfType;
        service.stopDrawingMode = stopDrawingMode;
        service.hideOverlay = hideOverlay;
        service.clearOverlay = clearOverlay;
        service.getAreaCoords = getAreaCoords;
        service.getAreaFormData = getAreaFormData;
        service.getPolygonCoords = getPolygonCoords;
        service.getRectangleCorners = getRectangleCorners;
        service.getRectangleCoords = getRectangleCoords;
        service.duplicateLot = duplicateLot;
        service.destroyDuplicateLot = destroyDuplicateLot;
        service.destroyUpdateLotPolygon = destroyUpdateLotPolygon;


        function initDrawingManager() {
            if (service.drawingManager) {
                if(service.overlayStrokeColor) gmapServices.changeDrawingManagerStrokeColor(service.overlayStrokeColor);

                // Reinitialize Drawing Listener
                service.initDrawingListener();
                return;
            }

            service.drawingManager = gmapServices.createDrawingManager(service.overlayStrokeColor);
            service.initDrawingListener();
        }


        function initDrawingListener() {
            if (!service.drawingManager) return;

            if (service.drawingCompleteListener) return;

            service.drawingCompleteListener = gmapServices.addListener(
                service.drawingManager, 'overlaycomplete', overlayCompleteListener);
        }


        function overlayCompleteListener(eventArgs) {
            // Set only one overlay
            if (service.overlay) {
                service.overlay.setMap(null);
                service.overlay = null;
                service.overlayDataArray = [];
            }

            service.overlay = eventArgs.overlay;
            service.overlay.setMap(gmapServices.map);

            service.overlayType = eventArgs.type;
            service.overlayDataArray = service.getAreaCoords();

            // Add Listener when overlay is resized
            service.setListenerOfType(eventArgs, function (args) {
                service.overlay = args.overlay;
                service.overlayType = args.type;
                service.overlayDataArray = service.getAreaCoords();
            });

            // Set control to pan every after drawing
            service.setPanControl();

            $rootScope.$broadcast('overlay-complete');
        }


        function setPanControl() {
            service.drawingManager.setDrawingMode(null);
        }


        function hideDrawingManager() {
            if (service.drawingManager) {
                gmapServices.hideDrawingManager(service.drawingManager);
            }
        }

        function startDrawingMode(strokeColor) {
            if(strokeColor) service.overlayStrokeColor = strokeColor;

            service.initDrawingManager();

            gmapServices.showDrawingManager(service.drawingManager);
        }

        function setListenerOfType(eArgs, callbackFn) {
            switch (eArgs.type) {
                // Add Listener Events For Rectangle Changed
                case google.maps.drawing.OverlayType.RECTANGLE:
                    google.maps.event.addListener(eArgs.overlay, 'bounds_changed', function () {
                        callbackFn(eArgs);
                    });
                    break;
                // Add Listener Events For Polygon Changed
                case google.maps.drawing.OverlayType.POLYGON:
                    google.maps.event.addListener(eArgs.overlay.getPath(), 'set_at', function () {
                        callbackFn(eArgs);
                    });
                    google.maps.event.addListener(eArgs.overlay.getPath(), 'insert_at', function (e) {
                        callbackFn(eArgs);
                    });
            }
        }

        function stopDrawingMode() {
            if (service.drawingCompleteListener) {
                gmapServices.removeListener(service.drawingCompleteListener);
                service.drawingCompleteListener = null;
            }

            service.hideDrawingManager();

            service.hideOverlay();
        }

        function cancelDrawingMode() {
            service.stopDrawingMode();
        }

        function hideOverlay() {
            if (!service.overlay) return;

            service.overlay.setMap(null);
            service.overlay = null;
        }

        function clearOverlay() {
            hideOverlay();

            service.overlayDataArray = [];
            service.overlayType = '';
        }

        function getAreaCoords() {
            if (service.overlayType == google.maps.drawing.OverlayType.POLYGON) {
                return service.getPolygonCoords();
            }
            else if (service.overlayType == google.maps.drawing.OverlayType.RECTANGLE) {
                return service.getRectangleCorners();
            }

            return [];
        }

        function getPolygonCoords(_polygon) {
            var polygon = _polygon || service.overlay;

            if (!polygon) return;

            var path = polygon.getPath().getArray();
            var data = [];

            for (var index in path) {
                data.push({
                    lat: path[index].lat(),
                    lng: path[index].lng()
                });
            }

            return data;
        }

        function getAreaFormData(_area) {
            return getPolygonCoords(_area);
        }

        function getRectangleCorners(_rect) {
            var rect = _rect || service.overlay;

            if (!rect) return;

            var bounds = rect.getBounds();
            var min = bounds.getNorthEast();
            var max = bounds.getSouthWest();
            var data = [];

            data.push({lat: min.lat(), lng: min.lng()});
            data.push({lat: max.lat(), lng: min.lng()});
            data.push({lat: max.lat(), lng: max.lng()});
            data.push({lat: min.lat(), lng: max.lng()});

            return data;
        }

        function getRectangleCoords() {
            if (!service.overlay) return;

            var bounds = service.overlay.getBounds();
            var min = bounds.getNorthEast(),
                max = bounds.getSouthWest();
            var data = [];

            data.push({lat: min.lat(), lng: min.lng()});
            data.push({lat: max.lat(), lng: max.lng()});

            return data;
        }

        service.editablePolyOpts = {
            clickable: true,
            draggable: true,
            editable: true,
            geodesic: false,
            fillColor: '#ffffff',
            fillOpacity: 0,
            strokeColor: service.strokeColor,
            strokeOpacity: 0.9,
            strokeWeight: 2,
            zIndex: 99999
        };

        function duplicateLot (lot) {
            if (!lot.polygon) return;
            var path = angular.copy(lot.polygon.getPath());

            if (!service.duplicateLotPolygon)  service.duplicateLotPolygon = gmapServices.createCustomPolygon(path, service.editablePolyOpts);
            else service.duplicateLotPolygon.setPath(path);

            // broadcast here
            $rootScope.$broadcast('duplicate-complete');
        }

        function destroyDuplicateLot () {
            if(!service.duplicateLotPolygon) return;

            service.duplicateLotPolygon.setMap(null);
            service.duplicateLotPolygon = null;
        }

        function destroyUpdateLotPolygon () {
            service.updateLotPolygon = null;
        }

        return service;
    }

}());
