let map;
let userLocation = null;
let markers = [];
let userMarker = null;

// Initialize the map with Leaflet and Geoapify
function initMap() {
    console.log('Medical Facility Finder loaded');
    
    // Initialize Leaflet map centered on New Delhi, India
    map = L.map('map').setView([28.6139, 77.2090], 11);

    // Add OpenStreetMap tile layer (free, no API key required)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18,
    }).addTo(map);
    
    // Event listeners
    document.getElementById('find-location-btn').addEventListener('click', findUserLocation);
    document.getElementById('search-location-btn').addEventListener('click', searchManualLocation);
    document.getElementById('search-facilities-btn').addEventListener('click', searchNearbyFacilities);
    
    // Enable search on Enter key for manual location input
    document.getElementById('manual-location-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchManualLocation();
        }
    });
    
    // Automatically load and display medical facilities on map initialization
    loadDefaultFacilities();
}

// Find user's current location
function findUserLocation() {
    const locationStatus = document.getElementById('location-status');
    const locationText = document.getElementById('location-text');
    const findLocationBtn = document.getElementById('find-location-btn');
    
    if (navigator.geolocation) {
        findLocationBtn.disabled = true;
        findLocationBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Getting Location...';
        
        locationStatus.className = 'alert alert-info';
        locationStatus.classList.remove('d-none');
        locationText.textContent = 'Getting your location...';
        
        navigator.geolocation.getCurrentPosition(
            (position) => {
                userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                
                // Update map center
                map.setView([userLocation.lat, userLocation.lng], 15);
                
                // Clear existing markers
                clearMarkers();
                
                // Add user location marker
                userMarker = L.marker([userLocation.lat, userLocation.lng], {
                    icon: L.divIcon({
                        html: '<div style="background-color: #007bff; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>',
                        iconSize: [20, 20],
                        iconAnchor: [10, 10],
                        className: 'user-location-marker'
                    })
                }).addTo(map);
                
                userMarker.bindPopup("Your Location");
                
                locationStatus.className = 'alert alert-success';
                locationText.textContent = `Location found: ${position.coords.latitude.toFixed(6)}, ${position.coords.longitude.toFixed(6)}`;
                
                // Enable search button
                document.getElementById('search-facilities-btn').disabled = false;
                
                findLocationBtn.disabled = false;
                findLocationBtn.innerHTML = '<i class="fas fa-crosshairs me-2"></i>Find My Location';
            },
            (error) => {
                console.error('Geolocation error:', error);
                locationStatus.className = 'alert alert-danger';
                locationStatus.classList.remove('d-none');
                
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        locationText.textContent = 'Location access denied. Please enable location services.';
                        break;
                    case error.POSITION_UNAVAILABLE:
                        locationText.textContent = 'Location information unavailable.';
                        break;
                    case error.TIMEOUT:
                        locationText.textContent = 'Location request timed out.';
                        break;
                    default:
                        locationText.textContent = 'An unknown error occurred while getting location.';
                        break;
                }
                
                findLocationBtn.disabled = false;
                findLocationBtn.innerHTML = '<i class="fas fa-crosshairs me-2"></i>Find My Location';
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    } else {
        locationStatus.className = 'alert alert-danger';
        locationStatus.classList.remove('d-none');
        locationText.textContent = 'Geolocation is not supported by this browser.';
    }
}

// Search for location manually using address/city/zip
function searchManualLocation() {
    const locationInput = document.getElementById('manual-location-input');
    const searchQuery = locationInput.value.trim();
    
    if (!searchQuery) {
        alert('Please enter an address, city, or ZIP code.');
        return;
    }
    
    let locationStatus = document.getElementById('location-status');
    let locationText = document.getElementById('location-text');
    const searchBtn = document.getElementById('search-location-btn');
    
    // Create status elements if they don't exist
    if (!locationStatus) {
        locationStatus = document.createElement('div');
        locationStatus.id = 'location-status';
        locationStatus.className = 'alert alert-info';
        locationInput.parentNode.parentNode.appendChild(locationStatus);
        
        locationText = document.createElement('small');
        locationText.id = 'location-text';
        locationStatus.appendChild(locationText);
    }
    
    // Show loading state
    searchBtn.disabled = true;
    searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    
    locationStatus.className = 'alert alert-info';
    locationStatus.classList.remove('d-none');
    locationText.textContent = 'Searching for location...';
    
    // First, try to search for hospitals with this name in India
    const hospitalSearchUrl = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery + ' India')}&limit=10&addressdetails=1&countrycodes=in`;
    
    fetch(hospitalSearchUrl)
        .then(response => response.json())
        .then(hospitalData => {
            searchBtn.disabled = false;
            searchBtn.innerHTML = '<i class="fas fa-search"></i>';
            
            if (hospitalData && hospitalData.length > 0) {
                // Found hospital(s) - use the first one
                const hospital = hospitalData[0];
                userLocation = {
                    lat: parseFloat(hospital.lat),
                    lng: parseFloat(hospital.lon)
                };
                
                // Update map center
                map.setView([userLocation.lat, userLocation.lng], 16);
                
                // Clear existing markers
                clearMarkers();
                
                // Add hospital location marker
                userMarker = L.marker([userLocation.lat, userLocation.lng], {
                    icon: L.divIcon({
                        html: '<div style="background-color: #28a745; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>',
                        iconSize: [20, 20],
                        iconAnchor: [10, 10],
                        className: 'user-location-marker'
                    })
                }).addTo(map);
                
                // Enable search button
                document.getElementById('search-facilities-btn').disabled = false;
                
                locationStatus.className = 'alert alert-success';
                locationStatus.classList.remove('d-none');
                locationText.textContent = `Hospital found: ${hospital.display_name}`;
                
                // Auto-search for nearby facilities
                searchNearbyFacilities();
                
            } else {
                // No hospital found, try general location search in India
                const geocodeUrl = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery + ' India')}&limit=1&addressdetails=1&countrycodes=in`;
                
                fetch(geocodeUrl)
                    .then(response => response.json())
                    .then(data => {
                        if (data && data.length > 0) {
                            const result = data[0];
                            userLocation = {
                                lat: parseFloat(result.lat),
                                lng: parseFloat(result.lon)
                            };
                            
                            // Update map center
                            map.setView([userLocation.lat, userLocation.lng], 15);
                            
                            // Clear existing markers
                            clearMarkers();
                            
                            // Add user location marker
                            userMarker = L.marker([userLocation.lat, userLocation.lng], {
                                icon: L.divIcon({
                                    html: '<div style="background-color: #007bff; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>',
                                    iconSize: [20, 20],
                                    iconAnchor: [10, 10],
                                    className: 'user-location-marker'
                                })
                            }).addTo(map);
                            
                            // Enable search button
                            document.getElementById('search-facilities-btn').disabled = false;
                            
                            locationStatus.className = 'alert alert-success';
                            locationStatus.classList.remove('d-none');
                            locationText.textContent = `Location found: ${result.display_name}`;
                            
                        } else {
                            locationStatus.className = 'alert alert-warning';
                            locationStatus.classList.remove('d-none');
                            locationText.textContent = 'Location not found. Please try a different address or hospital name.';
                        }
                    })
                    .catch(error => {
                        console.error('Geocoding error:', error);
                        locationStatus.className = 'alert alert-danger';
                        locationStatus.classList.remove('d-none');
                        locationText.textContent = 'Error searching for location. Please try again.';
                    });
            }
        })
        .catch(error => {
            console.error('Hospital search error:', error);
            searchBtn.disabled = false;
            searchBtn.innerHTML = '<i class="fas fa-search"></i>';
            
            locationStatus.className = 'alert alert-danger';
            locationStatus.classList.remove('d-none');
            locationText.textContent = 'Error searching for location. Please try again.';
        });
}

