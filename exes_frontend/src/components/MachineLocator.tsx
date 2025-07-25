import React, { useState, useEffect } from 'react';
import { MapPin, Info } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { useSearchParams, useNavigate } from 'react-router-dom';

// Types
interface Machine {
  id: string;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  availableSpace: number; // percentage
  availableFood: number; // number of items
  status: 'operational' | 'maintenance' | 'offline';
  lastUpdated: string;
}

const MachineLocator: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const initialMode = searchParams.get('mode') === 'receiver' ? 'receiver' : 'donor';
  const [viewMode, setViewMode] = useState<'donor' | 'receiver'>(initialMode);
  const [machines, setMachines] = useState<Machine[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [userLocation, setUserLocation] = useState<{lat: number, lng: number} | null>(null);
  const [locationError, setLocationError] = useState<string | null>(null);

  // Fetch machines data
  useEffect(() => {
    // In a real implementation, this would call the backend API
    // For now, we'll use mock data
    const fetchMachines = async () => {
      setLoading(true);
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Mock data
        const mockMachines: Machine[] = [
          {
            id: 'm1',
            name: 'Downtown Machine',
            address: '123 Main St, Downtown',
            latitude: 34.052235,
            longitude: -118.243683,
            availableSpace: 75,
            availableFood: 12,
            status: 'operational',
            lastUpdated: '2025-05-16T08:30:00Z'
          },
          {
            id: 'm2',
            name: 'Westside Machine',
            address: '456 Ocean Ave, Westside',
            latitude: 34.018363,
            longitude: -118.491764,
            availableSpace: 30,
            availableFood: 5,
            status: 'operational',
            lastUpdated: '2025-05-16T09:15:00Z'
          },
          {
            id: 'm3',
            name: 'Eastside Machine',
            address: '789 Valley Blvd, Eastside',
            latitude: 34.087124,
            longitude: -118.176163,
            availableSpace: 90,
            availableFood: 0,
            status: 'operational',
            lastUpdated: '2025-05-16T07:45:00Z'
          },
          {
            id: 'm4',
            name: 'Northside Machine',
            address: '101 Hill St, Northside',
            latitude: 34.129016,
            longitude: -118.328257,
            availableSpace: 10,
            availableFood: 20,
            status: 'operational',
            lastUpdated: '2025-05-16T10:00:00Z'
          },
          {
            id: 'm5',
            name: 'Southside Machine',
            address: '202 Harbor Blvd, Southside',
            latitude: 33.954376,
            longitude: -118.291541,
            availableSpace: 50,
            availableFood: 8,
            status: 'maintenance',
            lastUpdated: '2025-05-16T06:30:00Z'
          }
        ];
        
        setMachines(mockMachines);
      } catch (error) {
        console.error('Error fetching machines:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMachines();
  }, []);

  // Get user location
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
        },
        (error) => {
          console.error('Error getting location:', error);
          setLocationError('Unable to get your location. Please enable location services or enter your location manually.');
        }
      );
    } else {
      setLocationError('Geolocation is not supported by your browser.');
    }
  }, []);

  // Calculate distance between two points (simplified version)
  const calculateDistance = (lat1: number, lon1: number, lat2: number, lon2: number): number => {
    const R = 6371; // Radius of the earth in km
    const dLat = deg2rad(lat2 - lat1);
    const dLon = deg2rad(lon2 - lon1);
    const a = 
      Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
      Math.sin(dLon/2) * Math.sin(dLon/2); 
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
    const d = R * c; // Distance in km
    return d;
  };

  const deg2rad = (deg: number): number => {
    return deg * (Math.PI/180);
  };

  // Sort machines by distance if user location is available
  const sortedMachines = userLocation 
    ? [...machines].sort((a, b) => {
        const distA = calculateDistance(userLocation.lat, userLocation.lng, a.latitude, a.longitude);
        const distB = calculateDistance(userLocation.lat, userLocation.lng, b.latitude, b.longitude);
        return distA - distB;
      })
    : machines;

  // Filter machines based on view mode
  const filteredMachines = sortedMachines.filter(machine => {
    if (viewMode === 'donor') {
      // For donors, show machines with available space
      return machine.status === 'operational' && machine.availableSpace > 0;
    } else {
      // For receivers, show machines with available food
      return machine.status === 'operational' && machine.availableFood > 0;
    }
  });

  const handleModeChange = (value: string) => {
    const mode = value as 'donor' | 'receiver';
    setViewMode(mode);
    navigate(`/locate?mode=${mode}`);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-center mb-8 text-green-700">
        Find a {viewMode === 'donor' ? 'Donation' : 'Food Collection'} Machine
      </h1>

      <Tabs defaultValue={viewMode} onValueChange={handleModeChange} className="mb-8">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="donor">I want to donate food</TabsTrigger>
          <TabsTrigger value="receiver">I need food</TabsTrigger>
        </TabsList>
        <TabsContent value="donor">
          <p className="text-gray-700 mb-4">
            Find machines with available space to donate your excess food. All donations are anonymous.
          </p>
        </TabsContent>
        <TabsContent value="receiver">
          <p className="text-gray-700 mb-4">
            Find machines with available food that you can collect. Each person can collect up to 2 food items.
          </p>
        </TabsContent>
      </Tabs>

      {locationError && (
        <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded mb-6">
          <p>{locationError}</p>
        </div>
      )}

      {loading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-700 mx-auto mb-4"></div>
          <p>Loading machines...</p>
        </div>
      ) : filteredMachines.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <Info className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold mb-2">No Machines Available</h3>
          <p className="text-gray-600 mb-4">
            {viewMode === 'donor' 
              ? "Sorry, there are no machines with available space at the moment." 
              : "Sorry, there are no machines with available food at the moment."}
          </p>
          <Button onClick={() => handleModeChange(viewMode === 'donor' ? 'receiver' : 'donor')}>
            Switch to {viewMode === 'donor' ? 'Receiver' : 'Donor'} View
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredMachines.map(machine => (
            <Card key={machine.id} className="overflow-hidden">
              <CardHeader className={`
                ${machine.status === 'maintenance' ? 'bg-yellow-50' : 'bg-green-50'}
              `}>
                <CardTitle className="flex items-start justify-between">
                  <span className="text-lg">{machine.name}</span>
                  {userLocation && (
                    <span className="text-sm text-gray-500">
                      {calculateDistance(
                        userLocation.lat, 
                        userLocation.lng, 
                        machine.latitude, 
                        machine.longitude
                      ).toFixed(1)} km
                    </span>
                  )}
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-4">
                <div className="flex items-start mb-4">
                  <MapPin className="h-5 w-5 text-gray-500 mr-2 mt-0.5" />
                  <span className="text-gray-700">{machine.address}</span>
                </div>
                
                {viewMode === 'donor' ? (
                  <div className="mb-4">
                    <p className="text-sm text-gray-500 mb-1">Available Space:</p>
                    <div className="w-full bg-gray-200 rounded-full h-2.5">
                      <div 
                        className="bg-green-600 h-2.5 rounded-full" 
                        style={{ width: `${machine.availableSpace}%` }}
                      ></div>
                    </div>
                    <p className="text-right text-sm text-gray-500 mt-1">{machine.availableSpace}%</p>
                  </div>
                ) : (
                  <div className="mb-4">
                    <p className="text-sm text-gray-500 mb-2">Available Food Items:</p>
                    <p className="text-2xl font-bold text-green-700">{machine.availableFood}</p>
                  </div>
                )}
                
                <p className="text-xs text-gray-500 mb-4">
                  Last updated: {new Date(machine.lastUpdated).toLocaleString()}
                </p>
                
                <Button className="w-full">
                  {viewMode === 'donor' ? 'Get Directions to Donate' : 'Get Directions to Collect'}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default MachineLocator;
