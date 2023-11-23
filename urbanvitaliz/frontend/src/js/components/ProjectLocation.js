import Alpine from 'alpinejs'

import * as L from 'leaflet';
import 'leaflet/dist/leaflet.css'
import 'leaflet-control-geocoder';
import 'leaflet-providers'

import geolocUtils from '../utils/geolocation/'
import mapUtils from '../utils/map/'

function ProjectLocation(projectOptions) {
	return {
		mapIsSmall: true,
		project: null,
		mapModal: null,
		editLocationModal: null,
		interactiveMap: null,
		zoom: 5,

		async init() {
			this.project = {
				...projectOptions,
				location_x: projectOptions.location_x ? parseFloat(projectOptions.location_x) : null,
				location_y: projectOptions.location_y ? parseFloat(projectOptions.location_y) : null,
				commune: {
					...projectOptions.commune,
					latitude: projectOptions.commune.latitude ? parseFloat(projectOptions.commune.latitude) : null,
					longitude: projectOptions.commune.longitude ? parseFloat(projectOptions.commune.longitude) : null,
				}
			}
			const options = mapUtils.mapOptions({interactive: false});
			const { latitude, longitude, insee } = this.project.commune;


			this.zoom = latitude && longitude ? 11 : this.zoom;

			const geoData = {}

			geoData.commune = await geolocUtils.fetchCommuneIgn(insee);
			geoData.location = await geolocUtils.fetchGeolocationByAddress(this.project.location);

			const Map = mapUtils.initMap('map', this.project, options, this.zoom);
			mapUtils.initMapLayers(Map, this.project, geoData);

			// forces map redraw to fit container
			setTimeout(function(){Map.invalidateSize()}, 0);

			//Center Map
			Map.panTo(new L.LatLng(latitude, longitude));

			this.initProjectMapModal(this.project, geoData);
		},

		initProjectMapModal(project, geoData) {
			const element = document.getElementById("project-map-modal");
			this.mapModal = new bootstrap.Modal(element);

			const options = mapUtils.mapOptions({interactive: true});
			const zoom = this.zoom + 1;
			const latitude = project.commune.latitude ?? 	geolocUtils.LAT_LNG_FRANCE[0];
			const longitude = project.commune.longitude ?? 	geolocUtils.LAT_LNG_FRANCE[1];

			this.interactiveMap = mapUtils.initMap('map-modal', project, options, zoom);
			this.interactiveMap.panTo(new L.LatLng(latitude, longitude));
			this.interactiveMap.setMinZoom(zoom - 7);
			this.interactiveMap.setMaxZoom(zoom + 6);

			const map = this.interactiveMap;
			element.addEventListener('shown.bs.modal', function (event) {
				 // forces map redraw to fit container
				setTimeout(function(){  map.invalidateSize()}, 0);
			})
			mapUtils.initMapLayers(this.interactiveMap, this.project, geoData);
		},

		openProjectMapModal() {
			this.mapIsSmall = false;
			this.mapModal.show();
		},
	}
}


Alpine.data("ProjectLocation", ProjectLocation)