// Search for nearby medical facilities
function searchNearbyFacilities() {
    if (!userLocation) {
        alert('Please find your location first.');
        return;
    }
    
    const radius = document.getElementById('radius-select').value;
    const facilityType = document.getElementById('facility-type-select').value;
    const loadingSpinner = document.querySelector('.loading-spinner');
    const searchBtn = document.getElementById('search-facilities-btn');
    
    // Show loading state
    loadingSpinner.style.display = 'block';
    searchBtn.disabled = true;
    searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Searching...';
    
    // Clear existing facility markers
    clearMarkers();
    
    // Add user location marker back
    if (userMarker) {
        userMarker.addTo(map);
    }
    
    // Fetch nearby facilities with type filter
    fetch(`/health/api/nearby-facilities?lat=${userLocation.lat}&lng=${userLocation.lng}&radius=${radius}&type=${facilityType}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            searchBtn.disabled = false;
            searchBtn.innerHTML = '<i class="fas fa-search me-2"></i>Search Facilities';
            loadingSpinner.style.display = 'none';
            
            if (data.facilities && data.facilities.length > 0) {
                displayFacilities(data.facilities);
                updateFacilitiesList(data.facilities);
            } else {
                // Fallback to OpenStreetMap search
                searchOSMFacilities();
            }
        })
        .catch(error => {
            console.error('API search failed, using OpenStreetMap search:', error);
            searchBtn.disabled = false;
            searchBtn.innerHTML = '<i class="fas fa-search me-2"></i>Search Facilities';
            
            // Fallback to OpenStreetMap search
            searchOSMFacilities();
        });
}

// Fallback search using OpenStreetMap Overpass API
function searchOSMFacilities() {
    const radius = document.getElementById('radius-select').value;
    const facilityType = document.getElementById('facility-type-select').value;
    const loadingSpinner = document.querySelector('.loading-spinner');
    
    loadingSpinner.style.display = 'block';
    
    // Define Overpass query based on facility type
    let amenityQuery = '';
    switch(facilityType) {
        case 'hospital':
            amenityQuery = 'amenity=hospital';
            break;
        case 'clinic':
            amenityQuery = 'amenity=clinic';
            break;
        case 'pharmacy':
            amenityQuery = 'amenity=pharmacy';
            break;
        case 'dentist':
            amenityQuery = 'amenity=dentist';
            break;
        case 'doctors':
            amenityQuery = 'amenity=doctors';
            break;
        default:
            amenityQuery = 'amenity~"^(hospital|clinic|doctors|pharmacy|dentist)$"';
    }
    
    // Overpass API query - focused on India
    const overpassQuery = `
        [out:json][timeout:25];
        (
          node["${amenityQuery}"](around:${radius * 1609.34},${userLocation.lat},${userLocation.lng});
          way["${amenityQuery}"](around:${radius * 1609.34},${userLocation.lat},${userLocation.lng});
          relation["${amenityQuery}"](around:${radius * 1609.34},${userLocation.lat},${userLocation.lng});
        );
        out center meta;
    `;
    
    const overpassUrl = 'https://overpass-api.de/api/interpreter';
    
    fetch(overpassUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `data=${encodeURIComponent(overpassQuery)}`
    })
    .then(response => response.json())
    .then(data => {
        loadingSpinner.style.display = 'none';
        
        if (data.elements && data.elements.length > 0) {
            const facilities = data.elements.map(element => {
                // Get coordinates (handle different OSM element types)
                let lat, lon;
                if (element.lat && element.lon) {
                    lat = element.lat;
                    lon = element.lon;
                } else if (element.center) {
                    lat = element.center.lat;
                    lon = element.center.lon;
                } else {
                    return null;
                }
                
                return {
                    id: element.id,
                    name: element.tags?.name || 'Medical Facility',
                    type: element.tags?.amenity || facilityType,
                    address: formatAddress(element.tags),
                    lat: lat,
                    lng: lon,
                    phone: element.tags?.phone || 'Not available',
                    website: element.tags?.website || '',
                    opening_hours: element.tags?.opening_hours || 'Hours not specified',
                    wheelchair: element.tags?.wheelchair || 'Unknown'
                };
            }).filter(facility => facility !== null);
            
            if (facilities.length > 0) {
                displayFacilities(facilities);
                updateFacilitiesList(facilities);
                updateResultsInfo(facilities.length);
            } else {
                showNoResultsMessage();
            }
        } else {
            showNoResultsMessage();
        }
    })
    .catch(error => {
        console.error('Overpass API error:', error);
        loadingSpinner.style.display = 'none';
        showErrorMessage('Failed to search for facilities. Please try again.');
    });
}

// Clear all markers from map
function clearMarkers() {
    markers.forEach(marker => {
        map.removeLayer(marker);
    });
    markers = [];
}

// Display facilities on map
function displayFacilities(facilities) {
    clearMarkers();
    
    // Add user location marker back
    if (userMarker) {
        userMarker.addTo(map);
    }
    
    facilities.forEach((facility, index) => {
        const marker = L.marker([facility.lat, facility.lng], {
            icon: L.divIcon({
                html: `<div class="facility-marker ${facility.type}">
                         <i class="${getFacilityIcon(facility.type)}"></i>
                         <span class="facility-number">${index + 1}</span>
                       </div>`,
                iconSize: [40, 40],
                iconAnchor: [20, 40],
                className: 'custom-facility-marker'
            })
        });
        
        // Create popup content
        const popupContent = `
            <div class="facility-popup">
                <h6>${facility.name}</h6>
                <p class="facility-type">${facility.type.charAt(0).toUpperCase() + facility.type.slice(1)}</p>
                <p class="facility-address">${facility.address}</p>
                ${facility.phone !== 'Not available' ? `<p class="facility-phone"><i class="fas fa-phone"></i> ${facility.phone}</p>` : ''}
                <div class="popup-actions">
                    <button class="btn btn-sm btn-primary" onclick="getDirections(${facility.lat}, ${facility.lng}, '${facility.name}')">
                        <i class="fas fa-directions"></i> Directions
                    </button>
                    ${facility.phone !== 'Not available' ? `<button class="btn btn-sm btn-success" onclick="callFacility('${facility.phone}')"><i class="fas fa-phone"></i> Call</button>` : ''}
                </div>
            </div>
        `;
        
        marker.bindPopup(popupContent);
        marker.addTo(map);
        markers.push(marker);
    });
    
    // Fit map bounds to show all markers
    if (markers.length > 0) {
        // Create feature group with markers, include userMarker only if it exists
        const markersForBounds = userMarker ? [userMarker, ...markers] : markers;
        const group = new L.featureGroup(markersForBounds);
        map.fitBounds(group.getBounds().pad(0.1));
    }
}

// Update facilities list in sidebar
function updateFacilitiesList(facilities) {
    const facilitiesList = document.getElementById('facilities-list');
    
    if (facilities.length === 0) {
        facilitiesList.innerHTML = '<p class="text-muted">No facilities found in the selected area.</p>';
        return;
    }
    
    let listHTML = '';
    facilities.forEach((facility, index) => {
        // Calculate distance only if user location is available
        let distance = 'Unknown';
        if (userLocation) {
            distance = calculateDistance(userLocation.lat, userLocation.lng, facility.lat, facility.lng).toFixed(1) + ' km';
        } else {
            distance = 'Distance unknown';
        }
        
        listHTML += `
            <div class="facility-item" onclick="focusOnFacility(${facility.lat}, ${facility.lng}, ${index})">
                <div class="facility-number">${index + 1}</div>
                <div class="facility-details">
                    <h6>${facility.name}</h6>
                    <p class="facility-type">${facility.type.charAt(0).toUpperCase() + facility.type.slice(1)}</p>
                    <p class="facility-address">${facility.address}</p>
                    <p class="facility-distance">${distance} away</p>
                    ${facility.hours && facility.hours !== 'Hours not specified' ? `<p class="facility-hours"><i class="fas fa-clock"></i> ${facility.hours}</p>` : ''}
                </div>
                <div class="facility-actions">
                    <button class="btn btn-sm btn-outline-primary" onclick="event.stopPropagation(); getDirections(${facility.lat}, ${facility.lng}, '${facility.name}')">
                        <i class="fas fa-directions"></i>
                    </button>
                    ${facility.phone !== 'Not available' ? `<button class="btn btn-sm btn-outline-success" onclick="event.stopPropagation(); callFacility('${facility.phone}')"><i class="fas fa-phone"></i></button>` : ''}
                </div>
            </div>
        `;
    });
    
    facilitiesList.innerHTML = listHTML;
}

// Get facility icon based on type
function getFacilityIcon(type) {
    const icons = {
        hospital: 'fas fa-hospital',
        clinic: 'fas fa-clinic-medical',
        doctors: 'fas fa-user-md',
        pharmacy: 'fas fa-pills',
        dentist: 'fas fa-tooth'
    };
    return icons[type] || 'fas fa-map-marker-alt';
}

// Format address from OSM tags
function formatAddress(tags) {
    const parts = [];
    if (tags['addr:housenumber']) parts.push(tags['addr:housenumber']);
    if (tags['addr:street']) parts.push(tags['addr:street']);
    if (tags['addr:city']) parts.push(tags['addr:city']);
    if (tags['addr:postcode']) parts.push(tags['addr:postcode']);
    
    return parts.length > 0 ? parts.join(', ') : 'Address not available';
}

// Calculate distance between two points
function calculateDistance(lat1, lng1, lat2, lng2) {
    const R = 6371; // Earth's radius in kilometers
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLng = (lng2 - lng1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLng/2) * Math.sin(dLng/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
}

// Focus on specific facility
function focusOnFacility(lat, lng, index) {
    map.setView([lat, lng], 16);
    if (markers[index]) {
        markers[index].openPopup();
    }
}

// Get directions to facility
function getDirections(lat, lng, name) {
    if (userLocation) {
        const url = `https://www.google.com/maps/dir/${userLocation.lat},${userLocation.lng}/${lat},${lng}`;
        window.open(url, '_blank');
    } else {
        const url = `https://www.google.com/maps/search/${lat},${lng}`;
        window.open(url, '_blank');
    }
}

// Call facility
function callFacility(phone) {
    window.location.href = `tel:${phone}`;
}

// Update results info
function updateResultsInfo(count) {
    const resultsInfo = document.getElementById('results-info');
    if (resultsInfo) {
        resultsInfo.textContent = `Found ${count} medical facilities near your location`;
    }
}

// Show no results message
function showNoResultsMessage() {
    const facilitiesList = document.getElementById('facilities-list');
    facilitiesList.innerHTML = `
        <div class="no-results">
            <i class="fas fa-search fa-2x text-muted mb-3"></i>
            <h6>No facilities found</h6>
            <p class="text-muted">Try increasing the search radius or selecting a different facility type.</p>
        </div>
    `;
    
    updateResultsInfo(0);
}

// Show error message
function showErrorMessage(message) {
    const facilitiesList = document.getElementById('facilities-list');
    facilitiesList.innerHTML = `
        <div class="error-message">
            <i class="fas fa-exclamation-triangle fa-2x text-warning mb-3"></i>
            <h6>Search Error</h6>
            <p class="text-muted">${message}</p>
            <button class="btn btn-primary btn-sm" onclick="searchNearbyFacilities()">Try Again</button>
        </div>
    `;
}

// Load and display default medical facilities on map initialization
function loadDefaultFacilities() {
    console.log('Loading default medical facilities...');
    
    // Show loading state
    const facilitiesList = document.getElementById('facilities-list');
    if (facilitiesList) {
        facilitiesList.innerHTML = `
            <div class="text-center py-3">
                <i class="fas fa-spinner fa-spin me-2"></i>
                Loading medical facilities...
            </div>
        `;
    }
    
    // Fetch all available medical facilities
    fetch('/health/api/nearby-facilities')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Loaded facilities:', data);
            
            if (data.success && data.facilities && data.facilities.length > 0) {
                displayFacilities(data.facilities);
                updateFacilitiesList(data.facilities);
                updateResultsInfo(data.facilities.length);
                
                // Update status message
                const locationStatus = document.getElementById('location-status');
                const locationText = document.getElementById('location-text');
                if (locationStatus && locationText) {
                    locationStatus.className = 'alert alert-info';
                    locationStatus.classList.remove('d-none');
                    locationText.textContent = `Showing ${data.facilities.length} medical facilities in Delhi area`;
                }
            } else {
                // Show message if no facilities found
                if (facilitiesList) {
                    facilitiesList.innerHTML = `
                        <div class="text-center py-3">
                            <i class="fas fa-info-circle text-muted me-2"></i>
                            No medical facilities found in the database.
                        </div>
                    `;
                }
            }
        })
        .catch(error => {
            console.error('Error loading default facilities:', error);
            
            // Show error message
            if (facilitiesList) {
                facilitiesList.innerHTML = `
                    <div class="text-center py-3 text-danger">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Unable to load medical facilities. Please try again.
                    </div>
                `;
            }
        });
}

// Initialize map when document is ready
document.addEventListener('DOMContentLoaded', function() {
    if (typeof L !== 'undefined') {
        initMap();
    } else {
        console.error('Leaflet library not loaded');
    }
});